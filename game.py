from __future__ import annotations

import time
import tkinter as tk

from config import (
    BACKGROUND_COLOR,
    FPS_DELAY_MS,
    PLAYER_BOTTOM_MARGIN,
    PLAYER_HEIGHT,
    PLAYER_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from drawing import create_stars, draw_background, draw_player
from models import Player, Star


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

        self.stars = create_stars()
        self.player = create_player()
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
        if key == "escape":
            self.root.destroy()

    def on_key_release(self, event: tk.Event) -> None:
        self.pressed_keys.discard(event.keysym.lower())

    def update(self) -> None:
        current_time = time.perf_counter()
        delta_time = current_time - self.last_frame_time
        self.last_frame_time = current_time

        self.update_player(delta_time)
        self.draw()

        if self.root.winfo_exists():
            self.root.after(FPS_DELAY_MS, self.update)

    def update_player(self, delta_time: float) -> None:
        direction = self.get_player_direction()
        self.player.move(direction, delta_time)

    def get_player_direction(self) -> int:
        direction = 0
        if "left" in self.pressed_keys or "a" in self.pressed_keys:
            direction -= 1
        if "right" in self.pressed_keys or "d" in self.pressed_keys:
            direction += 1
        return direction

    def draw(self) -> None:
        self.canvas.delete("frame")
        draw_background(self.canvas, self.stars)
        draw_player(self.canvas, self.player)


def create_player() -> Player:
    player_x = SCREEN_WIDTH / 2 - PLAYER_WIDTH / 2
    player_y = SCREEN_HEIGHT - PLAYER_BOTTOM_MARGIN - PLAYER_HEIGHT
    return Player(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
