from typing import Optional


class ImgData:
    """Structure for image data"""
    def __init__(self, xvar: Optional[any] = None):
        self.width = xvar.maze.width * 16
        self.height = xvar.maze.height * 16
        self.img =  xvar.mlx.mlx_new_image(xvar.mlx_ptr, self.width, self.height)

        self.data, self.bpp, self.sl, self.iformat = \
        xvar.mlx.mlx_get_data_addr(self.img)


    def draw_pixel(self, xvar, size: int, x: int, y: int, color: int):
        px = x * size
        py = y * size

        for dy in range(size):
            for dx in range(size):
                offset = (py + dy) * self.sl + (px + dx) * 4
                xvar.img.data[offset:offset+4] = color.to_bytes(4, 'little')

        xvar.mlx.mlx_put_image_to_window(
            xvar.mlx_ptr,
            xvar.windows[0],
            xvar.img.img,
            0,
            0
        )



