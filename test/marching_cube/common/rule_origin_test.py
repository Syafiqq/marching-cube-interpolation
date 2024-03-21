import itertools
from typing import Dict, Tuple

import numpy as np


# Axes are:
#
#      z
#      |     y
#      |   /
#      | /
#      +----- x

# Vertex and edge layout:
#
#            6             7
#            +-------------+               +-------------+          +-------------+          24-----25------26
#          / |           / |             / |           / |        / |           / |        21 |   22     23 |
#        /   |         /   |           /   |         /   |      /   |         /   |      /   |         /    |
#    4 +-----+-------+  5  |         +-----+-------+     |    +-----15----16--+   17    18-----19-----20    |
#      |   2 +-------+-----+ 3       |     6-----7-+-----8    |  12  +--13--+--14--+    |     +-------+-----+
#      |   /         |   /           |   3     4   |   5      9   /  10     11   /      |   /         |   /
#      | /           | /             | /           | /        | /           | /         | /           | /
#    0 +-------------+ 1             0------1------2          +-------------+           +-------------+


coordinate_mapping: Dict[Tuple[int, int, int], int] = {
    (0, 0, 0): 0,
    (1, 0, 0): 1,
    (0, 1, 0): 2,
    (1, 1, 0): 3,
    (0, 0, 1): 4,
    (1, 0, 1): 5,
    (0, 1, 1): 6,
    (1, 1, 1): 7,
}

reverse_coordinate_mapping: Dict[int, list[int]] = {v: list(k) for k, v in coordinate_mapping.items()}
reverse_coordinate_mapping_tuple: Dict[int, Tuple[int, int, int]] = {v: k for k, v in coordinate_mapping.items()}


def rotate_points(points: np.array, angle: float, axis: str) -> np.array:
    rotation_matrix = np.eye(3)
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)

    if axis == 'x':
        rotation_matrix[1, 1] = cos_angle
        rotation_matrix[1, 2] = -sin_angle
        rotation_matrix[2, 1] = sin_angle
        rotation_matrix[2, 2] = cos_angle
    elif axis == 'y':
        rotation_matrix[0, 0] = cos_angle
        rotation_matrix[0, 2] = sin_angle
        rotation_matrix[2, 0] = -sin_angle
        rotation_matrix[2, 2] = cos_angle
    elif axis == 'z':
        rotation_matrix[0, 0] = cos_angle
        rotation_matrix[0, 1] = -sin_angle
        rotation_matrix[1, 0] = sin_angle
        rotation_matrix[1, 1] = cos_angle

    rotated_points = [np.dot(rotation_matrix, point) for point in points]
    return rotated_points


def rotate_points_around_center(points: [np.array], angle: float, axis: str, center: np.array) -> [np.array]:
    # Translate points so that center of rotation is at origin
    translated_points = [np.subtract(point, center) for point in points]

    # Rotate points
    rotated_points = rotate_points(translated_points, angle, axis)

    # Translate points back
    rotated_translated_points = [np.add(point, center) for point in rotated_points]

    return rotated_translated_points


def generate_binary_combinations():
    # create 256 combinations
    value = list(itertools.product([0, 1], repeat=8))

    # reverse the combination
    value_reversed = [tuple(reversed(point)) for point in value]

    # cnvert to map
    value_reversed = {i: point for i, point in enumerate(value_reversed)}
    return value_reversed


