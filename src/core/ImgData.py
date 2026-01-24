from __future__ import annotations

from typing import Any
from mlx import Mlx


class ImgData:
    """Container for MLX image data and metadata."""

    def __init__(
            self, mlx: Mlx, mlx_ptr: Any, width: int, height: int
    ) -> None:
        """Create a new image buffer with the given dimensions."""
        self.mlx: Mlx = mlx
        self.mlx_ptr: Any = mlx_ptr

        self.ptr: Any = mlx.mlx_new_image(mlx_ptr, width, height)

        self.width: int = width
        self.height: int = height

        # mlx_get_data_addr returns: (bytearray, bpp, size_line, format)
        data, bpp, sl, iformat = mlx.mlx_get_data_addr(self.ptr)

        self.data: bytearray = data
        self.bpp: int = bpp
        self.sl: int = sl
        self.iformat: int = iformat

        self.total_size: int = len(self.data) - 3

    def fill(self, color: int) -> None:
        """Fill the entire image with a single color."""
        color_bytes = color.to_bytes(4, "little")
        for i in range(0, self.total_size - 1, 4):
            self.data[i:i+4] = color_bytes

    def copy(self) -> ImgData:
        """Return a deep copy of the image buffer."""
        new_img = ImgData(self.mlx, self.mlx_ptr, self.width, self.height)
        new_img.data[:] = self.data[:]
        return new_img
