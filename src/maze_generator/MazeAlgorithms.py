from __future__ import annotations

from ctypes import c_uint
from collections import deque
from typing import Optional, Generator, Deque, Dict, List, Any
import random

from src.core.ImgData import ImgData
from src.rendering.render import draw_way
from src.maze_generator.MazeProtocol import MazeBase
from src.maze_generator import Position, VISITED, IS_42, Direction


class MazeAlgorithms:
    """Algorithms for maze generation and pathfinding."""

    def __init__(self, maze: MazeBase, img: ImgData) -> None:
        """Initialize the algorithm engine with a maze and an image buffer."""
        self.maze: MazeBase = maze
        self.img: ImgData = img

        self.shortest_path: List[Position] = []
        self.generation: Generator[None, None, None] = (
            self.backtracking_generate(0)
        )
        self.draw_generation: Optional[Generator[None, None, None]] = None

        self.cur: Position = maze.entry
        self.seeds: Dict[int, Dict[Any, Any]] = {}
        self.cell_size: c_uint = c_uint(16)

    def make_imperfect(self, chance: float) -> None:
        """Add random imperfections to the maze."""
        once: bool = True
        maze = self.maze
        maze.clear(VISITED)

        for y in range(1, maze.height - 1):
            for x in range(1, maze.width - 1):
                if (maze.maze[y][x] & IS_42) or \
                   (random.random() > chance and not once):
                    continue

                pos = Position(x, y)
                valid_dirs = self.possible_paths(pos, True)
                valid_dirs = [
                    d for d in valid_dirs
                    if not (maze.maze[d.y][d.x] & IS_42)
                ]
                if not valid_dirs:
                    continue

                wall = random.choice(valid_dirs)
                assert wall.direction is not None
                maze.maze[y][x] &= ~int(wall.direction)
                maze.maze[wall.y][wall.x] &= ~int(wall.rev_direction())

                curr = Position(x, y, wall.rev_direction())
                draw_way(self.img, curr, self.cell_size, 0xFFFFFFFF)
                once = False

    def possible_moves(self, pos: Position) -> List[Position]:
        """Return all valid unvisited neighbor cells."""
        maze = self.maze
        all_directions = [pos.up(), pos.down(), pos.right(), pos.left()]
        valid_directions: List[Position] = []

        for d in all_directions:
            if maze.is_inside(d) and not (maze.maze[d.y][d.x] & VISITED):
                valid_directions.append(d)

        return valid_directions

    def possible_paths(
        self,
        pos: Position,
        reverse: Optional[bool] = False,
    ) -> List[Position]:
        """Return all reachable connected cells from the current position."""
        grid = self.maze.maze
        cell = grid[pos.y][pos.x]

        if reverse:
            cell = ~cell

        valid_dirs: List[Position] = []

        if not (cell & Direction.NORTH) and not \
               (grid[pos.y - 1][pos.x] & VISITED):
            valid_dirs.append(pos.up())
        if not (cell & Direction.SOUTH) and not \
               (grid[pos.y + 1][pos.x] & VISITED):
            valid_dirs.append(pos.down())
        if not (cell & Direction.EAST) and not \
               (grid[pos.y][pos.x + 1] & VISITED):
            valid_dirs.append(pos.right())
        if not (cell & Direction.WEST) and not \
               (grid[pos.y][pos.x - 1] & VISITED):
            valid_dirs.append(pos.left())

        return valid_dirs

    def move(
        self,
        stack: List[Position],
        cur: Position,
        valid_moves: List[Position],
        render: Optional[bool] = False,
    ) -> Position:
        """Perform one step of the backtracking algorithm."""
        self.maze.maze[cur.y][cur.x] |= VISITED

        if valid_moves:
            stack.append(cur)
            next_cell = random.choice(valid_moves)

            if render:
                draw_way(self.img, cur, self.cell_size, 0xFFFF0000)

            assert next_cell.direction is not None
            self.maze.maze[cur.y][cur.x] &= ~int(next_cell.direction)
            self.maze.maze[next_cell.y][next_cell.x] &= (
                ~int(next_cell.rev_direction())
            )

            return next_cell

        if render:
            draw_way(self.img, cur, self.cell_size, 0xFFFFFFFF)

        return stack.pop()

    def find_shortest_path(self) -> None:
        """Compute the shortest path using BFS."""
        maze = self.maze
        maze.clear(VISITED)

        lst: Deque[Position] = deque([maze.entry])
        stack: Dict[Position, Optional[Position]] = {maze.entry: None}
        _exit = maze.exit

        while lst:
            cur = lst.popleft()
            maze.maze[cur.y][cur.x] |= VISITED

            if cur.x == _exit.x and cur.y == _exit.y:
                path: List[Position] = []
                cur_pos: Optional[Position] = cur
                while cur_pos is not None:
                    path.append(cur_pos)
                    cur_pos = stack.get(cur_pos)
                self.shortest_path = path[::-1]
                break

            for next_cell in self.possible_paths(cur):
                if next_cell not in stack:
                    stack[next_cell] = cur
                    lst.append(next_cell)

    def draw_shortest_path(self, color: int) -> Generator[None, None, None]:
        """Draw the shortest path step by step."""
        for cell in self.shortest_path:
            draw_way(self.img, cell, self.cell_size, color)
            yield

        entry = self.maze.entry
        _exit = self.maze.exit
        draw_way(self.img, entry, self.cell_size, 0xFF00FF00)
        draw_way(self.img, _exit, self.cell_size, 0xFFFF0000)

    def backtracking_generate(self, seed: int) -> Generator[None, None, None]:
        """Generate the maze using backtracking, with seed caching."""
        if seed in self.seeds:
            cached = self.seeds[seed]
            self.img = cached["img"].copy()
            self.maze.maze = cached["maze"][:]
            self.shortest_path = cached["path"][:]

            self.maze.save(self)
            self.draw_generation = self.draw_shortest_path(0xFF0FFFFF)
            return

        maze = self.maze
        self.cur = maze.entry
        backtracking: List[Position] = [maze.entry]

        maze.clear()
        maze.draw_42()

        while backtracking:
            valid_dirs = self.possible_moves(self.cur)
            self.cur = (
                self.move(backtracking, self.cur, valid_dirs, render=True)
            )
            yield

        if not maze.perfect:
            self.make_imperfect(0.1)

        self.find_shortest_path()

        self.seeds[seed] = {
            "maze": self.maze.maze[:],
            "path": self.shortest_path[:],
            "img": self.img.copy(),
        }

        self.maze.save(self)
        self.draw_generation = self.draw_shortest_path(0xFF0FFFFF)
