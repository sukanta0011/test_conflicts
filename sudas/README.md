*This project has been created as part of the 42 curriculum by danborys, sudas*

#A-Maze-Ing
## Description
This project focuses on the algorithmic generation and resolution of mazes. To provide a complete user experience, it features:

1. Maze Generator: A robust engine for creating various maze types.

2. Maze Solver: An integrated algorithm that finds the path between defined start and end points.

3. Graphical Visualizer: A real-time display built using the MiniLibX library.

The core logic is decoupled into a reusable Python package (`mazegen`), allowing the generation engine to be integrated into other projects independently. This package can be installed using `pip`.

## Instructions
#### Building the Reusable part

- build the mazegen distribution:

```bash
cd srcs/maze_generator
uv build
```

This generates mazegen-1.0.0-py3-none-any.whl inside the dist/ folder. This wheel can be installed via `pip` or `uv` in any Python environment.

#### Running the Visualizer
The project uses `uv` for dependency management and a Makefile for orchestration.

1. Copy the build: Ensure the `.whl` file is in the root directory.

2. Install: Run `make install` to set up the virtual environment and dependencies.

3. Execute: Run `make run` to launch the graphical interface.

Note: Configuration (Height, Width, Entry/Exit, Seed) is managed via config.txt.

#### The structure and format of the config file:
|key            | value     | DEscription |
|:--------------|:----------|:---------------------------|
|WIDTH          | Int       |Number of horizontal cells.|
|HEIGHT         | Int       |Number of vertical cells.|
|ENTRY          |Int, Int   |Starting coordinates (X,Y) |
|EXIT           |Int, Int   |Ending coordinates (X,Y)|
|OUTPUT_FILE    |String   |Filename to save the generated maze.|
|PERFECT        | Bool      |True/yes for exactly one path; False/no for loops.|
|SEED           |Int/None|Set for deterministic/reproducible mazes.|

#### Visual display

The visualizer uses the MiniLibX graphical library. The following interactions are
available in the graphical window:

| Key | Action                          |
|:----|:--------------------------------|
| `1` | Re-generate a new maze          |
| `2` | Show / Hide the solution path   |
| `3` | Rotate / Change wall colors    |
| `4` | Quit                            |

The visual parameters (cell pixel size, window dimensions, colors, etc.) can be
customized in `srcs/maze_visualizer/MazeParams.py`.

## Technical Overview
#### Generation Algorithm: Iterative DFS
We implemented an Iterative Depth First Search (DFS) using a stack.

- Why DFS? It is highly effective for generating "Perfect Mazes" with long, winding corridors and deep branches.

- Why Iterative? Using a manual stack avoids the RecursionLimit issues common in Python when generating large-scale mazes.


#### The team:
- danborys: Parsing logic, Maze Generation engine, Solver implementation, and Packaging.

- sudas: Graphical Visualizer (MiniLibX), Makefile orchestration, and Packaging.

#### Planning:
The project was divided into four parts: parsing, maze generation, maze solving, and
graphical visualization. We grouped the first three into a non-graphical backend and
kept the visualizer as a separate, loosely coupled frontend — the visualizer only needs
the maze grid and the solution path to render the result.

This separation worked well in practice and made it straightforward to package the
backend independently as the `mazegen` module.

#### What went well:
- The maze generator and solver work correctly and reliably.
- The loose coupling between backend and visualizer made development and packaging clean.
- The two parts were developed in parallel without significant conflicts.

#### What could be improved
- DFS generates very long solution paths in perfect mazes. Prim's algorithm would
  produce shorter, more varied paths.
- The non-perfect maze generation (opening walls randomly after DFS) could be improved
  with a more principled approach.
- The visualizer implements the bare minimum. Potential improvements include a
  generation animation, auto-scaling cell sizes based on maze dimensions, and
  interactive colour pickers.

## Resources
- [uv package manager](https://www.datacamp.com/tutorial/python-uv?utm_aid=192632748929&utm_loc=9222121-&utm_mtd=-c&utm_kw=&gad_campaignid=23340058065)
- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [MiniLibX documentation](https://harm-smits.github.io/42docs/libs/minilibx)


#### AI Usages
- Documentation: Docstrings were initially drafted by Gemini and manually refined for technical accuracy.

- Packaging: We utilized AI to streamline the transition to the uv build system.

- Code: All core logic and architectural implementations were authored solely by the project team.
