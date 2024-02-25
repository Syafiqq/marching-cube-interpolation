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
    ax.view_init(elev=15, azim=135)

    # Draw axis lines
    ax.plot([0, 1.5], [0, 0], [0, 0], color='r')
    ax.plot([0, 0], [0, 1.5], [0, 0], color='g')
    ax.plot([0, 0], [0, 0], [0, 1.5], color='b')

    # Voxels is used to customizations of the
    # sizes, positions and colors.
    plt.show()


if __name__ == "__main__":
    show_cube()
