import numpy as np

from marching_cube.common import math_helper
from marching_cube.domain.marching_cube_metadata import MarchingCubeMetadata
from marching_cube.domain.rules.manual_1 import rules_manual_1
import trimesh


# https://stackoverflow.com/a/752562
def __split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]


def __create_int_dict(start: int, end: int, inc: int) -> dict[int: int]:
    result: dict[int: int] = {}
    for i in range(start, end, inc):
        result[i] = 0
    return result


def build(
        values: [int],
        metadata: MarchingCubeMetadata,
        variant: int,
        faces_actual: [[int]],
        faces_expected: [[int]],
        incorrect_faces_index: [int]
) -> trimesh.Trimesh:
    dictionary = {}
    points_p = []
    faces_p = []

    digit_x = 10 ** (math_helper.num_digits(metadata.nxy_ratio_dims) + 1)
    digit_y = 10 ** (math_helper.num_digits(metadata.nxy_ratio_dims) + 1)

    max_z = digit_x * digit_y
    max_y = digit_x

    cxy = metadata.xyz_dims[0] * metadata.xyz_dims[1]
    cx = metadata.xyz_dims[0]
    cxy_plus1 = metadata.xyz_dims_plus1[0] * metadata.xyz_dims_plus1[1]
    cx_plus1 = metadata.xyz_dims_plus1[0]

    for i in np.arange(0, np.prod(metadata.xyz_dims), 1, dtype=int):
        # @formatter:off
        dz = i // cxy                                       # i div (dimension x and y) to get axis z
        dz_r = i - (dz * cxy)                               # get the remaining of dz
        dy = dz_r // cx                                     # remain of dz div (dimension of x) to get axis y
        dy_r = dz_r - (dy * cx)                             # get the remaining of dy
        dx = dy_r                                           # get the dx

        pt = dz * cxy_plus1 + dy * cx_plus1 + dx * 1        # mapping value to match array of points
        p0 = pt                                             # find the lowest x
        p1 = pt + 1                                         # find the lowest x + 1
        p2 = p0 + cx_plus1                                  # find the lowest x with y + 1
        p3 = p1 + cx_plus1                                  # find the lowest x + 1 with y + 1

        p4 = p0 + cxy_plus1
        p5 = p1 + cxy_plus1
        p6 = p2 + cxy_plus1
        p7 = p3 + cxy_plus1
        # @formatter:on

        point_type = (
                (np.sign(values[p0]) << 7) +
                (np.sign(values[p1]) << 6) +
                (np.sign(values[p2]) << 5) +
                (np.sign(values[p3]) << 4) +
                (np.sign(values[p4]) << 3) +
                (np.sign(values[p5]) << 2) +
                (np.sign(values[p6]) << 1) +
                (np.sign(values[p7]) << 0)
        )

        point_group = [
            metadata.xyz_points[p0],
            metadata.xyz_points[p1],
            metadata.xyz_points[p2],
            metadata.xyz_points[p3],
            metadata.xyz_points[p4],
            metadata.xyz_points[p5],
            metadata.xyz_points[p6],
            metadata.xyz_points[p7],
        ]
        poly_points = rules_manual_1.to_points(point_group, point_type, variant=variant)
        position = []
        for poly_point in poly_points:
            magnitude = poly_point[0] + (max_y * (poly_point[1] + 1)) + (max_z * (poly_point[2] + 1))
            if dictionary.get(magnitude) is None:
                points_p.append(poly_point)
                dictionary[magnitude] = len(points_p) - 1
            position.append(dictionary[magnitude])

        faces_candidate = rules_manual_1.to_faces(position, point_type, variant=variant)
        if faces_candidate:
            sanitised_faces_candidate = np.array(
                np.split(np.array(faces_candidate, dtype=int), len(faces_candidate) // 4)
            )[:, 1:].tolist()

            problematic_faces_index: [(int, int)] = []
            for candidate_index, face in enumerate(sanitised_faces_candidate):
                actual_index = faces_actual.index(face)
                if actual_index in incorrect_faces_index:
                    problematic_faces_index.append((actual_index, candidate_index))

            if problematic_faces_index:
                print(point_type, f'0b{'{0:b}'.format(point_type).zfill(8)}')
                for actual_index, candidate_index in problematic_faces_index:
                    actual = sanitised_faces_candidate[candidate_index]
                    expected = faces_expected[actual_index]
                    print(f'{candidate_index}\t{actual}\t{expected}')

                transition_mapping = __create_int_dict(0, 100, 1)
                transition_position = range(0, 100, 1)
                transition_faces = rules_manual_1.to_faces(transition_position, point_type, variant=variant)
                transition_faces_expected = transition_faces.copy()
                for _faces_index, _faces in enumerate(sanitised_faces_candidate):
                    for _face_index, _face in enumerate(_faces):
                        transition_mapping[_face] = transition_faces[_faces_index * 4 + _face_index + 1]

                for actual_index, candidate_index in problematic_faces_index:
                    expected = faces_expected[actual_index]

                    for _expected_index, _expected in enumerate(expected):
                        transition_faces_expected[candidate_index * 4 + _expected_index + 1] = \
                            transition_mapping[_expected]
                for _face in __split_list(transition_faces_expected, wanted_parts=len(transition_faces_expected) // 4):
                    print(f'3, p[{_face[1]}], p[{_face[2]}], p[{_face[3]}],')

                print()

        for poly_face in faces_candidate:
            faces_p.append(poly_face)

    faces_p = np.array(np.split(np.array(faces_p, dtype=int), len(faces_p) // 4))[:, 1:]

    mesh = trimesh.Trimesh(
        vertices=np.array(points_p, dtype=np.float64),
        faces=faces_p,
        process=False
    )

    return mesh
