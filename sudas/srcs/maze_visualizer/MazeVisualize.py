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


class MazeVisualizer(MyMLX, ABC):
    def __init__(self, name: str, w: int, h: int, 
                 start: Tuple, end: Tuple,
                 maze: List[List[int]], path: str):
        super().__init__(name, w, h)
        self.const = MazeParams()
        self.start = start
        self.end = end
        self.maze = maze
        self.path = path

    def mykey(self, key_num, mlx_var):
        if key_num == 49 or key_num == 65436:  # 1
            pass
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
            self.display_maze(self.maze, self.rgb_to_hex(r, g, b))
            self.put_buffer_image()
        if key_num == 52 or key_num == 65430:  # 4
            self.stop_mlx(self.mlx)

    @abstractmethod
    def display_maze(self, maze: List[List[int]], color=0xFFFFFFFF) -> None:
        pass

    @abstractmethod
    def show_path(self, path: str, color=0xFF00000) -> None:
        pass

    def show_user_interaction_options(self, txt_to_img: TxtToImage):
        pos_x = 10
        pos_y = len(self.maze) * self.const.grid_size + 50
        width = 0
        txts = ["1: regan, ", "2: path, ", "3: color, ", "4: quit"]
        for txt in txts:
            width = txt_to_img.print_txt(
                self.mlx, self.mlx.buff_img, txt, (pos_x + width, pos_y), 0.7)


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

        wall = self.const.wall_thickness
        bits = [0, 3, 1, 2]
        for y in range(maze_h):
            for bit in bits:
                for x in range(maze_w):
                    val = maze[y][x]
                    if bit == 0:
                        top_x = x * spacing
                        top_y = y * spacing
                        h = wall
                        w = spacing + wall
                    elif bit == 3:
                        top_x = x * spacing
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
                        top_x = (x + 1) * spacing
                        top_y = y * spacing
                        h = spacing
                        w = wall
                    elif bit == 2 and y == maze_h - 1:
                        top_x = x * spacing
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
                (self.start[0] * self.const.grid_size +
                 self.const.wall_thickness,
                 self.start[1] * self.const.grid_size +
                 self.const.wall_thickness),
                self.const.grid_size - self.const.wall_thickness,
                self.const.grid_size - self.const.wall_thickness,
                self.const.entry_color
            )
        ShapeGenerator.draw_filled_rectangle(
                self.mlx, self.mlx.buff_img,
                (self.end[0] * self.const.grid_size +
                 self.const.wall_thickness,
                 self.end[1] * self.const.grid_size +
                 self.const.wall_thickness),
                self.const.grid_size - self.const.wall_thickness,
                self.const.grid_size - self.const.wall_thickness,
                self.const.exit_color
            )

    def show_path(self, path: str, color=0xFF00000) -> None:
        if self.const.maze_visible:
            pos_x = self.start[0] * self.const.grid_size
            pos_y = self.start[1] * self.const.grid_size
            for direction in path:
                if direction == "E":
                    pos_x += self.const.grid_size
                if direction == "W":
                    pos_x -= self.const.grid_size
                if direction == "N":
                    pos_y -= self.const.grid_size
                if direction == "S":
                    pos_y += self.const.grid_size
                ShapeGenerator.draw_filled_rectangle(
                        self.mlx, self.mlx.buff_img,
                        (pos_x + self.const.wall_thickness,
                         pos_y + self.const.wall_thickness),
                        self.const.grid_size - self.const.wall_thickness,
                        self.const.grid_size - self.const.wall_thickness,
                        color
                    )
            self.draw_start_stop()
            self.const.path_visible = True
        else:
            print("Please generate the maze first")


