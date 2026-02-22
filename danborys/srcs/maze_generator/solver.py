from .grid import Grid, Wall
from .config_parser import Configuration
from collections import deque
from typing import Tuple, Deque, List, Set


class Solver():
    def __init__(self, grid: Grid, config: Configuration):
        self.cells = grid.cells
        self.config = config
        self.path = ""

    # def find_path(self) -> str:
    #     current_cell = self.config.entry
    #     row_cur, col_cur = current_cell
    #     neighbours_deque = self.find_neighbours(current_cell)
    #     while len(neighbours_deque) != 0:
    #         next_cell = neighbours_deque[-1]
    #         row_next, col_next = next_cell
    #         if row_next > row_cur:
    #             self.path += "S"
    #         elif row_next < row_cur:
    #             self.path += "N"
    #         elif col_next > col_cur:
    #             self.path += "E"
    #         elif col_next < col_cur:
    #             self.path += "W"
    #         next_neighbours = self.find_neighbours(next_cell)
    #         if len(next_neighbours) != 0:
    #             neighbours_deque.pop()
    #         if next_neighbours == self.config.exit:
    #             pass

    # def find_neighbours(self, current_cell: Tuple[int, int]) -> Deque[Tuple[int, int]]:
    #     cur_row, cur_col = current_cell
    #     neighbours_deque = deque()
    #     for wall in Wall:
    #         if self.cells[cur_row][cur_col] & wall.value == 0:
    #             if wall is Wall.EAST:
    #                 neighbours_deque.append((cur_row, cur_col + 1))
    #             elif wall is Wall.WEST:
    #                 neighbours_deque.append((cur_row, cur_col - 1))
    #             elif wall is Wall.NORTH:
    #                 neighbours_deque.append((cur_row - 1, cur_col))
    #             elif wall is Wall.SOUTH:
    #                 neighbours_deque.append((cur_row + 1, cur_col))
    #     return neighbours_deque

    def find_path(self) -> str:
        vaild_paths = []
        cells_deque: Deque = deque()
        cells_deque.append(self.config.entry)
        self.visited: Set[Tuple[int, int]] = set()
        self.visited.add(self.config.entry)
        while len(cells_deque) != 0:
            current_cell = cells_deque[-1]
            neighbours = self.find_neighbours(current_cell)
            if len(neighbours) == 0:
                cells_deque.pop()
                self.path = self.path[:-1]
                print(self.path)
            else:
                row_cur, col_cur = current_cell
                next_cell = neighbours[0]
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
                    print("path found")
                    vaild_paths.append(self.path)
        print(f"all paths: {len(vaild_paths)}")
        min_path = min([len(path) for path in vaild_paths])
        return vaild_paths

    def find_neighbours(self, current_cell: Tuple[int, int]) -> List[Tuple[int, int]]:
        neighbours: List[Tuple[int, int]] = []
        cur_row, cur_col = current_cell
        for wall in Wall:
            if self.cells[cur_row][cur_col] & wall.value == 0:
                if wall is Wall.EAST:
                    if (cur_row, cur_col + 1) not in self.visited:
                        neighbours.append((cur_row, cur_col + 1))
                elif wall is Wall.WEST:
                    if (cur_row, cur_col - 1) not in self.visited:
                        neighbours.append((cur_row, cur_col - 1))
                elif wall is Wall.NORTH:
                    if (cur_row - 1, cur_col) not in self.visited:
                        neighbours.append((cur_row - 1, cur_col))
                elif wall is Wall.SOUTH:
                    if (cur_row + 1, cur_col) not in self.visited:
                        neighbours.append((cur_row + 1, cur_col))
        return neighbours
