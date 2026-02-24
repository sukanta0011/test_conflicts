from .grid import Grid, Wall
from collections import deque
from typing import Tuple, List


class Solver():
    def find_path(self, grid: Grid, entry: Tuple[int, int], exit: Tuple[int, int]) -> str:
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
