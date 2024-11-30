#include <stdio.h>

// Define constants for directions
#define NORTH 0
#define EAST 1
#define SOUTH 2
#define WEST 3

// Maze dimensions
#define ROWS 7
#define COLS 7

// Function prototypes
void moveForward(int *x, int *y, int direction);
void turnLeft(int *direction);
void turnRight(int *direction);
int wallOnLeft(int maze[ROWS][COLS], int x, int y, int direction);
int wallInFront(int maze[ROWS][COLS], int x, int y, int direction);
int reachedGoal(int x, int y, int goalX, int goalY);

int main() {
    // Maze representation: 1 = Wall, 0 = Path
    int maze[ROWS][COLS] = {
        {1, 1, 1, 1, 1, 1, 1},
        {1, 0, 0, 0, 1, 0, 1},
        {1, 0, 1, 0, 1, 0, 1},
        {1, 0, 1, 0, 0, 0, 1},
        {1, 0, 1, 1, 1, 0, 1},
        {1, 0, 0, 0, 1, 0, 1},
        {1, 1, 1, 1, 1, 1, 1}
    };

    // Start and goal positions
    int startX = 1, startY = 1;  // Starting at (1, 1)
    int goalX = 5, goalY = 5;    // Goal at (5, 5)

    // Robot's current position and direction
    int x = startX, y = startY;
    int direction = NORTH;

    // Simulation loop
    printf("Starting maze navigation...\n");
    while (!reachedGoal(x, y, goalX, goalY)) {
        if (!wallOnLeft(maze, x, y, direction)) {
            turnLeft(&direction);
            moveForward(&x, &y, direction);
        } else if (!wallInFront(maze, x, y, direction)) {
            moveForward(&x, &y, direction);
        } else {
            turnRight(&direction);
        }

        // Print current position and direction
        printf("Robot is at (%d, %d), direction: %d\n", x, y, direction);
    }

    printf("Robot reached the goal at (%d, %d)!\n", x, y);
    return 0;
}

// Move the robot forward in the current direction
void moveForward(int *x, int *y, int direction) {
    if (direction == NORTH) (*y)--;
    else if (direction == EAST) (*x)++;
    else if (direction == SOUTH) (*y)++;
    else if (direction == WEST) (*x)--;
}

// Turn the robot left
void turnLeft(int *direction) {
    *direction = (*direction + 3) % 4;  // Equivalent to subtracting 1 with wrap-around
}

// Turn the robot right
void turnRight(int *direction) {
    *direction = (*direction + 1) % 4;  // Equivalent to adding 1 with wrap-around
}

// Check if there's a wall on the robot's left
int wallOnLeft(int maze[ROWS][COLS], int x, int y, int direction) {
    if (direction == NORTH) return maze[x - 1][y] == 1;
    if (direction == EAST)  return maze[x][y - 1] == 1;
    if (direction == SOUTH) return maze[x + 1][y] == 1;
    if (direction == WEST)  return maze[x][y + 1] == 1;
    return 1;  // Default to "wall present"
}

// Check if there's a wall in front of the robot
int wallInFront(int maze[ROWS][COLS], int x, int y, int direction) {
    if (direction == NORTH) return maze[x][y - 1] == 1;
    if (direction == EAST)  return maze[x + 1][y] == 1;
    if (direction == SOUTH) return maze[x][y + 1] == 1;
    if (direction == WEST)  return maze[x - 1][y] == 1;
    return 1;  // Default to "wall present"
}

// Check if the robot has reached the goal
int reachedGoal(int x, int y, int goalX, int goalY) {
    return x == goalX && y == goalY;
}
