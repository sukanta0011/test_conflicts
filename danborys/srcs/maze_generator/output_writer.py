from .config_parser import Configuration
from .solver import Solver
from .grid import Grid


class OutputWriter():
    def __init__(self, config: Configuration) -> None:
        self.config = config
        self.solver = Solver()

    def create_output(self, grid: Grid) -> None:
        path = self.solver.find_path(grid, self.config)
        print(path)
