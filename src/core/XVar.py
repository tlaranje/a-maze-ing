from __future__ import annotations

from typing import Optional
import random

from mlx import Mlx
from src.maze_generator.MazeGenerator import MazeGenerator
from .ImgData import ImgData
from src.maze_generator.MazeAlgorithms import MazeAlgorithms


class XVar:
    """Holds all main runtime variables for the application."""

    def __init__(self) -> None:
        """Initialize MLX, window pointers, and default state variables."""
        self.mlx: Mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()

        self.maze: Optional[MazeGenerator] = None
        self.window: Optional[int] = None
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

        width = (self.maze.width * 16) + 32
        height = (self.maze.height * 16) + 32

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
