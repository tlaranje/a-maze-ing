from maze_generator import Position, IS_42, XVar, draw_way
from typing import Optional


class MazeGenerator:
    # TODO
    """PUT DOCUMENTATION PLEASE"""

    def __init__(self, file: str, xvar: XVar) -> None:
        from parsing import read_config_file
        self.xvar: XVar = xvar
        self.height: int = None
        self.width: int = None
        self.entry: Position = None
        self.exit: Position = None
        self.output_file: str = None
        self.perfect: bool = None
        try:
            read_config_file(self, file)
        except Exception as e:
            print(f"{type(e).__name__}: {e}!")
            exit(1)
        self.total_cells: int = self.width * self.height
        self.maze: list[list[int]] = [
            [0xf for _ in range(self.width)] for _ in range(self.height)
        ]
        self.draw_42()
        _exit: Position = self.exit
        entry: Position = self.entry
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if (cell & IS_42) and \
                   (x == entry.x and y == entry.y or
                   x == _exit.x and y == _exit.y):
                    print("Error: Entry or Exit cannot be in 42 logo cells")
                    exit(1)

    def is_inside(self, pos: Position) -> bool:
        return (self.width > pos.x >= 0
                and self.height > pos.y >= 0)

    def clear(self, flag: Optional[int] = None) -> None:
        for x in range(self.width):
            for y in range(self.height):
                if flag is None:
                    self.maze[y][x] = 0xf
                else:
                    self.maze[y][x] &= ~(flag)

    def save(self, algorithm) -> None:
        try:
            with open(self.output_file, "w") as file:
                for line in self.maze:
                    for cell in line:
                        file.write(f"{cell & 0xf:X}")
                    file.write("\n")
                file.write(f"\n{self.entry.x}, {self.entry.y}")
                file.write(f"\n{self.exit.x}, {self.exit.y}\n")

                direction_map = {0x1: "N", 0x2: "E", 0x4: "S", 0x8: "W"}

                for cell in algorithm.shortest_path:
                    file.write(direction_map.get(cell.direction, ""))
        except Exception as e:
            print(f"Error: {e}")
            self.xvar.is_running = False

    def draw_42(xvar: XVar) -> None:
        maze, img = xvar.maze, xvar.algorithm.img
        width, height = maze.width, maze.height

        if width < 13 or height < 13:
            return

        logo_42 = [
            [48, 0, 0, 48, 0, 0, 0, 48, 48, 48, 48],
            [48, 0, 0, 48, 0, 0, 0, 0, 0, 0, 48],
            [48, 0, 0, 48, 0, 0, 0, 0, 0, 0, 48],
            [48, 0, 0, 48, 0, 0, 0, 0, 0, 0, 48],
            [48, 0, 0, 48, 0, 0, 0, 0, 0, 0, 48],
            [48, 48, 48, 48, 0, 0, 0, 48, 48, 48, 48],
            [0, 0, 0, 48, 0, 0, 0, 48, 0, 0, 0],
            [0, 0, 0, 48, 0, 0, 0, 48, 0, 0, 0],
            [0, 0, 0, 48, 0, 0, 0, 48, 0, 0, 0],
            [0, 0, 0, 48, 0, 0, 0, 48, 0, 0, 0],
            [0, 0, 0, 48, 0, 0, 0, 48, 48, 48, 48]
        ]

        start_x, start_y = (width - 11) // 2, (height - 11) // 2

        for y, row in enumerate(logo_42):
            for x, val in enumerate(row):
                maze.maze[start_y + y][start_x + x] |= val
                if img and val == 48:
                    draw_way(
                        img,
                        Position(start_x + x, start_y + y), 16, 0x10F2F2F2)
