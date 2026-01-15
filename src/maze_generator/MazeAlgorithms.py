from MazeGenerator import MazeGenerator as Maze


class MazeAlgorithms(Maze):
    """Provide diferent types of maze generation algorithms"""

    def possibles_directions(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        all_directions: list[tuple[int, int]] = [
            (pos[0], pos[1] - 1),   # UP
            (pos[0], pos[1] + 1),   # DOWN
            (pos[0] + 1, pos[1]),   # RIGHT
            (pos[0] - 1, pos[1]),   # LEFT
        ]

    def backtracking(self) -> None:
        visited_cells: int = 0
        backtracking_cells: list[tuple[int, int]] = []
        current_cell: tuple[int, int] = self.entry
        while visited_cells < self.total_cells:
