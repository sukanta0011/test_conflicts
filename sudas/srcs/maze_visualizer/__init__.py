try:
    import mlx
except ImportError:
    raise ImportError(
        "The 'mlx' module is missing. Please install the provided mlx wheel: "
        "'pip install mlx-2.2-py3-none-any.whl'"
    )

from .maze_visualizer import MazeVisualizerOne
from .maze_params import MazeParams

__all__ = ["MazeVisualizerOne", "MazeParams"]
