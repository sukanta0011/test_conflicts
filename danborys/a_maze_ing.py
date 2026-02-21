import sys
from config_parser import Configuration, ConfigParser
from pathlib import Path
from maze_generator import MazeGenerator


def main() -> None:
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
    generator.print_grid()


if __name__ == "__main__":
    main()
