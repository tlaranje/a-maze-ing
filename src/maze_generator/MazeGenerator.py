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

    def render(self, current_position) -> None:
        for y in range(self.height):
            for x in range(self.width):
                if (self.maze[x][y] & 0xf) == 0xf:
                    chr = "#"
                else:
                    chr = " "
                if x == current_position.x and y == current_position.y:
                    print(f"\033[31m{chr} \033[0m", end="")
                else:
                    print(f"{chr} ", end="")
            print()
