from .grid import Grid
from .abc_algorithm import Algorithm
from .perfect_algorithm import PerfectAlgorithm
from .solver import Solver
from typing import Tuple


class MazeGenerator():
    """
    High-level orchestrator responsible for maze creation and solving.

    This class coordinates:
        - Maze generation via a selected Algorithm implementation.
        - Path finding via a Solver.
        - Storage of the resulting grid and computed solution.

    It encapsulates the full maze lifecycle: initialization,
    generation, and shortest path computation.
    """
    grid: Grid
    algorithm: Algorithm
    solver: Solver
    solution: str

    def __init__(self,
                 width: int, height: int,
                 entry: Tuple[int, int], exit: Tuple[int, int],
                 perfect: bool,
                 seed: None | str = None) -> None:
        """
        Initialize the MazeGenerator.

        Args:
            width (int): Maze width.
            height (int): Maze height.
            entry (Tuple[int, int]): Entry cell coordinates (row, col).
            exit (Tuple[int, int]): Exit cell coordinates (row, col).
            perfect (bool): Whether to generate a perfect maze
                (i.e., exactly one unique path between any two cells).
            seed (str | None, optional): Optional seed value used
                for deterministic maze generation.

        Side Effects:
            - Instantiates the selected Algorithm implementation.
            - Generates the maze grid.
            - Computes the shortest path between entry and exit.
        """
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
        """
        Regenerate the maze and recompute its solution.

        This method:
            1. Calls the algorithm to create a new grid.
            2. Uses the solver to compute the shortest path
               from entry to exit.
        """
        self.grid = self.algorithm.generate()
        self.solution = self.solver.find_path(self.grid, self.entry, self.exit)
