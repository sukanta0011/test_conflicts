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
        self.grid_size = 30
        self.wall_thickness = 5
        self.bg_color = 0xFF000000
        self.wall_color = 0xFFFF0000
        self.color_42 = 0xFFFF00FF
        self.entry_color = 0xFF00FF00
        self.exit_color = 0xFFFF0000
        self.path_color = 0xFF50FFFF
        self.maze_visible = False
        self.path_visible = False

    @staticmethod
    def get_maze_size_in_pixels(rows: int, columns: int) -> Tuple:
        if rows <= 0 or columns <= 0:
            raise ValueError(
                "TO get maze size in pixels, please provide "
                f"positive rows ({rows}) and columns ({columns}).")
        const = MazeParams()
        w = rows * const.grid_size + const.wall_thickness
        # 100 pixels in is used for additional information
        h = columns * const.grid_size + const.wall_thickness + 100
        return (w, h)
