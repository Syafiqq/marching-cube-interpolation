import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def show_cube():
    # Plot figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

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
        ax.scatter(*point, label=label, s=100, c='blue')
        ax.text(*point, label, fontsize=16)

    points = [(0, 0, 0)]
    labels = ['1']
    # Plot points
    for point, label in zip(points, labels):
        ax.scatter(*point, label=label, s=50, c='red')
        ax.text(*point, label, fontsize=16)

    # Show legend

    plt.show()


if __name__ == "__main__":
    show_cube()
