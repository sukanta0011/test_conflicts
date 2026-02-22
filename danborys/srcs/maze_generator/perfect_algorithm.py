from .abc_algorithm import Algorithm
from .grid import Grid, Wall
from typing import Tuple, List, Set, Deque
import random
from collections import deque


class PerfectAlgorithm(Algorithm):
    def generate(self) -> Grid:
        self.grid.reset_cells()
        if self.config.seed:
            random.seed(self.config.seed)
        self.visited: Set[Tuple[int, int]] = set()
        cells_42 = self.get_42_cells()
        if isinstance(cells_42, str):
            print(cells_42)
            self.carve_maze_from(self.config.entry)
        else:
            self.visited.update(cells_42)
            self.carve_maze_from(self.config.entry)
        return self.grid

    def carve_maze_from(self, first_cell: Tuple[int, int]):
        cells_deque: Deque = deque()
        cells_deque.append(first_cell)
        self.visited.add(first_cell)
        while len(cells_deque) != 0:
            current_cell = cells_deque[-1]
            neighbours = self.find_neighbours(current_cell)
            if len(neighbours) == 0:
                cells_deque.pop()
            else:
                random.shuffle(neighbours)
                row_next, col_next = neighbours[0]
                row_cur, col_cur = current_cell
                self.visited.add((row_next, col_next))
                current_wall = 0
                if row_next > row_cur:
                    current_wall = Wall.SOUTH
                elif row_next < row_cur:
                    current_wall = Wall.NORTH
                elif col_next > col_cur:
                    current_wall = Wall.EAST
                elif col_next < col_cur:
                    current_wall = Wall.WEST
                self.grid.cells[row_cur][col_cur] &= ~current_wall
                self.grid.cells[row_next][col_next] &= ~current_wall.opposite()

                cells_deque.append((row_next, col_next))

    def find_neighbours(self,
                        cur_cell: Tuple[int, int]) -> List[Tuple[int, int]]:
        neighbours: List[Tuple[int, int]] = []
        left_neighbour = tuple([cur_cell[0], cur_cell[1] - 1])
        if (
            self.is_coord_in_boundry(left_neighbour)
            and left_neighbour not in self.visited
        ):
            neighbours.append(left_neighbour)

        right_neighbour = tuple([cur_cell[0], cur_cell[1] + 1])
        if (
            self.is_coord_in_boundry(right_neighbour)
            and right_neighbour not in self.visited
        ):
            neighbours.append(right_neighbour)

        up_neighbour = tuple([cur_cell[0] - 1, cur_cell[1]])
        if (
            self.is_coord_in_boundry(up_neighbour)
            and up_neighbour not in self.visited
        ):
            neighbours.append(up_neighbour)

        down_neighbour = tuple([cur_cell[0] + 1, cur_cell[1]])
        if (
            self.is_coord_in_boundry(down_neighbour)
            and down_neighbour not in self.visited
        ):
            neighbours.append(down_neighbour)
        return neighbours

    def is_coord_in_boundry(self, coords: Tuple[int, int]) -> bool:
        if (
            0 <= coords[0] < self.config.height
            and 0 <= coords[1] < self.config.width
        ):
            return True
        return False
