from typing import List, Tuple
import random
from abc import ABC, abstractmethod
from mlx import Mlx
from srcs.mlx_tools.BaseMLX import MyMLX
from srcs.mlx_tools.ShapeMaker import ShapeGenerator
from srcs.maze_visualizer.MazeParams import MazeParams
from srcs.mlx_tools.ImageOperations import (
    TxtToImage, ImageScaler, TxtColorChanger)
from srcs.mlx_tools.LetterToImageMapper import LetterToImageMapper
from srcs.maze_generator.maze_generator import MazeGenerator
from srcs.maze_generator.solver import Solver


class MazeVisualizer(MyMLX, ABC):
    def __init__(self, name: str, w: int, h: int,
                 const: MazeParams, generator: MazeGenerator,
                 path: str, solver: Solver,):
        super().__init__(name, w, h)
        self.const = const
        self.generator = generator
        self.solver = solver
        self.entry = self.generator.config.entry
        self.exit = self.generator.config.exit
        self.path = path
        self.cells = self.generator.grid.cells
        self.init_letter_map()

    def init_letter_map(self):
        letter_to_img_map = LetterToImageMapper(self.mlx)
        letter_to_img_map.create_map()

        self.txt_to_image = TxtToImage(
            self.mlx.base_letter_map,
            self.mlx.extended_letter_map)
        self.txt_to_image.add_stages(ImageScaler())
        self.txt_to_image.add_stages(TxtColorChanger())

    def mykey(self, key_num, mlx_var):
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
    def display_maze(self, maze: List[List[int]], color=0xFFFFFFFF) -> None:
        pass

    @abstractmethod
    def show_path(self, path: str, color=0xFF00000) -> None:
        pass

    def show_user_interaction_options(self):
        pos_x = (self.const.win_w - 430) // 2  # Text required appox 475pix
        pos_y = len(self.generator.grid.cells) * self.const.grid_size + 25
        texts = ["1: regan, ", "2: path, ", "3: color, ", "4: quit"]
        for txt in texts:
            pos_x = self.txt_to_image.print_txt(
                self.mlx, self.mlx.buff_img, txt, (pos_x, pos_y), 0.5)


class MazeVisualizerOne(MazeVisualizer):
    def display_maze(self, maze: List[List[int]], color=0xFFFFFFFF) -> None:
        """
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

    def draw_start_stop(self):
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

    def show_path(self, path: str, color=0xFF00000) -> None:
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
                    # offset_y += self.const.wall_thickness
                    # w += self.const.wall_thickness
                if direction == "W":
                    pos_x -= self.const.grid_size
                    # offset_y += self.const.wall_thickness
                    # w += self.const.wall_thickness

                if direction == "N":
                    pos_y -= self.const.grid_size
                    # offset_x += self.const.wall_thickness
                if direction == "S":
                    pos_y += self.const.grid_size
                    # offset_x += self.const.wall_thickness

                try:
                    ShapeGenerator.draw_filled_rectangle(
                            self.mlx, self.mlx.buff_img,
                            (pos_x + offset_x, pos_y + offset_y),
                            h, w, color
                        )
                except Exception:
                    pass
            self.draw_start_stop()
            self.const.path_visible = True
        else:
            print("Please generate the maze first")

    def calculate_h_w(self, current_dir: str, next_dir: str) -> Tuple[int, int]:
        pass


def maze_tester():
    path = "SWSESWSESWSSSEESEEENEESESEESSSEEESSSEEENNENEE"
    from srcs.maze_generator.a_maze_ing import ma
    generator = main()
    # path = "SES"
    data = generator.grid.cells
    # print(data)
    config: Configuration = generator.config
    # print(config.entry)
    try:
        # w, h = MazeParams.get_maze_size_in_pixels(len(data[0]), len(data))
        # print(len(data[0]), len(data))
        maze_params = MazeParams()
        maze_params.initialize_maze(len(data[0]), len(data))
        # print(maze_params.win_w, maze_params.win_h)
        visualizer = MazeVisualizerOne("A-Maze-Ing", maze_params.win_w,
                                       maze_params.win_h, config.entry,
                                       config.exit, maze_params, data, path)
        visualizer.set_background(visualizer.mlx.buff_img,
                                  (0, 0), visualizer.mlx.buff_img.w,
                                  visualizer.mlx.buff_img.w, 0xFF000000)
        letter_to_img_map = LetterToImageMapper(visualizer.mlx)
        letter_to_img_map.create_map()

        txt_to_image = TxtToImage(
            visualizer.mlx.base_letter_map,
            visualizer.mlx.extended_letter_map)
        txt_to_image.add_stages(ImageScaler())
        txt_to_image.add_stages(TxtColorChanger())
        visualizer.display_maze(data, visualizer.const.wall_color)
        visualizer.show_path(path, visualizer.const.path_color)
        visualizer.show_user_interaction_options(txt_to_image)
        visualizer.put_buffer_image()
        visualizer.start_mlx()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    maze_tester()
