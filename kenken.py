import sys
import random
import functools

def operation(operator):
    #converting the 'operator' to a real operation
    if operator == '+':
        return lambda a, b: a + b
    elif operator == '-':
        return lambda a, b: a - b
    elif operator == '*':
        return lambda a, b: a * b
    elif operator == '/':
        return lambda a, b: a / b
    else:
        return None

def are_neighbours(point1, point2):
    #checking if two cells are neighbours
    x1, y1 = point1
    x2, y2 = point2

    dx = x1 - x2
    dy = y1 - y2

    return (dx == 0 and abs(dy) == 1) or (dy == 0 and abs(dx) == 1)

#generating a board
def generate(size):
    board = [[((i + j) % size) + 1 for i in range(size)] for j in range(size)]

    # Shuffle the rows and columns
    for _ in range(size):
        random.shuffle(board)

    for c1 in range(size):
        for c2 in range(size):
            if random.random() > 0.5:
                for r in range(size):
                    board[r][c1], board[r][c2] = board[r][c2], board[r][c1]

    board = {(j + 1, i + 1): board[i][j] for i in range(size) for j in range(size)}

    uncaged = sorted(board.keys(), key=lambda var: var[1])

    operand_groups = []
    while uncaged:

        operand_groups.append([])

        csize = random.randint(1, 4)

        cell = uncaged[0]

        uncaged.remove(cell)

        operand_groups[-1].append(cell)

        for _ in range(csize - 1):

            adjs = [other for other in uncaged if are_neighbours(cell, other)]

            cell = random.choice(adjs) if adjs else None

            if not cell:
                break

            uncaged.remove(cell)

            operand_groups[-1].append(cell)

        csize = len(operand_groups[-1])
        if csize == 1:
            cell = operand_groups[-1][0]
            operand_groups[-1] = ((cell,), '.', board[cell])
            continue
        elif csize == 2:
            fst, snd = operand_groups[-1][0], operand_groups[-1][1]
            if board[fst] / board[snd] > 0 and not board[fst] % board[snd]:
                operator = "/"  # choice("+-*/")
            else:
                operator = "-"  # choice("+-*")
        else:
            operator = random.choice("+*")

        target = functools.reduce(operation(operator), [board[cell] for cell in operand_groups[-1]])

        operand_groups[-1] = (tuple(operand_groups[-1]), operator, int(target))

    return size, operand_groups

def print_operand_group(operand_group, shift = "", header = True):
    #shift: shifting text to left with a given number
    #header: shows or hides the header
    if header:
        print( shift + "operand_group:")
    print( shift + "| {%c}" %(operand_group[1]) )
    print( shift + "| {%i}" %(operand_group[2]) )
    print( shift + "| cells:")
    for point in operand_group[0]:
        print( shift +  "    | (%i,%i)" % (point[0], point[1]))



def print_operand_groups(operand_groups):
    #print elemets of an operand group
    print("\noperand_groups:")
    count = 0
    for item in operand_groups:
        print("| operand_groups[%i]:" % count)
        print_operand_group(item, "| ", False)
        print("|")
        count = count + 1


if __name__ == "__main__":
    size = 6
    algorithm = 2

    if len(sys.argv) == 3:
        # size of the problem
        size = int(sys.argv[1])

        # algorithm number
        algorithm = int(sys.argv[2])

    # generate board:
    #  operand_groups stores multiple operand_group's which contains:
    #    cells stored as X,Y coordinates,
    #    operation stored as char
    #    target value stored as int
    #   in form like this:
    #    [ ( ((<x>,<y>),(<x>,<y>), ... ), '<operator>', <target> ) , ... ]
    size, operand_groups = generate(size)

    print_operand_groups(operand_groups)

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