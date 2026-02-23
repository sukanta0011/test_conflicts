from typing import List
import random
from abc import ABC, abstractmethod
from srcs.mlx_tools.BaseMLX import MyMLX, MlxVar
from srcs.mlx_tools.ShapeMaker import ShapeGenerator
from srcs.maze_visualizer.MazeParams import MazeParams
from srcs.mlx_tools.ImageOperations import (
    TxtToImage, ImageScaler, TxtColorChanger)
from srcs.mlx_tools.LetterToImageMapper import LetterToImageMapper
from srcs.maze_generator.maze_generator import MazeGenerator
from srcs.maze_generator.solver import Solver


class MazeVisualizer(MyMLX, ABC):
    """Abstract base class for orchestrating maze rendering and user interaction.

    This class integrates the MLX engine with maze generation and solving logic. 
    It manages character mapping for UI text, handles keyboard events for 
    real-time maze updates, and defines the structural requirements for 
    displaying mazes and paths.

    Attributes:
        const (MazeParams): Configuration constants for colors and dimensions.
        generator (MazeGenerator): The engine responsible for maze structure.
        solver (Solver): The algorithm used to find the path through the maze.
        cells (List[List[int]]): The current grid state of the maze.
        txt_to_image (TxtToImage): Pipeline for rendering styled UI text.
    """
    def __init__(self, name: str, w: int, h: int,
                 const: MazeParams, generator: MazeGenerator,
                 path: str, solver: Solver):
        """Initializes the visualizer and sets up the graphical environment."""
        super().__init__(name, w, h)
        self.const = const
        self.generator = generator
        self.solver = solver
        self.entry = self.generator.config.entry
        self.exit = self.generator.config.exit
        self.path = path
        self.cells = self.generator.grid.cells
        self.init_letter_map()

    def init_letter_map(self) -> None:
        """Initializes the font system and configures the text processing pipeline.

        Loads the alphabet sprite sheet and adds scaling and coloring stages 
        to the text rendering engine.
        """
        letter_to_img_map = LetterToImageMapper(self.mlx)
        letter_to_img_map.create_map()

        self.txt_to_image = TxtToImage(
            self.mlx.base_letter_map,
            self.mlx.extended_letter_map)
        self.txt_to_image.add_stages(ImageScaler())
        self.txt_to_image.add_stages(TxtColorChanger())

    def mykey(self, key_num: int, mlx_var: MlxVar) -> None:
        """Handles keyboard input to trigger maze actions.

        Mapped Actions:
            - '1': Regenerate maze and solve path.
            - '2': Toggle path visibility.
            - '3': Randomize wall colors.
            - '4': Terminate application.

        Args:
            key_num: The integer code of the pressed key.
            mlx_var: The current MLX state.
        """
        if key_num == 49 or key_num == 65436:  # 1
            self.set_background(self.mlx.buff_img, (0, 0),
                                self.w, self.h, 0xFF000000)
            grid = self.generator.algorithm.generate()
            new_path = self.solver.find_path(grid, self.generator.config)
            self.cells = grid.cells
            self.display_maze(grid.cells, self.const.wall_color)
            self.show_path(self.path, self.const.bg_color)
            self.path = new_path
            if self.const.path_visible:
                self.show_path(self.path, self.const.path_color)
            self.show_user_interaction_options()
            self.put_buffer_image()
        if key_num == 50 or key_num == 65433:  # 2
            if self.const.path_visible:
                self.show_path(self.path, self.const.bg_color)
                self.put_buffer_image()
                self.const.path_visible = False
            else:
                self.show_path(self.path, self.const.path_color)
                self.put_buffer_image()
        if key_num == 51 or key_num == 65435:  # 3
            color_list = [i for i in range(256)]
            r = random.choice(color_list)
            g = random.choice(color_list)
            b = random.choice(color_list)
            # print(r, g, b)
            # self.display_maze(self.maze, 0xFF000000)
            self.display_maze(self.cells,
                              self.rgb_to_hex(r, g, b))
            self.put_buffer_image()
        if key_num == 52 or key_num == 65430:  # 4
            self.stop_mlx(self.mlx)

    @abstractmethod
    def display_maze(self, maze: List[List[int]],
                     color: int = 0xFFFFFFFF) -> None:
        """Abstract method to render the maze grid. Must be implemented by subclasses.

        Args:
            maze: The 2D grid representation of the maze.
            color: The color to use for the maze walls.
        """
        pass

    @abstractmethod
    def show_path(self, path: str, color: int = 0xFF00000) -> None:
        """Abstract method to render the solution path. Must be implemented by subclasses.

        Args:
            path: String representation or coordinate list of the path.
            color: The color to use for the path line/cells.
        """
        pass

    def show_user_interaction_options(self) -> None:
        """Renders the UI legend/menu at the bottom of the maze window.

        Calculates dynamic positioning to center the interaction instructions 
        based on the window width and maze height.
        """
        pos_x = (self.const.win_w - 430) // 2  # Text required appox 475pix
        pos_y = len(self.generator.grid.cells) * self.const.grid_size + 25
        texts = ["1: regan, ", "2: path, ", "3: color, ", "4: quit"]
        for txt in texts:
            pos_x = self.txt_to_image.print_txt(
                self.mlx, self.mlx.buff_img, txt, (pos_x, pos_y), 0.5)


