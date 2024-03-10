import numpy as np

from marching_cube.common.faces_helper import define_faces_from_center


def test_define_faces_from_center():
    vertices = np.array([[0.25, 0, 0], [0, 0.25, 0], [0, 0, 0.25]])
    center = np.array([0.5, 0.5, 0.5])
    expected_faces = [2, 1, 0]
    assert define_faces_from_center(vertices, center) == expected_faces


def main():
    vertices = np.array([[0.25, 0, 0], [0, 0.25, 0], [0, 0, 0.25]])
    center = np.array([0.5, 0.5, 0.5])

    # call construct_face_away
    faces = define_faces_from_center(vertices, center)
    v1, v2, v3 = vertices[faces]

    print(f"Vertices: {vertices}")
    print(f"Center: {center}")
    print(f"Faces: {faces}")
    print(f"v1: {v1}, v2: {v2}, v3: {v3}")


if __name__ == "__main__":
    main()
