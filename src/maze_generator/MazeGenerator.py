from src.maze_generator import Position, IS_42, XVar
from src.rendering.images_utils import draw_way, ImgData
from typing import Optional


class MazeGenerator:
    # TODO
    """PUT DOCUMENTATION PLEASE"""

    def __init__(self, file: str, xvar: XVar) -> None:
        from src.parsing.load_config import read_config_file
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
                if (cell & IS_42) \
                    and (x == entry.x and y == entry.y
                    or x == _exit.x and y == _exit.y):
                    print(f"Error: Entry or Exit cannot be in 42 logo cells")
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

    def draw_42(self, buffer_img: Optional[ImgData] = None) -> None:
        if self.height >= 13 and self.width >= 13:
            logo_42: list[list[int]] = [
                [48, 0,  0,  48, 0, 0, 0, 48, 48, 48, 48],
                [48, 0,  0,  48, 0, 0, 0, 0,  0,  0,  48],
                [48, 0,  0,  48, 0, 0, 0, 0,  0,  0,  48],
                [48, 0,  0,  48, 0, 0, 0, 0,  0,  0,  48],
                [48, 0,  0,  48, 0, 0, 0, 0,  0,  0,  48],
                [48, 48, 48, 48, 0, 0, 0, 48, 48, 48, 48],
                [0,  0,  0,  48, 0, 0, 0, 48, 0,  0,  0],
                [0,  0,  0,  48, 0, 0, 0, 48, 0,  0,  0],
                [0,  0,  0,  48, 0, 0, 0, 48, 0,  0,  0],
                [0,  0,  0,  48, 0, 0, 0, 48, 0,  0,  0],
                [0,  0,  0,  48, 0, 0, 0, 48, 48, 48, 48]
            ]
            maze_start_x: int = (self.width - 11) // 2
            maze_start_y: int = (self.height - 11) // 2
            for y in range(11):
                for x in range(11):
                    self.maze[maze_start_y + y][maze_start_x + x] |= logo_42[y][x]
                    if buffer_img is None:
                        continue
                    if logo_42[y][x] == 48:
                        pos: Position = Position(
                            maze_start_x + x, maze_start_y + y)
                        draw_way(buffer_img, pos, 16, 0x10F2F2F2)