class MazeVisualizerOne(MazeVisualizer):
    """Specific implementation of a maze visualizer using bitmask-based wall logic.

    This class interprets integers in a 2D grid as bitmasks representing walls 
    in four directions (North, East, South, West) and renders them as a 
    series of rectangles.

    Wall Bitmask Rule:
        0: North, 1: East, 2: South, 3: West
        Bit value 1 indicates a closed wall, 0 indicates an open passage.
    """
    def display_maze(self, maze: List[List[int]],
                     color: int = 0xFFFFFFFF) -> None:
        """Renders the maze structure by iterating through cell bitmasks.

        Calculates wall positions based on grid spacing and draws rectangles 
        for each active bit. Includes a special check for the '42' center 
        fill logic.

        Args:
            maze: 2D list of integers representing the wall bitmasks.
            color: Hexadecimal color for the walls.

        Maze rule:
        0:N, 1:E, 2:S, 3:W
        0 -> open, 1 -> closed
            N
        W       E
            S
        """
        maze_w, maze_h = len(maze[0]), len(maze)
        spacing = self.const.grid_size
        offset = self.const.w_offset

        wall = self.const.wall_thickness
        bits = [0, 3, 1, 2]
        for y in range(maze_h):
            for bit in bits:
                for x in range(maze_w):
                    val = maze[y][x]
                    top_x, top_y, h, w = 0, 0, 0, 0
                    if bit == 0:
                        top_x = x * spacing + offset
                        top_y = y * spacing
                        h = wall
                        w = spacing + wall
                    elif bit == 3:
                        top_x = x * spacing + offset
                        top_y = y * spacing
                        h = spacing
                        w = wall
                        if (val >> 0) & 1 and (val >> 1) & 1 and\
                           (val >> 2) & 1 and (val >> 3) & 1:
                            ShapeGenerator.draw_filled_rectangle(
                                    self.mlx, self.mlx.buff_img,
                                    (top_x, top_y + wall),
                                    spacing - wall, spacing,
                                    self.const.color_42
                                )
                    # there is some problem when x = maze_w - 1
                    elif bit == 1:
                        top_x = (x + 1) * spacing + offset
                        top_y = y * spacing
                        h = spacing
                        w = wall
                    elif bit == 2 and y == maze_h - 1:
                        top_x = x * spacing + offset
                        top_y = (y + 1) * spacing
                        h = wall
                        w = spacing + wall

                    if (val >> bit) & 1:
                        ShapeGenerator.draw_filled_rectangle(
                            self.mlx, self.mlx.buff_img, (top_x, top_y),
                            h, w, color
                        )
        self.draw_start_stop()
        self.const.maze_visible = True

    def draw_start_stop(self) -> None:
        """Highlights the entry and exit points of the maze.

        Draws filled rectangles using colors defined in the configuration 
        constants for the start (entry) and end (exit) coordinates.
        """
        ShapeGenerator.draw_filled_rectangle(
                self.mlx, self.mlx.buff_img,
                (self.entry[1] * self.const.grid_size + self.const.w_offset +
                 self.const.wall_thickness,
                 self.entry[0] * self.const.grid_size +
                 self.const.wall_thickness),
                self.const.grid_size - self.const.wall_thickness,
                self.const.grid_size - self.const.wall_thickness,
                self.const.entry_color
            )
        ShapeGenerator.draw_filled_rectangle(
                self.mlx, self.mlx.buff_img,
                (self.exit[1] * self.const.grid_size + self.const.w_offset +
                 self.const.wall_thickness,
                 self.exit[0] * self.const.grid_size +
                 self.const.wall_thickness),
                self.const.grid_size - self.const.wall_thickness,
                self.const.grid_size - self.const.wall_thickness,
                self.const.exit_color
            )

    def show_path(self, path: str, color: int = 0xFF00000) -> None:
        """Renders the solution path string as a series of connected rectangles.

        Args:
            path: A string of characters ('N', 'S', 'E', 'W') representing 
                the movement from the start point.
            color: Hexadecimal color for the path visualization.
        """
        if self.const.maze_visible:
            pos_x = self.entry[0] * self.const.grid_size + self.const.w_offset
            pos_y = self.entry[1] * self.const.grid_size
            for idx, direction in enumerate(path):
                h = self.const.grid_size - self.const.wall_thickness
                w = self.const.grid_size - self.const.wall_thickness
                offset_x = self.const.wall_thickness
                offset_y = self.const.wall_thickness
                if direction == "E":
                    pos_x += self.const.grid_size
                if direction == "W":
                    pos_x -= self.const.grid_size
                if direction == "N":
                    pos_y -= self.const.grid_size
                if direction == "S":
                    pos_y += self.const.grid_size

                if (self.const.w_offset <= pos_x + offset_x
                    <= self.const.win_w - self.const.w_offset) and\
                    (0 <= pos_y + offset_y
                        <= self.const.win_h - self.const.txt_h):
                    ShapeGenerator.draw_filled_rectangle(
                            self.mlx, self.mlx.buff_img,
                            (pos_x + offset_x, pos_y + offset_y),
                            h, w, color
                        )
                else:
                    print("Cannot draw outside the maze")

            self.draw_start_stop()
            self.const.path_visible = True
        else:
            print("Please generate the maze first")


