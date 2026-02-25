# mazegen

Reusable Python module for maze generation and solving.

This package provides the MazeGenerator class, which allows you to generate a maze and compute its solution programmatically.

## Basic Usage
```
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=20,
    height=10,
    entry=(0, 0),
    exit=(9, 19),
    perfect=True,
    seed="42"
)

print(maze.solution)
```
The maze is generated automatically during initialization.

## Custom Parameters
| Parameter | Type       | Description                                       |
| :-------- | :--------- | :------------------------------------------------ |
| `width`   | int        | Number of horizontal cells                        |
| `height`  | int        | Number of vertical cells                          |
| `entry`   | (int, int) | Entry coordinates (row, col)                      |
| `exit`    | (int, int) | Exit coordinates (row, col)                       |
| `perfect` | bool       | `True` → exactly one path; `False` → allows loops |
| `seed`    | str | None | Optional seed for deterministic mazes             |

## Accessing the Maze Structure
```
grid = maze.grid
cells = grid.cells
```
cells is a 2D list of integers representing wall bit flags.
The shortest path from entry to exit is available as:
```
solution = maze.solution
```
The solution is returned as a string composed of:
- 'N'
- 'E'
- 'S'
- 'W'

## Regenerating a Maze
```
maze.generate()
print(maze.solution)
```
This regenerates the maze and recomputes the solution.