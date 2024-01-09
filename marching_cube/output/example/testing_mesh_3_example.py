import numpy as np
import trimesh

from marching_cube.domain.point_clouds import point_clouds_generator_minimap

from marching_cube.domain.builder.manual_1 import marching_cube_builder_v1

__variant = 2


# https://stackoverflow.com/a/752562
def __split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]


def __export_model(mesh: trimesh.Trimesh, filename: str):
    mesh.export(filename)


def __import_model(filename: str) -> trimesh.Trimesh:
    return trimesh.load(filename)


def __print_object(mesh: trimesh.Trimesh):
    print('mesh.is_watertight', mesh.is_watertight)

    print('mesh.is_winding_consistent', mesh.is_winding_consistent)

    print('mesh.volume', mesh.volume)


def __show_vertex_normal(mesh: trimesh.Trimesh):
    vec = np.column_stack((mesh.vertices, mesh.vertices + (mesh.vertex_normals * mesh.scale * .05)))
    path = trimesh.load_path(vec.reshape((-1, 2, 3)))
    trimesh.Scene([mesh, path]).show()


def __example_verify_item():
    minimap = [(0 + k) % 256 for k in range(27)]
    minimap[len(minimap) // 2] = 1
    minimap = np.reshape(minimap, (3, 3, 3))
    values, metadata = point_clouds_generator_minimap.generate(minimap)
    mesh = marching_cube_builder_v1.build(values, metadata, __variant)

    # export_model(mesh, '~/Desktop/marching_cube_test.stl')
    __print_object(mesh)
    __show_vertex_normal(mesh)


def __looping_invalid_faces():
    for i in np.arange(0, 256, 1, dtype=int):
        for j in np.arange(1, 256, 1, dtype=int):
            minimap = [(i + k) % 256 for k in range(27)]
            minimap[len(minimap) // 2] = j
            minimap = np.reshape(minimap, (3, 3, 3))
            values, metadata = point_clouds_generator_minimap.generate(minimap)
            mesh = marching_cube_builder_v1.build(values, metadata, __variant)
            if not (mesh.is_watertight and mesh.is_winding_consistent and mesh.is_volume):
                # __export_model(mesh, f'~/Desktop/mc/{i}_{j}.stl')
                # __export_model(mesh, f'~/Desktop/mc/{i}_fixed.stl')
                print(i)
                # break


if __name__ == "__main__":
    __looping_invalid_faces()
    pass
