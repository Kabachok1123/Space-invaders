import random
import time
import tkinter as tk
from typing import Optional

from config import (
    BACKGROUND_COLOR,
    BULLET_HEIGHT,
    BULLET_WIDTH,
    ENEMY_BULLET_HEIGHT,
    ENEMY_BULLET_WIDTH,
    ENEMY_KILL_SPEED,
    ENEMY_LEVEL_SPEED,
    ENEMY_KILL_SHOT_SPEEDUP,
    ENEMY_MIN_SHOT_INTERVAL,
    ENEMY_MOVE_DOWN_STEP,
    ENEMY_MOVE_SPEED,
    ENEMY_SHOT_INTERVAL,
    FPS_DELAY_MS,
    MYSTERY_HEIGHT,
    MYSTERY_POINTS,
    MYSTERY_SPAWN_TIME,
    MYSTERY_SPEED,
    MYSTERY_TOP,
    MYSTERY_WIDTH,
    PLAYER_LIVES,
    POINTS_PER_ENEMY,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SIDE_PADDING,
)
from bunkers import damage_bunker_by_enemy_bullet
from drawing import GameRenderer
from geometry import rectangles_intersect
from leaderboard import Leaderboard
from level import create_bunkers, create_enemies, create_player
from models import Bullet, Enemy, EnemyBullet, MysteryShip


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
        self.renderer = GameRenderer(self.canvas)
        self.leaderboard = Leaderboard()

        self.pressed_keys: set[str] = set()
        self.last_frame_time = time.perf_counter()
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        self.reset_game()

    def reset_game(self) -> None:
        self.player = create_player()
        self.bullets: list[Bullet] = []
        self.enemy_bullets: list[EnemyBullet] = []
        self.level = 1
        self.score = 0
        self.lives = PLAYER_LIVES
        self.is_game_over = False
        self.score_saved = False
        self.setup_level()

    def setup_level(self) -> None:
        self.enemies = create_enemies()
        self.bunker_blocks = create_bunkers()
        self.mystery_ship: Optional[MysteryShip] = None
        self.mystery_timer = MYSTERY_SPAWN_TIME
        self.enemy_direction = 1
        self.enemy_shot_timer = ENEMY_SHOT_INTERVAL
        self.total_enemies = len(self.enemies)
        self.bullets.clear()
        self.enemy_bullets.clear()

    def run(self) -> None:
        self.update()
        self.root.mainloop()

    def on_key_press(self, event: tk.Event) -> None:
        key = event.keysym.lower()
        self.pressed_keys.add(key)
        if key == "space" and not self.is_game_over:
            self.shoot()
        if key in {"return", "kp_enter"} and self.is_game_over:
            self.reset_game()
        if key == "escape":
            self.root.destroy()

    def on_key_release(self, event: tk.Event) -> None:
        self.pressed_keys.discard(event.keysym.lower())

    def update(self) -> None:
        current_time = time.perf_counter()
        delta_time = current_time - self.last_frame_time
        self.last_frame_time = current_time

        if not self.is_game_over:
            self.update_player(delta_time)
            self.update_enemies(delta_time)
            self.update_mystery_ship(delta_time)
            self.update_bullets(delta_time)
            self.update_enemy_bullets(delta_time)
            self.update_enemy_shooting(delta_time)
            self.handle_collisions()
            self.check_level_complete()
            self.check_enemy_reached_player()
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

    def update_enemy_bullets(self, delta_time: float) -> None:
        for bullet in self.enemy_bullets:
            bullet.move(delta_time)
        self.enemy_bullets = [bullet for bullet in self.enemy_bullets if not bullet.is_outside_screen()]

    def update_enemies(self, delta_time: float) -> None:
        alive_enemies = get_alive_enemies(self.enemies)
        if not alive_enemies:
            return
        enemy_shift = self.enemy_direction * self.current_enemy_speed() * delta_time
        if enemies_reached_side(alive_enemies, enemy_shift):
            self.enemy_direction *= -1
            move_enemies_down(alive_enemies)
        else:
            move_enemies_side(alive_enemies, enemy_shift)

    def current_enemy_speed(self) -> float:
        killed_enemies = self.total_enemies - len(get_alive_enemies(self.enemies))
        return ENEMY_MOVE_SPEED + (self.level - 1) * ENEMY_LEVEL_SPEED + killed_enemies * ENEMY_KILL_SPEED

    def update_mystery_ship(self, delta_time: float) -> None:
        if self.mystery_ship is not None:
            self.mystery_ship.move(delta_time)
            if self.mystery_ship.right < -20 or self.mystery_ship.x > SCREEN_WIDTH + 20:
                self.mystery_ship = None
            return
        self.mystery_timer -= delta_time
        if self.mystery_timer <= 0:
            self.mystery_ship = create_mystery_ship()
            self.mystery_timer = MYSTERY_SPAWN_TIME

    def update_enemy_shooting(self, delta_time: float) -> None:
        self.enemy_shot_timer -= delta_time
        if self.enemy_shot_timer > 0:
            return
        shooter = choose_enemy_shooter(self.enemies)
        if shooter is not None:
            self.enemy_bullets.append(create_enemy_bullet(shooter))
        alive_count = len(get_alive_enemies(self.enemies))
        self.enemy_shot_timer = calculate_enemy_shot_interval(self.level, self.total_enemies, alive_count)

    def handle_collisions(self) -> None:
        self.handle_player_bullets()
        self.handle_enemy_bullets()

    def handle_player_bullets(self) -> None:
        active_bullets = []
        for bullet in self.bullets:
            if self.hit_mystery_ship(bullet):
                continue
            hit_enemy = find_hit_enemy(bullet, self.enemies)
            if hit_enemy is None:
                active_bullets.append(bullet)
            else:
                hit_enemy.is_alive = False
                self.score += POINTS_PER_ENEMY
        self.bullets = active_bullets

    def handle_enemy_bullets(self) -> None:
        active_enemy_bullets = []
        for bullet in self.enemy_bullets:
            if damage_bunker_by_enemy_bullet(bullet, self.bunker_blocks):
                continue
            if rectangles_intersect(bullet, self.player):
                self.damage_player()
                return
            active_enemy_bullets.append(bullet)
        self.enemy_bullets = active_enemy_bullets

    def hit_mystery_ship(self, bullet: Bullet) -> bool:
        if self.mystery_ship is None or not self.mystery_ship.is_alive:
            return False
        if not rectangles_intersect(bullet, self.mystery_ship):
            return False
        self.mystery_ship.is_alive = False
        self.mystery_ship = None
        self.score += MYSTERY_POINTS
        return True

    def damage_player(self) -> None:
        self.lives -= 1
        self.enemy_bullets.clear()
        if self.lives <= 0:
            self.finish_game()

    def finish_game(self) -> None:
        self.is_game_over = True
        if not self.score_saved:
            self.leaderboard.add_score("PLAYER", self.score, self.level)
            self.score_saved = True

    def check_level_complete(self) -> None:
        if get_alive_enemies(self.enemies):
            return
        self.level += 1
        self.setup_level()

    def check_enemy_reached_player(self) -> None:
        alive_enemies = get_alive_enemies(self.enemies)
        if alive_enemies and max(enemy.bottom for enemy in alive_enemies) >= self.player.y:
            self.finish_game()

    def get_player_direction(self) -> int:
        direction = 0
        if "left" in self.pressed_keys or "a" in self.pressed_keys:
            direction -= 1
        if "right" in self.pressed_keys or "d" in self.pressed_keys:
            direction += 1
        return direction

    def draw(self) -> None:
        self.renderer.draw(
            self.player,
            self.bullets,
            self.enemy_bullets,
            self.enemies,
            self.bunker_blocks,
            self.mystery_ship,
            self.score,
            self.lives,
            self.level,
            self.is_game_over,
            self.leaderboard.entries,
        )


def get_alive_enemies(enemies: list[Enemy]) -> list[Enemy]:
    return [enemy for enemy in enemies if enemy.is_alive]


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


def create_mystery_ship() -> MysteryShip:
    direction = random.choice([-1, 1])
    x = -MYSTERY_WIDTH if direction > 0 else SCREEN_WIDTH + MYSTERY_WIDTH
    speed = MYSTERY_SPEED * direction
    return MysteryShip(x, MYSTERY_TOP, MYSTERY_WIDTH, MYSTERY_HEIGHT, speed)


def find_hit_enemy(bullet: Bullet, enemies: list[Enemy]) -> Optional[Enemy]:
    for enemy in enemies:
        if enemy.is_alive and rectangles_intersect(bullet, enemy):
            return enemy
    return None
