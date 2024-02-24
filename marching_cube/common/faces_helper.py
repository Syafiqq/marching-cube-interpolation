import numpy as np


def __get_index(arr: [[int]], target: [int]) -> int:
    return np.where((arr == target).all(axis=1))[0][0]


def define_faces_from_center(vertices: [[int]], point_to_cover: [int]) -> [int]:
    # Calculate the vectors from the center to each vertex
    vectors = vertices - point_to_cover

    # Calculate the cross product of the vectors
    cross_product = np.cross(vectors[0], vectors[1])

    # Calculate the dot product of the cross product and the third vector
    dot_product = np.dot(cross_product, vectors[2])

    # If the dot product is negative, reverse the order of the vertices
    if dot_product < 0:
        vertices_reversed = vertices[::-1]
    else:
        vertices_reversed = vertices

    # Return the indices of the ordered vertices
    return [__get_index(vertices, vertex) for vertex in vertices_reversed]
