import random
from src.maze_generator import MazeGenerator as Maze
from src.maze_generator import Position, VISITED, IS_42, Direction
from typing import Optional as opt
from typing import Generator
from src.rendering.images_utils import ImgData, draw_way
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

    def make_imperfect(self, chance: float) -> None:
        maze: Maze = self.maze
        for y in range(1, maze.height - 1):
            for x in range(1, maze.width - 1):
                if (maze.maze[y][x] & IS_42) or (maze.maze[y+1][x] & IS_42):
                    continue
                if random.random() < chance:
                    maze.maze[y][x] &= ~(Direction.SOUTH)
                    maze.maze[y+1][x] &= ~(Direction.NORTH)
                    curr: Position = Position(x, y, Direction.NORTH)
                    draw_way(self.buffer_img, curr, 16, 0xFFFFFFFF)

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

    def possible_paths(self, pos: Position) -> list[Position]:
        maze: Maze = self.maze.maze
        cell: Position = maze[pos.y][pos.x]
        valid_dirs: list[Position] = []
        if not (cell & Direction.NORTH) and not (maze[pos.y-1][pos.x] & VISITED):
            valid_dirs.append(pos.up())
        if not (cell & Direction.SOUTH) and not (maze[pos.y+1][pos.x] & VISITED):
            valid_dirs.append(pos.down())
        if not (cell & Direction.EAST) and not (maze[pos.y][pos.x+1] & VISITED):
            valid_dirs.append(pos.right())
        if not (cell & Direction.WEST) and not (maze[pos.y][pos.x-1] & VISITED):
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
        draw_way(self.buffer_img, entry, 16, 0xFF0000FF)
        draw_way(self.buffer_img, _exit, 16, 0xFFFF0000)

    def backtracking_generate(self, seed: int) -> Generator:
        if seed in self.seeds:
            Maze.render(seed)
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
            self.make_imperfect(0.1)

        self.find_shortest_path()

        maze.seeds[seed] = {
            'maze': self.maze.maze,
            'path': self.shortest_path
        }

        self.draw_generation = self.draw_shortest_path(0xFF00FF00)
