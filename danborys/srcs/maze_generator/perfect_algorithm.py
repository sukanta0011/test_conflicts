from .abc_algorithm import Algorithm
from .grid import Grid, Wall
from typing import Tuple, List, Set, Deque
import random
from collections import deque


class PerfectAlgorithm(Algorithm):
    """
    Depth-First Search (DFS) based maze generation algorithm.

    This implementation generates a perfect maze by default
    (i.e., exactly one unique path between any two cells).
    When `perfect` is False, additional walls may be removed
    to introduce cycles and create multiple possible paths.

    The algorithm also reserves special cells used to represent
    the number "42" in the center of sufficiently large mazes.
    """
    def generate(self) -> Grid:
        """
        Generate the maze grid.

        Steps:
            1. Reset all grid cells to their initial state.
            2. Apply random seed (if provided).
            3. Reserve special "42" cells if possible.
            4. Generate a perfect maze using DFS backtracking.
            5. Optionally remove additional walls if
               non-perfect mode is enabled.

        Returns:
            Grid: The generated maze grid.
        """
        self.grid.reset_cells()
        if self.seed:
            random.seed(self.seed)
        self.visited: Set[Tuple[int, int]] = set()
        cells_42 = self.get_42_cells()
        if isinstance(cells_42, str):
            print(cells_42)
            self.carve_maze_from(self.entry)
        else:
            self.visited.update(cells_42)
            self.carve_maze_from(self.entry)
        if not self.perfect:
            self.visited = set()
            if not isinstance(cells_42, str):
                self.visited.update(cells_42)
            for r in range(self.grid.height):
                for c in range(self.grid.width):
                    if (r, c) not in self.visited and random.random() > 0.5:
                        unknown_neighbours = self.get_unknown_neighbour((r, c))
                        self.open_wall(unknown_neighbours, (r, c))
            for r in range(self.grid.height):
                for c in range(self.grid.width):
                    if self.grid.cells[r][c] == 0 and\
                        self.grid.cells[r - 1][c - 1] >> 1 & 0 and\
                            self.grid.cells[r - 1][c - 1] >> 2 & 0:
                        self.grid.cells[r][c] = 9
                        self.grid.cells[r - 1][c] |= Wall.SOUTH
                        self.grid.cells[r][c - 1] |= Wall.EAST
        return self.grid

    def carve_maze_from(self, first_cell: Tuple[int, int]) -> None:
        """
        Generate maze paths using iterative DFS with backtracking.

        This method:
            - Starts from the given cell.
            - Randomly explores unvisited neighbouring cells.
            - Removes walls between adjacent cells.
            - Uses a stack (deque) to backtrack when needed.

        Args:
            first_cell (Tuple[int, int]): Starting cell coordinates.
        """
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
                current_wall: Wall = Wall.SOUTH
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
        """
        Return all unvisited neighbouring cells.

        Only neighbours that:
            - Are within grid boundaries.
            - Have not been visited.

        Args:
            cur_cell (Tuple[int, int]): Current cell coordinates.

        Returns:
            List[Tuple[int, int]]: List of valid neighbouring cells.
        """
        neighbours: List[Tuple[int, int]] = []
        left_neighbour = (cur_cell[0], cur_cell[1] - 1)
        if (
            self.is_coord_in_boundry(left_neighbour)
            and left_neighbour not in self.visited
        ):
            neighbours.append(left_neighbour)

        right_neighbour = (cur_cell[0], cur_cell[1] + 1)
        if (
            self.is_coord_in_boundry(right_neighbour)
            and right_neighbour not in self.visited
        ):
            neighbours.append(right_neighbour)

        up_neighbour = (cur_cell[0] - 1, cur_cell[1])
        if (
            self.is_coord_in_boundry(up_neighbour)
            and up_neighbour not in self.visited
        ):
            neighbours.append(up_neighbour)

        down_neighbour = (cur_cell[0] + 1, cur_cell[1])
        if (
            self.is_coord_in_boundry(down_neighbour)
            and down_neighbour not in self.visited
        ):
            neighbours.append(down_neighbour)
        return neighbours

    def is_coord_in_boundry(self, coords: Tuple[int, int]) -> bool:
        """
        Check whether given coordinates are inside the maze boundaries.

        Args:
            coords (Tuple[int, int]): Cell coordinates (row, col).

        Returns:
            bool: True if coordinates are inside the grid,
            otherwise False.
        """
        if (
            0 <= coords[0] < self.height
            and 0 <= coords[1] < self.width
        ):
            return True
        return False

    def open_wall(self, neighbour: List[Tuple[int, int]],
                  cur_cell: Tuple[int, int]) -> None:
        """
        Remove a wall between the current cell and a random neighbour.

        This method is used when generating non-perfect mazes
        to introduce additional openings between cells.

        Args:
            neighbour (List[Tuple[int, int]]):
                List of candidate neighbouring cells.
            cur_cell (Tuple[int, int]):
                Current cell coordinates.
        """
        if len(neighbour) > 0:
            random.shuffle(neighbour)
            row_next, col_next = neighbour[0]
            row_cur, col_cur = cur_cell
            self.visited.add((row_next, col_next))
            current_wall: Wall = Wall.SOUTH
            if row_next > row_cur:
                current_wall = Wall.SOUTH
            elif row_next < row_cur:
                current_wall = Wall.NORTH
            elif col_next > col_cur:
                current_wall = Wall.EAST
            elif col_next < col_cur:
                current_wall = Wall.WEST
            self.grid.cells[row_cur][col_cur] &= ~current_wall
            self.grid.cells[row_next][col_next] &=\
                ~current_wall.opposite()

    def get_unknown_neighbour(
            self, cur_cell: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Return neighbouring cells separated by intact walls.

        This method:
            - Inspects wall bit flags of the current cell.
            - Detects neighbours where a wall still exists.
            - Filters neighbours that are within boundaries
              and not yet visited.

        Args:
            cur_cell (Tuple[int, int]): Current cell coordinates.

        Returns:
            List[Tuple[int, int]]: List of neighbouring cells
            that are still separated by a wall.
        """
        unknown_neighbours: List[Tuple[int, int]] = []
        curr_val = self.grid.cells[cur_cell[0]][cur_cell[1]]
        if curr_val >> 0 & 1:
            neighbour_pos = (cur_cell[0] - 1, cur_cell[1])
            if (self.is_coord_in_boundry(neighbour_pos) and
               neighbour_pos not in self.visited):
                unknown_neighbours.append(neighbour_pos)
        if curr_val >> 1 & 1:
            neighbour_pos = (cur_cell[0], cur_cell[1] + 1)
            if (self.is_coord_in_boundry(neighbour_pos) and
               neighbour_pos not in self.visited):
                unknown_neighbours.append(neighbour_pos)
        if curr_val >> 2 & 1:
            neighbour_pos = (cur_cell[0] + 1, cur_cell[1])
            if (self.is_coord_in_boundry(neighbour_pos) and
               neighbour_pos not in self.visited):
                unknown_neighbours.append(neighbour_pos)
        if curr_val >> 3 & 1:
            neighbour_pos = (cur_cell[0], cur_cell[1] - 1)
            if (self.is_coord_in_boundry(neighbour_pos) and
               neighbour_pos not in self.visited):
                unknown_neighbours.append(neighbour_pos)

        return unknown_neighbours
