from mlx import Mlx
from maze_generator import Position, Direction


class ImgData:
    """Structure for image data"""

    def __init__(self, mlx: Mlx, mlx_ptr, width: int, height: int):
        self.mlx = mlx
        self.mlx_ptr = mlx_ptr
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

    def copy(self) -> any:
        new_img = ImgData(self.mlx, self.mlx_ptr, self.width, self.height)
        new_img.data[:] = self.data[:]
        return new_img


def draw_way(
        buffer_img: ImgData, start: Position, size: int, color: int
) -> None:
    """ Draw block of pixels on images buffer """
    border: int = 1
    start_x = ((start.x + 1) * size)
    size_x: int = size
    start_y = ((start.y + 1) * size)
    size_y: int = size
    direction: int = start.rev_direction()
    if direction == Direction.NORTH:
        start_y -= border
        start_x += border
        size_x -= border * 2
    elif direction == Direction.SOUTH:
        start_y += border
        start_x += border
        size_x -= border * 2
    elif direction == Direction.WEST:
        start_y += border
        size_y -= border * 2
        start_x -= border
    elif direction == Direction.EAST:
        start_y += border
        size_y -= border * 2
        start_x += border
    else:
        start_y += border
        size_y -= border * 2
        start_x += border
        size_x -= border * 2
    color = color.to_bytes(4, 'little')
    for _ in range(size_y):
        x: int = start_x
        for _ in range(size_x):
            pos: int = (buffer_img.width * start_y + x) * 4
            if pos >= buffer_img.total_size:
                continue
            buffer_img.data[pos:pos+4] = color
            x += 1
        start_y += 1
