*This project has been created as part of the 42 curriculum by joesanto, tlaranje*

A‑Maze‑ing
🧩 Description

This project consists of building a fully functional maze generator and solver in Python, capable of producing both:

    Perfect mazes (no cycles, exactly one unique path between any two points)

    Imperfect mazes (with cycles and multiple possible paths)

The program also computes one of the shortest paths between the entry and exit points and renders the maze visually using the MLX graphics library.
The goal is to combine algorithmic problem‑solving, rendering, and clean software architecture into a cohesive and interactive project.
⚙️ Instructions
Installation

From the root of the repository:
Code

make install

Execution

To run the program:
Code

make run

The program automatically reads the configuration from config.txt, allowing you to customize maze size, entry/exit points, output file, and whether the maze should be perfect or imperfect.
📄 Config File Structure

The configuration file must follow the KEY=VALUE format and include all mandatory fields:
Key	Description	Example
WIDTH	Maze width (number of cells)	WIDTH=20
HEIGHT	Maze height	HEIGHT=15
ENTRY	Entry coordinates (x,y)	ENTRY=0,0
EXIT	Exit coordinates (x,y)	EXIT=19,14
OUTPUT_FILE	Output filename	OUTPUT_FILE=maze.txt
PERFECT	Whether the maze is perfect (True/False)	PERFECT=True
🎮 Key Bindings (Rendering)

During visualization, the following keys are available:

    h — Hide shortest path

    p — Show shortest path

    s — Enter a custom seed for maze generation

    c — Change wall colors

    r — Regenerate a new maze

🧠 Maze Generation Algorithm
Algorithm Used: Iterative Backtracking (Depth‑First Search)

We chose the backtracking algorithm because:

    It is intuitive and highly educational.

    It teaches core concepts of DFS, state tracking, and non‑recursive backtracking.

    It produces visually appealing mazes with a natural “carving” animation.

    It performs efficiently when implemented with a stack instead of recursion.

How It Works (Summary)

    Start at a random cell.

    Explore unvisited neighbors, carving passages as you go.

    Each time a branching decision is made, push the current cell onto a stack.

    When no unvisited neighbors remain, pop from the stack and continue.

    Repeat until all cells have been visited.

This guarantees a perfect maze.
To generate imperfect mazes, we introduce controlled randomness to create cycles.
🔁 Reusable Code

The project is structured into modular, reusable components:
Reusable Modules

    Maze Generator — Can be reused in games, simulations, or procedural map generation.

    Pathfinding Module — Useful for AI navigation, grid‑based games, or robotics simulations.

    Rendering Engine (MLX wrapper) — Can be adapted for:

        2D games

        2.5D raycasting engines

        Visual debugging tools

The separation of concerns allows each module to be imported independently into other projects.
👥 Team & Project Management
Team Members & Roles

We chose to work together on all parts of the project rather than splitting tasks.
This allowed us to:

    Learn from each other’s perspectives

    Debate solutions and improve design decisions

    Maintain a shared understanding of the entire codebase

Planning & Evolution

Our initial objective was clear:
➡️ Create a clean, animated maze rendering with efficient generation.

However, our approach evolved:

    Early rendering was functional but slow.

    We researched MLX image buffers and significantly improved performance.

    Initially, we redrew the entire maze every frame.

    Later, we optimized by rendering only the updated parts, improving speed dramatically.

Each iteration refined both performance and code quality.
What Worked Well

    Strong communication and pair‑programming workflow

    Continuous refactoring and optimization

    Clear shared goals

    Effective debugging sessions

What Could Be Improved

    Applying mypy type checking earlier would have saved time later.

    Using AI earlier could have helped validate our understanding of complex algorithms before implementation.

Tools Used

    MLX for rendering

    mypy for type checking

    AI assistance for:

        Understanding maze algorithms

        Generating test cases

        Clarifying edge‑case behavior

📚 Resources
Maze Generation References

    Professor L’s excellent maze algorithm explanations:
    https://professor-l.github.io/mazes/

AI Usage

AI was used to:

    Understand complex algorithmic concepts

    Explore alternative maze generation strategies

    Generate diverse test cases

    Improve documentation clarity
