from .config_parser import Configuration
from .grid import Grid


class OutputWriter():
    def __init__(self, config: Configuration) -> None:
        self.config = config

    def create_output(self, grid: Grid, path: str) -> None:
        print(path)
