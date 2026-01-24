from typing import Protocol, Any, Dict
from mazegen.maze_generator import Position


class MazeBase(Protocol):
    """Protocol describing the required interface for a maze structure."""

    width: int
    height: int
    maze: list[list[int]]
    entry: Position
    exit: Position
    perfect: bool
    seeds: dict[int, Dict[Any, Any]]

    def is_inside(self, pos: Position) -> bool:
        """Return True if the given position is inside the maze bounds."""
        ...

    def clear(self, flag: int | None = None) -> None:
        """Clear the maze or remove a specific flag from all cells."""
        ...

    def draw_42(self) -> None:
        """Draw the 42 logo inside the maze grid."""
        ...

    def save(self, algorithm: Any) -> None:
        """Save the maze and the computed path to the output file."""
        ...
