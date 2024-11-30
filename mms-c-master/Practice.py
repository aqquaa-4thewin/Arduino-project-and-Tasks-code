from collections import deque

# Define the maze
maze = [
    [18, 13, 12, 13, 14, 21, 20, 21, 21, 20, 21, 23, 23, 24, 25],
    [17, 14, 10, -1, 16, 15, 16, -1, 17, 18, 19, 20, -1, 25, -1],
    [16, 15, -1, 9, -1, 11, 12, -1, 15, 18, 19, 19, -1, 25, 26],
    [18, 19, -1, 7, -1, 5, 10, -1, 13, 17, 18, 21, -1, 24, 29],
    [27, 26, 21, 8, -1, 4, -1, 3, -1, 11, 14, -1, 23, 23, 30],
    [28, 25, -1, 7, -1, 38, 37, 38, 39, -1, -1, -1, -1, -1, 34],
    [30, 33, 34, 35, -1, 36, 37, 38, 23, 22, -1, 19, 21, -1, 30],
    [31, 32, 36, 37, 38, -1, 26, 25, 24, 21, 20, -1, 20, -1, 30],
    [41, 40, 39, 36, -1, 27, 28, -1, 30, 32, -1, 22, 23, 29, 31],
    [45, -1, 38, 37, 50, 49, 48, -1, 31, 32, 33, 34, -1, 28, 29],
    [47, -1, 48, 50, 52, 51, 48, 47, -1, -1, 36, 35, -1, 36, 37],
]

ROWS, COLS = len(maze), len(maze[0])

# Print the maze
def print_maze(maze):
    for row in maze:
        print(" ".join(f"{cell:3}" if cell != -1 else "###" for cell in row))

# Print maze with solution path
def print_solution_path(maze, path):
    solution_maze = [row[:] for row in maze]
    for x, y in path:
        solution_maze[x][y] = "PPP"
    for row in solution_maze:
        print(" ".join(f"{cell:3}" if isinstance(cell, int) else cell for cell in row))

# Solve the maze using BFS
def solve_maze(maze, start, end):
    queue = deque([(*start, [])])  # (x, y, path)
    visited = set()

    while queue:
        x, y, path = queue.popleft()

        if (x, y) == end:
            return path + [(x, y)]

        if (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and maze[nx][ny] != -1 and (nx, ny) not in visited:
                queue.append((nx, ny, path + [(x, y)]))

    return None

# Main function
if __name__ == "__main__":
    print("Initial Maze:")
    print_maze(maze)

    start = (0, 0)
    end = (ROWS - 1, COLS - 1)

    path = solve_maze(maze, start, end)

    if path:
        print("\nSolution Path:")
        print(path)
        print("\nMaze with Solution Path:")
        print_solution_path(maze, path)
    else:
        print("\nNo solution found.")
