# Create a README file named readme.me with the full English content

content = """*This project has been created as part of the 42 curriculum by joesanto, tlaranje.*

# A-Maze-ing

## Description

This project consists of developing a **maze generator and solver in Python**.
The objective is to randomly generate mazes that can be either:

- **Perfect mazes** (no cycles and only one unique path between any two points)
- **Imperfect mazes** (with cycles and multiple possible paths between points)

In addition to generation, the program is able to **compute and display one of the shortest paths**
between the entry and exit points.

The maze is rendered in real time using the **MLX graphics library**, allowing interactive
visualization and user input during execution.

## Instructions

### Installation

To install all required dependencies, run:

make install

### Execution

To run the program, execute the following command from the root of the repository:

make run

The program reads its configuration from the `config.txt` file.
You can customize the maze by editing this file before execution.

## Configuration File

The configuration file **must contain all mandatory fields** using the `KEY=VALUE` format.

### Mandatory Fields

WIDTH        Maze width (number of cells)        Example: WIDTH=20
HEIGHT       Maze height (number of cells)       Example: HEIGHT=15
ENTRY        Entry coordinates (x,y)             Example: ENTRY=0,0
EXIT         Exit coordinates (x,y)              Example: EXIT=19,14
OUTPUT_FILE  Output filename                     Example: OUTPUT_FILE=maze.txt
PERFECT      Defines whether the maze is perfect Example: PERFECT=True

If any of these fields are missing or incorrectly formatted, the program may fail to run.

## Controls (Rendering)

During execution, the following keyboard controls are available:

h  Hide the shortest path
p  Show the shortest path
s  Enter a specific seed for maze generation
c  Change the wall colors
r  Regenerate a new maze

## Maze Generation Algorithm

### Chosen Algorithm: Iterative Backtracking

We chose the **backtracking algorithm**, implemented iteratively using a stack instead of recursion.

### Why This Algorithm?

- It is educational and helps develop a strong understanding of backtracking concepts
- The iterative approach avoids recursion overhead and improves performance
- It produces visually pleasing and natural-looking mazes
- It guarantees perfect maze generation when required

### Algorithm Overview

1. The algorithm starts from a cell and explores all possible directions
2. When multiple choices are available, the current position is stored on a stack
3. Once a path is fully explored, the algorithm backtracks to the last saved position
4. This process continues until all reachable cells have been visited

## Code Reusability

The project is organized into well-defined classes, each responsible for a specific task:

- Maze generation
- Shortest path calculation
- Rendering

Thanks to this modular design, several components of the project are reusable and can be applied
to other contexts, such as:

- 2D games
- 2.5D games (e.g. raycasting)
- Procedural map generation
- Pathfinding systems

## Team and Project Management

### Team Members

- joesanto
- tlaranje

### Roles

We decided to work collaboratively on all parts of the project instead of assigning fixed roles.
This allowed us to exchange ideas, debate solutions, and gain a deeper understanding of the entire project.

### Planning and Evolution

Our initial goal was to create a clean and animated maze rendering.
While this goal remained the same, the implementation evolved significantly.

At first, rendering was functional but not efficient.
By researching MLX image buffers, we greatly improved rendering performance.
Later, instead of rendering the entire maze every frame, we optimized the process
by updating only the parts that changed.

### What Worked Well

- Iterative backtracking implementation
- Rendering optimizations
- Continuous collaboration and discussion

### What Could Be Improved

- Earlier use of static type checking (mypy) would have saved debugging time
- Using AI earlier for design validation could have prevented misunderstandings in complex parts

### Tools Used

- Python
- MLX
- Makefile
- Git
- AI tools

## Resources

Maze generation algorithms reference:
https://professor-l.github.io/mazes/

### AI Usage

AI was used to:
- Help understand complex maze generation logic
- Generate extensive test cases
- Assist in problem-solving during challenging phases

AI was used strictly as a learning and support tool.
"""

path = "/mnt/data/readme.me"
with open(path, "w", encoding="utf-8") as f:
    f.write(content)

path
