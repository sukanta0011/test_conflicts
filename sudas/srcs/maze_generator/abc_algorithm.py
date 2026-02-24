from abc import ABC, abstractmethod
from .grid import Grid
from typing import Tuple, Set


class Algorithm(ABC):
    grid: Grid

    def __init__(self, width: int, height: int,
                 entry: Tuple[int, int], exit: Tuple[int, int],
                 perfect: bool,
                 seed: None | str) -> None:
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
        pass

    def get_42_cells(self) -> Set[Tuple[int, int]] | str:
        if self.width < 7 or self.height < 5:
            return ("'42' number can not be represented. "
                    "Maze size is too small\n")
        # x and y represent center coordinates
        row, col = self.grid.center
        cells_42: Set[Tuple[int, int]] = set()
        # insert '4'
        cells_42.add(tuple([row, col - 1]))
        cells_42.add(tuple([row, col - 2]))
        cells_42.add(tuple([row, col - 3]))
        cells_42.add(tuple([row - 1, col - 3]))
        cells_42.add(tuple([row - 2, col - 3]))
        cells_42.add(tuple([row + 1, col - 1]))
        cells_42.add(tuple([row + 2, col - 1]))
        # # insert '2'
        cells_42.add(tuple([row, col + 1]))
        cells_42.add(tuple([row, col + 2]))
        cells_42.add(tuple([row, col + 3]))
        cells_42.add(tuple([row - 2, col + 1]))
        cells_42.add(tuple([row - 2, col + 2]))
        cells_42.add(tuple([row - 2, col + 3]))
        cells_42.add(tuple([row + 2, col + 1]))
        cells_42.add(tuple([row + 2, col + 2]))
        cells_42.add(tuple([row + 2, col + 3]))
        cells_42.add(tuple([row - 1, col + 3]))
        cells_42.add(tuple([row + 1, col + 1]))

        if self.entry in cells_42:
            return ("ENTRY coordinates are in '42' cells. "
                    "'42' number can not be represented.\n")
        if self.exit in cells_42:
            return ("Exit coordinates are in '42' cells. "
                    "'42' number can not be represented.\n")
        return cells_42
