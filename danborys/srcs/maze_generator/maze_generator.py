from .grid import Grid
from .abc_algorithm import Algorithm
from .perfect_algorithm import PerfectAlgorithm
from typing import Tuple


class MazeGenerator():
    grid: Grid
    algorithm: Algorithm

    def __init__(self,
                 width: int, height: int,
                 entry: Tuple[int, int], exit: Tuple[int, int],
                 output_file: str,
                 perfect: bool,
                 seed: None | str = None) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed

        self.algorithm = PerfectAlgorithm(self.width,
                                          self.height,
                                          self.entry,
                                          self.exit,
                                          self.perfect,
                                          self.seed)
        self.grid = self.algorithm.generate()
