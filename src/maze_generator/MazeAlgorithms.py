import random
from src.maze_generator import MazeGenerator as Maze
from src.maze_generator import Position, VISITED
from typing import Optional, Generator
from src.rendering.images_utils import ImgData, draw_wall


class MazeAlgorithms:
    """Provide diferent types of maze generation algorithms"""

    def __init__(self, maze: Maze, buffer_img: ImgData) -> None:
        self.all_possible_dir_cells: dict[Position, list[Position]] = {}
        #self.visited_cells: int = 0
        self.shortest_path: list[Position] = []
        self.maze: Maze = maze
        self.buffer_img: ImgData = buffer_img
        self.generation: Generator = self.backtracking_generate()
        self.cur: Position = maze.entry

    def possible_moves(self,
                       pos: Position,
                       set_visited: Optional[bool] = True) -> list[Position]:
        maze: Maze = self.maze
        if pos in self.all_possible_dir_cells:
            return self.all_possible_dir_cells[pos]
        all_directions: list[Position] = [
            pos.up(),
            pos.down(),
            pos.right(),
            pos.left()
        ]
        valid_dirs: list[Position] = [
            p for p in all_directions
            if maze.is_inside(p) and not (maze.maze[p.y][p.x] & VISITED)
        ]

        if not set_visited:
            return valid_dirs

        maze.maze[pos.y][pos.x] |= VISITED
        for p in valid_dirs:
            maze.maze[p.y][p.x] |= VISITED
        #self.visited_cells += len(valid_dirs)
        self.all_possible_dir_cells[pos] = valid_dirs
        return valid_dirs

    def move(self, stack: list[Position], cur: Position, render: Optional[bool] = False) -> None:
        valid_moves: list[Position] = self.possible_moves(cur)
        if valid_moves:
            stack.append(cur)
            next_cell: Position = random.choice(valid_moves)
            valid_moves.remove(next_cell)
            if self.possible_moves(next_cell, set_visited=False):
                if render:
                    draw_wall(self.buffer_img, cur.x+1, cur.y+1, 16, 0xFFFF0000)
                self.maze.maze[cur.y][cur.x] &= ~(next_cell.direction)
                self.maze.maze[next_cell.y][next_cell.x] &= ~(next_cell.rev_direction())
            return next_cell
        back_cell: Position = stack.pop()
        if render:
            draw_wall(self.buffer_img, back_cell.x+1, back_cell.y+1, 16, 0xFFFFFFFF)
        return back_cell

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
        self.shortest_path = []
        self.all_possible_dir_cells = {}
        while not self.found_exit(current_cell):
            current_cell = self.move(self.shortest_path, current_cell)
        self.shortest_path += [current_cell, maze.exit]

    def backtracking_generate(self) -> Generator:
        maze: Maze = self.maze
        total_cells: int = maze.total_cells - maze.borders
        self.find_shortest_path()
        backtracking: list[Position] = []
        #self.visited_cells = 1
        maze.clear()
        self.all_possible_dir_cells = {}
        path_len: int = len(self.shortest_path)
        for i, cell in enumerate(self.shortest_path):
            self.cur = cell
            valid_moves: list[Position] = self.possible_moves(cell)
            backtracking.append(cell)
            if i < path_len - 1:
                next_cell: Position = self.shortest_path[i + 1]
                valid_moves.remove(next_cell)
                if self.possible_moves(next_cell, set_visited=False):
                    draw_wall(self.buffer_img, cell.x+1, cell.y+1, 16, 0xFFFF0000)
                    self.maze.maze[cell.y][cell.x] &= ~(next_cell.direction)
                    self.maze.maze[next_cell.y][next_cell.x] &= ~(next_cell.rev_direction())
            yield
        #while self.visited_cells < total_cells:
        while backtracking:
            self.cur = self.move(backtracking, self.cur, render=True)
            yield
        self.cur = Position(-1, -1, None)
