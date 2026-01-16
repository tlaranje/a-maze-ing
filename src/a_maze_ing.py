from .rendering.windows_utils import close_windows, create_window
from .rendering.images_utils import ImgData, create_xpm_image
from mlx import Mlx
from src.maze_generator.MazeGenerator import MazeGenerator
from src.maze_generator.MazeAlgorithms import MazeAlgorithms
import sys
import random


class XVar:
    """Structure for main vars"""
    def __init__(self) -> None:
        self.mlx = None
        self.mlx_ptr = None
        self.windows: list[int] = []
        self.images: list[ImgData] = []
        self.maze: MazeGenerator = None
        self.algorithn: MazeAlgorithms = None


def draw_walls(maze: list[list[int]]):
    cubes = ["images/wall_1.xpm", "images/wall_2.xpm"]
    for row_index, row in enumerate(maze):
        for col_index, cell in enumerate(row):
            if (cell & 15) == 15:
                create_xpm_image(
                    xvar,
                    "images/wall_1.xpm",
                    xvar.windows[0],
                    col_index * 16,
                    row_index * 16
                )
            else:
                create_xpm_image(
                    xvar,
                    "images/wall_2.xpm",
                    xvar.windows[0],
                    col_index * 16,
                    row_index * 16
                )


def gere_key(key, xvar):
    if key == 114:  # 'r'
        xvar.mlx.mlx_clear_window(xvar.mlx_ptr, xvar.windows[0])
        print(len(xvar.images))
        for im in xvar.images:
            xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, im.img)
            xvar.images.remove(im)
            
        print(len(xvar.images))
        if len(xvar.images) == 0:
            xvar.algorithm.find_shortest_path(xvar.maze)
            xvar.algorithm.backtracking_generate(xvar.maze)
            draw_walls(xvar.maze.maze)
        return 0


if __name__ == "__main__":
    xvar = XVar()

    xvar.maze = MazeGenerator("config.txt")
    xvar.algorithm = MazeAlgorithms()

    lst_cords = [
        (0, 0),
    ]

    windows = [
        {"title": "Test 1", "width": 1920, "height": 1080},
    ]

    # Mlx Initialisation
    try:
        xvar.mlx = Mlx()
    except Exception as e:
        print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
        sys.exit(1)

    xvar.mlx_ptr = xvar.mlx.mlx_init()

    # Windows creation
    try:
        for w in windows:
            create_window(xvar, w["title"], w["width"], w["height"])
    except Exception as e:
        print(f"Error Win create: {e}", file=sys.stderr)
        sys.exit(1)

    draw_walls(xvar.maze.maze)
    xvar.mlx.mlx_key_hook(xvar.windows[0], gere_key, xvar)

    close_windows(xvar)
    xvar.mlx.mlx_loop(xvar.mlx_ptr)