def main():
    """
    Create a dictionary of all possible combinations of 8 points
    {
        0: (0, 0, 0, 0, 0, 0, 0, 0, 0)
        1: (1, 0, 0, 0, 0, 0, 0, 0, 0)
        ...
        255: (1, 1, 1, 1, 1, 1, 1, 1, 1)
    }
    """
    cube_points: Dict[int, Tuple[int, ...]] = generate_binary_combinations()

    "Total of combinations is 256"
    total_combinations: [int] = list(range(256))

    "Total of point num is 9 starting from 0 to 8"
    num_of_points: [int] = list(range(9))

    "To calculate the rotation"
    center = np.array([0.5, 0.5, 0.5])

    """
    Define rotate possibilities
    """
    axes = ['z', 'y', 'x']
    angles = [0, 90, 180, 270]
    rotate_possibilities_raw = list(itertools.product(axes, angles, repeat=3))
    rotate_possibilities = [
        [tuple(combination[i:i + 2]) for i in range(0, len(combination), 2)] for
        combination in rotate_possibilities_raw
    ]

    """
    To Hold the uniqueness
    {
        0: { # Number of points
            (0, 0, 0, 0, 0, 0, 0, 0, 0): [ # Combination
                (
                    0, # Index
                    [] # Rotation rules
                )
            ]
        }
    }
    """
    uniqueness: Dict[int, Dict[Tuple[int, ...], list[Tuple[int, list[Tuple[str, int]]]]]] = {}

    for cube_point_index in total_combinations:
        for num_of_point in num_of_points:
            cube_point_expected = cube_points[cube_point_index]
            if sum(cube_point_expected) == num_of_point:
                if num_of_point not in uniqueness:
                    uniqueness[num_of_point] = {cube_point_expected: [(cube_point_index, [])]}
                else:
                    "Check if there is any matching data"
                    has_matched = False
                    for cube_point_start in uniqueness[num_of_point]:
                        "Get vertices given cube_point_start"
                        indices = [i for i, x in enumerate(cube_point_start) if x == 1]
                        vertices = [reverse_coordinate_mapping[i] for i in indices]
                        np_vertices = np.array(vertices)

                        for rotation_attempt in rotate_possibilities:
                            rotated_points = np_vertices
                            executed_rotation: list[Tuple[str, int]] = []

                            for axis, angle in rotation_attempt:
                                if angle == 0:
                                    continue
                                executed_rotation.append((axis, angle))
                                angles_rad = angle * (np.pi / 180)
                                rotated_points = rotate_points_around_center(rotated_points, angles_rad, axis, center)

                            """
                            Construct cube_points_actual
                            """
                            rotated_points_tuple: [Tuple[int, int, int]] = [
                                tuple(np.round(point).astype(int)) for point in rotated_points
                            ]
                            cube_points_actual_list = [0, 0, 0, 0, 0, 0, 0, 0]
                            for point in rotated_points_tuple:
                                index = coordinate_mapping.get(point)
                                if index is not None:
                                    cube_points_actual_list[index] = 1
                            cube_point_actual = tuple(cube_points_actual_list)

                            if cube_point_actual == cube_point_expected:
                                uniqueness[num_of_point][cube_point_start].append(
                                    (cube_point_index, executed_rotation)
                                )
                                has_matched = True
                                break

                    if not has_matched:
                        uniqueness[num_of_point][cube_point_expected] = [(cube_point_index, [])]

    print('''\nNormal\n''')
    for unique in uniqueness:
        print(unique, uniqueness[unique])

    print('''\nIndex Only\n''')
    # Index only
    for unique in uniqueness:
        uniqueness1 = uniqueness[unique]
        for unique1 in uniqueness1:
            list_of_tuples = uniqueness1[unique1]
            first_indexes = list(map(lambda x: x[0], list_of_tuples))  # Get list of first indices from tuples
            print(
                str(unique).ljust(3),
                str(len(first_indexes)).ljust(3),
                first_indexes
            )

    print('''\nGrouped by index key\n''')
    result: Dict[int, str] = {}
    for unique in uniqueness:
        uniqueness1 = uniqueness[unique]
        for unique1 in uniqueness1:
            list_of_tuples = uniqueness1[unique1]
            comparison = list_of_tuples[0]
            for _tuple in list_of_tuples:
                result[_tuple[0]] = f'{str(comparison[0]).ljust(3)} - {_tuple[1]}'
    for index in list(range(256)):
        print(
            str(index).ljust(3),
            result[index]
        )

    print('''\nGrouped by group key\n''')
    for unique in uniqueness:
        uniqueness1 = uniqueness[unique]
        for unique1 in uniqueness1:
            list_of_tuples = uniqueness1[unique1]
            comparison = list_of_tuples[0]
            print(f'Group Key - {str(unique).ljust(3)} - {str(comparison[0]).ljust(3)}')
            for _tuple in list_of_tuples:
                print(f'{str(_tuple[0]).ljust(3)} - {_tuple[1]}')
            print()


