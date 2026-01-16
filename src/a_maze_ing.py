from .rendering.windows_utils import close_windows, create_window
from .rendering.images_utils import ImgData, create_xpm_image
from mlx import Mlx
from src.maze_generator.MazeGenerator import MazeGenerator
from src.maze_generator.MazeAlgorithms import MazeAlgorithms
import sys
import time


class XVar:
    """Structure for main vars"""
    def __init__(self) -> None:
        self.mlx = None
        self.mlx_ptr = None
        self.windows: list[int] = []
        self.maze: MazeGenerator = None
        self.algorithn: MazeAlgorithms = None
        self.wall_1: ImgData = None
        self.wall_2: ImgData = None
        self.finish_render: bool = True


def draw_walls(xvar, maze):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            img = xvar.wall_1 if (cell & 15) == 15 else xvar.wall_2
            time.sleep(0.001)
            xvar.mlx.mlx_put_image_to_window(
                xvar.mlx_ptr,
                xvar.windows[0],
                img.img,
                x * img.width,
                y * img.height
            )


def gere_key(key, xvar):
    if key == 114 and xvar.finish_render: # 'r'
        xvar.finish_render = False
        xvar.mlx.mlx_clear_window(xvar.mlx_ptr, xvar.windows[0])
        xvar.algorithm.find_shortest_path(xvar.maze)
        xvar.algorithm.backtracking_generate(xvar.maze)
        draw_walls(xvar, xvar.maze.maze)
        xvar.finish_render = True

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

    xvar.wall_1 = create_xpm_image(xvar, "images/wall_1.xpm")
    xvar.wall_2 = create_xpm_image(xvar, "images/wall_2.xpm")

    draw_walls(xvar, xvar.maze.maze)

    xvar.mlx.mlx_key_hook(xvar.windows[0], gere_key, xvar)

    close_windows(xvar)
    xvar.mlx.mlx_loop(xvar.mlx_ptr)

    xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, xvar.wall_1.img)
    xvar.mlx.mlx_destroy_image(xvar.mlx_ptr, xvar.wall_2.img)

    xvar.mlx.mlx_release(xvar.mlx_ptr)


