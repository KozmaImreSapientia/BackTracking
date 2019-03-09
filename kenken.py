import sys

if __name__ == "__main__":
    size = 6
    algorithm = 2

    if len(sys.argv) == 3:
        # size of the problem
        size = int(sys.argv[1])

        # algorithm number
        algorithm = int(sys.argv[2])

    # generate board

    if algorithm == 1:
        # backtracing
        1
    elif algorithm == 2:
        # backtracing + mrv + fwcheck
        2
    elif algorithm == 3:
        # backtracking + mrv + AC3
        3

    #print("Constraint checks:", ...)
    #print("Assignments:", ...)