from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


def create_3d_plot(fig: Figure, fig_index: Tuple[int, int, int], vertices: [Tuple[int, int, int]]):
    # Create the subplot
    ax = fig.add_subplot(fig_index[0], fig_index[1], fig_index[2], projection='3d')

    # Set label
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Set orientation of the axes
    ax.view_init(elev=-345, azim=-35)

    # Set tick marks
    ax.set_xticks([0, 0.5, 1, 1.5])
    ax.set_yticks([0, 0.5, 1, 1.5])
    ax.set_zticks([0, 0.5, 1, 1.5])

    # Draw axis lines
    ax.plot([0, 1.5], [0, 0], [0, 0], color='r')
    ax.plot([0, 0], [0, 1.5], [0, 0], color='g')
    ax.plot([0, 0], [0, 0], [0, 1.5], color='b')

    # Define points and labels
    points = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]
    labels = ['1', '2', '3', '4', '5', '6', '7', '8']

    # Plot points
    for point, label in zip(points, labels):
        ax.scatter(*point, label=label, s=100, c='gray')
        ax.text(*point, label, fontsize=16)


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
    show_cube()