def maze_tester():
    data = [
        [9, 5, 1, 5, 3, 9, 1, 5, 3, 9, 5, 5, 1, 7, 9, 5, 1, 5, 1, 1, 5, 1, 1, 5, 3],   # Row  0
        [14, 11, 10, 11, 10, 14, 8, 1, 2, 8, 5, 3, 12, 1, 4, 1, 2, 11, 10, 8, 1, 2, 8, 1, 2],  # Row  1
        [9, 6, 10, 8, 4, 1, 6, 10, 8, 4, 5, 4, 5, 4, 1, 2, 10, 12, 4, 2, 8, 2, 12, 2, 10],     # Row  2
        [12, 3, 10, 8, 3, 8, 1, 6, 10, 9, 3, 9, 5, 3, 8, 4, 4, 5, 3, 10, 8, 2, 13, 0, 2],      # Row  3
        [9, 6, 8, 4, 2, 10, 8, 5, 2, 10, 12, 0, 7, 10, 10, 13, 1, 3, 10, 8, 2, 8, 3, 12, 2],   # Row  4
        [12, 1, 2, 9, 6, 12, 4, 3, 10, 10, 11, 8, 3, 10, 10, 9, 2, 10, 10, 8, 6, 8, 6, 11, 10],# Row  5
        [9, 2, 14, 8, 5, 3, 9, 6, 8, 4, 2, 8, 4, 4, 4, 6, 8, 2, 10, 12, 1, 2, 9, 0, 2],        # Row  6
        [10, 12, 3, 8, 1, 4, 4, 5, 2, 15, 10, 8, 3, 15, 15, 15, 8, 2, 12, 5, 2, 12, 4, 2, 10], # Row  7
        [8, 5, 6, 8, 4, 1, 1, 7, 10, 15, 12, 6, 8, 5, 7, 15, 10, 12, 1, 3, 8, 3, 13, 0, 6],    # Row  8
        [12, 5, 3, 10, 13, 0, 4, 3, 10, 15, 15, 15, 10, 15, 15, 15, 8, 5, 6, 10, 10, 8, 1, 4, 3], # Row  9
        [9, 1, 4, 4, 1, 2, 9, 4, 2, 9, 7, 15, 10, 15, 13, 5, 0, 1, 1, 4, 2, 12, 6, 11, 10],    # Row 10
        [10, 10, 9, 1, 2, 10, 12, 3, 8, 4, 3, 15, 10, 15, 15, 15, 8, 2, 8, 5, 6, 13, 5, 2, 10],# Row 11
        [8, 4, 2, 10, 8, 6, 9, 2, 10, 9, 2, 11, 8, 5, 1, 7, 12, 4, 4, 5, 1, 5, 5, 2, 10],      # Row 12
        [8, 1, 6, 10, 12, 3, 8, 4, 4, 6, 8, 2, 8, 5, 2, 9, 3, 9, 1, 7, 10, 9, 5, 4, 2],        # Row 13
        [12, 4, 1, 6, 9, 2, 8, 5, 1, 3, 12, 4, 4, 3, 10, 8, 2, 8, 4, 5, 6, 12, 3, 11, 10],     # Row 14
        [9, 1, 4, 1, 6, 10, 10, 9, 2, 12, 3, 9, 3, 10, 8, 2, 8, 0, 1, 5, 5, 3, 10, 10, 10],    # Row 15
        [10, 8, 1, 2, 9, 2, 10, 10, 8, 1, 4, 6, 8, 2, 12, 6, 10, 8, 6, 9, 3, 12, 6, 10, 10],   # Row 16
        [10, 8, 4, 4, 2, 12, 6, 12, 2, 12, 1, 1, 6, 8, 5, 5, 2, 12, 1, 6, 10, 9, 5, 4, 2],     # Row 17
        [8, 6, 9, 5, 6, 9, 5, 1, 6, 9, 2, 12, 1, 4, 5, 5, 4, 1, 6, 9, 2, 8, 5, 5, 2],          # Row 18
        [12, 5, 4, 5, 5, 4, 5, 4, 5, 6, 12, 5, 4, 5, 5, 5, 5, 4, 5, 4, 4, 4, 5, 5, 6],         # Row 19
        ]
    path = "SWSESWSESWSSSEESEEENEESESEESSSEEESSSEEENNENEE"
    try:
        w, h = MazeParams.get_maze_size_in_pixels(len(data[0]), len(data))
        # print(len(data[0]), len(data), w, h)
        visualizer = MazeVisualizerOne("A-Maze-Ing", w, h, (1, 1),
                                       (19, 14), data, path)
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
