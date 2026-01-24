from __future__ import annotations

from ctypes import c_uint
from src.core.ImgData import ImgData
from src.maze_generator import Position, Direction


def draw_way(
    img: ImgData,
    start: Position,
    size: c_uint,
    color: int
) -> None:
    """Draw a colored square or corridor segment on the image buffer."""

    border = 1

    # Base coordinates
    size_int = size.value
    start_x = (start.x + 1) * size_int
    start_y = (start.y + 1) * size_int
    size_x = size_int
    size_y = size_int

    direction = start.rev_direction()

    # Offsets table for each direction
    # (start_x, start_y, size_x, size_y)
    offsets = {
        Direction.NORTH: (+border, -border, -2 * border, 0),
        Direction.SOUTH: (+border, +border, -2 * border, 0),
        Direction.WEST:  (-border, +border, 0, -2 * border),
        Direction.EAST:  (+border, +border, 0, -2 * border),
        "default":       (+border, +border, -2 * border, -2 * border),
    }

    dx, dy, dsx, dsy = offsets.get(direction, offsets["default"])

    start_x += dx
    start_y += dy
    size_x += dsx
    size_y += dsy

    color_bytes = color.to_bytes(4, "little")

    for _ in range(size_y):
        x = start_x
        for _ in range(size_x):
            pos = (int(img.width) * start_y + x) * 4

            if pos < img.total_size:
                img.data[pos:pos + 4] = color_bytes
            x += 1
        start_y += 1
