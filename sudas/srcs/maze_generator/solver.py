from .grid import Grid, Wall
from .config_parser import Configuration
from collections import deque
from typing import Tuple, Deque, List, Set


class Solver():
    def __init__(self, grid: Grid, config: Configuration):
        self.cells = grid.cells
        self.config = config
        self.path = ""

    def find_path(self) -> List[str]:
        valid_paths = []
        cells_deque: Deque = deque()
        cells_deque.append(self.config.entry)
        self.visited: Set[Tuple[int, int]] = set()
        self.visited.add(self.config.entry)

        while len(cells_deque) != 0:
            current_cell = cells_deque[-1]
            neighbors = self.find_neighbors(current_cell, self.visited)
            if len(neighbors) == 0:
                cells_deque.pop()
                self.path = self.path[:-1]
                # self.visited.pop()
                # print(self.path)
            else:
                row_cur, col_cur = current_cell
                next_cell = neighbors[0]
                self.visited.add(next_cell)
                cells_deque.append(next_cell)
                row_next, col_next = next_cell
                if row_next > row_cur:
                    self.path += "S"
                elif row_next < row_cur:
                    self.path += "N"
                elif col_next > col_cur:
                    self.path += "E"
                elif col_next < col_cur:
                    self.path += "W"
                if next_cell == self.config.exit:
                    valid_paths.append(self.path)
                    continue
                    # cells_deque.clear()
                    # cells_deque.pop()
                    # self.path = self.path[:-1]
        print(len(valid_paths))
        return valid_paths

    def find_neighbors(
            self, current_cell: Tuple[int, int],
            visited: set[Tuple[int, int]]) -> List[Tuple[int, int]]:
        neighbors: List[Tuple[int, int]] = []
        cur_row, cur_col = current_cell
        for wall in Wall:
            if self.cells[cur_row][cur_col] & wall.value == 0:
                if wall is Wall.EAST:
                    if (cur_row, cur_col + 1) not in visited:
                        neighbors.append((cur_row, cur_col + 1))
                elif wall is Wall.WEST:
                    if (cur_row, cur_col - 1) not in visited:
                        neighbors.append((cur_row, cur_col - 1))
                elif wall is Wall.NORTH:
                    if (cur_row - 1, cur_col) not in visited:
                        neighbors.append((cur_row - 1, cur_col))
                elif wall is Wall.SOUTH:
                    if (cur_row + 1, cur_col) not in visited:
                        neighbors.append((cur_row + 1, cur_col))
        return neighbors
