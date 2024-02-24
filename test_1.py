import itertools
from typing import Dict
from typing import Tuple

import numpy as np

coordinate_mapping = {
    (0, 0, 0): 0,
    (1, 0, 0): 1,
    (1, 1, 0): 2,
    (0, 1, 0): 3,
    (0, 0, 1): 4,
    (1, 0, 1): 5,
    (1, 1, 1): 6,
    (0, 1, 1): 7,
}

reverse_coordinate_mapping = {v: list(k) for k, v in coordinate_mapping.items()}


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


def main1():
    cube_points: Dict[int, Tuple[int, ...]] = generate_binary_combinations()

    total_combinations: [int] = list(range(256))
    num_of_points: [int] = list(range(9))
    center = np.array([0.5, 0.5, 0.5])

    uniqueness: Dict[int, Dict[Tuple[int, ...], [int]]] = {}

    for num_of_point in num_of_points:
        for cube_point_index in total_combinations:
            cube_point = cube_points[cube_point_index]
            if sum(cube_point) == num_of_point:
                if num_of_point not in uniqueness:
                    uniqueness[num_of_point] = {cube_point: [cube_point_index]}
                else:
                    has_matched = False
                    indices = [i for i, x in enumerate(cube_point) if x == 1]
                    vertices = [reverse_coordinate_mapping[i] for i in indices]
                    np_vertices = np.array(vertices)

                    for axis in ['z', 'y', 'x']:
                        for angle in [0, np.pi / 2, np.pi, np.pi * 3 / 2]:
                            rotated_points = rotate_points_around_center(np_vertices, angle, axis, center)
                            rotated_points_tuple: [Tuple[int, int, int]] = [tuple(np.round(point).astype(int)) for point
                                                                            in rotated_points]
                            rotated_cube_points = [0, 0, 0, 0, 0, 0, 0, 0]
                            for point in rotated_points_tuple:
                                index = coordinate_mapping.get(point)
                                if index is not None:
                                    rotated_cube_points[index] = 1
                            rotated_cube_points_tuple = tuple(rotated_cube_points)

                            # print(num_of_point, cube_point_index, cube_point, axis, rotated_cube_points_tuple,
                            #       rotated_cube_points_tuple in uniqueness[num_of_point])
                            if rotated_cube_points_tuple in uniqueness[num_of_point]:
                                uniqueness[num_of_point][rotated_cube_points_tuple].append(cube_point_index)
                                has_matched = True
                                break
                        if has_matched:
                            break
                    if not has_matched:
                        uniqueness[num_of_point][cube_point] = [cube_point_index]

    for unique in uniqueness:
        print(unique, uniqueness[unique])


def main2():
    cube_points: Dict[int, Tuple[int, ...]] = generate_binary_combinations()

    total_combinations: [int] = list(range(256))
    num_of_points: [int] = list(range(9))
    center = np.array([0.5, 0.5, 0.5])

    uniqueness: Dict[int, Dict[Tuple[int, ...], [int]]] = {}

    for num_of_point in num_of_points:
        for cube_point_index in total_combinations:
            cube_point = cube_points[cube_point_index]
            if sum(cube_point) == num_of_point:
                if num_of_point not in uniqueness:
                    uniqueness[num_of_point] = {cube_point: [cube_point_index]}
                else:
                    has_matched = False
                    indices = [i for i, x in enumerate(cube_point) if x == 1]
                    vertices = [reverse_coordinate_mapping[i] for i in indices]
                    np_vertices = np.array(vertices)
                    rotated_points = np_vertices

                    axes = ['x', 'y', 'z']
                    angles = [0, np.pi / 2, np.pi, np.pi * 3 / 2]
                    combinations = list(itertools.product(axes, angles, repeat=3))
                    split_combinations = [[tuple(combination[i:i + 2]) for i in range(0, len(combination), 2)] for
                                          combination in
                                          combinations]
                    for combination in split_combinations:
                        for axis, angle in combination:
                            rotated_points = rotate_points_around_center(rotated_points, angle, axis, center)
                        rotated_points_tuple: [Tuple[int, int, int]] = [tuple(np.round(point).astype(int)) for point
                                                                        in rotated_points]
                        rotated_cube_points = [0, 0, 0, 0, 0, 0, 0, 0]
                        for point in rotated_points_tuple:
                            index = coordinate_mapping.get(point)
                            if index is not None:
                                rotated_cube_points[index] = 1
                        rotated_cube_points_tuple = tuple(rotated_cube_points)

                        if rotated_cube_points_tuple in uniqueness[num_of_point]:
                            uniqueness[num_of_point][rotated_cube_points_tuple].append(cube_point_index)
                            has_matched = True
                            break
                    if not has_matched:
                        uniqueness[num_of_point][cube_point] = [cube_point_index]

    for unique in uniqueness:
        print(unique, uniqueness[unique])


if __name__ == "__main__":
    main2()
