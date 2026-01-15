import sys
from typing import Optional
from ..maze_generator.MazeGenerator import MazeGenerator


def uint(string: str, only_positive: Optional[bool] = False) -> int:
    """Convert a string to an unsigned integer"""
    number: int = int(string)
    if only_positive and number <= 0:
        raise ValueError("Number must be positive")
    if number < 0:
        raise ValueError("Number must be unsigned")
    return number


def parse_maze(maze: MazeGenerator, key: str, value: str) -> None:
    """Get all mandatory maze datas and raise errors"""
    match key:
        case "WIDTH":
            maze.width = uint(value, only_positive=True)
        case "HEIGHT":
            maze.height = uint(value, only_positive=True)
        case "ENTRY":
            entry: tuple = tuple(map(uint, value.split(",")))
            if len(entry) != 2:
                raise Exception("ENTRY must be x, y values")
            maze.entry = entry
        case "EXIT":
            exit_: tuple = tuple(map(uint, value.split(",")))
            if len(exit_) != 2:
                raise Exception("EXIT must be x, y values")
            maze.exit = exit_
        case "OUTPUT_FILE":
            maze.output_file = value
        case "PERFECT":
            if value != "True" and value != "False":
                raise Exception("PERFECT must be True or False")
            maze.perfect = value == "True"


def read_config_file(file: str) -> MazeGenerator:
    """Read and parse the configuration file"""
    maze: MazeGenerator = MazeGenerator()
    try:
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
                parse_maze(maze, key_value[0], key_value[1])
        for _, value in vars(maze).items():
            if value is None:
                raise ValueError("Missing mandatory values on config")
        if maze.entry == maze.exit:
            raise ValueError("Entry and Exits must be different")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    return maze
