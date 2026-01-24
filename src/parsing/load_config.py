from __future__ import annotations

from typing import Optional, Protocol
from src.maze_generator import Position


class MazeConfig(Protocol):
    width: int
    height: int
    entry: Position
    exit: Position
    output_file: str
    perfect: bool

    def is_inside(self, pos: Position) -> bool: ...


def uint(value: str, key: Optional[str] = None,
         only_positive: bool = False) -> int:
    """Convert a string to an integer with basic validation."""
    number: int = int(value)

    if only_positive and number <= 0:
        raise ValueError(f"{key} must be positive int")

    if number < 0:
        raise ValueError(f"{key} must be unsigned int")

    return number


def parse_config(maze: MazeConfig, key: str, value: str) -> None:
    """Apply a single KEY=VALUE pair to the maze config."""
    match key:
        case "WIDTH":
            maze.width = uint(value, key, only_positive=True)

        case "HEIGHT":
            maze.height = uint(value, key, only_positive=True)

        case "ENTRY":
            parts = value.split(",")
            if len(parts) != 2:
                raise ValueError("ENTRY must be x,y values")
            maze.entry = Position(uint(parts[0]), uint(parts[1]))

        case "EXIT":
            parts = value.split(",")
            if len(parts) != 2:
                raise ValueError("EXIT must be x,y values")
            maze.exit = Position(uint(parts[0]), uint(parts[1]))

        case "OUTPUT_FILE":
            maze.output_file = value

        case "PERFECT":
            if value not in ("True", "False"):
                raise ValueError("PERFECT must be True or False")
            maze.perfect = value == "True"

        case _:
            raise ValueError(f"Unknown key in config file: {key}")


def read_config_file(maze: MazeConfig, file: str) -> None:
    """Load all config values from a file and validate them."""
    with open(file, "r") as fd:
        for i, line in enumerate(fd, start=1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            key_value = line.split("=")
            if len(key_value) != 2:
                raise ValueError(f"Invalid KEY=VALUE in line {i}")

            key, value = key_value[0].strip(), key_value[1].strip()
            parse_config(maze, key, value)

    # Validate mandatory fields
    for attr, value in vars(maze).items():
        if value is None:
            raise ValueError(f"Missing mandatory value: {attr}")

    assert maze.entry is not None
    assert maze.exit is not None

    if not maze.is_inside(maze.entry):
        raise ValueError("ENTRY point is not inside maze bounds")

    if not maze.is_inside(maze.exit):
        raise ValueError("EXIT point is not inside maze bounds")

    if maze.entry == maze.exit:
        raise ValueError("ENTRY and EXIT must be different")
