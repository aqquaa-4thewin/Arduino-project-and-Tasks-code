import API

# Define flood and other required data structures
SIZE = 20  # Maze size (20x20 for example)
flood = [[SIZE * SIZE for _ in range(SIZE)] for _ in range(SIZE)]
goal_x, goal_y = SIZE // 2 - 1, SIZE // 2 - 1  # Goal at the center of a 20x20 maze

def log(message):
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

        # Update walls
        if L:
            API.setWall(x, y, getDirection(orient, 'L'))
        if R:
            API.setWall(x, y, getDirection(orient, 'R'))
        if F:
            API.setWall(x, y, getDirection(orient, 'F'))

        # Determine the next move based on flood costs
        next_x, next_y, next_orient = getNextMove(x, y, orient)
        if next_orient == (orient + 3) % 4:  # Turn left
            API.turnLeft()
        elif next_orient == (orient + 1) % 4:  # Turn right
            API.turnRight()
        elif next_orient == (orient + 2) % 4:  # Turn around
            API.turnLeft()
            API.turnLeft()

        # Update the robot's position and orientation
        x, y = next_x, next_y
        orient = next_orient
        API.moveForward()

    # Mark the goal cell and stop
    API.setColor(x, y, 'green')
    log("Goal reached! Stopping.")

def getDirection(orient, relative):
    """Get the absolute direction based on the current orientation and relative move."""
    directions = {'F': 0, 'R': 1, 'B': 2, 'L': 3}  # Relative moves
    return (orient + directions[relative]) % 4

def getNextMove(x, y, orient):
    """Determine the next cell to move to based on flood costs."""
    min_cost = SIZE * SIZE
    best_x, best_y, best_orient = x, y, orient
    for dy, dx, relative in [(0, 1, 'F'), (1, 0, 'R'), (0, -1, 'B'), (-1, 0, 'L')]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < SIZE and 0 <= ny < SIZE and flood[ny][nx] < min_cost:
            if relative == 'F' and not API.wallFront():
                min_cost = flood[ny][nx]
                best_x, best_y, best_orient = nx, ny, getDirection(orient, 'F')
            elif relative == 'R' and not API.wallRight():
                min_cost = flood[ny][nx]
                best_x, best_y, best_orient = nx, ny, getDirection(orient, 'R')
            elif relative == 'L' and not API.wallLeft():
                min_cost = flood[ny][nx]
                best_x, best_y, best_orient = nx, ny, getDirection(orient, 'L')
    return best_x, best_y, best_orient

def main():
    """Main function to initialize and start the flood-fill algorithm."""
    log("Starting Flood-Fill Algorithm...")
    initializeFlood()
    floodFill()
    moveToGoal()

# Start the program
main()
