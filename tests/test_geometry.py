from geometry import bullet_path_hits_point, clamp, point_inside_rect
from models import Bullet


def test_bullet_path_hits_point() -> None:
    assert bullet_path_hits_point(10, 10, 9, 9, 9, 9) is True


def test_point_inside_rect() -> None:
    bullet = Bullet(10, 10, 4, 16)

    assert point_inside_rect(10, 10, bullet) is True
    assert point_inside_rect(9, 9, bullet) is False


def test_clamp_blocks_wall_escape() -> None:
    assert clamp(-10, 0, 100) == 0
    assert clamp(120, 0, 100) == 100
    assert clamp(50, 0, 100) == 50
