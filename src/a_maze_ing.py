from src.rendering.windows_utils import close_windows, create_window
from src.maze_generator.MazeAlgorithms import MazeAlgorithms
from src.maze_generator.MazeGenerator import MazeGenerator
from mlx import Mlx
import sys


class XVar:
    """Structure for main vars"""
    def __init__(self) -> None:
        self.mlx = Mlx()
        self.mlx_ptr = None
        self.windows: list[int] = []
        self.maze: MazeGenerator = MazeGenerator("config.txt")
        self.algorithn: MazeAlgorithms = MazeAlgorithms()
        self.finish_render: bool = True
        self.cell_size: int = 16
        self.img: ImgData = None


def gere_key(key, xvar):
    if key == 114 and xvar.finish_render: # 'r'

        """ xvar.algorithm.find_shortest_path(xvar.maze)
        xvar.algorithm.backtracking_generate(xvar.maze) """
        return 0


if __name__ == "__main__":
    from src.rendering.images_utils import ImgData
    
    try:
        xvar = XVar()
        xvar.img = ImgData(xvar)
    except Exception as e:
        print(e)

    windows = [
        {
            "title": "Test 1",
            "width": xvar.maze.width * 16,
            "height": xvar.maze.height * 16
        },
    ]

    xvar.mlx_ptr = xvar.mlx.mlx_init()

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


