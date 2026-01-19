from mlx import Mlx
from typing import Optional
import sys


class XVar:
    """Structure for main vars"""
    def __init__(self) -> None:
        self.maze_width = 10
        self.maze_height = 10

        self.mlx = Mlx()
        self.mlx_ptr = None
        self.windows: list[int] = []
        self.cell_size: int = 16
        self.img: ImgData = None


class ImgData:
    """Structure for image data"""
    def __init__(self, xvar: Optional[XVar]):
        self.width = xvar.maze_width * xvar.cell_size
        self.height = xvar.maze_height * xvar.cell_size

        self.img = xvar.mlx.mlx_new_image(xvar.mlx_ptr, self.width, self.height)
        self.data, self.bpp, self.sl, self.iformat = \
            xvar.mlx.mlx_get_data_addr(self.img)


def create_window(xvar, title: str, width: int, height: int) -> None:
    win = xvar.mlx.mlx_new_window(xvar.mlx_ptr, width, height, title)
    if not win:
            raise Exception("Can't create window")
    xvar.windows.append(win)


def close_windows(xvar) -> None:
    def close_single(w):
        xvar.mlx.mlx_destroy_window(xvar.mlx_ptr, w)
        xvar.windows.remove(w)

        if not xvar.windows:
            xvar.mlx.mlx_loop_exit(xvar.mlx_ptr)

    for win in xvar.windows:
        xvar.mlx.mlx_hook(win, 33, 0, (lambda w=win: close_single(w)), win)


def gere_key(key, xvar):
    if key == 114 and xvar.finish_render: # 'r'
        return 0


if __name__ == "__main__":
    xvar = XVar()
    xvar.mlx_ptr = xvar.mlx.mlx_init()
    xvar.img = ImgData(xvar)

    windows = [{"title": "Test 1",
                "width": xvar.maze_width * 16,
                "height": xvar.maze_height * 16}]


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