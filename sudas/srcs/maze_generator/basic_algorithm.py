from typing import Tuple, Set, List
import random
from .abc_algorithm import Algorithm
from .grid import Grid, Wall
from .perfect_algorithm import PerfectAlgorithm


class BasicAlgorithm(Algorithm):
    def generate(self) -> Grid:
        self.grid = PerfectAlgorithm(self.config).generate()
        if self.config.seed:
            random.seed(self.config.seed)
        self.visited: Set[Tuple[int, int]] = set()
        cells_42 = self.get_42_cells()
        if not isinstance(cells_42, str):
            self.visited.update(cells_42)
        for r in range(self.grid.height):
            for c in range(self.grid.width):
                if (r, c) not in self.visited and random.random() > 0.5:
                    unknown_neighbours = self.get_unknown_neighbour((r, c))
                    self.open_wall(unknown_neighbours, (r, c))
        for r in range(self.grid.height):
            for c in range(self.grid.width):
                if self.grid.cells[r][c] == 0 and\
                    self.grid.cells[r - 1][c - 1] >> 1 & 0 and\
                    self.grid.cells[r - 1][c - 1] >> 2 & 0:
                    self.grid.cells[r][c] = 9
                    self.grid.cells[r - 1][c] |= Wall.SOUTH
                    self.grid.cells[r][c - 1] |= Wall.EAST

        return self.grid

    def open_wall(self, neighbour: List[Tuple[int, int]],
                  cur_cell: Tuple[int, int]) -> None:
        if len(neighbour) > 0:
            random.shuffle(neighbour)
            row_next, col_next = neighbour[0]
            row_cur, col_cur = cur_cell
            self.visited.add((row_next, col_next))
            current_wall = 0
            if row_next > row_cur:
                current_wall = Wall.SOUTH
            elif row_next < row_cur:
                current_wall = Wall.NORTH
            elif col_next > col_cur:
                current_wall = Wall.EAST
            elif col_next < col_cur:
                current_wall = Wall.WEST
            self.grid.cells[row_cur][col_cur] &= ~current_wall
            self.grid.cells[row_next][col_next] &=\
                ~current_wall.opposite()

    def get_unknown_neighbour(
            self, cur_cell: Tuple[int, int]) -> List[Tuple[int, int]]:
        unknown_neighbours: List[Tuple[int, int]] = []
        curr_val = self.grid.cells[cur_cell[0]][cur_cell[1]]
        if curr_val >> 0 & 1:
            neighbour_pos = (cur_cell[0] - 1, cur_cell[1])
            if (self.is_coord_in_boundry(neighbour_pos) and
               neighbour_pos not in self.visited):
                unknown_neighbours.append(neighbour_pos)
        if curr_val >> 1 & 1:
            neighbour_pos = (cur_cell[0], cur_cell[1] + 1)
            if (self.is_coord_in_boundry(neighbour_pos) and
               neighbour_pos not in self.visited):
                unknown_neighbours.append(neighbour_pos)
        if curr_val >> 2 & 1:
            neighbour_pos = (cur_cell[0] + 1, cur_cell[1])
            if (self.is_coord_in_boundry(neighbour_pos) and
               neighbour_pos not in self.visited):
                unknown_neighbours.append(neighbour_pos)
        if curr_val >> 3 & 1:
            neighbour_pos = (cur_cell[0], cur_cell[1] - 1)
            if (self.is_coord_in_boundry(neighbour_pos) and
               neighbour_pos not in self.visited):
                unknown_neighbours.append(neighbour_pos)

        return unknown_neighbours

    def is_coord_in_boundry(self, coords: Tuple[int, int]) -> bool:
        if (
            0 <= coords[0] < self.config.height
            and 0 <= coords[1] < self.config.width
        ):
            return True
        return False


def tester():
    from .config_parser import Configuration, ConfigParser
    from .maze_generator import MazeGenerator
    from pathlib import Path
    import sys
    from .maze_generator import MazeGenerator
    from srcs.maze_visualizer.MazeVisualize import MazeVisualizerOne
    from srcs.maze_visualizer.MazeParams import MazeParams
    from srcs.mlx_tools.ImageOperations import (
        TxtToImage, ImageScaler, TxtColorChanger)
    from srcs.mlx_tools.LetterToImageMapper import LetterToImageMapper

    configuration: Configuration = ConfigParser.parse_config(Path(sys.argv[1]))
    generator = MazeGenerator(config=configuration)
    # print(generator.grid)
    path = ""
    data = generator.grid.cells
    print(generator.grid.print_hex_format())
    # print(data)
    # config: Configuration = generator.config
    # print(config.entry)
    try:
        # w, h = MazeParams.get_maze_size_in_pixels(len(data[0]), len(data))
        # print(len(data[0]), len(data))
        maze_params = MazeParams()
        maze_params.initialize_maze(len(data[0]), len(data))
        # print(maze_params.win_w, maze_params.win_h)
        visualizer = MazeVisualizerOne("A-Maze-Ing", maze_params.win_w,
                                       maze_params.win_h, maze_params,
                                       generator, path)
        visualizer.set_background(visualizer.mlx.buff_img,
                                  (0, 0), visualizer.mlx.buff_img.w,
                                  visualizer.mlx.buff_img.w, 0xFF000000)
        visualizer.display_maze(data, visualizer.const.wall_color)
        visualizer.show_path(path, visualizer.const.path_color)
        visualizer.show_user_interaction_options()
        visualizer.put_buffer_image()
        visualizer.start_mlx()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    tester()
