from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from enum import IntEnum

# MACROS
VISITED: int = 0x10
IS_42: int = 0x20


class Direction(IntEnum):
    """Enum of all directions."""
    NORTH = 0x1
    EAST = 0x2
    SOUTH = 0x4
    WEST = 0x8
    NONE = 0xf


@dataclass(frozen=True)
class Position:
    """Represent a 2D position in the maze."""
    x: int
    y: int
    direction: Optional[Direction] = None

    def up(self) -> Position:
        return Position(self.x, self.y - 1, Direction.NORTH)

    def down(self) -> Position:
        return Position(self.x, self.y + 1, Direction.SOUTH)

    def right(self) -> Position:
        return Position(self.x + 1, self.y, Direction.EAST)

    def left(self) -> Position:
        return Position(self.x - 1, self.y, Direction.WEST)

    def rev_direction(self) -> Direction:
        if self.direction == Direction.NORTH:
            return Direction.SOUTH
        if self.direction == Direction.SOUTH:
            return Direction.NORTH
        if self.direction == Direction.EAST:
            return Direction.WEST
        if self.direction == Direction.WEST:
            return Direction.EAST
        return Direction.NONE
