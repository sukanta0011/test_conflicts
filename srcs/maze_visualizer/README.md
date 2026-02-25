# MazeView

A Python library for visualizing and interacting with maze structures using MLX graphics.

## Features

- 🎨 Customizable maze rendering with configurable colors and dimensions
- 🖼️ Interactive visualization with user interaction support
- 🧩 Flexible grid-based maze representation
- 🎯 Entry, exit, and path visualization
- 🔧 Easy-to-use parameter configuration system

## Installation

Install MazeView using pip:

```bash
pip install mazeview-1.0.0-py3-none-any.whl
pip install mlx-2.2-py3-none-any.whl
```

## Quick Start

Here's a simple example to get you started:

```python
from mazeview import MazeVisualizerOne, MazeParams

def main() -> None:
    try:
        # Define your maze structure (binary representation)
        data = [
            [15, 15, 15],
            [15, 15, 15],
            [15, 15, 15]
        ]
        
        # Configure maze parameters
        maze_params = MazeParams()
        maze_params.grid_size = 50
        maze_params.wall_thickness = 10
        maze_params.initialize_maze(len(data[0]), len(data))
        
        # Create visualizer instance
        visualizer = MazeVisualizerOne(
            name="A-Maze-Ing",
            w=maze_params.win_w,
            h=maze_params.win_h,
            const=maze_params,
            cells=data,
            entry=(10, 0),
            exit=(0, 0)
        )
        
        # Display and run
        visualizer.display_maze(data, maze_params.wall_color)
        visualizer.show_user_interaction_options()
        visualizer.put_buffer_image()
        visualizer.start_mlx()
        visualizer.clean_mlx()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

Run your maze visualization:

```bash
python3 your_script.py
```

## Configuration

### MazeParams

The `MazeParams` class allows you to customize various aspects of your maze visualization:

#### Dimension Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `grid_size` | 16 | Size of each grid cell in pixels |
| `wall_thickness` | 4 | Thickness of maze walls in pixels |

#### Color Parameters (ARGB format: 0xAARRGGBB)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `bg_color` | `0xFF000000` | Background color (black) |
| `wall_color` | `0xFFFFFFFF` | Wall color (white) |
| `color_42` | `0xFFFF00FF` | Special marker color (magenta) |
| `entry_color` | `0xFF00FF00` | Entry point color (green) |
| `exit_color` | `0xFFFF0000` | Exit point color (red) |
| `path_color` | `0xFF008FFF` | Solution path color (blue) |

### Example: Custom Configuration

```python
maze_params = MazeParams()

# Adjust dimensions
maze_params.grid_size = 32
maze_params.wall_thickness = 6

# Customize colors
maze_params.wall_color = 0xFF00FFFF  # Cyan walls
maze_params.entry_color = 0xFFFFFF00  # Yellow entry
maze_params.exit_color = 0xFFFF6600   # Orange exit

maze_params.initialize_maze(width, height)
```

## MazeVisualizerOne Parameters

When creating a `MazeVisualizerOne` instance, you can specify:

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Window title/project name |
| `w` | `int` | Window width in pixels |
| `h` | `int` | Window height in pixels |
| `const` | `MazeParams` | Maze parameters object |
| `cells` | `List[List[int]]` | 2D array representing maze structure |
| `entry` | `Tuple[int, int]` | Entry coordinates (x, y) |
| `exit` | `Tuple[int, int]` | Exit coordinates (x, y) |
| `path` | `str` | Solution path (optional, default: `""`) |
| `generator` | `MazeGenerator` | Maze generator instance (optional) |
| `output_writer` | `OutputWriter` | Output writer instance (optional) |

## Maze Structure

The maze is represented as a 2D list where each cell is an integer value. The binary representation of these values determines which walls are present:

- Bit 0 (1): Top wall
- Bit 1 (2): Right wall
- Bit 2 (4): Bottom wall
- Bit 3 (8): Left wall

**Example:**
- `15` (binary: 1111) = All walls present
- `12` (binary: 1100) = Bottom and left walls only
- `0` (binary: 0000) = No walls (open cell)

## Project Structure

```
.
├── README.md
├── __init__.py
├── dist/
│   ├── mazeview-1.0.0-py3-none-any.whl
│   └── mazeview-1.0.0.tar.gz
├── maze_params.py
├── maze_visualizer.py
├── mlx_tools/
│   ├── __init__.py
│   ├── alphabets.xpm
│   ├── base_mlx.py
│   ├── image_operations.py
│   ├── letter_to_img_map.py
│   ├── mlx_errors.py
│   └── shape_maker.py
├── pyproject.toml
└── uv.lock
```

## Requirements

- Python 3.x
- MLX library (included: `mlx-2.2-py3-none-any.whl`)

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Support

For issues, questions, or contributions, please [add contact/repository information].

---

**Happy Maze Building! 🎮🧩**