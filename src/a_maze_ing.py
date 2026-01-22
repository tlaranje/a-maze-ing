from .rendering.images_utils import ImgData, draw_way
from mlx import Mlx
from src.maze_generator.MazeGenerator import MazeGenerator
from src.maze_generator.MazeAlgorithms import MazeAlgorithms
from src.maze_generator import Position
from typing import Generator
import sys


class XVar:
    """Structure for main vars"""

    def __init__(self, file_path: str) -> None:
        self.mlx: Mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.window: int = None
        self.maze: MazeGenerator = MazeGenerator(file_path)
        self.buffer_img: ImgData = ImgData(
            self.mlx, self.mlx_ptr, 1920, 1080
        )
        self.algorithm: MazeAlgorithms = MazeAlgorithms(
            self.maze, self.buffer_img
        )

    """ def render(self) -> None:
        for y, row in enumerate(self.maze.maze):
            for x, cell in enumerate(row):
                if x == self.algorithm.cur.x and y == self.algorithm.cur.y:
                    draw_way(self.buffer_img, x+1, y+1, 16, 0xfffec5d7)
                elif x == self.maze.entry.x and y == self.maze.entry.y:
                    draw_way(self.buffer_img, x+1, y+1, 16, 0xFF0000FF)
                elif x == self.maze.exit.x and y == self.maze.exit.y:
                    draw_way(self.buffer_img, x+1, y+1, 16, 0xFFFF0000)
                elif (cell & 0xf) == 0xf:
                    draw_way(self.buffer_img, x+1, y+1, 16, 0xFF000000)
                else:
                    draw_way(self.buffer_img, x+1, y+1, 16, 0xFFFFFFFF)
        self.maze.draw_42(self.buffer_img) """

def close_window(xvar: XVar) -> None:
    xvar.mlx.mlx_destroy_window(xvar.mlx_ptr, xvar.window)
    xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)


def gere_key(key: int, xvar: XVar) -> None:
    if key == 114: # 'r'
        xvar.buffer_img.fill(0xFF000000)
        xvar.algorithm.generation = xvar.algorithm.backtracking_generate()

    elif key == 106: # 'j'
        try:
            for _ in range(1):
                next(xvar.algorithm.generation)
        except StopIteration:
            try:
                for _ in range(1):
                    next(xvar.algorithm.draw_generation)
            except StopIteration:
                pass
        xvar.mlx.mlx_put_image_to_window(xvar.mlx_ptr, xvar.window, xvar.buffer_img.ptr, 0, 0)
    return 0


def rendering_loop(xvar: XVar) -> None:
    try:
        for _ in range(10):
            next(xvar.algorithm.generation)
    except StopIteration:
        try:
            for _ in range(10):
                next(xvar.algorithm.draw_generation)
        except StopIteration:
            pass

    xvar.mlx.mlx_put_image_to_window(xvar.mlx_ptr, xvar.window, xvar.buffer_img.ptr, 0, 0)


if __name__ == "__main__":
    xvar = XVar("config.txt")

    # Windows creation
    try:
        xvar.window = xvar.mlx.mlx_new_window(
            xvar.mlx_ptr,
            (xvar.maze.width * 16) + 32,
            (xvar.maze.height * 16) + 32,
            "a_maze_ing")

        if xvar.window == None:
            raise Exception("Can't create window!")
    except Exception as e:
        print(f"Error Win create: {e}", file=sys.stderr)
        sys.exit(1)
    xvar.buffer_img.fill(0xFF000000)

    xvar.mlx.mlx_key_hook(xvar.window, gere_key, xvar)

    xvar.mlx.mlx_hook(xvar.window, 33, 0, close_window, xvar)

    xvar.mlx.mlx_loop_hook(xvar.mlx_ptr, rendering_loop, xvar)
    xvar.mlx.mlx_loop(xvar.mlx_ptr)

    xvar.mlx.mlx_release(xvar.mlx_ptr)


