from mlx import Mlx


class ImgData:
    """Structure for image data"""

    def __init__(self, mlx: Mlx, mlx_ptr, width: int, height: int):
        self.ptr = mlx.mlx_new_image(mlx_ptr, width, height)
        self.width: int = width
        self.height: int = height
        self.data, self.bpp, self.sl, self.iformat = \
            mlx.mlx_get_data_addr(self.ptr)
        self.total_size: int = len(self.data) - 3

    def fill(self, color: int) -> None:
        color = color.to_bytes(4, 'little')
        for i in range(0, self.total_size - 1, 4):
            self.data[i:i+4] = color


def draw_wall(buffer_img: ImgData, start_x: int, start_y: int, size: int, color: int) -> None:
    """Draw block of pixels on images buffer"""
    start_x *= size
    start_y *= size
    color = color.to_bytes(4, 'little')
    for _ in range(size):
        x: int = start_x
        for _ in range(size):
            pos: int = (buffer_img.width * start_y + x) * 4
            if pos >= buffer_img.total_size:
                continue
            buffer_img.data[pos:pos+4] = color
            x += 1
        start_y += 1
