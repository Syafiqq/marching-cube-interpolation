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
    if n_cols > 1:
        # remove extra header
        for i in range(1 + 1, n_cols + 1):
            subplot_index.remove(i)
        # remove extra content
        extra_content = rotation % 2
        for i in range((n_rows * n_cols) - n_cols + 1 - extra_content, (n_rows * n_cols) - n_cols + 1):
            subplot_index.remove(i)
        # remove extra footer
        for i in range((n_rows * n_cols) - n_cols + 1 + 1, (n_rows * n_cols) + 1):
            subplot_index.remove(i)
    subplots = []
    for subplot in subplot_index:
        subplots.append((n_rows, n_cols, subplot))
    return subplots


def create_image_plot(index: int, origin: int, rotation: list[Tuple[str, int]]):
    new_rotation: list[Tuple[str, int]] = []
    for axis, value in rotation:
        if value > 90:
            for v in split_number(value, 90):
                new_rotation.append((axis, v))

    if len(new_rotation) > 0:
        rotation = new_rotation
    del new_rotation

    n_rows = 2 + math.ceil(len(rotation) / 2)
    n_cols = 2 if len(rotation) > 1 else 1
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
    start_cube_point = cube_points[origin]
    start_indices = [i for i, x in enumerate(start_cube_point) if x == 1]
    start_vertices: list[Tuple[int, int, int]] = [reverse_coordinate_mapping_tuple[i] for i in start_indices]
    vertices.append(start_vertices)
    titles.append(f'Initial rule:${origin}')

    np_vertices = np.array(start_vertices)
    rotated_points = np_vertices
    for axis, angle in rotation:
        angles_rad = angle * (np.pi / 180)
        rotated_points = rotate_points_around_center(rotated_points, angles_rad, axis, center)
        rotated_points_tuple: [Tuple[int, int, int]] = [
            tuple(np.round(point).astype(int)) for point in rotated_points
        ]


def create_3d_plot(fig: Figure, fig_index: Tuple[int, int, int], vertices: [Tuple[int, int, int]]):
    # Create the subplot
    plot = fig.add_subplot(fig_index[0], fig_index[1], fig_index[2], projection='3d')

    # Set label
    plot.set_xlabel('X')
    plot.set_ylabel('Y')
    plot.set_zlabel('Z')

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

    # Plot points
    for point, label in zip(points, labels):
        plot.scatter(*point, label=label, s=100, c='gray')
        plot.text(*point, label, fontsize=16)


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
    create_image_plot(254, 127, [('x', 270)])
