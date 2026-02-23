from .config_parser import Configuration
from .grid import Grid


class OutputWriter():
    def __init__(self, config: Configuration) -> None:
        self.config = config

    def create_output(self, grid: Grid, path: str) -> None:
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
