from marching_cube.domain.rules.manual_1 import rules_manual_1_v1
from marching_cube.domain.rules.manual_1 import rules_manual_1_v2


def to_points(p: [[float]], point_type: int, variant: int = 1) -> [[float]]:
    if variant == 1:
        return rules_manual_1_v1.to_points(p, point_type)
    elif variant == 2:
        return rules_manual_1_v2.to_points(p, point_type)
    else:
        raise RuntimeError('unknown variant')


def to_faces(p: [[float]], point_type: int, variant: int = 1) -> [int]:
    if variant == 1:
        return rules_manual_1_v1.to_faces(p, point_type)
    elif variant == 2:
        return rules_manual_1_v2.to_faces(p, point_type)
    else:
        raise RuntimeError('unknown variant')
