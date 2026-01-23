from typing import Optional as opt
from maze_generator import MazeGenerator
from maze_generator import Position


def uint(value: str, key: opt[str] = None,
         only_positive: opt[bool] = False) -> int:
    """Convert a string to an unsigned integer"""
    number: int = int(value)
    if only_positive and number <= 0:
        raise ValueError(f"{key} must be positive int")
    if number < 0:
        raise ValueError(f"{key} must be unsigned int")
    return number


def parse_config(maze: MazeGenerator, key: str, value: str) -> None:
    """Get all mandatory config datas and raise errors"""
    match key:
        case "WIDTH":
            maze.width = uint(value, key, only_positive=True)
        case "HEIGHT":
            maze.height = uint(value, key, only_positive=True)
        case "ENTRY":
            entry: list[int] = list(map(uint, value.split(",")))
            if len(entry) != 2:
                raise ValueError("ENTRY must be x, y values")
            maze.entry = Position(entry[0], entry[1])
        case "EXIT":
            exit_: list[int] = list(map(uint, value.split(",")))
            if len(exit_) != 2:
                raise ValueError("EXIT must be x, y values")
            maze.exit = Position(exit_[0], exit_[1])
        case "OUTPUT_FILE":
            maze.output_file = value
        case "PERFECT":
            if value != "True" and value != "False":
                raise ValueError("PERFECT must be True or False")
            maze.perfect = value == "True"
        case _:
            raise ValueError("Unknown key in config file")


def read_config_file(maze: MazeGenerator, file: str) -> None:
    """Read and parse the configuration file"""
    with open(file, "r") as fd:
        for i, line in enumerate(fd, start=1):
            line = line.strip()
            if line.startswith("#"):
                continue
            key_value: list[str] = line.split("=")
            if len(key_value) != 2:
                raise ValueError(
                    f"Invalid KEY VALUE in line {i}"
                )
            parse_config(maze, key_value[0], key_value[1])
    for _, value in vars(maze).items():
        if value is None:
            raise ValueError("Missing mandatory values on config")
    if not maze.is_inside(maze.entry):
        raise ValueError("ENTRY point is not inside config")
    if not maze.is_inside(maze.exit):
        raise ValueError("EXIT is not inside config")
    if maze.entry == maze.exit:
        raise ValueError("Entry and Exits must be different")
