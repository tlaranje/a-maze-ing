import random
import time
from src.maze_generator import MazeGenerator as Maze
from src.maze_generator import Position, VISITED


class MazeAlgorithms:
    """Provide diferent types of maze generation algorithms"""

    def __init__(self) -> None:
        self.all_possible_dir_cells: dict[Position, list[Position]] = {}
        self.visited_cells: int = 0

    def possibles_dirs(self, maze: Maze, pos: Position) -> list[Position]:
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

    @staticmethod
    def found_exit(pos: Position, _exit: Position) -> bool:
        all_directions: list[Position] = [
            pos.up(),
            pos.down(),
            pos.right(),
            pos.left()
        ]
        """ print(pos.up())
        print(pos.down())
        print(pos.right())
        print(pos.left()) """
        for d in all_directions:
            if (d.x == _exit.x) and (d.y == _exit.y):
                return True
        return False

    def shortest_path(self, maze: Maze) -> list[Position]:
        backtracking_cells: list[Position] = []
        current_cell: Position = maze.entry
        while not self.found_exit(current_cell, maze.exit):
            maze.render(current_cell)
            print(current_cell)
            print(maze.exit)
            print()
            time.sleep(1)
            valid_dirs: list[Position] = self.possibles_dirs(maze, current_cell)
            if valid_dirs:
                backtracking_cells.append(current_cell)
                next_cell: Position = random.choice(valid_dirs)
                valid_dirs.remove(next_cell)
                current_cell = next_cell
            else:
                current_cell = backtracking_cells.pop()
        maze.render(current_cell)
        print(current_cell)
        print()
        return backtracking_cells

    def backtracking(self, maze: Maze) -> None:
        total_cells: int = maze.total_cells - maze.borders
        backtracking_cells: list[Position] = []
        current_cell: Position = maze.entry
        self.visited_cells = 1
        while self.visited_cells < total_cells:
            maze.render(current_cell)
            print(current_cell)
            print(f"{self.visited_cells}/{total_cells}")
            print()
            time.sleep(0.001)
            valid_dirs: list[Position] = self.possibles_dirs(maze, current_cell)
            if valid_dirs:
                backtracking_cells.append(current_cell)
                next_cell: Position = random.choice(valid_dirs)
                valid_dirs.remove(next_cell)
                current_cell = next_cell
            else:
                current_cell = backtracking_cells.pop()
        maze.render(Position(-1, -1))
        print(current_cell)
        print(f"{self.visited_cells}/{total_cells}")
        print()
