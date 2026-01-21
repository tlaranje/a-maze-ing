from dataclasses import dataclass
from typing import Optional
from enum import IntEnum

# MACROS
VISITED: int = 0x10
IS_42: int = 0x20

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

    def rev_direction(self) -> Direction:
        if self.direction == Direction.NORTH:
            return Direction.SOUTH
        elif self.direction == Direction.SOUTH:
            return Direction.NORTH
        elif self.direction == Direction.EAST:
            return Direction.WEST
        elif self.direction == Direction.WEST:
            return Direction.EAST
