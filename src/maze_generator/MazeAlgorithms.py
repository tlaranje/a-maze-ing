import random
import time
from src.maze_generator import MazeGenerator as Maze
from src.maze_generator import Position, VISITED



class MazeAlgorithms:
    """Provide diferent types of maze generation algorithms"""

    def __init__(self) -> None:
        self.all_possible_dir_cells: dict[Position, list[Position]] = {}
        self.visited_cells: int = 0
        self.shortest_path: list[Position] = []

    def possible_moves(self, maze: Maze, pos: Position) -> list[Position]:
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
            if maze.is_inside(p) and not (maze.maze[p.x][p.y] & VISITED)
        ]
        maze.maze[pos.x][pos.y] |= VISITED
        for p in valid_dirs:
            maze.maze[pos.x][pos.y] &= ~(p.direction)
            maze.maze[p.x][p.y] |= VISITED
        self.visited_cells += len(valid_dirs)
        self.all_possible_dir_cells[pos] = valid_dirs
        return valid_dirs

    def move(self, maze: Maze, stack: list[Position], cur: Position) -> None:
        valid_moves: list[Position] = self.possible_moves(maze, cur)
        if valid_moves:
            stack.append(cur)
            next_cell: Position = random.choice(valid_moves)
            valid_moves.remove(next_cell)
            cur = next_cell
        else:
            cur = stack.pop()
        return cur

    @staticmethod
    def found_exit(pos: Position, maze: Maze) -> bool:
        _exit: Position = maze.exit
        all_directions: list[Position] = [
            pos.up(),
            pos.down(),
            pos.right(),
            pos.left()
        ]
        for pos in all_directions:
            if pos.x == _exit.x and pos.y == _exit.y:
                maze.exit = Position(_exit.x, _exit.y, pos.direction)
                return True
        return False

    def find_shortest_path(self, maze: Maze) -> None:
        #from src.a_maze_ing import draw_walls
        current_cell: Position = maze.entry
        maze.clear()
        self.shortest_path = []
        self.all_possible_dir_cells = {}
        while not self.found_exit(current_cell, maze):
            #draw_walls(xvar, maze)
            current_cell = self.move(maze, self.shortest_path, current_cell)
        self.shortest_path += [current_cell, maze.exit]

    def backtracking_generate(self, maze: Maze) -> None:
        total_cells: int = maze.total_cells - maze.borders
        backtracking: list[Position] = []
        self.visited_cells = 1
        maze.clear()
        self.all_possible_dir_cells = {}
        for i, cur in enumerate(self.shortest_path):
            valid_dirs = self.possible_moves(maze, cur)
            backtracking.append(cur)
            if i < len(self.shortest_path) - 1:
                self.all_possible_dir_cells[cur].remove(self.shortest_path[i + 1])
        current_cell = maze.exit
        while self.visited_cells < total_cells:
            current_cell = self.move(maze, backtracking, current_cell)

