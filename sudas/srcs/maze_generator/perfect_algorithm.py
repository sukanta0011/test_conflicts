from .abc_algorithm import Algorithm
from .grid import Grid, Wall
from typing import Tuple, List, Set
import time
import random


class PerfectAlgorithm(Algorithm):
    def generate(self) -> Grid:
        self.grid.reset_cells()
        if self.config.seed:
            random.seed(self.config.seed)
        self.visited: Set[Tuple[int, int]] = set()
        cells_42 = self.get_42_cells()
        if isinstance(cells_42, str):
            print(cells_42)
            self.find_neighbour(self.config.entry)
        else:
            self.visited.update(cells_42)
            self.find_neighbour(self.config.entry)
        return self.grid

    def find_neighbour(self, current_cell: Tuple[int, int]):
        self.visited.add(current_cell)

        neighbours: List[Tuple[int, int]] = []
        left_neighbour = tuple([current_cell[0], current_cell[1] - 1])
        if self.is_coord_in_boundry(left_neighbour) and left_neighbour not in self.visited:
            neighbours.append(left_neighbour)

        right_neighbour = tuple([current_cell[0], current_cell[1] + 1])
        if self.is_coord_in_boundry(right_neighbour) and right_neighbour not in self.visited:
            neighbours.append(right_neighbour)
        up_neighbour = tuple([current_cell[0] - 1, current_cell[1]])
        if self.is_coord_in_boundry(up_neighbour) and up_neighbour not in self.visited:
            neighbours.append(up_neighbour)
        down_neighbour = tuple([current_cell[0] + 1, current_cell[1]])
        if self.is_coord_in_boundry(down_neighbour) and down_neighbour not in self.visited:
            neighbours.append(down_neighbour)

        random.shuffle(neighbours)
        for neighbour in neighbours:
            if neighbour not in self.visited:
                current_wall = 0
                if neighbour[0] > current_cell[0]:
                    current_wall = Wall.SOUTH
                elif neighbour[0] < current_cell[0]:
                    current_wall = Wall.NORTH
                elif neighbour[1] > current_cell[1]:
                    current_wall = Wall.EAST
                elif neighbour[1] < current_cell[1]:
                    current_wall = Wall.WEST
                self.grid.cells[current_cell[0]][current_cell[1]] &= ~current_wall
                self.grid.cells[neighbour[0]][neighbour[1]] &= ~current_wall.opposite()
                self.find_neighbour(neighbour)

    def is_coord_in_boundry(self, coords: Tuple[int, int]) -> bool:
        if 0 <= coords[0] < self.config.height and 0 <= coords[1] < self.config.width:
            return True
        return False
