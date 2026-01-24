This project has been created as part of the 42 curriculum by joesanto, tlaranje

<div align="center">
🌀 A‑Maze‑ing — This is the Way
A Python Maze Generator & Solver with MLX Rendering

✨ Procedural generation, pathfinding, and smooth animations — all in one project.

</div>
📘 Description

This project implements a fully interactive maze generator and solver written in Python.
It supports:

    Perfect mazes — no cycles, exactly one unique path between any two points

    Imperfect mazes — cycles allowed, multiple possible solutions

    Shortest‑path solving between entry and exit

    Real‑time rendering using the MLX graphics library

The goal is to explore algorithmic design, procedural generation, and efficient rendering while maintaining clean architecture and reusable components.
⚙️ Instructions
🔧 Installation
sh

make install

▶️ Running the Program
sh

make run

The program automatically loads configuration values from config.txt.
Modify this file to customize maze size, entry/exit points, output file, and maze type.
📝 Config File Structure

Your config.txt must follow the KEY=VALUE format and include all fields below:
Key	Description	Example
WIDTH	Maze width (number of cells)	WIDTH=20
HEIGHT	Maze height	HEIGHT=15
ENTRY	Entry coordinates (x,y)	ENTRY=0,0
EXIT	Exit coordinates (x,y)	EXIT=19,14
OUTPUT_FILE	Output filename	OUTPUT_FILE=maze.txt
PERFECT	Whether the maze is perfect (True/False)	PERFECT=True
🎮 Key Bindings (Rendering Controls)
Key	Action
h	Hide shortest path
p	Show shortest path
s	Enter a custom seed
c	Change wall colors
r	Regenerate a new maze
🧠 Maze Generation Algorithm
🔍 Algorithm Used: Iterative Backtracking (Depth‑First Search)

We selected the backtracking algorithm because it is:

    Educational and intuitive

    Great for understanding DFS and state management

    Efficient when implemented iteratively with a stack

    Visually appealing during generation

    Perfect for producing clean, organic maze structures

🧩 How It Works

    Start at a random cell

    Visit unvisited neighbors, carving passages

    Push branching points onto a stack

    When stuck, pop from the stack and continue

    Repeat until all cells are visited

This produces a perfect maze.
To create imperfect mazes, we introduce controlled randomness to add cycles.
♻️ Reusable Code

The project is structured into modular components that can be reused independently:
🔧 Reusable Modules

    Maze Generator — ideal for games, simulations, or procedural map creation

    Pathfinding Module — applicable to AI navigation or robotics

    Rendering Engine (MLX wrapper) — adaptable for:

        2D games

        2.5D raycasting engines

        Visual debugging tools

The architecture encourages clean imports and easy integration into other projects.
👥 Team & Project Management
🧑‍🤝‍🧑 Team Members

    joesanto — Co‑developer (algorithms, rendering, debugging)

    tlaranje — Co‑developer (architecture, pathfinding, optimization)

We chose to work together on all parts of the project.
This allowed us to:

    Share perspectives

    Debate solutions

    Maintain a unified understanding of the entire codebase

📅 Planning & Evolution

Our main objective stayed constant:
➡️ Create a clean, animated, efficient maze rendering.

But our approach evolved:

    Early rendering was slow → we researched MLX image buffers

    We optimized by drawing only updated regions instead of the entire maze

    Each iteration improved performance and clarity

⭐ What Worked Well

    Strong communication

    Pair‑programming workflow

    Continuous refactoring

    Efficient debugging

🛠️ What Could Be Improved

    Applying mypy earlier would have prevented late‑stage fixes

    Using AI earlier could have clarified complex algorithmic concepts sooner

🧰 Tools Used

    MLX graphics library

    mypy type checking

    AI assistance for:

        Understanding algorithms

        Generating test cases

        Improving documentation

📚 Resources
🔗 Maze Generation References

    https://professor-l.github.io/mazes/

🤖 AI Usage

AI was used to:

    Understand complex algorithmic behavior

    Explore alternative maze generation strategies

    Produce diverse test cases

    Improve documentation clarity and structure
