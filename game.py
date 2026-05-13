from __future__ import annotations

import time
import tkinter as tk

from config import (
    BACKGROUND_COLOR,
    BULLET_HEIGHT,
    BULLET_WIDTH,
    ENEMY_COLUMNS,
    ENEMY_HEIGHT,
    ENEMY_HORIZONTAL_GAP,
    ENEMY_ROWS,
    ENEMY_TOP_MARGIN,
    ENEMY_VERTICAL_GAP,
    ENEMY_WIDTH,
    FPS_DELAY_MS,
    PLAYER_BOTTOM_MARGIN,
    PLAYER_HEIGHT,
    PLAYER_WIDTH,
    POINTS_PER_ENEMY,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from drawing import draw_background, draw_bullets, draw_enemies, draw_player, draw_score
from models import Bullet, Enemy, Player, rectangles_intersect


class SpaceInvadersGame:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Space Invaders")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            self.root,
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            bg=BACKGROUND_COLOR,
            highlightthickness=0,
        )
        self.canvas.pack()

        self.player = create_player()
        self.bullets: list[Bullet] = []
        self.enemies = create_enemies()
        self.score = 0
        self.pressed_keys: set[str] = set()
        self.last_frame_time = time.perf_counter()

        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def run(self) -> None:
        self.update()
        self.root.mainloop()

    def on_key_press(self, event: tk.Event) -> None:
        key = event.keysym.lower()
        self.pressed_keys.add(key)
        if key == "space":
            self.shoot()
        if key == "escape":
            self.root.destroy()

    def on_key_release(self, event: tk.Event) -> None:
        self.pressed_keys.discard(event.keysym.lower())

    def update(self) -> None:
        current_time = time.perf_counter()
        delta_time = current_time - self.last_frame_time
        self.last_frame_time = current_time

        self.update_player(delta_time)
        self.update_bullets(delta_time)
        self.handle_bullet_enemy_collisions()
        self.draw()

        if self.root.winfo_exists():
            self.root.after(FPS_DELAY_MS, self.update)

    def update_player(self, delta_time: float) -> None:
        direction = self.get_player_direction()
        self.player.move(direction, delta_time)

    def shoot(self) -> None:
        if self.bullets:
            return
        bullet_x = self.player.center_x - BULLET_WIDTH / 2
        bullet_y = self.player.y - BULLET_HEIGHT
        self.bullets.append(Bullet(bullet_x, bullet_y, BULLET_WIDTH, BULLET_HEIGHT))

    def update_bullets(self, delta_time: float) -> None:
        for bullet in self.bullets:
            bullet.move(delta_time)
        self.bullets = [bullet for bullet in self.bullets if not bullet.is_outside_screen()]

    def handle_bullet_enemy_collisions(self) -> None:
        active_bullets = []
        for bullet in self.bullets:
            hit_enemy = find_hit_enemy(bullet, self.enemies)
            if hit_enemy is None:
                active_bullets.append(bullet)
            else:
                hit_enemy.is_alive = False
                self.score += POINTS_PER_ENEMY
        self.bullets = active_bullets

    def get_player_direction(self) -> int:
        direction = 0
        if "left" in self.pressed_keys or "a" in self.pressed_keys:
            direction -= 1
        if "right" in self.pressed_keys or "d" in self.pressed_keys:
            direction += 1
        return direction

    def draw(self) -> None:
        self.canvas.delete("frame")
        draw_background(self.canvas)
        draw_enemies(self.canvas, self.enemies)
        draw_bullets(self.canvas, self.bullets)
        draw_player(self.canvas, self.player)
        draw_score(self.canvas, self.score)


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
            enemies.append(Enemy(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT))
    return enemies


def find_hit_enemy(bullet: Bullet, enemies: list[Enemy]) -> Enemy | None:
    for enemy in enemies:
        if enemy.is_alive and rectangles_intersect(bullet, enemy):
            return enemy
    return None
