import sys
import random
import functools
import backtracking
from itertools import permutations, product
from functools import reduce

import boardprinter


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
    #creating a size x size board
    board = [[((i + j) % size) + 1 for i in range(size)] for j in range(size)]

    #shuffle the rows and columns
    for _ in range(size):
        random.shuffle(board)

    for c1 in range(size):
        for c2 in range(size):
            if random.random() > 0.5:
                for r in range(size):
                    board[r][c1], board[r][c2] = board[r][c2], board[r][c1]

    board = {(j + 1, i + 1): board[i][j] for i in range(size) for j in range(size)}

    #the cells without the index of group that we want to put into groups later
    uncaged = sorted(board.keys(), key=lambda var: var[1])

    operand_groups = []
    #putting the operands, variables and targets into operand_groups
    while uncaged:

        operand_groups.append([])

        csize = random.randint(1, 4)
        #taking the first element from the uncaged list, then put it to the operand_group
        cell = uncaged[0]

        uncaged.remove(cell)

        operand_groups[-1].append(cell)

        for _ in range(csize - 1):
            #adjs contains the neighbours of the choosen cell
            adjs = [other for other in uncaged if are_neighbours(cell, other)]
            #one of the adjs join for the group of the cell
            cell = random.choice(adjs) if adjs else None

            if not cell:
                break

            uncaged.remove(cell)

            operand_groups[-1].append(cell)

        csize = len(operand_groups[-1])
        #check the size of the game and give the range of the operations
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
        #generating the target from the values and the random operator
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

########################################################################
def is_different_row_or_column(xy1, xy2):
    """
    Checks if they  are in the same row / column
    
    """
    return (xy1[0] == xy2[0]) != (xy1[1] == xy2[1])

def is_conflicting(A, a, B, b):
    """
   Checks if they are in conflict
    """
    for i in range(len(A)):
        for j in range(len(B)):
            mA = A[i]
            mB = B[j]

            ma = a[i]
            mb = b[j]
            if is_different_row_or_column(mA, mB) and ma == mb:
                return True

    return False

def is_satisfies(values, operation, target):
    """
    Checks if the permutation of a value is equal to the specified target.
    Calls the permutation form python library
    """
    for p in permutations(values):
        if reduce(operation, p) == target:
            return True

    return False

def generate_domains(size, operand_groups):
    """
       Generates the domains
    """
    domains = {}
    # iterate over the groups
    for operand_group in operand_groups:
        cells, operator, target = operand_group

        domains[cells] = list(product(range(1, size + 1), repeat=len(cells)))

        qualifies = lambda values: not is_conflicting(cells, values, cells, values) and is_satisfies(values, operation(operator), target)

        domains[cells] = list(filter(qualifies, domains[cells]))
    # finally  return the domains
    return domains

def generate_neighbors(operand_groups):
    """   
    Adding the neighbours  
    """
    neighbors = {}
    for cells, _, _ in operand_groups:
        neighbors[cells] = []

    for A, _, _ in operand_groups:
        for B, _, _ in operand_groups:
            if A != B and B not in neighbors[A]:
                if is_conflicting(A, [-1] * len(A), B, [-1] * len(B)):
                    neighbors[A].append(B)
                    neighbors[B].append(A)

    return neighbors


########################################################################

class Kenken(backtracking.Backtrack):
    # Class initialization
    def __init__(self, size, operand_groups):
        variables = [cells for cells, _, _ in operand_groups]
        domains = generate_domains(size, operand_groups)
        neighbors = generate_neighbors(operand_groups)

        backtracking.Backtrack.__init__(self, variables, domains, neighbors, self.constraint)

        self.size = size

        # Sets the checks
        self.checks = 0

        # For displaying
        self.padding = 0

        self.meta = {}
        for cells, operator, target in operand_groups:
            self.meta[cells] = (operator, target)
            self.padding = max(self.padding, len(str(target)))

    def constraint(self, A, a, B, b):
          
            # Adds the check at every call
            self.checks += 1

            return A == B or not is_conflicting(A, a, B, b)

    def display(self, assignment):
        # printUnsolvedBoard(self.meta, size)
        boardprinter.printSolvedBoard(self.meta, assignment, size)

if __name__ == "__main__":
    size = 6
    algorithm = 1

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

    # print_operand_groups(operand_groups)

    ken = Kenken(size, operand_groups)


    if algorithm == 1:
        # backtracking
        assignments, board = backtracking.just_backtracking(ken, {})
    elif algorithm == 2:
        # backtracking + mrv + fwcheck
        assignments, board = 0,0 # backtracking.advanced_backtracking_with_forward_checking (ken, {})
    elif algorithm == 3:
        # backtracking + mrv + AC3
        assignments, board = backtracking.advanced_backtracking_with_ac3(ken, {})

    ken.display(board)

    print("Constraint checks:", ken.checks)
    print("Assignments:", assignments)
