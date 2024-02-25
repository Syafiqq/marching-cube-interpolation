import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def show_cube():
    # Create axis
    axes = [1, 1, 1]

    # Plot figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Set labels for axes
    ax.plot([0, 1], [0, 0], [0, 0], color='r')
    ax.plot([0, 0], [0, 1], [0, 0], color='g')
    ax.plot([0, 0], [0, 0], [0, 1], color='b')

    # Voxels is used to customizations of the
    # sizes, positions and colors.
    plt.show()


if __name__ == "__main__":
    show_cube()
