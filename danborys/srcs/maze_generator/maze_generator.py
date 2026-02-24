from .grid import Grid
from .abc_algorithm import Algorithm
from .perfect_algorithm import PerfectAlgorithm
from .solver import Solver
from typing import Tuple


class MazeGenerator():
    grid: Grid
    algorithm: Algorithm
    solver: Solver
    solution: str

    def __init__(self,
                 width: int, height: int,
                 entry: Tuple[int, int], exit: Tuple[int, int],
                 perfect: bool,
                 seed: None | str = None) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        self.algorithm = PerfectAlgorithm(self.width,
                                          self.height,
                                          self.entry,
                                          self.exit,
                                          self.perfect,
                                          self.seed)
        self.solver = Solver()
        self.grid = self.algorithm.generate()
        self.solution = self.solver.find_path(self.grid, self.entry, self.exit)

    def generate(self) -> None:
        self.grid = self.algorithm.generate()
        self.solution = self.solver.find_path(self.grid, self.entry, self.exit)
