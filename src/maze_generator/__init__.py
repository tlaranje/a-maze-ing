from typing import Optional
from enum import Enum


# MACROS
VISITED: int = 0xf


class Direction(Enum):
    """Enum of all directions"""
    NORTH: int = 0x1
    EAST: int = 0x2
    SOUTH: int = 0x4
    WEST: int = 0x8


class Position:
    """Represent the 2D position in the maze"""

    def __init__(self, x: int, y: int, dir: Optional[Direction] = 0) -> None:
        self.x = x
        self.y = y
        self.direction = dir

    def up(self):
        return Position(self.x, self.y - 1, Direction.NORTH)

    def down(self):
        return Position(self.x, self.y + 1, Direction.SOUTH)

    def right(self):
        return Position(self.x + 1, self.y, Direction.EAST)

    def left(self):
        return Position(self.x - 1, self.y, Direction.WEST)
