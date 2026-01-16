from .rendering.windows_utils import close_windows, create_window
from .rendering.images_utils import ImgData, create_png_image
from mlx import Mlx
from src.maze_generator.MazeGenerator import MazeGenerator
from src.maze_generator.MazeAlgorithms import MazeAlgorithms
import sys


class XVar:
    """Structure for main vars"""
    def __init__(self) -> None:
        self.mlx = None
        self.mlx_ptr = None
        self.windows: list[int] = []
        self.images: list[ImgData] = []


def draw_walls(lst_cords: list[tuple[int, int]]):
    for x, y in lst_cords:
        create_png_image(xvar, "images/wall.png", xvar.windows[0], x, y)


if __name__ == "__main__":
    xvar = XVar()

    maze: MazeGenerator = MazeGenerator("config.txt")

    lst_cords = [
        (0, 0),
    ]

    windows = [
        {"title": "Test 1", "width": maze.width, "height": maze.height},
    ]

    # Mlx Initialisation
    try:
        xvar.mlx = Mlx()
    except Exception as e:
        print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
        sys.exit(1)

    xvar.mlx_ptr = xvar.mlx.mlx_init()

    # Windows creation
    # try:
    #     for w in windows:
    #         create_window(xvar, w["title"], w["width"], w["height"])
    # except Exception as e:
    #     print(f"Error Win create: {e}", file=sys.stderr)
    #     sys.exit(1)

    backtracking_algorithn = MazeAlgorithms()
    backtracking_algorithn.find_shortest_path(maze)
    backtracking_algorithn.backtracking_generate(maze)
    #draw_walls(lst_cords)

    # close_windows(xvar)
    # xvar.mlx.mlx_loop(xvar.mlx_ptr)
