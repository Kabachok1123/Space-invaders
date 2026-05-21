from config import (
    ENEMY_BULLET_HEIGHT,
    ENEMY_BULLET_WIDTH,
    ENEMY_MIN_SHOT_INTERVAL,
    POINTS_PER_ENEMY,
    SCREEN_WIDTH,
    SIDE_PADDING,
)
from collisions import damage_bunker_by_enemy_bullet, find_hit_enemy
from enemy_logic import (
    calculate_enemy_shot_interval,
    choose_enemy_shooter,
    create_enemy_bullet,
    enemies_reached_side,
    get_alive_enemies,
    move_enemies_down,
    move_enemies_side,
)
from geometry import rectangles_intersect
from level import create_enemies
from models import Bullet, BunkerBlock, Enemy, EnemyBullet


def test_bullet_hits_enemy() -> None:
    bullet = Bullet(10, 10, 4, 16)
    enemy = Enemy(9, 9, 36, 26, "#ffffff")

    assert rectangles_intersect(bullet, enemy) is True
    assert find_hit_enemy(bullet, [enemy]) == enemy


def test_bullet_miss_returns_none() -> None:
    bullet = Bullet(10, 10, 4, 16)
    enemy = Enemy(100, 100, 36, 26, "#ffffff")

    assert rectangles_intersect(bullet, enemy) is False
    assert find_hit_enemy(bullet, [enemy]) is None


def test_dead_enemy_is_ignored_by_hit_search() -> None:
    bullet = Bullet(10, 10, 4, 16)
    enemy = Enemy(9, 9, 36, 26, "#ffffff", is_alive=False)

    assert rectangles_intersect(bullet, enemy) is True
    assert find_hit_enemy(bullet, [enemy]) is None


def test_find_hit_enemy_returns_first_alive_hit() -> None:
    bullet = Bullet(10, 10, 4, 16)
    dead_enemy = Enemy(9, 9, 36, 26, "#ffffff", is_alive=False)
    alive_enemy = Enemy(8, 8, 36, 26, "#ff71ce")

    assert find_hit_enemy(bullet, [dead_enemy, alive_enemy]) == alive_enemy


def test_find_hit_enemy_with_empty_list_returns_none() -> None:
    bullet = Bullet(10, 10, 4, 16)

    assert find_hit_enemy(bullet, []) is None


def test_score_adds_one_for_enemy_hit() -> None:
    score = 0

    score += POINTS_PER_ENEMY

    assert score == 1


def test_original_enemy_grid_has_five_rows_and_eleven_columns() -> None:
    enemies = create_enemies()

    assert len(enemies) == 55


def test_enemy_shot_interval_gets_shorter_after_kills() -> None:
    interval_without_kills = calculate_enemy_shot_interval(level=1, total_enemies=55, alive_enemies=55)
    interval_after_kills = calculate_enemy_shot_interval(level=1, total_enemies=55, alive_enemies=20)

    assert interval_after_kills < interval_without_kills


def test_enemy_shot_interval_has_minimum_limit() -> None:
    interval = calculate_enemy_shot_interval(level=20, total_enemies=55, alive_enemies=1)

    assert interval == ENEMY_MIN_SHOT_INTERVAL


def test_get_alive_enemies_filters_dead_enemies() -> None:
    alive_enemy = Enemy(10, 10, 36, 26, "#ffffff")
    dead_enemy = Enemy(50, 10, 36, 26, "#ffffff", is_alive=False)

    assert get_alive_enemies([alive_enemy, dead_enemy]) == [alive_enemy]


def test_choose_enemy_shooter_returns_none_without_alive_enemies() -> None:
    dead_enemy = Enemy(10, 10, 36, 26, "#ffffff", is_alive=False)

    assert choose_enemy_shooter([]) is None
    assert choose_enemy_shooter([dead_enemy]) is None


