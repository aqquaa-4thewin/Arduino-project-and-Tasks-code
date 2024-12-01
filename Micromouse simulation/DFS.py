import API
import sys

# Dictionary to track visited cells (key: (x, y), value: boolean)
visited_cells = {}

# Directions (up, right, down, left) corresponding to API's turn and movement
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
current_direction = 0  # Initially facing "up" (north)
x, y = 0, 0  # Starting position

# Maze size (can be dynamically set)
maze_width = API.mazeWidth()
maze_height = API.mazeHeight()

def log(string):
    """Logs messages for debugging."""
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def mark_current_cell(x, y):
    """Marks the current cell as visited."""
    if (x, y) not in visited_cells:
        visited_cells[(x, y)] = True
        API.setColor(x, y, "B")  # Blue color to indicate visited
        API.setText(x, y, "V")

def turn_left():
    """Turns the robot left and updates the direction."""
    global current_direction
    API.turnLeft()
    current_direction = (current_direction - 1) % 4

def turn_right():
    """Turns the robot right and updates the direction."""
    global current_direction
    API.turnRight()
    current_direction = (current_direction + 1) % 4

def move_forward():
    """Moves the robot forward and updates its position."""
    global x, y, current_direction
    if not API.wallFront():
        API.moveForward()
        dx, dy = DIRECTIONS[current_direction]
        x += dx
        y += dy
        mark_current_cell(x, y)  # Mark the new cell as visited
    else:
        log(f"Blocked at ({x}, {y}). Cannot move forward.")

def turn_around():
    """Turns the robot 180 degrees."""
    turn_left()
    turn_left()

def is_center(x, y):
    """Checks if the current position (x, y) is the center of the maze."""
    center_x = maze_width // 2
    center_y = maze_height // 2
    center_coords = [
        (center_x, center_y),
        (center_x - 1, center_y),
        (center_x, center_y - 1),
        (center_x - 1, center_y - 1)
    ]
    return (x, y) in center_coords

def dfs():
    """Implements Depth-First Search to navigate the maze."""
    global x, y

    # Mark the starting cell
    mark_current_cell(x, y)

    # If the center is reached, stop
    if is_center(x, y):
        API.setColor(x, y, "G")  # Green for the goal
        API.setText(x, y, "End")
        log("Reached the center of the maze!")
        return True

    # Try moving in each direction
    for i in range(4):
        dx, dy = DIRECTIONS[current_direction]
        next_x, next_y = x + dx, y + dy

        if not API.wallFront() and (next_x, next_y) not in visited_cells:
            move_forward()  # Move forward
            if dfs():  # Recursive call to explore the next cell
                return True
            turn_around()  # Backtrack if dead-end
            move_forward()  # Move back to previous cell
            turn_around()  # Face the original direction

        # Turn right to try the next direction
        turn_right()

    return False

def main():
    """Runs the DFS algorithm."""
    log("Starting Depth-First Search (DFS)...")
    if dfs():
        log("Maze solved!")
    else:
        log("Could not solve the maze.")

if __name__ == "__main__":
    main()
