import numpy as np

from marching_cube.domain.marching_cube_metadata import MarchingCubeMetadata
from marching_cube.common import multiarray


def generate(minimap: [[[int]]]) -> ([int], MarchingCubeMetadata):
    minimap = np.pad(minimap, pad_width=1)

    nxy_dims = min(minimap.shape[1], minimap.shape[2])
    nz_dims = minimap.shape[0]

    nz_ratio_dims = nz_dims
    nxy_ratio_dims = int(nxy_dims * 1)

    xyz_dims = np.array([nxy_ratio_dims, nxy_ratio_dims, nz_ratio_dims])
    xyz_dims_plus1 = [xyz_dims[0] + 1, xyz_dims[1] + 1, xyz_dims[2] + 1]

    xyz_spacing = (nxy_dims / xyz_dims[0], nxy_dims / xyz_dims[1], 1)
    xyz_points = multiarray.uniform_grid(
        dims=xyz_dims_plus1,
        spacing=xyz_spacing,
        origin=(0, 0, 0),
    )

    metadata = MarchingCubeMetadata(
        nz_dims,
        nxy_dims,
        nz_ratio_dims,
        nxy_ratio_dims,
        xyz_dims,
        xyz_dims_plus1,
        xyz_points
    )

    cxy = metadata.xyz_dims[0] * metadata.xyz_dims[1]
    cx = metadata.xyz_dims[0]

    cxy_plus1 = metadata.xyz_dims_plus1[0] * metadata.xyz_dims_plus1[1]
    cx_plus1 = metadata.xyz_dims_plus1[0]

    values = np.zeros((np.prod(metadata.xyz_dims_plus1),), dtype=int)

    for i in np.arange(0, np.prod(metadata.xyz_dims), 1, dtype=int):
        # @formatter:off
        dz = i // cxy                                       # i div (dimension x and y) to get axis z
        dz_r = i - (dz * cxy)                               # get the remaining of dz
        dy = dz_r // cx                                     # remain of dz div (dimension of x) to get axis y
        dy_r = dz_r - (dy * cx)                             # get the remaining of dy
        dx = dy_r                                           # get the dx

        pt = dz * cxy_plus1 + dy * cx_plus1 + dx * 1        # mapping value to match array of points
        p0 = pt                                             # find the lowest x
        p1 = pt + 1                                         # find the lowest x + 1
        p2 = p0 + cx_plus1                                  # find the lowest x with y + 1
        p3 = p1 + cx_plus1                                  # find the lowest x + 1 with y + 1
        # @formatter:on

        p4 = p0 + cxy_plus1
        p5 = p1 + cxy_plus1
        p6 = p2 + cxy_plus1
        p7 = p3 + cxy_plus1

        value = minimap[dz, dy, dx]

        values[p0] |= value >> 0 & 1
        values[p1] |= value >> 1 & 1
        values[p2] |= value >> 2 & 1
        values[p3] |= value >> 3 & 1
        values[p4] |= value >> 4 & 1
        values[p5] |= value >> 5 & 1
        values[p6] |= value >> 6 & 1
        values[p7] |= value >> 7 & 1

    return values, metadata
