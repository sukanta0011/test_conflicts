from abc import ABC, abstractmethod
from .grid import Grid
from typing import Tuple, Set


class Algorithm(ABC):
    """
    Abstract base class for maze generation algorithms.

    This class defines the common interface and shared logic for
    concrete maze generation implementations. Subclasses must
    implement the `generate()` method.

    Attributes:
        width (int): Width of the maze grid.
        height (int): Height of the maze grid.
        entry (Tuple[int, int]): Entry cell coordinates.
        exit (Tuple[int, int]): Exit cell coordinates.
        perfect (bool): Indicates whether the maze must be perfect
            (i.e., without cycles and with a unique solution).
        seed (None | str): Optional seed for deterministic generation.
        grid (Grid): Internal grid representation of the maze.
    """
    grid: Grid

    def __init__(self, width: int, height: int,
                 entry: Tuple[int, int], exit: Tuple[int, int],
                 perfect: bool,
                 seed: None | str) -> None:
        """
        Initialize common algorithm parameters and create the grid.

        Args:
            width (int): Maze width.
            height (int): Maze height.
            entry (Tuple[int, int]): Entry cell coordinates.
            exit (Tuple[int, int]): Exit cell coordinates.
            perfect (bool): Whether the maze must be perfect.
            seed (None | str): Optional random seed for reproducibility.
        """
        super().__init__()
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        self.grid = Grid(width, height)

    @abstractmethod
    def generate(self) -> Grid:
        """
        Generate the maze structure.

        This method must be implemented by concrete subclasses.
        It should populate the internal grid according to the
        chosen maze generation algorithm.

        Returns:
            Grid: The generated maze grid.
        """
        pass

    def get_42_cells(self) -> Set[Tuple[int, int]] | str:
        """
        Compute the set of grid cells used to represent the '42' pattern.

        The pattern is centered in the maze and consists of a fixed
        arrangement of cells forming the digits '4' and '2'.
        If the maze dimensions are too small to represent the pattern,
        or if the entry/exit coordinates overlap with the pattern,
        a descriptive error message is returned instead.

        Returns:
            Set[Tuple[int, int]] | str:
                - A set of (row, col) coordinates forming the '42' pattern,
                  if representation is possible.
                - A string error message if the pattern cannot be represented.
        """
        if self.width < 7 or self.height < 5:
            return ("'42' number can not be represented. "
                    "Maze size is too small\n")
        row, col = self.grid.center
        cells_42: Set[Tuple[int, int]] = set()
        cells_42.add((row, col - 1))
        cells_42.add((row, col - 2))
        cells_42.add((row, col - 3))
        cells_42.add((row - 1, col - 3))
        cells_42.add((row - 2, col - 3))
        cells_42.add((row + 1, col - 1))
        cells_42.add((row + 2, col - 1))
        cells_42.add((row, col + 1))
        cells_42.add((row, col + 2))
        cells_42.add((row, col + 3))
        cells_42.add((row - 2, col + 1))
        cells_42.add((row - 2, col + 2))
        cells_42.add((row - 2, col + 3))
        cells_42.add((row + 2, col + 1))
        cells_42.add((row + 2, col + 2))
        cells_42.add((row + 2, col + 3))
        cells_42.add((row - 1, col + 3))
        cells_42.add((row + 1, col + 1))

        if self.entry in cells_42:
            return ("ENTRY coordinates are in '42' cells. "
                    "'42' number can not be represented.\n")
        if self.exit in cells_42:
            return ("Exit coordinates are in '42' cells. "
                    "'42' number can not be represented.\n")
        return cells_42