# def maze_tester():
#     path = "SWSESWSESWSSSEESEEENEESESEESSSEEESSSEEENNENEE"
#     from srcs.maze_generator.a_maze_ing import ma
#     generator = main()
#     # path = "SES"
#     data = generator.grid.cells
#     # print(data)
#     config: Configuration = generator.config
#     # print(config.entry)
#     try:
#         # w, h = MazeParams.get_maze_size_in_pixels(len(data[0]), len(data))
#         # print(len(data[0]), len(data))
#         maze_params = MazeParams()
#         maze_params.initialize_maze(len(data[0]), len(data))
#         # print(maze_params.win_w, maze_params.win_h)
#         visualizer = MazeVisualizerOne("A-Maze-Ing", maze_params.win_w,
#                                        maze_params.win_h, config.entry,
#                                        config.exit, maze_params, data, path)
#         visualizer.set_background(visualizer.mlx.buff_img,
#                                   (0, 0), visualizer.mlx.buff_img.w,
#                                   visualizer.mlx.buff_img.w, 0xFF000000)
#         letter_to_img_map = LetterToImageMapper(visualizer.mlx)
#         letter_to_img_map.create_map()

#         txt_to_image = TxtToImage(
#             visualizer.mlx.base_letter_map,
#             visualizer.mlx.extended_letter_map)
#         txt_to_image.add_stages(ImageScaler())
#         txt_to_image.add_stages(TxtColorChanger())
#         visualizer.display_maze(data, visualizer.const.wall_color)
#         visualizer.show_path(path, visualizer.const.path_color)
#         visualizer.show_user_interaction_options(txt_to_image)
#         visualizer.put_buffer_image()
#         visualizer.start_mlx()
#     except Exception as e:
#         print(e)


if __name__ == "__main__":
    pass
    # maze_tester()
