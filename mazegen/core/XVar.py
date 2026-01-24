from __future__ import annotations

from typing import Optional, cast
from ctypes import c_uint
import random

from mazegen.mlx import Mlx
from .mlx_types import MLX
from ctypes import c_void_p
from mazegen.maze_generator.MazeGenerator import MazeGenerator
from .ImgData import ImgData
from mazegen.maze_generator.MazeAlgorithms import MazeAlgorithms


class XVar:
    """Holds all main runtime variables for the application."""

    def __init__(self) -> None:
        """Initialize MLX, window pointers, and default state variables."""
        self.mlx: MLX = cast(MLX, Mlx())
        self.mlx_ptr: c_void_p = self.mlx.mlx_init()

        self.maze: Optional[MazeGenerator] = None
        self.window: Optional[c_void_p] = None
        self.img: Optional[ImgData] = None
        self.algorithm: Optional[MazeAlgorithms] = None

        self.seed: int = random.randint(0, 10000)
        self.finish_render: bool = False
        self.walls_color: int = 0xFF000000
        self.is_running: bool = True

    def setup(self, file_path: str) -> None:
        """
        Load the maze, create the window, image buffer, and algorithm engine.
        """
        self.maze = MazeGenerator(file_path, self)

        assert self.maze.width is not None
        assert self.maze.height is not None

        width: c_uint = c_uint((self.maze.width * 16) + 32)
        height: c_uint = c_uint((self.maze.height * 16) + 32)

        self.window = self.mlx.mlx_new_window(
            self.mlx_ptr,
            width,
            height,
            "a_maze_ing"
        )

        self.img = ImgData(
            self.mlx,
            self.mlx_ptr,
            width,
            height
        )

        self.algorithm = MazeAlgorithms(
            self.maze,
            self.img
        )
