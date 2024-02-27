import itertools
from typing import Dict
from typing import Tuple

import numpy as np

coordinate_mapping: Dict[Tuple[int, int, int], int] = {
    (0, 0, 0): 0,
    (1, 0, 0): 1,
    (1, 1, 0): 2,
    (0, 1, 0): 3,
    (0, 0, 1): 4,
    (1, 0, 1): 5,
    (1, 1, 1): 6,
    (0, 1, 1): 7,
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


def main3():
    cube_points: Dict[int, Tuple[int, ...]] = generate_binary_combinations()

    total_combinations: [int] = list(range(256))
    num_of_points: [int] = list(range(9))
    center = np.array([0.5, 0.5, 0.5])

    uniqueness: Dict[int, Dict[Tuple[int, ...], [(int, [Tuple])]]] = {}

    for num_of_point in num_of_points:
        for cube_point_index in total_combinations:
            cube_point = cube_points[cube_point_index]
            if sum(cube_point) == num_of_point:
                if num_of_point not in uniqueness:
                    uniqueness[num_of_point] = {cube_point: [(cube_point_index, [])]}
                else:
                    has_matched = False
                    indices = [i for i, x in enumerate(cube_point) if x == 1]
                    vertices = [reverse_coordinate_mapping[i] for i in indices]
                    np_vertices = np.array(vertices)
                    rotated_points = np_vertices

                    axes = ['x', 'y', 'z']
                    angles = [0, 90, 180, 270]
                    combinations = list(itertools.product(axes, angles, repeat=3))
                    split_combinations = [[tuple(combination[i:i + 2]) for i in range(0, len(combination), 2)] for
                                          combination in
                                          combinations]
                    for combination in split_combinations:
                        for axis, angle in combination:
                            angles_rad = angle * (np.pi / 180)
                            rotated_points = rotate_points_around_center(rotated_points, angles_rad, axis, center)
                        rotated_points_tuple: [Tuple[int, int, int]] = [tuple(np.round(point).astype(int)) for point
                                                                        in rotated_points]
                        rotated_cube_points = [0, 0, 0, 0, 0, 0, 0, 0]
                        for point in rotated_points_tuple:
                            index = coordinate_mapping.get(point)
                            if index is not None:
                                rotated_cube_points[index] = 1
                        rotated_cube_points_tuple = tuple(rotated_cube_points)

                        if rotated_cube_points_tuple in uniqueness[num_of_point]:
                            uniqueness[num_of_point][rotated_cube_points_tuple].append((cube_point_index, combination))
                            has_matched = True
                            break
                    if not has_matched:
                        uniqueness[num_of_point][cube_point] = [(cube_point_index, [])]

    for unique in uniqueness:
        print(unique, uniqueness[unique])


def main4():
    cube_points: Dict[int, Tuple[int, ...]] = generate_binary_combinations()

    total_combinations: [int] = list(range(256))
    num_of_points: [int] = list(range(9))
    center = np.array([0.5, 0.5, 0.5])

    uniqueness: Dict[int, Dict[Tuple[int, ...], [(int, [Tuple])]]] = {}

    for num_of_point in num_of_points:
        for cube_point_index in total_combinations:
            cube_point = cube_points[cube_point_index]
            if sum(cube_point) == num_of_point:
                if num_of_point not in uniqueness:
                    uniqueness[num_of_point] = {cube_point: [(cube_point_index, [])]}
                else:
                    has_matched = False
                    indices = [i for i, x in enumerate(cube_point) if x == 1]
                    vertices = [reverse_coordinate_mapping[i] for i in indices]
                    np_vertices = np.array(vertices)
                    rotated_points = np_vertices

                    axes = ['x', 'y', 'z']
                    angles = [0, 90, 180, 270]
                    combinations = list(itertools.product(axes, angles, repeat=3))
                    split_combinations = [[tuple(combination[i:i + 2]) for i in range(0, len(combination), 2)] for
                                          combination in
                                          combinations]
                    for combination in split_combinations:
                        for axis, angle in combination:
                            angles_rad = angle * (np.pi / 180)
                            rotated_points = rotate_points_around_center(rotated_points, angles_rad, axis, center)
                        rotated_points_tuple: [Tuple[int, int, int]] = [tuple(np.round(point).astype(int)) for point
                                                                        in rotated_points]
                        rotated_cube_points = [0, 0, 0, 0, 0, 0, 0, 0]
                        for point in rotated_points_tuple:
                            index = coordinate_mapping.get(point)
                            if index is not None:
                                rotated_cube_points[index] = 1
                        rotated_cube_points_tuple = tuple(rotated_cube_points)

                        if rotated_cube_points_tuple in uniqueness[num_of_point]:
                            uniqueness[num_of_point][rotated_cube_points_tuple].append((cube_point_index, combination))
                            has_matched = True
                            break
                    if not has_matched:
                        uniqueness[num_of_point][cube_point] = [(cube_point_index, [])]

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


def main5():
    cube_points: Dict[int, Tuple[int, ...]] = generate_binary_combinations()

    total_combinations: [int] = list(range(256))
    num_of_points: [int] = list(range(9))
    center = np.array([0.5, 0.5, 0.5])

    uniqueness: Dict[int, Dict[Tuple[int, ...], [(int, [Tuple])]]] = {}

    for num_of_point in num_of_points:
        for cube_point_index in total_combinations:
            cube_point = cube_points[cube_point_index]
            if sum(cube_point) == num_of_point:
                if num_of_point not in uniqueness:
                    uniqueness[num_of_point] = {cube_point: [(cube_point_index, [])]}
                else:
                    has_matched = False
                    indices = [i for i, x in enumerate(cube_point) if x == 1]
                    vertices = [reverse_coordinate_mapping[i] for i in indices]
                    np_vertices = np.array(vertices)
                    rotated_points = np_vertices

                    axes = ['x', 'y', 'z']
                    angles = [0, 90, 180, 270]
                    combinations = list(itertools.product(axes, angles, repeat=3))
                    split_combinations = [[tuple(combination[i:i + 2]) for i in range(0, len(combination), 2)] for
                                          combination in
                                          combinations]
                    for combination in split_combinations:
                        combination_execution = []
                        for axis, angle in combination:
                            if angle == 0:
                                continue
                            combination_execution.append((axis, angle))
                            angles_rad = angle * (np.pi / 180)
                            rotated_points = rotate_points_around_center(rotated_points, angles_rad, axis, center)
                        rotated_points_tuple: [Tuple[int, int, int]] = [tuple(np.round(point).astype(int)) for point
                                                                        in rotated_points]
                        rotated_cube_points = [0, 0, 0, 0, 0, 0, 0, 0]
                        for point in rotated_points_tuple:
                            index = coordinate_mapping.get(point)
                            if index is not None:
                                rotated_cube_points[index] = 1
                        rotated_cube_points_tuple = tuple(rotated_cube_points)

                        if rotated_cube_points_tuple in uniqueness[num_of_point]:
                            uniqueness[num_of_point][rotated_cube_points_tuple].append(
                                (cube_point_index, combination_execution))
                            has_matched = True
                            break
                    if not has_matched:
                        uniqueness[num_of_point][cube_point] = [(cube_point_index, [])]

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


def main6():
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


def reconcile1():
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
        (4,   1,   [('z', 180)]),
        (5,   5,   []),
        (6,   3,   [('z', 90)]),
        (7,   7,   []),
        (8,   1,   [('z', 270)]),
        (9,   3,   [('z', 270)]),
        (10,  5,   [('z', 90)]),
        (11,  7,   [('z', 270)]),
        (12,  3,   [('z', 180)]),
        (13,  7,   [('z', 180)]),
        (14,  7,   [('z', 90)]),
        (15,  15,  []),
        (16,  1,   [('y', 90)]),
        (17,  3,   [('y', 90)]),
        (18,  5,   [('x', 270)]),
        (19,  7,   [('z', 180), ('x', 270)]),
        (20,  20,  []),
        (21,  21,  []),
        (22,  21,  [('z', 180), ('x', 270)]),
        (23,  23,  []),
        (24,  5,   [('y', 90)]),
        (25,  7,   [('y', 90)]),
        (26,  26,  []),
        (27,  27,  []),
        (28,  21,  [('z', 180), ('y', 90)]),
        (29,  29,  []),
        (30,  30,  []),
        (31,  31,  []),
        (32,  1,   [('y', 180)]),
        (33,  5,   [('z', 90), ('x', 270)]),
        (34,  3,   [('y', 270)]),
        (35,  7,   [('z', 90), ('x', 270)]),
        (36,  5,   [('z', 90), ('y', 270)]),
        (37,  26,  [('z', 90)]),
        (38,  7,   [('z', 270), ('y', 270)]),
        (39,  27,  [('z', 90)]),
        (40,  20,  [('z', 90)]),
        (41,  21,  [('z', 270), ('x', 270)]),
        (42,  21,  [('z', 90)]),
        (43,  29,  [('z', 90)]),
        (44,  21,  [('z', 270), ('y', 270)]),
        (45,  30,  [('z', 90)]),
        (46,  23,  [('z', 90)]),
        (47,  31,  [('z', 90)]),
        (48,  3,   [('y', 180)]),
        (49,  7,   [('z', 270), ('x', 270)]),
        (50,  7,   [('x', 270)]),
        (51,  15,  [('x', 270)]),
        (52,  21,  [('z', 90), ('y', 270)]),
        (53,  30,  [('z', 180), ('x', 270)]),
        (54,  29,  [('z', 90), ('y', 270)]),
        (55,  31,  [('z', 180), ('x', 270)]),
        (56,  21,  [('y', 90)]),
        (57,  23,  [('y', 90)]),
        (58,  30,  [('z', 270), ('x', 270)]),
        (59,  31,  [('z', 270), ('x', 270)]),
        (60,  60,  []),
        (61,  61,  []),
        (62,  61,  [('z', 180), ('x', 270)]),
        (63,  63,  []),
        (64,  1,   [('z', 90), ('x', 180)]),
        (65,  20,  [('z', 180)]),
        (66,  5,   [('y', 270)]),
        (67,  21,  [('y', 270)]),
        (68,  3,   [('z', 90), ('x', 90)]),
        (69,  21,  [('z', 180)]),
        (70,  7,   [('z', 180), ('y', 270)]),
        (71,  29,  [('z', 180)]),
        (72,  5,   [('x', 90)]),
        (73,  21,  [('x', 90)]),
        (74,  26,  [('z', 180)]),
        (75,  30,  [('z', 180)]),
        (76,  7,   [('x', 90)]),
        (77,  23,  [('z', 180)]),
        (78,  27,  [('z', 180)]),
        (79,  31,  [('z', 180)]),
        (80,  5,   [('z', 90), ('y', 180)]),
        (81,  21,  [('z', 90), ('y', 180)]),
        (82,  26,  [('y', 180)]),
        (83,  30,  [('z', 90), ('x', 270)]),
        (84,  21,  [('z', 90), ('x', 180)]),
        (85,  60,  [('y', 270)]),
        (86,  30,  [('z', 90), ('y', 270)]),
        (87,  61,  [('y', 270)]),
        (88,  26,  [('x', 180)]),
        (89,  30,  [('z', 270), ('y', 90)]),
        (90,  90,  []),
        (91,  91,  []),
        (92,  30,  [('z', 270), ('x', 90)]),
        (93,  61,  [('z', 180), ('y', 90)]),
        (94,  91,  [('z', 180)]),
        (95,  95,  []),
        (96,  3,   [('z', 90), ('y', 270)]),
        (97,  21,  [('z', 90), ('x', 270)]),
        (98,  7,   [('y', 270)]),
        (99,  23,  [('y', 270)]),
        (100, 7,   [('z', 90), ('y', 270)]),
        (101, 30,  [('y', 270)]),
        (102, 15,  [('y', 270)]),
        (103, 31,  [('y', 270)]),
        (104, 21,  [('z', 180), ('x', 90)]),
        (105, 60,  [('z', 90)]),
        (106, 30,  [('z', 270), ('y', 270)]),
        (107, 61,  [('z', 90)]),
        (108, 29,  [('z', 180), ('x', 90)]),
        (109, 61,  [('z', 270), ('y', 270)]),
        (110, 31,  [('z', 270), ('y', 270)]),
        (111, 63,  [('z', 90)]),
        (112, 7,   [('z', 90), ('x', 180)]),
        (113, 29,  [('z', 90), ('y', 180)]),
        (114, 27,  [('y', 180)]),
        (115, 31,  [('z', 90), ('x', 270)]),
        (116, 23,  [('z', 90), ('y', 270)]),
        (117, 61,  [('z', 90), ('x', 270)]),
        (118, 31,  [('z', 90), ('y', 270)]),
        (119, 63,  [('y', 270)]),
        (120, 30,  [('x', 180)]),
        (121, 61,  [('z', 90), ('y', 180)]),
        (122, 91,  [('y', 180)]),
        (123, 95,  [('z', 90), ('x', 270)]),
        (124, 61,  [('z', 180), ('x', 90)]),
        (125, 125, []),
        (126, 95,  [('z', 90), ('y', 270)]),
        (127, 127, []),
        (128, 1,   [('x', 180)]),
        (129, 5,   [('z', 90), ('y', 90)]),
        (130, 20,  [('z', 270)]),
        (131, 21,  [('z', 90), ('y', 90)]),
        (132, 5,   [('z', 90), ('x', 90)]),
        (133, 26,  [('z', 270)]),
        (134, 21,  [('z', 90), ('x', 90)]),
        (135, 30,  [('z', 270)]),
        (136, 3,   [('z', 180), ('y', 90)]),
        (137, 7,   [('z', 90), ('y', 90)]),
        (138, 21,  [('z', 270)]),
        (139, 23,  [('z', 270)]),
        (140, 7,   [('z', 270), ('x', 90)]),
        (141, 27,  [('z', 270)]),
        (142, 29,  [('z', 270)]),
        (143, 31,  [('z', 270)]),
        (144, 3,   [('z', 90), ('y', 180)]),
        (145, 7,   [('z', 270), ('y', 90)]),
        (146, 21,  [('x', 270)]),
        (147, 29,  [('x', 270)]),
        (148, 21,  [('z', 270), ('x', 90)]),
        (149, 30,  [('z', 180), ('y', 90)]),
        (150, 60,  [('z', 270)]),
        (151, 61,  [('z', 90), ('y', 90)]),
        (152, 7,   [('z', 180), ('y', 90)]),
        (153, 15,  [('y', 90)]),
        (154, 30,  [('z', 90), ('y', 90)]),
        (155, 31,  [('z', 90), ('y', 90)]),
        (156, 23,  [('z', 180), ('y', 90)]),
        (157, 31,  [('z', 180), ('y', 90)]),
        (158, 61,  [('z', 270)]),
        (159, 63,  [('z', 270)]),
        (160, 5,   [('y', 180)]),
        (161, 26,  [('y', 90)]),
        (162, 21,  [('y', 180)]),
        (163, 30,  [('x', 270)]),
        (164, 26,  [('z', 90), ('x', 180)]),
        (165, 90,  [('z', 90)]),
        (166, 30,  [('z', 180), ('y', 270)]),
        (167, 91,  [('z', 90)]),
        (168, 21,  [('x', 180)]),
        (169, 30,  [('y', 90)]),
        (170, 60,  [('y', 90)]),
        (171, 61,  [('z', 270), ('x', 270)]),
        (172, 30,  [('z', 180), ('x', 90)]),
        (173, 91,  [('z', 270)]),
        (174, 61,  [('z', 90), ('x', 90)]),
        (175, 95,  [('z', 90)]),
        (176, 7,   [('y', 180)]),
        (177, 27,  [('y', 90)]),
        (178, 23,  [('y', 180)]),
        (179, 31,  [('x', 270)]),
        (180, 30,  [('z', 90), ('x', 180)]),
        (181, 91,  [('y', 90)]),
        (182, 61,  [('z', 90), ('y', 270)]),
        (183, 95,  [('x', 270)]),
        (184, 29,  [('y', 90)]),
        (185, 31,  [('y', 90)]),
        (186, 61,  [('y', 90)]),
        (187, 63,  [('y', 90)]),
        (188, 61,  [('x', 180)]),
        (189, 95,  [('y', 90)]),
        (190, 125, [('z', 270)]),
        (191, 127, [('z', 270)]),
        (192, 3,   [('x', 180)]),
        (193, 21,  [('z', 270), ('y', 90)]),
        (194, 21,  [('z', 180), ('y', 270)]),
        (195, 60,  [('z', 180)]),
        (196, 7,   [('z', 90), ('x', 90)]),
        (197, 30,  [('x', 90)]),
        (198, 23,  [('z', 90), ('x', 90)]),
        (199, 61,  [('z', 180)]),
        (200, 7,   [('z', 180), ('x', 90)]),
        (201, 29,  [('x', 90)]),
        (202, 30,  [('z', 90), ('x', 90)]),
        (203, 61,  [('x', 90)]),
        (204, 15,  [('x', 90)]),
        (205, 31,  [('x', 90)]),
        (206, 31,  [('z', 90), ('x', 90)]),
        (207, 63,  [('z', 180)]),
        (208, 7,   [('z', 90), ('y', 180)]),
        (209, 23,  [('z', 90), ('y', 180)]),
        (210, 30,  [('y', 180)]),
        (211, 61,  [('x', 270)]),
        (212, 29,  [('z', 90), ('x', 180)]),
        (213, 61,  [('z', 270), ('x', 90)]),
        (214, 61,  [('z', 90), ('x', 180)]),
        (215, 125, [('z', 180)]),
        (216, 27,  [('x', 180)]),
        (217, 31,  [('z', 270), ('y', 90)]),
        (218, 91,  [('x', 180)]),
        (219, 95,  [('z', 90), ('y', 90)]),
        (220, 31,  [('z', 270), ('x', 90)]),
        (221, 63,  [('z', 180), ('y', 90)]),
        (222, 95,  [('z', 90), ('x', 90)]),
        (223, 127, [('z', 180)]),
        (224, 7,   [('x', 180)]),
        (225, 30,  [('z', 90), ('y', 180)]),
        (226, 29,  [('y', 180)]),
        (227, 61,  [('y', 180)]),
        (228, 27,  [('z', 90), ('x', 180)]),
        (229, 91,  [('z', 90), ('x', 180)]),
        (230, 31,  [('z', 180), ('y', 270)]),
        (231, 95,  [('y', 270)]),
        (232, 23,  [('x', 180)]),
        (233, 61,  [('z', 270), ('y', 90)]),
        (234, 61,  [('z', 180), ('y', 270)]),
        (235, 125, [('z', 90)]),
        (236, 31,  [('z', 180), ('x', 90)]),
        (237, 95,  [('x', 90)]),
        (238, 63,  [('z', 90), ('x', 90)]),
        (239, 127, [('z', 90)]),
        (240, 15,  [('y', 180)]),
        (241, 31,  [('z', 90), ('y', 180)]),
        (242, 31,  [('y', 180)]),
        (243, 63,  [('y', 180)]),
        (244, 31,  [('z', 90), ('x', 180)]),
        (245, 95,  [('z', 90), ('y', 180)]),
        (246, 63,  [('z', 90), ('y', 270)]),
        (247, 127, [('y', 270)]),
        (248, 31,  [('x', 180)]),
        (249, 63,  [('z', 90), ('y', 180)]),
        (250, 95,  [('y', 180)]),
        (251, 127, [('y', 180)]),
        (252, 63,  [('x', 180)]),
        (253, 127, [('z', 90), ('y', 180)]),
        (254, 127, [('x', 180)]),
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
    reconcile1()
