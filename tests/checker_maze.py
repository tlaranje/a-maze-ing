import sys

def parse_maze(maze_str):
    """Parse the maze string into a 2D grid of hex values."""
    lines = maze_str.strip().split('\n')
    return [[int(c, 16) for c in line] for line in lines]

def get_walkable_neighbors(grid, row, col):
    """Get all walkable neighbors from a cell based on wall bits."""
    cell = grid[row][col]
    rows, cols = len(grid), len(grid[0])
    neighbors = []

    # North (bit 0): row - 1
    if not (cell & 0x1) and row > 0:
        neighbors.append((row - 1, col))

    # East (bit 1): col + 1
    if not (cell & 0x2) and col < cols - 1:
        neighbors.append((row, col + 1))

    # South (bit 2): row + 1
    if not (cell & 0x4) and row < rows - 1:
        neighbors.append((row + 1, col))

    # West (bit 3): col - 1
    if not (cell & 0x8) and col > 0:
        neighbors.append((row, col - 1))

    return neighbors

def is_perfect_maze(maze_str):
    """
    Check if a maze is perfect.
    A perfect maze has:
    1. All cells are connected (single connected component)
    2. No loops (number of edges = number of nodes - 1)
    """
    from collections import deque

    grid = parse_maze(maze_str)
    rows, cols = len(grid), len(grid[0])

    # Collect walkable cells
    walkable_cells = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] != 0xF]

    if not walkable_cells:
        return False, "No walkable cells found"

    total_cells = len(walkable_cells)

    # BFS with deque for better performance
    visited = set()
    queue = deque([walkable_cells[0]])
    visited.add(walkable_cells[0])
    edge_count = 0

    while queue:
        row, col = queue.popleft()
        neighbors = get_walkable_neighbors(grid, row, col)

        for n_row, n_col in neighbors:
            edge_count += 1

            if (n_row, n_col) not in visited:
                visited.add((n_row, n_col))
                queue.append((n_row, n_col))

    # Check connectivity
    if len(visited) != total_cells:
        return False, f"Maze is not fully connected: {len(visited)}/{total_cells} cells reachable"

    # Check for loops: expected_edges = 2 * (nodes - 1) for undirected graph
    expected_edges = 2 * (total_cells - 1)

    if edge_count == expected_edges:
        return True, f"Perfect maze: {total_cells} cells, {edge_count // 2} edges"
    elif edge_count > expected_edges:
        loops = (edge_count - expected_edges) // 2
        return False, f"Maze has loops: {loops} extra edge(s)"
    else:
        return False, f"Maze has disconnected regions"

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 checker.py <file.maze>")
        sys.exit(1)

    maze_file = sys.argv[1]

    try:
        with open(maze_file, 'r') as f:
            maze_input = f.read()

        is_perfect, message = is_perfect_maze(maze_input)

        if is_perfect:
            print(f"✓ PERFECT MAZE")
            print(f"  {message}")
        else:
            print(f"✗ NOT A PERFECT MAZE")
            print(f"  {message}")

        sys.exit(0 if is_perfect else 1)

    except FileNotFoundError:
        print(f"Error: File '{maze_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

# Test with the loop example
if __name__ == "__main__":
    # If no arguments, test the provided example
    if len(sys.argv) == 1:
        test_maze = """FFFFFFFFFFFFFFFFFFFF
FD553FF9553FF953FFFF
FFFFC3FAFFAFFAFAFD3F
FFBFFC56F96FFAFC3FAF
FF853FFF96F956FFC52F
F96FAFF96FFAFFBFFFAF
FAFFAFFAF956FFAFFFAF
FAFFEFFAFAFFF945556F
F853FFFAFAFFD2FFFFFF
FAFC5556FAFFFC3FFD3F
FAFFFFFFFC553FC3FFAF
FAFFFF953FFFC3FAFFAF
FAFD156FC53FFAFC552F
FC3FAFFFFFC3FAFFFFAF
FFC56F957FFAFC553FAF
FFFFFFAFFF96FFFFAFAF
FD153D05556FFBF96FAF
FD6FAFAFFFFFF856FFAF
FFFFC545555556FFFD6F
FFFFFFFFFFFFFFFFFFFF"""

        print("Testing maze for loops...")
        is_perfect, message = is_perfect_maze(test_maze)
        print(f"\nResult: {'✓ PERFECT MAZE' if is_perfect else '✗ NOT A PERFECT MAZE'}")
        print(f"Details: {message}")
    else:
        main()

if __name__ == "__main__":
    main()
