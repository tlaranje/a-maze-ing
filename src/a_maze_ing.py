from .rendering.windows_utils import close_windows, create_window
from .rendering.images_utils import ImgData
from src.maze_generator.MazeAlgorithms import MazeAlgorithms
from src.maze_generator.MazeGenerator import MazeGenerator
from mlx import Mlx
import time
import sys


class XVar:
    """Structure for main vars"""
    def __init__(self) -> None:
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.windows: list[int] = []
        self.maze: MazeGenerator = MazeGenerator("config.txt")
        self.algorithn: MazeAlgorithms = MazeAlgorithms()
        self.img = ImgData(self)


def gere_key(key, xvar):
    if key == 114: # 'r'
        xvar.img.draw_pixel(xvar, 32, 0, 0, 0xffff0000)
        xvar.img.draw_pixel(xvar, 32, 1, 0, 0xffff0000)
        #xvar.mlx.mlx_clear_window(xvar.mlx_ptr, xvar.windows[0])
        #xvar.algorithm.find_shortest_path(xvar.maze)
        #xvar.algorithm.backtracking_generate(xvar.maze)
        return 0


if __name__ == "__main__":
    xvar = XVar()

    windows = [{"title": "Test 1",
                "width": (xvar.maze.width * 16),
                "height": (xvar.maze.height * 16)}]

    # Windows creation
    try:
        for w in windows:
            create_window(xvar, w["title"], w["width"], w["height"])
    except Exception as e:
        print(f"Error Win create: {e}", file=sys.stderr)
        sys.exit(1)

    xvar.mlx.mlx_key_hook(xvar.windows[0], gere_key, xvar)

    close_windows(xvar)
    xvar.mlx.mlx_loop(xvar.mlx_ptr)

    xvar.mlx.mlx_release(xvar.mlx_ptr)


