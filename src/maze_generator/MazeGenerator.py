from src.maze_generator import Position
from src.rendering.images_utils import draw_wall, ImgData
from typing import Optional


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
        try:
            read_config_file(self, file)
        except Exception as e:
            print(f"{type(e).__name__}: {e}!")
            exit(1)
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

    def save(self, xvar) -> None:
        try:
            with open(self.output_file, "w") as file:
                for line in self.maze:
                    for cell in line:
                        file.write(f"{cell & 0xf:X}")
                    file.write("\n")
                file.write(f"\n{self.entry.x}, {self.entry.y}")
                file.write(f"\n{self.exit.x}, {self.exit.y}\n")

                direction_map = {0x1: "N", 0x2: "E", 0x4: "S", 0x8: "W"}

                for cell in xvar.algorithm.shortest_path:
                    file.write(direction_map.get(cell.direction, ""))
        except Exception as e:
            print(f"Error: {e}")
            exit(1)
 
    def draw_42(self, buffer_img: Optional[ImgData] = None) -> None:
        logo_42: list[list[int]] = [
            [16, 0,  16, 0,  0, 0, 0, 16, 16, 16, 16],
            [16, 0,  16, 0,  0, 0, 0, 0,  0,  0,  16],
            [16, 0,  16, 0,  0, 0, 0, 0,  0,  0,  16],
            [16, 0,  16, 0,  0, 0, 0, 0,  0,  0,  16],
            [16, 0,  16, 0,  0, 0, 0, 0,  0,  0,  16],
            [16, 16, 16, 16, 0, 0, 0, 16, 16, 16, 16],
            [0,  0,  16, 0,  0, 0, 0, 16, 0,  0,  0 ],
            [0,  0,  16, 0,  0, 0, 0, 16, 0,  0,  0 ],
            [0,  0,  16, 0,  0, 0, 0, 16, 0,  0,  0 ],
            [0,  0,  16, 0,  0, 0, 0, 16, 0,  0,  0 ],
            [0,  0,  16, 0,  0, 0, 0, 16, 16, 16, 16]
        ]
        maze_start_x: int = (self.width - 11) // 2
        maze_start_y: int = (self.height - 11) // 2
        for y in range(11):
            for x in range(11):
                self.maze[maze_start_y + y][maze_start_x + x] |= logo_42[y][x]
                if buffer_img is None:
                    continue
                if logo_42[y][x] == 16:
                    draw_wall(buffer_img, maze_start_x + x + 1, maze_start_y + y + 1, 16, 0x100FFFFF)

