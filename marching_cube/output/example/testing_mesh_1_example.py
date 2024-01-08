import numpy as np
import trimesh
from pathlib import Path

from marching_cube.domain.point_clouds import point_clouds_generator_minimap

from marching_cube.domain.builder.manual_1 import marching_cube_builder_v1
from marching_cube.domain.builder.manual_1 import marching_cube_builder_v1_debug

__variant = 1


def export_model(mesh: trimesh.Trimesh, filename: str):
    mesh.export(filename)


def import_model(filename: str) -> trimesh.Trimesh:
    return trimesh.load(filename)


def print_object(mesh: trimesh.Trimesh):
    # is the current mesh watertight?
    print('mesh.is_watertight', mesh.is_watertight)

    print('mesh.is_winding_consistent', mesh.is_winding_consistent)

    print('mesh.volume', mesh.volume)


def show_vertex_normal(mesh: trimesh.Trimesh):
    vec = np.column_stack((mesh.vertices, mesh.vertices + (mesh.vertex_normals * mesh.scale * .05)))
    path = trimesh.load_path(vec.reshape((-1, 2, 3)))
    trimesh.Scene([mesh, path]).show()


def example_verify_1d_item():
    values, metadata = point_clouds_generator_minimap.generate([[[1]]])
    mesh = marching_cube_builder_v1.build(values, metadata, __variant)

    # export_model(mesh, '~/Desktop/marching_cube_test.stl')
    print_object(mesh)
    show_vertex_normal(mesh)


def example_verify_1d_item_from_file():
    mesh = import_model('~/Desktop/marching_cube_test_fixed.stl')
    print_object(mesh)
    # show_vertex_normal(mesh)
    # mesh1 = import_model('~/Desktop/marching_cube_test.stl')
    # print(mesh1.vertex_normals)
    # print(mesh1.face_normals)

    # mesh = import_model('~/Desktop/marching_cube_test_fixed.stl')
    # print(mesh.vertices)
    # print(mesh.vertex_normals)
    # print(mesh.faces)
    # print(mesh.face_normals)


def compare_original_and_fixes():
    values, metadata = point_clouds_generator_minimap.generate([[[1]]])
    mesh = marching_cube_builder_v1.build(values, metadata, __variant)
    mesh_fixed = import_model('~/Desktop/marching_cube_test_fixed.stl')
    print('point', np.array_equal(mesh.vertices, mesh_fixed.vertices))
    print('faces', np.array_equal(mesh.faces, mesh_fixed.faces))


def looping_invalid_faces():
    for i in range(1, 256, 1):
        values, metadata = point_clouds_generator_minimap.generate([[[i]]])
        mesh = marching_cube_builder_v1.build(values, metadata, __variant)
        if not (mesh.is_watertight and mesh.is_winding_consistent and mesh.is_volume):
            # export_model(mesh, f'~/Desktop/mc/{i}.stl')
            # export_model(mesh, f'~/Desktop/mc/{i}_fixed.stl')
            print(i)
            # break


def fixing_faces_batch():
    for idx in range(1, 256, 1):
        if not Path(f'~/Desktop/mc/{idx}.stl').expanduser().is_file():
            continue
        print(idx)
        values, metadata = point_clouds_generator_minimap.generate([[[idx]]])
        mesh_actual = marching_cube_builder_v1.build(values, metadata, __variant)
        mesh_expected = import_model(f'~/Desktop/mc/{idx}_fixed.stl')
        faces_actual = mesh_actual.faces
        faces_expected = mesh_expected.faces
        vertices_actual = mesh_actual.vertices
        vertices_expected = mesh_expected.vertices
        vertices_expected_list = vertices_expected.tolist()

        # fix faces index
        if not np.array_equal(vertices_actual, vertices_expected):
            swapped_index: [(int, int)] = []  # problematic, actual
            for i, vertices_actual_item in enumerate(vertices_actual):
                if not np.array_equal(vertices_actual_item, vertices_expected[i]):
                    swapped_index.append((vertices_expected_list.index(list(vertices_actual_item)), i))

            i = 0
            while i < len(swapped_index):
                swapped_value = swapped_index[i]
                swapped = (swapped_value[1], swapped_value[0])
                if swapped in swapped_index:
                    del swapped_index[swapped_index.index(swapped)]
                i += 1

            if swapped_index:
                for swapped in swapped_index:
                    if np.array_equal(vertices_actual, np.array(vertices_expected_list)):
                        break
                    vertices_expected_list[swapped[0]], vertices_expected_list[swapped[1]] = \
                        vertices_expected_list[swapped[1]], vertices_expected_list[swapped[0]]

                    faces_expected[faces_expected == swapped[0]] = swapped[0] + 100
                    faces_expected[faces_expected == swapped[1]] = swapped[0]
                    faces_expected[faces_expected == swapped[0] + 100] = swapped[1]

                assert np.array_equal(vertices_actual, np.array(vertices_expected_list))

        faces_comparison = (faces_actual == faces_expected).all(axis=1)
        incorrect_faces_index = [i for i, x in enumerate(faces_comparison) if not x]
        values, metadata = point_clouds_generator_minimap.generate([[[idx]]])
        marching_cube_builder_v1_debug.build(
            values,
            metadata,
            __variant,
            faces_actual.tolist(),
            faces_expected.tolist(),
            incorrect_faces_index
        )


def check_fixed_faces_watertight():
    for i in range(1, 256, 1):
        if not Path(f'~/Desktop/mc/{i}.stl').expanduser().is_file():
            continue
        mesh_actual = import_model(f'~/Desktop/mc/{i}.stl')
        mesh_expected = import_model(f'~/Desktop/mc/{i}_fixed.stl')
        if not (mesh_expected.is_watertight and mesh_expected.is_winding_consistent and mesh_expected.is_volume):
            print(i)


if __name__ == "__main__":
    pass
