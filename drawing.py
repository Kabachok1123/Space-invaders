import tkinter as tk
from typing import Optional

from config import (
    BACKGROUND_COLOR,
    BULLET_COLOR,
    BUNKER_COLOR,
    ENEMY_BULLET_COLOR,
    GROUND_COLOR,
    PLAYER_ACCENT_COLOR,
    PLAYER_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TEXT_COLOR,
)
from models import BunkerBlock, Bullet, Enemy, EnemyBullet, MysteryShip, Player


class GameRenderer:
    def __init__(self, canvas: tk.Canvas) -> None:
        self.canvas = canvas

    def draw(
        self,
        player: Player,
        bullets: list[Bullet],
        enemy_bullets: list[EnemyBullet],
        enemies: list[Enemy],
        bunker_blocks: list[BunkerBlock],
        mystery_ship: Optional[MysteryShip],
        score: int,
        lives: int,
        level: int,
        is_game_over: bool,
        leaderboard_entries,
    ) -> None:
        self.canvas.delete("frame")
        self.draw_background()
        self.draw_bunker_blocks(bunker_blocks)
        self.draw_enemies(enemies)
        self.draw_mystery_ship(mystery_ship)
        self.draw_bullets(bullets)
        self.draw_enemy_bullets(enemy_bullets)
        self.draw_player(player)
        self.draw_hud(score, lives, level)
        if is_game_over:
            self.draw_game_over(leaderboard_entries)

    def draw_background(self) -> None:
        self.canvas.create_rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, fill=BACKGROUND_COLOR, width=0, tags="frame")
        ground_y = SCREEN_HEIGHT - 35
        self.canvas.create_line(18, ground_y, SCREEN_WIDTH - 18, ground_y, fill=GROUND_COLOR, width=2, tags="frame")

    def draw_hud(self, score: int, lives: int, level: int) -> None:
        self.canvas.create_text(24, 22, text=f"SCORE: {score}", anchor="w", fill=TEXT_COLOR, font=("Consolas", 16, "bold"), tags="frame")
        self.canvas.create_text(SCREEN_WIDTH / 2, 22, text=f"LEVEL: {level}", anchor="center", fill=TEXT_COLOR, font=("Consolas", 16, "bold"), tags="frame")
        self.canvas.create_text(SCREEN_WIDTH - 24, 22, text=f"LIVES: {lives}", anchor="e", fill=TEXT_COLOR, font=("Consolas", 16, "bold"), tags="frame")

    def draw_player(self, player: Player) -> None:
        body_top = player.y + player.height * 0.45
        self.canvas.create_rectangle(player.x + 7, body_top, player.right - 7, player.bottom, fill=PLAYER_COLOR, outline="", tags="frame")
        self.canvas.create_rectangle(player.center_x - 5, player.y, player.center_x + 5, player.y + player.height * 0.55, fill=PLAYER_COLOR, outline="", tags="frame")
        self.canvas.create_rectangle(player.x, player.y + player.height * 0.72, player.x + 13, player.bottom, fill=PLAYER_ACCENT_COLOR, outline="", tags="frame")
        self.canvas.create_rectangle(player.right - 13, player.y + player.height * 0.72, player.right, player.bottom, fill=PLAYER_ACCENT_COLOR, outline="", tags="frame")

    def draw_bullets(self, bullets: list[Bullet]) -> None:
        for bullet in bullets:
            self.canvas.create_rectangle(bullet.x, bullet.y, bullet.right, bullet.bottom, fill=BULLET_COLOR, outline="", tags="frame")

    def draw_enemy_bullets(self, bullets: list[EnemyBullet]) -> None:
        for bullet in bullets:
            self.canvas.create_rectangle(bullet.x, bullet.y, bullet.right, bullet.bottom, fill=ENEMY_BULLET_COLOR, outline="", tags="frame")

    def draw_enemies(self, enemies: list[Enemy]) -> None:
        for enemy in enemies:
            if enemy.is_alive:
                self.draw_enemy(enemy)

    def draw_enemy(self, enemy: Enemy) -> None:
        self.canvas.create_rectangle(enemy.x + 5, enemy.y + 6, enemy.right - 5, enemy.bottom - 4, fill=enemy.color, outline="", tags="frame")
        self.canvas.create_rectangle(enemy.x, enemy.y + 12, enemy.x + 9, enemy.bottom, fill=enemy.color, outline="", tags="frame")
        self.canvas.create_rectangle(enemy.right - 9, enemy.y + 12, enemy.right, enemy.bottom, fill=enemy.color, outline="", tags="frame")
        self.canvas.create_rectangle(enemy.x + 11, enemy.y, enemy.x + 16, enemy.y + 7, fill=enemy.color, outline="", tags="frame")
        self.canvas.create_rectangle(enemy.right - 16, enemy.y, enemy.right - 11, enemy.y + 7, fill=enemy.color, outline="", tags="frame")

    def draw_bunker_blocks(self, blocks: list[BunkerBlock]) -> None:
        for block in blocks:
            self.canvas.create_rectangle(block.x, block.y, block.right, block.bottom, fill=BUNKER_COLOR, outline="", tags="frame")

    def draw_mystery_ship(self, ship: Optional[MysteryShip]) -> None:
        if ship is None or not ship.is_alive:
            return
        self.canvas.create_rectangle(ship.x + 8, ship.y + 8, ship.right - 8, ship.bottom, fill="#ff5468", outline="", tags="frame")
        self.canvas.create_rectangle(ship.x + 18, ship.y + 2, ship.right - 18, ship.y + 10, fill="#ff5468", outline="", tags="frame")
        self.canvas.create_rectangle(ship.x, ship.y + 13, ship.x + 12, ship.bottom, fill="#ff5468", outline="", tags="frame")
        self.canvas.create_rectangle(ship.right - 12, ship.y + 13, ship.right, ship.bottom, fill="#ff5468", outline="", tags="frame")

    def draw_game_over(self, leaderboard_entries) -> None:
        self.canvas.create_text(SCREEN_WIDTH / 2, 245, text="GAME OVER", anchor="center", fill=TEXT_COLOR, font=("Consolas", 42, "bold"), tags="frame")
        self.canvas.create_text(SCREEN_WIDTH / 2, 302, text="LEADERBOARD", anchor="center", fill=TEXT_COLOR, font=("Consolas", 18, "bold"), tags="frame")
        if not leaderboard_entries:
            self.canvas.create_text(SCREEN_WIDTH / 2, 336, text="NO SCORES YET", anchor="center", fill=TEXT_COLOR, font=("Consolas", 14), tags="frame")
        for index, entry in enumerate(leaderboard_entries, start=1):
            text = f"{index}. {entry.name:<10} {entry.score:03d}  L{entry.level}"
            self.canvas.create_text(SCREEN_WIDTH / 2, 326 + index * 24, text=text, anchor="center", fill=TEXT_COLOR, font=("Consolas", 14), tags="frame")
        self.canvas.create_text(SCREEN_WIDTH / 2, 505, text="ENTER - RESTART", anchor="center", fill=TEXT_COLOR, font=("Consolas", 14, "bold"), tags="frame")
