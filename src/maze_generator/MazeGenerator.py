from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Any
from src.maze_generator import Position, IS_42
from src.rendering import draw_way

if TYPE_CHECKING:
    from src.core.XVar import XVar
    from src.maze_generator.MazeAlgorithms import MazeAlgorithms


class MazeGenerator:
    """Maze generator and configuration handler."""

    def __init__(self, file: str, xvar: XVar) -> None:
        from src.parsing import read_config_file

        self.xvar: XVar = xvar

        # Optional até serem carregados pelo config
        self.width: int = 0
        self.height: int = 0
        self.entry: Position = Position(0, 0)
        self.exit: Position = Position(0, 0)
        self.output_file: str = ""
        self.perfect: bool = False
        self.seeds: dict[int, dict[str, Any]] = {}

        try:
            read_config_file(self, file)
        except Exception as e:
            print(f"{type(e).__name__}: {e}!")
            exit(1)

        # Garantir para o mypy
        assert self.width is not None
        assert self.height is not None
        assert self.entry is not None
        assert self.exit is not None

        width: int = self.width
        height: int = self.height

        self.total_cells: int = width * height
        self.maze: list[list[int]] = [
            [0xF for _ in range(width)] for _ in range(height)
        ]

        # Validar que ENTRY/EXIT não estão no logo
        ex = (self.entry.x, self.entry.y)
        ex2 = (self.exit.x, self.exit.y)

        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if (cell & IS_42) and ((x, y) == ex or (x, y) == ex2):
                    print("Error: Entry or Exit cannot be in 42 logo cells")
                    exit(1)

    def is_inside(self, pos: Position) -> bool:
        assert self.width is not None
        assert self.height is not None
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def clear(self, flag: Optional[int] = None) -> None:
        assert self.width is not None
        assert self.height is not None

        for y in range(self.height):
            for x in range(self.width):
                if flag is None:
                    self.maze[y][x] = 0xF
                else:
                    self.maze[y][x] &= ~flag

    def save(self, algorithm: MazeAlgorithms) -> None:
        try:
            assert self.output_file is not None
            assert self.entry is not None
            assert self.exit is not None

            with open(self.output_file, "w") as file:
                for line in self.maze:
                    file.write("".join(f"{cell & 0xF:X}" for cell in line))
                    file.write("\n")

                file.write(f"\n{self.entry.x}, {self.entry.y}")
                file.write(f"\n{self.exit.x}, {self.exit.y}\n")

                direction_map = {0x1: "N", 0x2: "E", 0x4: "S", 0x8: "W"}

                for cell in algorithm.shortest_path:
                    if cell.direction is None:
                        file.write("")
                    else:
                        file.write(direction_map.get(int(cell.direction), ""))
        except Exception as e:
            print(f"Error: {e}")
            self.xvar.is_running = False

    def draw_42(self) -> None:
        """Draw the 42 logo inside the maze grid."""
        assert self.width is not None
        assert self.height is not None

        maze = self
        img = getattr(self.xvar.algorithm, "img", None)  # evita erro mypy

        width: int = self.width
        height: int = self.height

        if width < 13 or height < 13:
            return

        logo_42 = [
            [48, 0, 0, 48, 0, 0, 0, 48, 48, 48, 48],
            [48, 0, 0, 48, 0, 0, 0, 0, 0, 0, 48],
            [48, 0, 0, 48, 0, 0, 0, 0, 0, 0, 48],
            [48, 0, 0, 48, 0, 0, 0, 0, 0, 0, 48],
            [48, 0, 0, 48, 0, 0, 0, 0, 0, 0, 48],
            [48, 48, 48, 48, 0, 0, 0, 48, 48, 48, 48],
            [0, 0, 0, 48, 0, 0, 0, 48, 0, 0, 0],
            [0, 0, 0, 48, 0, 0, 0, 48, 0, 0, 0],
            [0, 0, 0, 48, 0, 0, 0, 48, 0, 0, 0],
            [0, 0, 0, 48, 0, 0, 0, 48, 0, 0, 0],
            [0, 0, 0, 48, 0, 0, 0, 48, 48, 48, 48]
        ]

        start_x = (width - 11) // 2
        start_y = (height - 11) // 2

        for y, row in enumerate(logo_42):
            for x, val in enumerate(row):
                maze.maze[start_y + y][start_x + x] |= val
                if img is not None and val == 48:
                    draw_way(
                        img,
                        Position(start_x + x, start_y + y),
                        16,
                        0x10F2F2F2
                    )
