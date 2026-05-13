from __future__ import annotations

import random
import tkinter as tk

from config import (
    BACKGROUND_COLOR,
    BULLET_COLOR,
    ENEMY_COLOR,
    GROUND_COLOR,
    PLAYER_ACCENT_COLOR,
    PLAYER_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    STAR_COLORS,
    STAR_COUNT,
    STAR_RANDOM_SEED,
)
from models import Bullet, Enemy, Player, Star


def create_stars() -> list[Star]:
    random_generator = random.Random(STAR_RANDOM_SEED)
    stars = []
    for _ in range(STAR_COUNT):
        stars.append(create_star(random_generator))
    return stars


def create_star(random_generator: random.Random) -> Star:
    return Star(
        x=random_generator.randrange(12, SCREEN_WIDTH - 12),
        y=random_generator.randrange(20, SCREEN_HEIGHT - 75),
        size=random_generator.choice((1, 1, 1, 2)),
        color=random_generator.choice(STAR_COLORS),
    )


def draw_background(canvas: tk.Canvas, stars: list[Star]) -> None:
    canvas.create_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, fill=BACKGROUND_COLOR, width=0, tags="frame")
    for star in stars:
        canvas.create_rectangle(
            star.x,
            star.y,
            star.x + star.size,
            star.y + star.size,
            fill=star.color,
            outline="",
            tags="frame",
        )
    draw_ground_line(canvas)


def draw_ground_line(canvas: tk.Canvas) -> None:
    ground_y = SCREEN_HEIGHT - 35
    canvas.create_line(18, ground_y, SCREEN_WIDTH - 18, ground_y, fill=GROUND_COLOR, width=2, tags="frame")
    for x in range(18, SCREEN_WIDTH - 18, 18):
        canvas.create_line(x, ground_y + 7, x + 8, ground_y + 7, fill=GROUND_COLOR, tags="frame")


def draw_player(canvas: tk.Canvas, player: Player) -> None:
    body_top = player.y + player.height * 0.45
    cannon_top = player.y
    cannon_bottom = player.y + player.height * 0.55

    canvas.create_rectangle(
        player.x + 7,
        body_top,
        player.right - 7,
        player.bottom,
        fill=PLAYER_COLOR,
        outline="",
        tags="frame",
    )
    canvas.create_rectangle(
        player.center_x - 5,
        cannon_top,
        player.center_x + 5,
        cannon_bottom,
        fill=PLAYER_COLOR,
        outline="",
        tags="frame",
    )
    canvas.create_rectangle(
        player.x,
        player.y + player.height * 0.72,
        player.x + 13,
        player.bottom,
        fill=PLAYER_ACCENT_COLOR,
        outline="",
        tags="frame",
    )
    canvas.create_rectangle(
        player.right - 13,
        player.y + player.height * 0.72,
        player.right,
        player.bottom,
        fill=PLAYER_ACCENT_COLOR,
        outline="",
        tags="frame",
    )


def draw_bullets(canvas: tk.Canvas, bullets: list[Bullet]) -> None:
    for bullet in bullets:
        canvas.create_rectangle(
            bullet.x,
            bullet.y,
            bullet.right,
            bullet.bottom,
            fill=BULLET_COLOR,
            outline="",
            tags="frame",
        )


def draw_enemies(canvas: tk.Canvas, enemies: list[Enemy]) -> None:
    for enemy in enemies:
        if enemy.is_alive:
            draw_enemy(canvas, enemy)


def draw_enemy(canvas: tk.Canvas, enemy: Enemy) -> None:
    canvas.create_rectangle(
        enemy.x + 5,
        enemy.y + 6,
        enemy.right - 5,
        enemy.bottom - 4,
        fill=ENEMY_COLOR,
        outline="",
        tags="frame",
    )
    canvas.create_rectangle(
        enemy.x,
        enemy.y + 12,
        enemy.x + 9,
        enemy.bottom,
        fill=ENEMY_COLOR,
        outline="",
        tags="frame",
    )
    canvas.create_rectangle(
        enemy.right - 9,
        enemy.y + 12,
        enemy.right,
        enemy.bottom,
        fill=ENEMY_COLOR,
        outline="",
        tags="frame",
    )
    canvas.create_rectangle(
        enemy.x + 11,
        enemy.y,
        enemy.x + 16,
        enemy.y + 7,
        fill=ENEMY_COLOR,
        outline="",
        tags="frame",
    )
    canvas.create_rectangle(
        enemy.right - 16,
        enemy.y,
        enemy.right - 11,
        enemy.y + 7,
        fill=ENEMY_COLOR,
        outline="",
        tags="frame",
    )
