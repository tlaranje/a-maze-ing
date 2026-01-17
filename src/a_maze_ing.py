from .rendering.windows_utils import close_windows, create_window
from .rendering.images_utils import ImgData, draw_wall
from mlx import Mlx
from src.maze_generator.MazeGenerator import MazeGenerator
from src.maze_generator.MazeAlgorithms import MazeAlgorithms
from typing import Optional
import time
import sys


class XVar:
    """Structure for main vars"""

    def __init__(self, file_path: str) -> None:
        self.mlx: Mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.windows: list[int] = []
        self.maze: MazeGenerator = MazeGenerator(file_path)
        self.algorithm: MazeAlgorithms = MazeAlgorithms()
        self.buffer_img: ImgData = ImgData(
            self.mlx, self.mlx_ptr, 1920, 1080
        )

    def render(self) -> None:
        for y, row in enumerate(self.maze.maze):
            for x, cell in enumerate(row):
                if x == self.maze.entry.x and y == self.maze.entry.y:
                    draw_wall(self.buffer_img, x+1, y+1, 16, 0xFF00FF00)
                elif x == self.maze.exit.x and y == self.maze.exit.y:
                    draw_wall(self.buffer_img, x+1, y+1, 16, 0xFF00FF00)
                elif (cell & 0xf) == 0xf:
                    draw_wall(self.buffer_img, x+1, y+1, 16, 0xFFFF0000)
                else:
                    draw_wall(self.buffer_img, x+1, y+1, 16, 0xFF0000FF)
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.windows[0], self.buffer_img.ptr, 0, 0)


def gere_key(key, xvar):
    if key == 114: # 'r'
        xvar.algorithm.find_shortest_path(xvar.maze)
        xvar.algorithm.backtracking_generate(xvar.maze)
        xvar.maze.save()
        xvar.render()

        return 0


if __name__ == "__main__":
    xvar = XVar("config.txt")

    windows = [
        {
            "title": "Test 1", 
            "width": (xvar.maze.width * 16) + 32,
            "height": (xvar.maze.height * 16) + 32
        },
    ]

    # Windows creation
    try:
        for w in windows:
            create_window(xvar, w["title"], w["width"], w["height"])
    except Exception as e:
        print(f"Error Win create: {e}", file=sys.stderr)
        sys.exit(1)

    xvar.render()
    xvar.mlx.mlx_key_hook(xvar.windows[0], gere_key, xvar)

    close_windows(xvar)
    xvar.mlx.mlx_loop(xvar.mlx_ptr)

    xvar.mlx.mlx_release(xvar.mlx_ptr)


