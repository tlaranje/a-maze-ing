from src.maze_generator import Position


class MazeGenerator:
    # TODO
    """PUT DOCUMENTATION PLEASE"""

    def __init__(self, file: str) -> None:
        from src.parsing.load_config import read_config_file
        self.height: int = None
        self.width: int = None
        self.entry: Position = None
        self.exit: Position = None
        self.output_file: str = None
        self.perfect: bool = None
        read_config_file(self, file)
        self.total_cells: int = self.width * self.height
        self.borders: int = (self.height * 2) - 4 + self.width * 2
        self.maze: list[list[int]] = [
            [0xf for _ in range(self.width)] for _ in range(self.height)
        ]

    def is_inside(self, pos: Position) -> bool:
        return (self.width - 1 > pos.x > 0
                and self.height - 1 > pos.y > 0)

    def clear(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                self.maze[x][y] = 0xf

    def save(self) -> None:
        try:
            with open(self.output_file, "w") as file:
                for line in self.maze:
                    for cell in line:
                        file.write(f"{cell & 0xf:X}")
                    file.write("\n")
        except Exception as e:
            print(f"Error: {e}")
            exit(1)
