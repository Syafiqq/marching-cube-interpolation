import numpy as np


def uniform_grid(
        dims: [int],
        spacing: (float, float, float) = (1.0, 1.0, 1.0),
        origin: (float, float, float) = (0.0, 0.0, 0.0)
) -> np.ndarray:
    nx, ny, nz = dims
    nx -= 1
    ny -= 1
    nz -= 1
    # get the points and convert to spacings
    dx, dy, dz = spacing
    # Now make the cell arrays
    ox, oy, oz = np.array(origin)  # type: ignore
    x = np.insert(np.cumsum(np.full(nx, dx)), 0, 0.0) + ox
    y = np.insert(np.cumsum(np.full(ny, dy)), 0, 0.0) + oy
    z = np.insert(np.cumsum(np.full(nz, dz)), 0, 0.0) + oz
    xx, yy, zz = np.meshgrid(x, y, z, indexing='ij')
    return np.c_[xx.ravel(order='F'), yy.ravel(order='F'), zz.ravel(order='F')]
