from typing import List, Tuple
from enum import IntEnum


class Grid:
    """
    Represents the internal maze grid.

    Each cell contains an integer encoding its wall configuration
    using 4 bits:

        Bit 0  -> North wall
        Bit 1  -> East wall
        Bit 2  -> South wall
        Bit 3  -> West wall

    A bit value of 1 means the wall is CLOSED.
    A bit value of 0 means the wall is OPEN.

    During initialization, cells are set to 15.
    The value 15 indicates that the cell has four closed doors (1111).
    """
    # 2D matrix of cells: cells[row][col]
    cells: List[List[int]]

    def __init__(self, width: int, height: int):
        """
        Initialize an empty grid of given width and height.

        :param width: Number of columns
        :param height: Number of rows
        """
        self.width = width
        self.height = height
        # Initialize all cells to 15
        self.cells = [[15 for _ in range(width)] for _ in range(height)]
        # Store grid center coordinates (row, column)
        # Useful for positioning the "42" pattern
        self.center = tuple([height // 2, width // 2])
        # Total number of cells in the grid
        self.cells_count = width * height

    def reset_cells(self):
        self.cells = [
            [15 for _ in range(self.width)] for _ in range(self.height)]

    def find_neighbours(self,
                        cur_cell: Tuple[int, int]) -> List[Tuple[int, int]]:
        neighbours: List[Tuple[int, int]] = []
        left_neighbour = tuple([cur_cell[0], cur_cell[1] - 1])
        if (
            self.is_coord_in_boundry(left_neighbour)
        ):
            neighbours.append(left_neighbour)

        right_neighbour = tuple([cur_cell[0], cur_cell[1] + 1])
        if (
            self.is_coord_in_boundry(right_neighbour)
        ):
            neighbours.append(right_neighbour)

        up_neighbour = tuple([cur_cell[0] - 1, cur_cell[1]])
        if (
            self.is_coord_in_boundry(up_neighbour)
        ):
            neighbours.append(up_neighbour)

        down_neighbour = tuple([cur_cell[0] + 1, cur_cell[1]])
        if (
            self.is_coord_in_boundry(down_neighbour)
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

    def __str__(self) -> str:
        """
        Return a readable string representation of the grid.
        Mainly used for debugging purposes.
        """
        return "\n".join([str(row) for row in self.cells])

    def print_hex_format(self) -> None:
        """
        Debug helper. Prints the grid in hexadecimal format
        """
        for row in self.cells:
            print([hex(cell).removeprefix("0x").upper()
                   for cell in row])


class Wall(IntEnum):
    """
    Represents the four walls of a grid cell.

    Each wall is encoded as a power of two so it can be used
    as a bit flag inside a single integer (0-15).

    Bit representation:
        NORTH = 0001
        EAST  = 0010
        SOUTH = 0100
        WEST  = 1000

    This design allows efficient wall manipulation using
    bitwise operations (&, |, ~).
    """
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def opposite(self) -> "Wall":
        """
        Return the opposite wall.

        Useful when removing a wall between two adjacent cells.
        Example:
            If you open the EAST wall of the current cell,
            you must also open the WEST wall of the neighboring cell.
        """
        return {
            Wall.NORTH: Wall.SOUTH,
            Wall.SOUTH: Wall.NORTH,
            Wall.EAST: Wall.WEST,
            Wall.WEST: Wall.EAST}[self]
