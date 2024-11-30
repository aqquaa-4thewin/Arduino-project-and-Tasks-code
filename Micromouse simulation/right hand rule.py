import API
import sys

def log(string):
    """Logs messages for debugging."""
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def main():
    """Implements the Right-Hand Rule to solve the maze."""
    log("Running...")
    API.setColor(0, 0, "G")  # Mark the starting position with green
    API.setText(0, 0, "Start")  # Annotate the starting position

    while True:
        # If there is no wall on the right, turn right and move forward
        if not API.wallRight():
            API.turnRight()
            API.moveForward()
        # If there is a wall in front, turn left until the path is clear
        elif API.wallFront():
            API.turnLeft()
        # Otherwise, move forward
        else:
            API.moveForward()

if __name__ == "__main__":
    main()
