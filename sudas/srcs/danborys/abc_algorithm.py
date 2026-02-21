from abc import ABC, abstractmethod
from grid import Grid
from config_parser import Configuration
from typing import List, Tuple


class Algorithm(ABC):
    config: Configuration
    grid: Grid

    def __init__(self, config: Configuration) -> None:
        super().__init__()
        self.config = config
        self.grid = Grid(config.width, config.height)

    @abstractmethod
    def generate(self) -> Grid:
        pass

    def get_42_cells(self) -> List[Tuple[int, int]] | str:
        if self.config.width < 7 or self.config.height < 5:
            return ("'42' number can not be represented. "
                    "Maze size is too small\n")
        # x and y represent center coordinates
        row, col = self.grid.center
        cells_42: List[Tuple[int, int]] = list()
        # insert '4'
        cells_42.append(tuple([row, col - 1]))
        cells_42.append(tuple([row, col - 2]))
        cells_42.append(tuple([row, col - 3]))
        cells_42.append(tuple([row - 1, col - 3]))
        cells_42.append(tuple([row - 2, col - 3]))
        cells_42.append(tuple([row + 1, col - 1]))
        cells_42.append(tuple([row + 2, col - 1]))
        # # insert '2'
        cells_42.append(tuple([row, col + 1]))
        cells_42.append(tuple([row, col + 2]))
        cells_42.append(tuple([row, col + 3]))
        cells_42.append(tuple([row - 2, col + 1]))
        cells_42.append(tuple([row - 2, col + 2]))
        cells_42.append(tuple([row - 2, col + 3]))
        cells_42.append(tuple([row + 2, col + 1]))
        cells_42.append(tuple([row + 2, col + 2]))
        cells_42.append(tuple([row + 2, col + 3]))
        cells_42.append(tuple([row - 1, col + 3]))
        cells_42.append(tuple([row + 1, col + 1]))

        if self.config.entry in cells_42:
            return ("ENTRY coordinates are in '42' cells. "
                    "'42' number can not be represented.\n")
        if self.config.exit in cells_42:
            return ("Exit coordinates are in '42' cells. "
                    "'42' number can not be represented.\n")
        return cells_42
