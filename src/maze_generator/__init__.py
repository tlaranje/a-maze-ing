from dataclasses import dataclass
from typing import Optional
from enum import IntEnum

# MACROS
VISITED: int = 0xf


class Direction(IntEnum):
    """Enum of all directions"""
    NORTH: int = 0x1
    EAST: int = 0x2
    SOUTH: int = 0x4
    WEST: int = 0x8


@dataclass(frozen=True)
class Position:
    """Represent the 2D position in the maze"""
    x: int
    y: int
    direction: Optional[Direction] = None

    def up(self): return Position(self.x, self.y - 1, Direction.NORTH)

    def down(self): return Position(self.x, self.y + 1, Direction.SOUTH)

    def right(self): return Position(self.x + 1, self.y, Direction.EAST)

    def left(self): return Position(self.x - 1, self.y, Direction.WEST)
