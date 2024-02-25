import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def show_cube():
    # Create axis
    axes = [5, 5, 5]

    # Create Data
    data = np.ones(axes, dtype=bool)

    # Control Transparency
    alpha = 0.9

    # Control colour
    colors = np.empty(axes + [4], dtype=np.float32)

    colors[:] = [1, 0, 0, alpha]  # red

    # Plot figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Set labels for axes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Voxels is used to customizations of the
    # sizes, positions and colors.
    ax.voxels(data, facecolors=colors)
    plt.show()


if __name__ == "__main__":
    show_cube()
