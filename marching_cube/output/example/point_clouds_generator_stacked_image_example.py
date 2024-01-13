from marching_cube.domain.point_clouds import point_clouds_generator_stacked_image


def example():
    input_paths = [
        '../../input/resource/image/sq-object/sq-0001.png',
        '../../input/resource/image/sq-object/sq-0002.png',
        '../../input/resource/image/sq-object/sq-0003.png',
        '../../input/resource/image/sq-object/sq-0004.png',
        '../../input/resource/image/sq-object/sq-0005.png',
        '../../input/resource/image/sq-object/sq-0006.png',
    ]
    xy_size = 20

    values, metadata = point_clouds_generator_stacked_image.generate(input_paths, xy_size)
    print(metadata)


if __name__ == "__main__":
    pass
