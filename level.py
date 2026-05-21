import random

from config import (
    BUNKER_BLOCK_HP,
    BUNKER_BLOCK_SIZE,
    BUNKER_COUNT,
    BUNKER_LEFT_MARGIN,
    BUNKER_TOP,
    ENEMY_COLORS,
    ENEMY_COLUMNS,
    ENEMY_HEIGHT,
    ENEMY_HORIZONTAL_GAP,
    ENEMY_ROWS,
    ENEMY_TOP_MARGIN,
    ENEMY_VERTICAL_GAP,
    ENEMY_WIDTH,
    MYSTERY_HEIGHT,
    MYSTERY_SPEED,
    MYSTERY_TOP,
    MYSTERY_WIDTH,
    PLAYER_BOTTOM_MARGIN,
    PLAYER_HEIGHT,
    PLAYER_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from models import BunkerBlock, Enemy, MysteryShip, Player


def create_player() -> Player:
    player_x = SCREEN_WIDTH / 2 - PLAYER_WIDTH / 2
    player_y = SCREEN_HEIGHT - PLAYER_BOTTOM_MARGIN - PLAYER_HEIGHT
    return Player(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)


def create_enemies() -> list[Enemy]:
    enemies = []
    formation_width = ENEMY_WIDTH + (ENEMY_COLUMNS - 1) * ENEMY_HORIZONTAL_GAP
    start_x = SCREEN_WIDTH / 2 - formation_width / 2
    for row in range(ENEMY_ROWS):
        for column in range(ENEMY_COLUMNS):
            enemy_x = start_x + column * ENEMY_HORIZONTAL_GAP
            enemy_y = ENEMY_TOP_MARGIN + row * ENEMY_VERTICAL_GAP
            enemy_color = ENEMY_COLORS[row % len(ENEMY_COLORS)]
            enemies.append(Enemy(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT, enemy_color))
    return enemies


def create_bunkers() -> list[BunkerBlock]:
    blocks = []
    pattern = [
        "01111110",
        "11111111",
        "11111111",
        "11100111",
        "11000011",
    ]
    bunker_width = len(pattern[0]) * BUNKER_BLOCK_SIZE
    spacing = (SCREEN_WIDTH - 2 * BUNKER_LEFT_MARGIN - BUNKER_COUNT * bunker_width) / (BUNKER_COUNT - 1)
    for bunker_index in range(BUNKER_COUNT):
        start_x = BUNKER_LEFT_MARGIN + bunker_index * (bunker_width + spacing)
        add_bunker_blocks(blocks, pattern, start_x)
    return blocks


def add_bunker_blocks(blocks: list[BunkerBlock], pattern: list[str], start_x: float) -> None:
    for row_index, row in enumerate(pattern):
        for column_index, mark in enumerate(row):
            if mark == "1":
                block_x = start_x + column_index * BUNKER_BLOCK_SIZE
                block_y = BUNKER_TOP + row_index * BUNKER_BLOCK_SIZE
                blocks.append(BunkerBlock(block_x, block_y, BUNKER_BLOCK_SIZE, BUNKER_BLOCK_HP))


def create_mystery_ship() -> MysteryShip:
    direction = random.choice([-1, 1])
    x = -MYSTERY_WIDTH if direction > 0 else SCREEN_WIDTH + MYSTERY_WIDTH
    speed = MYSTERY_SPEED * direction
    return MysteryShip(x, MYSTERY_TOP, MYSTERY_WIDTH, MYSTERY_HEIGHT, speed)
