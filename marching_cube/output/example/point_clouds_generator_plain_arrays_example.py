from marching_cube.domain.point_clouds import point_clouds_generator_plain_arrays


def example_sq_object_from_sanitised_txt():
    input_path = '../../input/resource/plain/sq_object_sanitised.txt'
    xy_size = 21
    z_size = 8

    _, metadata = point_clouds_generator_plain_arrays.generate_by_input(input_path, xy_size, z_size)
    print(metadata)


if __name__ == "__main__":
    pass
