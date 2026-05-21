from dataclasses import dataclass

from config import (
    BULLET_SPEED,
    ENEMY_BULLET_SPEED,
    PLAYER_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SIDE_PADDING,
)
from geometry import clamp


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
class EnemyBullet:
    x: float
    y: float
    width: int
    height: int
    previous_y: float = -1

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def previous_bottom(self) -> float:
        return self.previous_y + self.height

    def __post_init__(self) -> None:
        if self.previous_y < 0:
            self.previous_y = self.y

    def move(self, delta_time: float) -> None:
        self.previous_y = self.y
        self.y += ENEMY_BULLET_SPEED * delta_time

    def is_outside_screen(self) -> bool:
        return self.y > SCREEN_HEIGHT


@dataclass
class Enemy:
    x: float
    y: float
    width: int
    height: int
    color: str
    is_alive: bool = True

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height


@dataclass
class BunkerBlock:
    x: float
    y: float
    size: int
    hp: int

    @property
    def width(self) -> int:
        return self.size

    @property
    def height(self) -> int:
        return self.size

    @property
    def right(self) -> float:
        return self.x + self.size

    @property
    def bottom(self) -> float:
        return self.y + self.size

    def damage(self) -> None:
        self.hp -= 1


@dataclass
class MysteryShip:
    x: float
    y: float
    width: int
    height: int
    speed: float
    is_alive: bool = True

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    def move(self, delta_time: float) -> None:
        self.x += self.speed * delta_time
