import math
from typing import Tuple, Dict

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from test_1 import generate_binary_combinations, reverse_coordinate_mapping, rotate_points_around_center, \
    reverse_coordinate_mapping_tuple


def split_number(number: int, max_value: int) -> list[int]:
    result = []
    while number > max_value:
        result.append(max_value)
        number -= max_value
    result.append(number)
    return result


def create_subplot_index(n_rows: int, n_cols: int, rotation: int):
    subplot_index = list(range(1, (n_rows * n_cols) + 1))
    if n_cols > 1 and rotation > 0:
        # remove extra content
        extra_content = rotation % 2
        for i in range((n_rows * n_cols) + 1 - extra_content, (n_rows * n_cols) + 1):
            subplot_index.remove(i)
    subplots = []
    for subplot in subplot_index:
        subplots.append((n_rows, n_cols, subplot))
    return subplots


def create_image_plot(file_path: str, index: int, origin: int, rotation: list[Tuple[str, int]]):
    new_rotation: list[Tuple[str, int]] = []
    for axis, value in rotation:
        if value > 90:
            for v in split_number(value, 90):
                new_rotation.append((axis, v))

    if len(new_rotation) > 0:
        rotation = new_rotation
    del new_rotation

    n_rows = 1 + math.ceil(len(rotation) / 2)
    n_cols = 2
    fig_index = create_subplot_index(n_rows, n_cols, len(rotation))

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
    center = np.array([0.5, 0.5, 0.5])
    vertices: list[list[Tuple[int, int, int]]] = []
    titles: list[str] = []

    # Vertices start
    end_cube_point = cube_points[index]
    end_indices = [i for i, x in enumerate(end_cube_point) if x == 1]
    end_vertices: list[Tuple[int, int, int]] = [reverse_coordinate_mapping_tuple[i] for i in end_indices]
    vertices.append(end_vertices)
    titles.append(f'Rule: {index}')

    # Vertices start
    start_cube_point = cube_points[origin]
    start_indices = [i for i, x in enumerate(start_cube_point) if x == 1]
    start_vertices: list[Tuple[int, int, int]] = [reverse_coordinate_mapping_tuple[i] for i in start_indices]
    vertices.append(start_vertices)
    titles.append(f'Origin: {origin}')

    np_vertices = np.array(start_vertices)
    rotated_points = np_vertices
    for axis, angle in rotation:
        angles_rad = angle * (np.pi / 180)
        rotated_points = rotate_points_around_center(rotated_points, angles_rad, axis, center)
        rotated_points_tuple: list[Tuple[int, int, int]] = [
            tuple(np.round(point).astype(int)) for point in rotated_points
        ]
        vertices.append(rotated_points_tuple)
        titles.append(f'Rotate: {angle}° axis: {axis}')

    # Create a figure
    fig = plt.figure(figsize=(240 * n_cols / 80, 240 * n_rows / 80), dpi=80)
    for (fig_index, title, vertex) in zip(fig_index, titles, vertices):
        create_3d_plot(fig, fig_index, title, vertex)

    plt.savefig(file_path)
    plt.close()


def create_3d_plot(
        fig: Figure,
        fig_index: Tuple[int, int, int],
        title: str,
        vertices: [Tuple[int, int, int]],
):
    # Create the subplot
    plot = fig.add_subplot(fig_index[0], fig_index[1], fig_index[2], projection='3d')

    # Set label
    plot.set_xlabel('X')
    plot.set_ylabel('Y')
    plot.set_zlabel('Z')

    plot.set_title(title)

    # Set orientation of the axes
    plot.view_init(elev=-345, azim=-35)

    # Set tick marks
    plot.set_xticks([0, 0.5, 1, 1.5])
    plot.set_yticks([0, 0.5, 1, 1.5])
    plot.set_zticks([0, 0.5, 1, 1.5])

    # Draw axis lines
    plot.plot([0, 1.5], [0, 0], [0, 0], color='r')
    plot.plot([0, 0], [0, 1.5], [0, 0], color='g')
    plot.plot([0, 0], [0, 0], [0, 1.5], color='b')

    # Define points and labels
    points = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]
    labels = ['1', '2', '3', '4', '5', '6', '7', '8']

    # Plot points placeholder
    for point, label in zip(points, labels):
        plot.scatter(*point, label=label, s=50, c='gray')
        plot.text(*point, label, fontsize=16)

    # Plot points placeholder
    for vertex in vertices:
        plot.scatter(*vertex, s=100, c='red')


def show_cube():
    # Create a figure
    fig = plt.figure(figsize=(960 / 80, 480 / 80), dpi=80)

    # Create the first subplot
    ax1 = fig.add_subplot(121, projection='3d')

    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')

    # Set orientation of the axes
    ax1.view_init(elev=-345, azim=-35)

    # Set tick marks
    ax1.set_xticks([0, 0.5, 1, 1.5])
    ax1.set_yticks([0, 0.5, 1, 1.5])
    ax1.set_zticks([0, 0.5, 1, 1.5])

    # Draw axis lines
    ax1.plot([0, 1.5], [0, 0], [0, 0], color='r')
    ax1.plot([0, 0], [0, 1.5], [0, 0], color='g')
    ax1.plot([0, 0], [0, 0], [0, 1.5], color='b')

    # Define points and labels
    points = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]
    labels = ['1', '2', '3', '4', '5', '6', '7', '8']

    # Plot points
    for point, label in zip(points, labels):
        ax1.scatter(*point, label=label, s=100, c='blue')
        ax1.text(*point, label, fontsize=16)

    points = [(0, 0, 0)]
    labels = ['1']
    # Plot points
    for point, label in zip(points, labels):
        ax1.scatter(*point, label=label, s=50, c='red')
        ax1.text(*point, label, fontsize=16)

    # Define mesh points
    mesh_points = np.array([(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)])
    mesh_points_line = np.append(mesh_points, [mesh_points[0]], axis=0)
    ax1.plot(mesh_points_line[:, 0], mesh_points_line[:, 1], mesh_points_line[:, 2], color='red', linewidth=3)

    # Create mesh
    X = np.array([[mesh_points[0, 0], mesh_points[1, 0]], [mesh_points[3, 0], mesh_points[2, 0]]])
    Y = np.array([[mesh_points[0, 1], mesh_points[1, 1]], [mesh_points[3, 1], mesh_points[2, 1]]])
    Z = np.array([[mesh_points[0, 2], mesh_points[1, 2]], [mesh_points[3, 2], mesh_points[2, 2]]])
    ax1.plot_surface(X, Y, Z, color='yellow', alpha=0.5)

    # Define line points
    line_points = np.array([(1, 0, 0), (0, 1, 0)])

    # Create line
    ax1.plot(line_points[:, 0], line_points[:, 1], line_points[:, 2], color='red', linewidth=3)

    # Create the second subplot
    ax2 = fig.add_subplot(122)

    # Plot on the second subplot
    ax2.plot([4, 3, 2, 1])

    # Adjust the spacing between subplots
    plt.subplots_adjust(wspace=0.5, hspace=0.5)

    # Show the figure with both subplots
    plt.show()


if __name__ == "__main__":
    # show_cube()
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
    for index, origin, rotation in dataset:
        create_image_plot(f'/tmp/fig_ordered/{str(index).zfill(3)}.png', index, origin, rotation)
