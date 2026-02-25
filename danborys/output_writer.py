from config_parser import Configuration
from mazegen.grid import Grid


class OutputWriter():
    """
    Responsible for exporting the generated maze and its solution
    to an output file defined in the configuration.

    The output file format is:
        - HEIGHT lines of WIDTH hexadecimal characters representing the maze.
        - An empty line.
        - The entry coordinates.
        - The exit coordinates.
        - The shortest path using directions ('N', 'E', 'S', 'W').
    """

    def __init__(self, config: Configuration) -> None:
        """
        Initialize the OutputWriter.

        Args:
            config (Configuration): Validated configuration object
                containing maze dimensions, entry/exit coordinates,
                and output file path.
        """
        self.config = config

    def create_output(self, grid: Grid, path: str) -> None:
        """
        Generate and write the maze report to the output file.

        The maze grid is encoded using hexadecimal characters
        (0-F), where each cell value is reduced modulo 16
        to ensure a single hexadecimal digit per cell.

        The final output structure is:
            1. Maze representation (HEIGHT x WIDTH characters).
            2. Empty line.
            3. Entry coordinates (row, col).
            4. Exit coordinates (row, col).
            5. Shortest path as a sequence of directions.

        Args:
            grid (Grid): Maze grid object containing cell values.
            path (str): Shortest path from entry to exit,
                represented as a string of directions
                ('N', 'E', 'S', 'W').

        Raises:
            None: Errors during file writing are caught and reported
            to standard output.
        """
        report = ""
        hex = "0123456789ABCDEF"
        for row in range(self.config.height):
            for col in range(self.config.width):
                report += hex[grid.cells[row][col] % 16]
            report += "\n"
        report += "\n"

        row, col = self.config.entry
        report += f"{row}, {col}\n"

        row, col = self.config.exit
        report += f"{row}, {col}\n"
        report += path
        report += "\n"

        try:
            with open(self.config.output_file, "w") as f:
                f.write(report)
        except Exception:
            print(f"[ERROR] failed to write output file: "
                  f"{self.config.output_file}")
