from typing import Optional
from src.a_maze_ing import XVar 

class ImgData:
    """Structure for image data"""
    def __init__(self, xvar: Optional[XVar]):
        self.width = xvar.maze.width * xvar.cell_size
        self.height = xvar.maze.height * xvar.cell_size
        self.img = xvar.mlx.mlx_new_image(xvar.mlx_ptr, self.width, self.height)
        self.data = None
        self.sl = 0  # size line
        self.bpp = 0  # bits per pixel
        self.iformat = 0
        self.data, self.bpp, self.sl, self.iformat = \
            xvar.mlx.mlx_get_data_addr(self.img)


def draw_pixel(xvar: XVar, size: int, x: int, y: int, color: str):
    xvar.mlx.mlx_sync(xvar.mlx_ptr, xvar.mlx.SYNC_IMAGE_WRITABLE, xvar.img_2.img)
    # fill image in white
    for offset in range(0, xvar.img_2.sl * 100, 4):
        xvar.img_2.data[offset:offset+4] = (0xFFFFFFFF).to_bytes(4, 'little')

    xvar.mlx.mlx_put_image_to_window(xvar.mlx_ptr, xvar.win_1, xvar.img_2.img, 50, 50)
