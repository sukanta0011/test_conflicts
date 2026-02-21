from .abc_algorithm import Algorithm
from .grid import Grid, Wall
from typing import Tuple, List
import time


class PerfectAlgorithm(Algorithm):
    def generate(self) -> Grid:
        cells_42 = self.get_42_cells()
        if isinstance(cells_42, str):
            print(cells_42)
            self.find_neighbour(self.config.entry, [])
        else:
            self.find_neighbour(self.config.entry, cells_42)
        return self.grid

    def find_neighbour(self, current_cell: Tuple[int, int], visited: List[Tuple[int, int]]):
        visited.append(current_cell)

        if len(visited) == self.grid.cells_count:
            return

        neighbours: List[Tuple[int, int]] = []
        left_neighbour = tuple([current_cell[0], current_cell[1] - 1])
        if self.is_coord_in_boundry(left_neighbour) and left_neighbour not in visited:
            neighbours.append(left_neighbour)

        right_neighbour = tuple([current_cell[0], current_cell[1] + 1])
        if self.is_coord_in_boundry(right_neighbour) and right_neighbour not in visited:
            neighbours.append(right_neighbour)
        up_neighbour = tuple([current_cell[0] - 1, current_cell[1]])
        if self.is_coord_in_boundry(up_neighbour) and up_neighbour not in visited:
            neighbours.append(up_neighbour)
        down_neighbour = tuple([current_cell[0] + 1, current_cell[1]])
        if self.is_coord_in_boundry(down_neighbour) and down_neighbour not in visited:
            neighbours.append(down_neighbour)
        # if len(neighbours) == 0:
        #     return
        # print(visited)
        counter = 0
        for neighbour in neighbours:
            current_wall = 0
            neighbour_wall = 0
            if neighbour[0] > current_cell[0]:
                current_wall = Wall.SOUTH
                neighbour_wall = Wall.NORTH
            if neighbour[0] < current_cell[0]:
                current_wall = Wall.NORTH
                neighbour_wall = Wall.SOUTH
            if neighbour[1] > current_cell[1]:
                current_wall = Wall.EAST
                neighbour_wall = Wall.WEST
            if neighbour[1] < current_cell[1]:
                current_wall = Wall.WEST
                neighbour_wall = Wall.EAST
            self.grid.cells[current_cell[0]][current_cell[1]] &= ~current_wall
            self.grid.cells[neighbour[0]][neighbour[1]] &= ~neighbour_wall
            print(neighbours)
            time.sleep(1)
            counter += 1
            if counter == 2:
                return
            self.find_neighbour(neighbour, visited)

    def is_coord_in_boundry(self, coords: Tuple[int, int]) -> bool:
        if 0 <= coords[0] < self.config.height and 0 <= coords[1] < self.config.width:
            # print(coords)
            return True
        return False
