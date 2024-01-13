from marching_cube.domain.point_clouds import point_clouds_generator_minimap


def example():
    values, metadata = point_clouds_generator_minimap.generate([[[1]]])
    print(metadata)


if __name__ == "__main__":
    pass
