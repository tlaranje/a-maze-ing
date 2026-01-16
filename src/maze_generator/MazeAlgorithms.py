import random
import time
from src.maze_generator import MazeGenerator as Maze
from src.maze_generator import Position, Direction, VISITED


class MazeAlgorithms:
    """Provide diferent types of maze generation algorithms"""

    def __init__(self) -> None:
        self.all_possible_dir_cells: dict[Position, list[Position]] = {}

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
            if maze.is_inside(p) and maze.maze[p.x][p.y] & VISITED
        ]
        for p in valid_dirs:
            maze.maze[p.x][p.y] &= ~(p.direction)
            maze.maze[p.x][p.y] |= VISITED
        self.all_possible_dir_cells[pos] = valid_dirs
        return valid_dirs

    def backtracking(self, maze: Maze) -> None:
        visited_cells: int = 0
        backtracking_cells: list[Position] = []
        current_cell: Position = maze.entry
        while visited_cells < maze.total_cells:
            maze.render(current_cell)
            print(current_cell)
            print(visited_cells)
            print()
            time.sleep(1)
            valid_dirs: list[Position] = self.possibles_dirs(maze, current_cell)
            if valid_dirs:
                backtracking_cells.append(current_cell)
                next_cell: Position = random.choice(valid_dirs)
                valid_dirs.remove(next_cell)
                current_cell = next_cell
                visited_cells += 1
            else:
                current_cell = backtracking_cells.pop()
