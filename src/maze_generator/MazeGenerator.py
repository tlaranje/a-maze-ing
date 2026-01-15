from typing import Optional as op


class MazeGenerator:
    # TODO
    """PUT DOCUMENTATION PLEASE"""
    def __init__(self,
                 height: op[int] = None,
                 width: op[int] = None,
                 entry: op[tuple] = None,
                 _exit: op[tuple] = None,
                 output_file: op[str] = None,
                 perfect: op[bool] = None) -> None:
        self.height: int = height
        self.width: int = width
        self.entry: tuple = entry
        self.exit: tuple = _exit
        self.output_file: str = output_file
        self.perfect: bool = perfect

    def is_inside(self, point: tuple[int, int]) -> bool:
        return (self.width - 1 > point[0] > 0
                and self.height - 1 > point[1] > 0)
