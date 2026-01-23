import random
from maze_generator import MazeGenerator as Maze
from maze_generator import (Position, VISITED, IS_42,
                            Direction, ImgData, draw_way)
from typing import Optional as opt
from typing import Generator
from collections import deque


class MazeAlgorithms:
    """Provide diferent types of maze generation algorithms"""

    def __init__(self, maze: Maze, buffer_img: ImgData) -> None:
        self.shortest_path: list[Position] = []
        self.maze: Maze = maze
        self.buffer_img: ImgData = buffer_img
        self.generation: Generator = self.backtracking_generate(0)
        self.draw_generation: Generator = None
        self.cur: Position = maze.entry
        self.seeds: dict[int, dict] = {}

    def make_imperfect(self, chance: float) -> None:
        once: bool = True
        maze: Maze = self.maze
        self.maze.clear(VISITED)

        for y in range(1, maze.height - 1):
            for x in range(1, maze.width - 1):
                if (maze.maze[y][x] & IS_42) or \
                   (random.random() > chance and not once):
                    continue
                pos: Position = Position(x, y)
                valid_dirs: list[Position] = self.possible_paths(pos, True)
                valid_dirs = [
                    dir for dir in valid_dirs
                    if not (maze.maze[dir.y][dir.x] & IS_42)
                ]
                if not valid_dirs:
                    continue
                wall: Position = random.choice(valid_dirs)
                maze.maze[y][x] &= ~(wall.direction)
                maze.maze[wall.y][wall.x] &= ~(wall.rev_direction())
                curr: Position = Position(x, y, wall.rev_direction())
                draw_way(self.buffer_img, curr, 16, 0xFFFFFFFF)
                once = False

    def possible_moves(self, pos: Position) -> list[Position]:
        maze: Maze = self.maze
        all_directions: list[Position] = [
            pos.up(),
            pos.down(),
            pos.right(),
            pos.left()
        ]
        valid_directions: list[Position] = []
        for dir in all_directions:
            if maze.is_inside(dir) and not (maze.maze[dir.y][dir.x] & VISITED):
                valid_directions.append(dir)
        return valid_directions

    def possible_paths(
            self, pos: Position, reverse: opt[bool] = False
    ) -> list[Position]:
        maze: Maze = self.maze.maze
        cell: Position = maze[pos.y][pos.x]
        if reverse:
            cell = ~(cell)
        valid_dirs: list[Position] = []
        if not (cell & Direction.NORTH) and not \
               (maze[pos.y-1][pos.x] & VISITED):
            valid_dirs.append(pos.up())
        if not (cell & Direction.SOUTH) and not \
               (maze[pos.y+1][pos.x] & VISITED):
            valid_dirs.append(pos.down())
        if not (cell & Direction.EAST) and not \
               (maze[pos.y][pos.x+1] & VISITED):
            valid_dirs.append(pos.right())
        if not (cell & Direction.WEST) and not \
               (maze[pos.y][pos.x-1] & VISITED):
            valid_dirs.append(pos.left())
        return valid_dirs

    def move(self, stack: list[Position], cur: Position,
             valid_moves: list[Position], render: opt[bool] = False
             ) -> Position:
        self.maze.maze[cur.y][cur.x] |= VISITED
        if valid_moves:
            stack.append(cur)
            next_cell: Position = random.choice(valid_moves)
            if render:
                draw_way(self.buffer_img, cur, 16, 0xFFFF0000)
            self.maze.maze[cur.y][cur.x] &= ~(next_cell.direction)
            self.maze.maze[next_cell.y][next_cell.x] &= \
                ~(next_cell.rev_direction())
            return next_cell
        if render:
            draw_way(self.buffer_img, cur, 16, 0xFFFFFFFF)
        return stack.pop()

    def find_shortest_path(self) -> None:
        maze: Maze = self.maze
        maze.clear(VISITED)
        lst: deque[Position] = deque([maze.entry])
        stack: dict[Position, Position | None] = {maze.entry: None}
        _exit = maze.exit

        while lst:
            cur = lst.popleft()
            maze.maze[cur.y][cur.x] |= VISITED

            if (cur.x == _exit.x and cur.y == _exit.y):
                path = []
                while cur is not None:
                    path.append(cur)
                    cur = stack.get(cur)
                self.shortest_path = path[::-1]
                break

            for next_cell in self.possible_paths(cur):
                if next_cell not in stack:
                    stack[next_cell] = cur
                    lst.append(next_cell)

    def draw_shortest_path(self, color: int) -> Generator:
        for cell in self.shortest_path:
            draw_way(self.buffer_img, cell, 16, color)
            yield
        entry: Position = self.maze.entry
        _exit: Position = self.maze.exit
        draw_way(self.buffer_img, entry, 16, 0xFF00FF00)
        draw_way(self.buffer_img, _exit, 16, 0xFFFF0000)

    def backtracking_generate(self, seed: int) -> Generator:
        if seed in self.seeds:
            self.buffer_img = self.seeds[seed]['buffer_img'].copy()
            self.maze.maze = self.seeds[seed]['maze'][:]
            self.shortest_path = self.seeds[seed]['path'][:]

            self.maze.save(self)
            self.draw_generation = self.draw_shortest_path(0xFF0FFFFF)
            return
        maze: Maze = self.maze
        self.cur = maze.entry
        backtracking: list[Position] = [maze.entry]
        maze.clear()
        maze.draw_42(self.buffer_img)
        while backtracking:
            valid_dirs: list[Position] = self.possible_moves(self.cur)
            self.cur = self.move(backtracking, self.cur,
                                 valid_dirs, render=True)
            yield
        if not maze.perfect:
            self.make_imperfect(.1)

        self.find_shortest_path()

        self.seeds[seed] = {
            'maze': self.maze.maze[:],
            'path': self.shortest_path[:],
            'buffer_img': self.buffer_img.copy()
        }
        self.maze.save(self)
        self.draw_generation = self.draw_shortest_path(0xFF0FFFFF)
