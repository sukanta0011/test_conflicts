from typing import List
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

    def reset_cells(self) -> None:
        """
        Reset all grid cells to their default value.

        Reinitializes the internal 2D grid structure so that every cell
        is set to 15 (0xF in hexadecimal), which represents a fully
        closed cell with all walls present.

        This method is typically used before generating or regenerating
        a maze to ensure a clean initial state.
        """
        self.cells = [
            [15 for _ in range(self.width)] for _ in range(self.height)]

    def __str__(self) -> str:
        """
        Return a readable string representation of the grid.
        Mainly used for debugging purposes.
        """
        return "\n".join([str(row) for row in self.cells])


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
