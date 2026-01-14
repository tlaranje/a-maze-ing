from .utlis.windows_utlis import close_windows, create_window
from .utlis.img_utlis import ImgData, create_png_image, create_xpm_image
from .load_config import read_config_file
from mlx import Mlx
import sys


class XVar:
    """Structure for main vars"""
    def __init__(self) -> None:
        self.mlx = None
        self.mlx_ptr = None
        self.windows: list[int] = []
        self.images: list[ImgData] = []


if __name__ == "__main__":
    xvar = XVar()

    windows = [
        {"title": "Test 1", "width": 200, "height": 200},
        {"title": "Test 2", "width": 400, "height": 400}
    ]

    # Mlx Initialisation
    try:
        xvar.mlx = Mlx()
    except Exception as e:
        print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
        sys.exit(1)

    xvar.mlx_ptr = xvar.mlx.mlx_init()

    read_config_file("config.txt")
    # Windows creation
    try:
        for w in windows:
            create_window(xvar, w["title"], w["width"], w["height"])
    except Exception as e:
        print(f"Error Win create: {e}", file=sys.stderr)
        sys.exit(1)

    """ # Images creation
    create_png_image(xvar, "images/puffy_small.png", xvar.windows[0], 0, 0)
    create_xpm_image(xvar, "images/Dont_panic.xpm", xvar.windows[1], 0, 0) """

    close_windows(xvar)
    xvar.mlx.mlx_loop(xvar.mlx_ptr)
