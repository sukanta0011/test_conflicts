import sys
from pathlib import Path
from mazegen import MazeGenerator
# from srcs.maze_generator.maze_generator import MazeGenerator
from config_parser import Configuration, ConfigParser
from srcs.maze_visualizer.MazeVisualize import MazeVisualizerOne
from srcs.maze_visualizer.MazeParams import MazeParams
from output_writer import OutputWriter
import faulthandler


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
    generator = MazeGenerator(configuration.width,
                              configuration.height,
                              configuration.entry,
                              configuration.exit,
                              configuration.perfect,
                              configuration.seed)
    data = generator.grid.cells
    path = generator.solution
    output_writer = OutputWriter(configuration)
    output_writer.create_output(generator.grid, path)

    try:
        maze_params = MazeParams()
        maze_params.initialize_maze(len(data[0]), len(data))
        visualizer = MazeVisualizerOne("A-Maze-Ing", maze_params.win_w,
                                       maze_params.win_h, maze_params,
                                       generator, path, output_writer)
        visualizer.set_background(visualizer.mlx.buff_img,
                                  (0, 0), visualizer.mlx.buff_img.w,
                                  visualizer.mlx.buff_img.w, 0xFF000000)
        visualizer.display_maze(data, visualizer.const.wall_color)
        visualizer.show_user_interaction_options()
        visualizer.put_buffer_image()
        visualizer.start_mlx()
        visualizer.clean_mlx()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    faulthandler.enable()
    main()