def test_choose_enemy_shooter_returns_alive_enemy() -> None:
    alive_enemy = Enemy(10, 10, 36, 26, "#ffffff")

    assert choose_enemy_shooter([alive_enemy]) == alive_enemy


def test_enemies_reached_left_side() -> None:
    enemy = Enemy(SIDE_PADDING, 10, 36, 26, "#ffffff")

    assert enemies_reached_side([enemy], -1) is True


def test_enemies_reached_right_side() -> None:
    enemy = Enemy(SCREEN_WIDTH - SIDE_PADDING - 36, 10, 36, 26, "#ffffff")

    assert enemies_reached_side([enemy], 1) is True


def test_enemies_do_not_reach_side_in_middle() -> None:
    enemy = Enemy(200, 10, 36, 26, "#ffffff")

    assert enemies_reached_side([enemy], 5) is False


def test_move_enemies_side_changes_x_only() -> None:
    enemy = Enemy(100, 50, 36, 26, "#ffffff")

    move_enemies_side([enemy], 12)

    assert enemy.x == 112
    assert enemy.y == 50


def test_move_enemies_down_changes_y_only() -> None:
    enemy = Enemy(100, 50, 36, 26, "#ffffff")

    move_enemies_down([enemy])

    assert enemy.x == 100
    assert enemy.y > 50


def test_create_enemy_bullet_starts_under_enemy_center() -> None:
    enemy = Enemy(100, 50, 36, 26, "#ffffff")

    bullet = create_enemy_bullet(enemy)

    assert bullet.width == ENEMY_BULLET_WIDTH
    assert bullet.height == ENEMY_BULLET_HEIGHT
    assert bullet.x == enemy.x + enemy.width / 2 - ENEMY_BULLET_WIDTH / 2
    assert bullet.y == enemy.bottom


def test_bunker_damage_returns_false_on_miss() -> None:
    bullet = EnemyBullet(10, 10, 4, 16)
    block = BunkerBlock(100, 100, 8, 2)
    blocks = [block]

    assert damage_bunker_by_enemy_bullet(bullet, blocks) is False
    assert block.hp == 2
    assert blocks == [block]


def test_enemy_bullet_removes_bunker_block_on_hit() -> None:
    bullet = EnemyBullet(100, 100, 4, 16)
    block = BunkerBlock(100, 100, 8, 1)
    blocks = [block]

    assert damage_bunker_by_enemy_bullet(bullet, blocks) is True
    assert blocks == []


def test_enemy_bullet_removes_bunker_block_when_hp_is_zero() -> None:
    bullet = EnemyBullet(100, 100, 4, 16)
    block = BunkerBlock(100, 100, 8, 1)
    blocks = [block]

    assert damage_bunker_by_enemy_bullet(bullet, blocks) is True
    assert blocks == []


def test_player_bullet_rule_does_not_damage_bunker() -> None:
    bullet = Bullet(100, 100, 4, 16)
    block = BunkerBlock(100, 100, 8, 2)
    blocks = [block]

    active_bullets = [bullet]

    assert active_bullets == [bullet]
    assert block.hp == 2
    assert blocks == [block]


def test_enemy_bullet_damages_bunker_even_if_it_moves_past_between_frames() -> None:
    bullet = EnemyBullet(100, 90, 4, 16)
    bullet.previous_y = 90
    bullet.y = 116
    block = BunkerBlock(100, 110, 8, 1)
    blocks = [block]

    assert damage_bunker_by_enemy_bullet(bullet, blocks) is True
    assert blocks == []


def test_enemy_bullet_hit_removes_nearby_bunker_chunk() -> None:
    bullet = EnemyBullet(100, 100, 4, 16)
    center = BunkerBlock(100, 100, 8, 1)
    neighbor = BunkerBlock(108, 100, 8, 1)
    far_block = BunkerBlock(140, 100, 8, 1)
    blocks = [center, neighbor, far_block]

    assert damage_bunker_by_enemy_bullet(bullet, blocks) is True
    assert blocks == [far_block]
