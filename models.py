from __future__ import annotations

from dataclasses import dataclass

from config import PLAYER_SPEED, SCREEN_WIDTH, SIDE_PADDING


@dataclass
class Star:
    x: int
    y: int
    size: int
    color: str


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


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))
