from __future__ import annotations

from dataclasses import dataclass

from config import BULLET_SPEED, PLAYER_SPEED, SCREEN_WIDTH, SIDE_PADDING


@dataclass
class Player:
    x: float
    y: float
    width: int
    height: int

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    def move(self, direction: int, delta_time: float) -> None:
        next_x = self.x + direction * PLAYER_SPEED * delta_time
        max_x = SCREEN_WIDTH - self.width - SIDE_PADDING
        self.x = clamp(next_x, SIDE_PADDING, max_x)


@dataclass
class Bullet:
    x: float
    y: float
    width: int
    height: int

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    def move(self, delta_time: float) -> None:
        self.y -= BULLET_SPEED * delta_time

    def is_outside_screen(self) -> bool:
        return self.bottom < 0


@dataclass
class Enemy:
    x: float
    y: float
    width: int
    height: int
    is_alive: bool = True

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height


def rectangles_intersect(first: Bullet, second: Enemy) -> bool:
    return (
        first.x < second.right
        and first.right > second.x
        and first.y < second.bottom
        and first.bottom > second.y
    )


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))
