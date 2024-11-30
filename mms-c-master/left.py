import API

SIZE = 20  # Maze size
flood = [[SIZE * SIZE for _ in range(SIZE)] for _ in range(SIZE)]
goal_x, goal_y = SIZE // 2 - 1, SIZE // 2 - 1  # Goal at the center of a 20x20 maze


def log(message):
    """Log messages to the simulator."""
    print(message)
    API.setText(0, 0, message)


def initializeFlood():
    """Initialize the flood array with high values and set the goal to 0."""
    for y in range(SIZE):
        for x in range(SIZE):
            flood[y][x] = SIZE * SIZE
    flood[goal_y][goal_x] = 0  # Center goal


def floodFill():
    """Perform the flood-fill algorithm to calculate costs."""
    updated = True
    while updated:
        updated = False
        for y in range(SIZE):
            for x in range(SIZE):
                if flood[y][x] < SIZE * SIZE:
                    for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        ny, nx = y + dy, x + dx
                        if 0 <= nx < SIZE and 0 <= ny < SIZE:
                            if flood[ny][nx] > flood[y][x] + 1:
                                flood[ny][nx] = flood[y][x] + 1
                                updated = True


def moveToGoal():
    """Move the robot to the goal using the flood array."""
    x, y = 0, 0  # Starting position
    orient = 0  # Initial orientation (0: North, 1: East, 2: South, 3: West)

    while flood[y][x] != 0:  # Stop when reaching the goal
        API.setColor(x, y, 'red')  # Mark the current cell
        L = API.wallLeft()
        R = API.wallRight()
        F = API.wallFront()

        # Update walls in the flood array
        if L:
            API.setWall(x, y, getDirection(orient, 'L'))
        if R:
            API.setWall(x, y, getDirection(orient, 'R'))
        if F:
            API.setWall(x, y, getDirection(orient, 'F'))

        # Get the next move based on flood costs
        next_x, next_y, next_orient = getNextMove(x, y, orient, F, R, L)

        # Turn the robot to the correct direction
        if next_orient == (orient + 3) % 4:  # Turn left
            API.turnLeft()
        elif next_orient == (orient + 1) % 4:  # Turn right
            API.turnRight()
        elif next_orient == (orient + 2) % 4:  # Turn around
            API.turnLeft()
            API.turnLeft()

        # Move forward only if there is no wall
        if not F or (x != next_x or y != next_y):
            API.moveForward()
            x, y = next_x, next_y
            orient = next_orient
        else:
            log("Blocked by a wall. Adjusting...")
            break  # Safety exit to prevent crashes

    # Mark the goal cell and stop
    API.setColor(x, y, 'green')
    log("Goal reached! Stopping.")


def getDirection(orient, relative):
    """Get the absolute direction based on the current orientation and relative move."""
    directions = {'F': 0, 'R': 1, 'B': 2, 'L': 3}  # Relative moves
    return (orient + directions[relative]) % 4


def getNextMove(x, y, orient, F, R, L):
    """Determine the next cell to move to based on flood costs."""
    min_cost = SIZE * SIZE
    best_x, best_y, best_orient = x, y, orient
    moves = [(0, 1, 'F', F), (1, 0, 'R', R), (0, -1, 'B', True), (-1, 0, 'L', L)]

    for dy, dx, relative, can_move in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < SIZE and 0 <= ny < SIZE and flood[ny][nx] < min_cost and not can_move:
            min_cost = flood[ny][nx]
            best_x, best_y, best_orient = nx, ny, getDirection(orient, relative)

    return best_x, best_y, best_orient


def main():
    """Main function to initialize and start the flood-fill algorithm."""
    log("Starting Flood-Fill Algorithm...")
    initializeFlood()
    floodFill()
    moveToGoal()


# Start the program
main()
