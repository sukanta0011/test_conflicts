from typing import Tuple


class MazeParams:
    def __init__(self) -> None:
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

    @staticmethod
    def get_maze_size_in_pixels(rows: int, columns: int) -> Tuple:
        if rows <= 0 or columns <= 0:
            raise ValueError(
                "TO get maze size in pixels, please provide "
                f"positive rows ({rows}) and columns ({columns}).")
        const = MazeParams()
        w = rows * const.grid_size + const.wall_thickness
        # 100 pixels in is used for additional information
        h = columns * const.grid_size + const.wall_thickness + 50
        return (w, h)

    def initialize_maze(self, rows: int, columns: int) -> None:
        if rows <= 0 or columns <= 0:
            raise ValueError(
                "TO get maze size in pixels, please provide "
                f"positive rows ({rows}) and columns ({columns}).")
        w = rows * self.grid_size + self.wall_thickness
        h = columns * self.grid_size + self.wall_thickness + 50
        if w > self.win_w:
            self.win_w = w
        else:
            self.w_offset = (self.win_w - w) // 2
        if h > self.win_h:
            self.win_h = h

