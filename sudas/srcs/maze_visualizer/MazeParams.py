from typing import Tuple


class MazeParams:
    """Configuration container for maze visual parameters and window dimensions.

    This class manages the visual state of the maze, including color palettes 
    (ARGB), grid dimensions, and calculated window offsets for rendering.

    Attributes:
        grid_size (int): The size of each square cell in pixels.
        wall_thickness (int): The thickness of the maze walls in pixels.
        bg_color (int): Background color in 0xAARRGGBB format.
        wall_color (int): Color used for maze boundaries.
        color_42 (int): The signature '42 Prague' purple/magenta color.
        entry_color (int): Color indicating the maze start point.
        exit_color (int): Color indicating the maze end point.
        path_color (int): Color used to render the solved path.
        maze_visible (bool): Toggle for rendering the maze structure.
        path_visible (bool): Toggle for rendering the solution path.
        win_w (int): Total width of the application window in pixels.
        win_h (int): Total height of the application window in pixels.
        w_offset (int): Horizontal padding to center the maze in the window.
    """
    def __init__(self) -> None:
        """Initializes default maze parameters and color schemes."""
        # colors are in hex color code, 00->0, FF -> 255
        # from left to right
        # 0x(FF)FFFFFF -> Transparency
        # 0xFF(FF)FFFF -> red
        # 0xFFFF(FF)FF -> green
        # 0xFFFFFF(FF) -> blue

        # Dimensions are in pixels
        self.grid_size = 10
        self.wall_thickness = 1
        self.bg_color = 0xFF000000
        self.wall_color = 0xFFFF0000
        self.color_42 = 0xFFFF00FF
        self.entry_color = 0xFF00FF00
        self.exit_color = 0xFFFF0000
        self.path_color = 0xFF008FFF
        self.maze_visible = False
        self.path_visible = False
        self.win_w = 500
        self.win_h = 50
        self.w_offset = 0
        self.txt_h = 50

    def initialize_maze(self, rows: int, columns: int) -> None:
        """Sets the window size and centers the maze based on grid dimensions.

        Updates `win_w`, `win_h`, and `w_offset` based on the provided 
        maze structure and the current `grid_size`.

        Args:
            rows (int): Number of horizontal cells.
            columns (int): Number of vertical cells.

        Raises:
            ValueError: If dimensions are non-positive.
        """
        if rows <= 0 or columns <= 0:
            raise ValueError(
                "TO get maze size in pixels, please provide "
                f"positive rows ({rows}) and columns ({columns}).")
        w = rows * self.grid_size + self.wall_thickness
        h = columns * self.grid_size + self.wall_thickness + self.txt_h
        if w > self.win_w:
            self.win_w = w
        else:
            self.w_offset = (self.win_w - w) // 2
        if h > self.win_h:
            self.win_h = h
