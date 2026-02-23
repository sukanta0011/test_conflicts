from .config_parser import Configuration
from .grid import Grid
from .abc_algorithm import Algorithm
from .perfect_algorithm import PerfectAlgorithm


class MazeGenerator():
    config: Configuration
    grid: Grid
    algorithm: Algorithm

    def __init__(self, config: Configuration) -> None:
        self.config = config
        # if config.perfect:
        #     self.algorithm = PerfectAlgorithm(config)
        # else:
        #     self.algorithm = BasicAlgorithm(config)
        self.algorithm = PerfectAlgorithm(config)
        self.grid = self.algorithm.generate()

    def print_grid(self) -> None:
        print(self.grid)
        print()
        self.grid.print_hex_format()