def reconcile():
    """
    Create a dictionary of all possible combinations of 8 points
    {
        0: (0, 0, 0, 0, 0, 0, 0, 0, 0)
        1: (1, 0, 0, 0, 0, 0, 0, 0, 0)
        ...
        255: (1, 1, 1, 1, 1, 1, 1, 1, 1)
    }
    """
    cube_points: Dict[int, Tuple[int, ...]] = generate_binary_combinations()

    dataset: [Tuple[int, int, list[Tuple[str, int]]]] = [
        # @formatter:off
        (0,   0,   []),
        (1,   1,   []),
        (2,   1,   [('z', 90)]),
        (3,   3,   []),
        (4,   1,   [('z', 270)]),
        (5,   3,   [('z', 270)]),
        (6,   6,   []),
        (7,   7,   []),
        (8,   1,   [('z', 180)]),
        (9,   6,   [('z', 90)]),
        (10,  3,   [('z', 90)]),
        (11,  7,   [('z', 90)]),
        (12,  3,   [('z', 180)]),
        (13,  7,   [('z', 270)]),
        (14,  7,   [('z', 180)]),
        (15,  15,  []),
        (16,  1,   [('y', 90)]),
        (17,  3,   [('y', 90)]),
        (18,  6,   [('z', 90), ('x', 270)]),
        (19,  7,   [('z', 270), ('x', 270)]),
        (20,  6,   [('z', 90), ('y', 90)]),
        (21,  7,   [('z', 90), ('y', 90)]),
        (22,  22,  []),
        (23,  23,  []),
        (24,  24,  []),
        (25,  25,  []),
        (26,  25,  [('z', 180), ('x', 270)]),
        (27,  27,  []),
        (28,  25,  [('z', 180), ('y', 90)]),
        (29,  29,  []),
        (30,  30,  []),
        (31,  31,  []),
        (32,  1,   [('y', 180)]),
        (33,  6,   [('x', 270)]),
        (34,  3,   [('y', 270)]),
        (35,  7,   [('z', 180), ('x', 270)]),
        (36,  24,  [('z', 90)]),
        (37,  25,  [('z', 270), ('x', 270)]),
        (38,  25,  [('z', 90)]),
        (39,  29,  [('z', 90)]),
        (40,  6,   [('y', 270)]),
        (41,  22,  [('z', 90)]),
        (42,  7,   [('y', 270)]),
        (43,  23,  [('z', 90)]),
        (44,  25,  [('z', 270), ('y', 270)]),
        (45,  30,  [('z', 90)]),
        (46,  27,  [('z', 90)]),
        (47,  31,  [('z', 90)]),
        (48,  3,   [('y', 180)]),
        (49,  7,   [('x', 270)]),
        (50,  7,   [('z', 90), ('x', 270)]),
        (51,  15,  [('x', 270)]),
        (52,  25,  [('y', 90)]),
        (53,  27,  [('y', 90)]),
        (54,  30,  [('z', 270), ('x', 270)]),
        (55,  31,  [('z', 270), ('x', 270)]),
        (56,  25,  [('z', 90), ('y', 270)]),
        (57,  30,  [('z', 180), ('x', 270)]),
        (58,  29,  [('z', 90), ('y', 270)]),
        (59,  31,  [('z', 180), ('x', 270)]),
        (60,  60,  []),
        (61,  61,  []),
        (62,  61,  [('z', 180), ('x', 270)]),
        (63,  63,  []),
        (64,  1,   [('x', 180)]),
        (65,  6,   [('y', 90)]),
        (66,  24,  [('z', 270)]),
        (67,  25,  [('z', 90), ('y', 90)]),
        (68,  3,   [('z', 180), ('y', 90)]),
        (69,  7,   [('z', 180), ('y', 90)]),
        (70,  25,  [('z', 270)]),
        (71,  27,  [('z', 270)]),
        (72,  6,   [('x', 90)]),
        (73,  22,  [('z', 270)]),
        (74,  25,  [('z', 90), ('x', 90)]),
        (75,  30,  [('z', 270)]),
        (76,  7,   [('x', 90)]),
        (77,  23,  [('z', 270)]),
        (78,  29,  [('z', 270)]),
        (79,  31,  [('z', 270)]),
        (80,  3,   [('z', 90), ('y', 180)]),
        (81,  7,   [('y', 90)]),
        (82,  25,  [('x', 270)]),
        (83,  29,  [('x', 270)]),
        (84,  7,   [('z', 270), ('y', 90)]),
        (85,  15,  [('y', 90)]),
        (86,  30,  [('z', 90), ('y', 90)]),
        (87,  31,  [('z', 90), ('y', 90)]),
        (88,  25,  [('z', 270), ('x', 90)]),
        (89,  30,  [('z', 180), ('y', 90)]),
        (90,  60,  [('z', 270)]),
        (91,  61,  [('z', 90), ('y', 90)]),
        (92,  27,  [('z', 180), ('y', 90)]),
        (93,  31,  [('z', 180), ('y', 90)]),
        (94,  61,  [('z', 270)]),
        (95,  63,  [('z', 270)]),
        (96,  6,   [('z', 90), ('y', 180)]),
        (97,  22,  [('y', 90)]),
        (98,  25,  [('y', 180)]),
        (99,  30,  [('x', 270)]),
        (100, 25,  [('x', 180)]),
        (101, 30,  [('y', 90)]),
        (102, 60,  [('y', 90)]),
        (103, 61,  [('z', 270), ('x', 270)]),
        (104, 22,  [('z', 90), ('x', 180)]),
        (105, 105, []),
        (106, 30,  [('z', 180), ('y', 270)]),
        (107, 107, []),
        (108, 30,  [('z', 180), ('x', 90)]),
        (109, 107, [('z', 180)]),
        (110, 61,  [('z', 90), ('x', 90)]),
        (111, 111, []),
        (112, 7,   [('z', 90), ('y', 180)]),
        (113, 23,  [('y', 90)]),
        (114, 27,  [('y', 180)]),
        (115, 31,  [('x', 270)]),
        (116, 29,  [('y', 90)]),
        (117, 31,  [('y', 90)]),
        (118, 61,  [('y', 90)]),
        (119, 63,  [('y', 90)]),
        (120, 30,  [('z', 90), ('x', 180)]),
        (121, 107, [('y', 180)]),
        (122, 61,  [('z', 90), ('y', 270)]),
        (123, 111, [('z', 90), ('x', 270)]),
        (124, 61,  [('x', 180)]),
        (125, 111, [('z', 90), ('y', 90)]),
        (126, 126, []),
        (127, 127, []),
        (128, 1,   [('z', 90), ('x', 180)]),
        (129, 24,  [('z', 180)]),
        (130, 6,   [('z', 90), ('y', 270)]),
        (131, 25,  [('y', 270)]),
        (132, 6,   [('z', 90), ('x', 90)]),
        (133, 25,  [('x', 90)]),
        (134, 22,  [('z', 180)]),
        (135, 30,  [('z', 180)]),
        (136, 3,   [('z', 90), ('x', 90)]),
        (137, 25,  [('z', 180)]),
        (138, 7,   [('z', 270), ('y', 270)]),
        (139, 29,  [('z', 180)]),
        (140, 7,   [('z', 90), ('x', 90)]),
        (141, 27,  [('z', 180)]),
        (142, 23,  [('z', 180)]),
        (143, 31,  [('z', 180)]),
        (144, 6,   [('y', 180)]),
        (145, 25,  [('z', 90), ('y', 180)]),
        (146, 22,  [('y', 180)]),
        (147, 30,  [('z', 90), ('x', 270)]),
        (148, 22,  [('x', 180)]),
        (149, 30,  [('z', 270), ('y', 90)]),
        (150, 105, [('z', 90)]),
        (151, 107, [('z', 270)]),
        (152, 25,  [('z', 90), ('x', 180)]),
        (153, 60,  [('y', 270)]),
        (154, 30,  [('z', 90), ('y', 270)]),
        (155, 61,  [('y', 270)]),
        (156, 30,  [('z', 270), ('x', 90)]),
        (157, 61,  [('z', 180), ('y', 90)]),
        (158, 107, [('z', 90)]),
        (159, 111, [('z', 90)]),
        (160, 3,   [('z', 90), ('y', 270)]),
        (161, 25,  [('z', 90), ('x', 270)]),
        (162, 7,   [('z', 90), ('y', 270)]),
        (163, 27,  [('y', 270)]),
        (164, 25,  [('z', 180), ('x', 90)]),
        (165, 60,  [('z', 90)]),
        (166, 30,  [('z', 270), ('y', 270)]),
        (167, 61,  [('z', 90)]),
        (168, 7,   [('z', 180), ('y', 270)]),
        (169, 30,  [('y', 270)]),
        (170, 15,  [('y', 270)]),
        (171, 31,  [('y', 270)]),
        (172, 29,  [('z', 180), ('x', 90)]),
        (173, 61,  [('z', 270), ('y', 270)]),
        (174, 31,  [('z', 270), ('y', 270)]),
        (175, 63,  [('z', 90)]),
        (176, 7,   [('y', 180)]),
        (177, 29,  [('z', 90), ('y', 180)]),
        (178, 23,  [('y', 180)]),
        (179, 31,  [('z', 90), ('x', 270)]),
        (180, 30,  [('x', 180)]),
        (181, 61,  [('z', 90), ('y', 180)]),
        (182, 107, [('y', 270)]),
        (183, 111, [('x', 270)]),
        (184, 27,  [('z', 90), ('y', 270)]),
        (185, 61,  [('z', 90), ('x', 270)]),
        (186, 31,  [('z', 90), ('y', 270)]),
        (187, 63,  [('y', 270)]),
        (188, 61,  [('z', 180), ('x', 90)]),
        (189, 126, [('z', 90)]),
        (190, 111, [('y', 270)]),
        (191, 127, [('z', 90)]),
        (192, 3,   [('x', 180)]),
        (193, 25,  [('z', 270), ('y', 90)]),
        (194, 25,  [('z', 180), ('y', 270)]),
        (195, 60,  [('z', 180)]),
        (196, 7,   [('z', 270), ('x', 90)]),
        (197, 29,  [('x', 90)]),
        (198, 30,  [('z', 90), ('x', 90)]),
        (199, 61,  [('x', 90)]),
        (200, 7,   [('z', 180), ('x', 90)]),
        (201, 30,  [('x', 90)]),
        (202, 27,  [('z', 90), ('x', 90)]),
        (203, 61,  [('z', 180)]),
        (204, 15,  [('x', 90)]),
        (205, 31,  [('x', 90)]),
        (206, 31,  [('z', 90), ('x', 90)]),
        (207, 63,  [('z', 180)]),
        (208, 7,   [('x', 180)]),
        (209, 27,  [('z', 90), ('y', 180)]),
        (210, 30,  [('y', 180)]),
        (211, 61,  [('x', 270)]),
        (212, 23,  [('x', 180)]),
        (213, 31,  [('z', 270), ('y', 90)]),
        (214, 107, [('z', 90), ('y', 180)]),
        (215, 111, [('y', 90)]),
        (216, 29,  [('z', 90), ('x', 180)]),
        (217, 61,  [('z', 270), ('x', 90)]),
        (218, 61,  [('z', 90), ('x', 180)]),
        (219, 126, [('z', 270)]),
        (220, 31,  [('z', 270), ('x', 90)]),
        (221, 63,  [('z', 180), ('y', 90)]),
        (222, 111, [('x', 90)]),
        (223, 127, [('z', 270)]),
        (224, 7,   [('z', 90), ('x', 180)]),
        (225, 30,  [('z', 90), ('y', 180)]),
        (226, 29,  [('y', 180)]),
        (227, 61,  [('y', 180)]),
        (228, 27,  [('x', 180)]),
        (229, 61,  [('z', 270), ('y', 90)]),
        (230, 61,  [('z', 180), ('y', 270)]),
        (231, 126, [('z', 180)]),
        (232, 23,  [('z', 90), ('x', 180)]),
        (233, 107, [('x', 180)]),
        (234, 31,  [('z', 180), ('y', 270)]),
        (235, 111, [('z', 90), ('y', 270)]),
        (236, 31,  [('z', 180), ('x', 90)]),
        (237, 111, [('z', 90), ('x', 90)]),
        (238, 63,  [('z', 90), ('x', 90)]),
        (239, 127, [('z', 180)]),
        (240, 15,  [('y', 180)]),
        (241, 31,  [('z', 90), ('y', 180)]),
        (242, 31,  [('y', 180)]),
        (243, 63,  [('y', 180)]),
        (244, 31,  [('x', 180)]),
        (245, 63,  [('z', 90), ('y', 180)]),
        (246, 111, [('z', 90), ('y', 180)]),
        (247, 127, [('y', 90)]),
        (248, 31,  [('z', 90), ('x', 180)]),
        (249, 111, [('y', 180)]),
        (250, 63,  [('z', 90), ('y', 270)]),
        (251, 127, [('y', 180)]),
        (252, 63,  [('x', 180)]),
        (253, 127, [('x', 180)]),
        (254, 127, [('z', 90), ('x', 180)]),
        (255, 255, []),
        # @formatter:on
    ]

    "To calculate the rotation"
    center = np.array([0.5, 0.5, 0.5])

    for data in dataset:
        cube_point_expected = cube_points[data[0]]
        cube_point_start = cube_points[data[1]]

        "Get vertices given cube_point_start"
        indices = [i for i, x in enumerate(cube_point_start) if x == 1]
        vertices = [reverse_coordinate_mapping[i] for i in indices]
        np_vertices = np.array(vertices)
        rotated_points = np_vertices

        for axis, angle in data[2]:
            angles_rad = angle * (np.pi / 180)
            rotated_points = rotate_points_around_center(rotated_points, angles_rad, axis, center)

        """
        Construct cube_points_actual
        """
        rotated_points_tuple: [Tuple[int, int, int]] = [
            tuple(np.round(point).astype(int)) for point in rotated_points
        ]
        cube_points_actual_list = [0, 0, 0, 0, 0, 0, 0, 0]
        for point in rotated_points_tuple:
            index = coordinate_mapping.get(point)
            if index is not None:
                cube_points_actual_list[index] = 1
        cube_point_actual = tuple(cube_points_actual_list)

        assert cube_point_actual == cube_point_expected


if __name__ == "__main__":
    main()
