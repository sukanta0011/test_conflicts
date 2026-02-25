from .grid import Grid, Wall
from collections import deque
from typing import Tuple, List


class Solver():
    """
    Breadth-First Search (BFS) maze solver.

    This class is responsible for computing the shortest path
    between two cells in a maze grid.

    The solver interprets wall bit flags to determine accessible
    neighbouring cells and returns the path as a string of
    directions:
        - 'N' (North)
        - 'E' (East)
        - 'S' (South)
        - 'W' (West)
    """
    def find_path(self, grid: Grid, entry: Tuple[int, int],
                  exit: Tuple[int, int]) -> str:
        """
        Compute the shortest path from entry to exit using BFS.

        This method:
            - Explores the maze level by level.
            - Tracks visited cells to avoid revisiting.
            - Accumulates movement directions while traversing.
            - Stops as soon as the exit cell is reached.

        Args:
            grid (Grid): The maze grid containing wall information.
            entry (Tuple[int, int]): Starting cell coordinates.
            exit (Tuple[int, int]): Target cell coordinates.

        Returns:
            str: Shortest path as a sequence of directions
            ('N', 'E', 'S', 'W').
            Returns an empty string if no path exists.
        """
        self.grid = grid
        start = entry
        end = exit
        queue = deque([(start, "")])
        visited = set()
        visited.add(start)
        while queue:
            current, cur_path = queue.popleft()
            if current == end:
                return cur_path
            neighbours = self.find_neighbours(current)
            for neighbour, next_path in neighbours:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append((neighbour, cur_path + next_path))
        return ""

    def find_neighbours(self,
                        current_cell: Tuple[int, int]) -> List[
                            Tuple[Tuple[int, int], str]]:
        """
        Return accessible neighbouring cells from the current cell.

        A neighbour is considered accessible if the corresponding
        wall bit flag is not set (i.e., the wall is open).

        Each returned neighbour includes:
            - The neighbour's coordinates.
            - The direction required to reach it.

        Args:
            current_cell (Tuple[int, int]):
                Current cell coordinates.

        Returns:
            List[Tuple[Tuple[int, int], str]]:
                List of reachable neighbours paired with their
                movement direction.
        """
        cur_row, cur_col = current_cell
        neighbours = []
        for wall in Wall:
            if self.grid.cells[cur_row][cur_col] & wall.value == 0:
                if wall is Wall.EAST:
                    neighbours.append(((cur_row, cur_col + 1), "E"))
                elif wall is Wall.WEST:
                    neighbours.append(((cur_row, cur_col - 1), "W"))
                elif wall is Wall.NORTH:
                    neighbours.append(((cur_row - 1, cur_col), "N"))
                elif wall is Wall.SOUTH:
                    neighbours.append(((cur_row + 1, cur_col), "S"))
        return neighbours
