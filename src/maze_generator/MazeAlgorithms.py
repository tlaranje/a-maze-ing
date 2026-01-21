import random
from src.maze_generator import MazeGenerator as Maze
from src.maze_generator import Position, VISITED, IS_42, Direction
from typing import Optional, Generator
from src.rendering.images_utils import ImgData, draw_way


class MazeAlgorithms:
    """Provide diferent types of maze generation algorithms"""

    def __init__(self, maze: Maze, buffer_img: ImgData) -> None:
        self.shortest_path: list[Position] = []
        self.maze: Maze = maze
        self.buffer_img: ImgData = buffer_img
        self.generation: Generator = self.backtracking_generate()
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

    def move(self, stack: list[Position], cur: Position, render: Optional[bool] = False) -> Position:
        self.maze.maze[cur.y][cur.x] |= VISITED
        valid_moves: list[Position] = self.possible_moves(cur)
        if valid_moves:
            stack.append(cur)
            next_cell: Position = random.choice(valid_moves)
            if render:
                draw_way(self.buffer_img, cur, 16, 0xFFFF0000)
            self.maze.maze[cur.y][cur.x] &= ~(next_cell.direction)
            self.maze.maze[next_cell.y][next_cell.x] &= ~(next_cell.rev_direction())
            return next_cell
        if render:
            draw_way(self.buffer_img, cur, 16, 0xFFFFFFFF)
        return stack.pop()

    def found_exit(self, pos: Position) -> bool:
        maze: Maze = self.maze
        all_directions: list[Position] = [
            pos.up(),
            pos.right(),
            pos.left(),
            pos.down()
        ]
        _exit: Position = maze.exit
        for pos in all_directions:
            if pos.x == _exit.x and pos.y == _exit.y:
                maze.exit = Position(_exit.x, _exit.y, pos.direction)
                return True
        return False

    def find_shortest_path(self) -> None:
        maze: Maze = self.maze
        current_cell: Position = maze.entry
        maze.clear()
        maze.draw_42()
        self.shortest_path = []
        while not self.found_exit(current_cell):
            current_cell = self.move(self.shortest_path, current_cell)
        self.shortest_path += [current_cell, maze.exit]

    def draw_shortest_path(self, color: int, stack: Optional[list[Position]] = None) -> Generator:
        if stack is None:
            for cell in self.shortest_path:
                draw_way(self.buffer_img, cell, 16, color)
                yield
            entry: Position = self.maze.entry
            _exit: Position = self.maze.exit
            draw_way(self.buffer_img, entry, 16, 0xFF0000FF)
            draw_way(self.buffer_img, _exit, 16, 0xFFFF0000)
            return
        path_len: int = len(self.shortest_path)
        for i, cell in enumerate(self.shortest_path):
            self.cur = cell
            stack.append(cell)
            if i < path_len - 1:
                next_cell: Position = self.shortest_path[i + 1]
                draw_way(self.buffer_img, cell, 16, color)
                self.maze.maze[cell.y][cell.x] &= ~(next_cell.direction)
                self.maze.maze[next_cell.y][next_cell.x] &= ~(next_cell.rev_direction())
                self.maze.maze[cell.y][cell.x] |= VISITED
            yield

    def backtracking_generate(self) -> Generator:
        maze: Maze = self.maze
        self.find_shortest_path()
        backtracking: list[Position] = []
        maze.clear()
        maze.draw_42(self.buffer_img)
        yield from self.draw_shortest_path(0xFFFF0000, backtracking)
        while backtracking:
            self.cur = self.move(backtracking, self.cur, render=True)
            yield
        if not maze.perfect:
            self.make_imperfect(0.1)
        maze.save(self)
        self.draw_generation = self.draw_shortest_path(0xFF00FF00)
