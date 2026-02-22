import sys
from .config_parser import Configuration, ConfigParser
from pathlib import Path
from .maze_generator import MazeGenerator
from srcs.maze_visualizer.MazeVisualize import MazeVisualizerOne
from srcs.maze_visualizer.MazeParams import MazeParams
from srcs.mlx_tools.ImageOperations import (
    TxtToImage, ImageScaler, TxtColorChanger)
from srcs.mlx_tools.LetterToImageMapper import LetterToImageMapper
from srcs.maze_generator.solver import Solver


def main():
    """
    Entry point of the A-Maze-ing application.

    This function validates command-line arguments, parses the provided
    configuration file, and initializes the maze configuration.

    The program expects exactly one argument:
        - Path to the configuration file.

    If the number of arguments is incorrect, an error message is printed
    to stderr and the program exits with a non-zero status code.

    Raises:
        SystemExit: If the number of command-line arguments is invalid
        or if configuration parsing fails.

    Returns:
        None
    """
    if len(sys.argv) != 2:
        print("Use python a_maze_ing.py [config.txt]", file=sys.stderr)
        exit(1)

    configuration: Configuration = ConfigParser.parse_config(Path(sys.argv[1]))
    generator = MazeGenerator(config=configuration)
    data = generator.grid.cells
    # print(data)
    # config: Configuration = generator.config
    # print(config.entry)
    solver = Solver(generator.grid, configuration)
    path = solver.find_path()[0]
    # print(path)
    try:
        # w, h = MazeParams.get_maze_size_in_pixels(len(data[0]), len(data))
        # print(len(data[0]), len(data))
        maze_params = MazeParams()
        maze_params.initialize_maze(len(data[0]), len(data))
        # print(maze_params.win_w, maze_params.win_h)
        visualizer = MazeVisualizerOne("A-Maze-Ing", maze_params.win_w,
                                       maze_params.win_h, maze_params,
                                       generator, solver, path)
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
    # return generator


if __name__ == "__main__":
    main()
