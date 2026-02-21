from abc_algorithm import Algorithm
from grid import Grid


class PerfectAlgorithm(Algorithm):
    def generate(self) -> Grid:
        cells_42 = self.get_42_cells()
        if isinstance(cells_42, str):
            print(cells_42)
        return self.grid
