from abc_algorithm import Algorithm
from grid import Grid


class BasicAlgorithm(Algorithm):
    def generate(self) -> Grid:
        cells_42 = self.get_42_cells()
        if isinstance(cells_42, str):
            print(cells_42)
            for row_ind, row in enumerate(self.grid.cells, start=0):
                for col_ind, cell in enumerate(row, start=0):
                    self.grid.cells[row_ind][col_ind] = 0
            return self.grid
        for row_ind, row in enumerate(self.grid.cells, start=0):
            for col_ind, cell in enumerate(row, start=0):
                if tuple([row_ind, col_ind]) in cells_42:
                    continue
                self.grid.cells[row_ind][col_ind] = 0
        return self.grid
