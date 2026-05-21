import random
from typing import Optional

from config import (
    ENEMY_BULLET_HEIGHT,
    ENEMY_BULLET_WIDTH,
    ENEMY_KILL_SHOT_SPEEDUP,
    ENEMY_KILL_SPEED,
    ENEMY_LEVEL_SPEED,
    ENEMY_MIN_SHOT_INTERVAL,
    ENEMY_MOVE_DOWN_STEP,
    ENEMY_MOVE_SPEED,
    ENEMY_SHOT_INTERVAL,
    SCREEN_WIDTH,
    SIDE_PADDING,
)
from models import Enemy, EnemyBullet


def get_alive_enemies(enemies: list[Enemy]) -> list[Enemy]:
    return [enemy for enemy in enemies if enemy.is_alive]


def calculate_enemy_speed(level: int, total_enemies: int, alive_enemies: int) -> float:
    killed_enemies = max(0, total_enemies - alive_enemies)
    return ENEMY_MOVE_SPEED + (level - 1) * ENEMY_LEVEL_SPEED + killed_enemies * ENEMY_KILL_SPEED


def enemies_reached_side(enemies: list[Enemy], enemy_shift: float) -> bool:
    left_side = min(enemy.x for enemy in enemies)
    right_side = max(enemy.right for enemy in enemies)
    return left_side + enemy_shift < SIDE_PADDING or right_side + enemy_shift > SCREEN_WIDTH - SIDE_PADDING


def move_enemies_side(enemies: list[Enemy], enemy_shift: float) -> None:
    for enemy in enemies:
        enemy.x += enemy_shift


def move_enemies_down(enemies: list[Enemy]) -> None:
    for enemy in enemies:
        enemy.y += ENEMY_MOVE_DOWN_STEP


def choose_enemy_shooter(enemies: list[Enemy]) -> Optional[Enemy]:
    alive_enemies = get_alive_enemies(enemies)
    if not alive_enemies:
        return None
    return random.choice(alive_enemies)


def calculate_enemy_shot_interval(level: int, total_enemies: int, alive_enemies: int) -> float:
    killed_enemies = max(0, total_enemies - alive_enemies)
    level_speedup = max(0, level - 1) * 0.08
    kill_speedup = killed_enemies * ENEMY_KILL_SHOT_SPEEDUP
    interval = ENEMY_SHOT_INTERVAL - level_speedup - kill_speedup
    return max(ENEMY_MIN_SHOT_INTERVAL, interval)


def create_enemy_bullet(enemy: Enemy) -> EnemyBullet:
    bullet_x = enemy.x + enemy.width / 2 - ENEMY_BULLET_WIDTH / 2
    bullet_y = enemy.bottom
    return EnemyBullet(bullet_x, bullet_y, ENEMY_BULLET_WIDTH, ENEMY_BULLET_HEIGHT)
