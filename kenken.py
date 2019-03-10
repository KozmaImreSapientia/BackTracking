import sys
import random
import functools
import backtracking
from itertools import permutations, product
from functools import reduce

import backtracking


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


class Kenken(backtracking.Backtrack):

    def __init__ (self, size, operand_groups):
        """
        In my implementation, I consider the operand_groups themselves as variables.
        A operand_group is of the format (((X1, Y1), ..., (XN, YN)), <operation>, <target>)
        where
            * (X1, Y1), ..., (XN, YN) are the members of the operand_group
            * <operation> is either addition, subtraction, division or multiplication
            * <target> is the value that the <operation> should produce
              when applied on the members of the operand_group
        """

        variables = [members for members, _, _ in operand_groups]

        domains = generate_domains(size, operand_groups)

        neighbors = generate_neighbors(operand_groups)

        backtracking.Backtrack.__init__(self, variables, domains, neighbors, self.constraint)

        self.size = size

        # Used in benchmarking
        self.checks = 0

        # Used in displaying
        self.padding = 0

        self.meta = {}
        for members, operator, target in operand_groups:
            self.meta[members] = (operator, target)
            self.padding = max(self.padding, len(str(target)))

            # def nconflicts(self, var, val, board):

    # def assign(self, var, val, board):

    # def unassign(self, var, board):

    def constraint (self, A, a, B, b):
        """
        Any two variables satisfy the constraint if they are the same
        or they are not 'conflicting' i.e. every member of variable A
        which shares the same row or column with a member of variable B
        must not have the same value assigned to it
        """
        self.checks += 1

        return A == B or not is_conflicting(A, a, B, b)

    def display (self, board):
        """
        Print the kenken puzzle in a format easily readable by a human
        """
        if board:
            atomic = {}
            for members in self.variables:
                values = board.get(members)

                if values:
                    for i in range(len(members)):
                        atomic[members[i]] = values[i]
                else:
                    for member in members:
                        atomic[member] = None
        else:
            atomic = {member: None for members in self.variables for member in members}

        atomic = sorted(atomic.items(), key=lambda item: item[0][1] * self.size + item[0][0])

        padding = lambda c, offset: (c * (self.padding + 2 - offset))

        embrace = lambda inner, beg, end: beg + inner + end

        mentioned = set()

        def meta (member):
            for var, val in self.meta.items():
                if member in var and var not in mentioned:
                    mentioned.add(var)
                    return str(val[1]) + " " + (val[0] if val[0] != "." else " ")

            return ""

        fit = lambda word: padding(" ", len(word)) + word + padding(" ", 0)

        cpadding = embrace(2 * padding(" ", 0), "|", "") * self.size + "|"

        def show (row):

            rpadding = "".join(["|" + fit(meta(item[0])) for item in row]) + "|"

            data = "".join(["|" + fit(str(item[1] if item[1] else "")) for item in row]) + "|"

            print(rpadding, data, cpadding, sep="\n")

        rpadding = embrace(2 * padding("-", 0), "+", "") * self.size + "+"

        print(rpadding)
        for i in range(1, self.size + 1):
            show(list(filter(lambda item: item[0][1] == i, atomic)))

            print(rpadding)


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

    print_operand_groups(operand_groups)

    ken = Kenken(size, operand_groups)

    if algorithm == 1:
        # backtracing
        assignments, board = backtracking.just_backtracking(ken, {})
    elif algorithm == 2:
        # backtracing + mrv + fwcheck
        assignments, board = 0, 0
    elif algorithm == 3:
        # backtracking + mrv + AC3
        assignments, board = 0, 0

    # ken.display(board)

    print("Constraint checks:", ken.checks)
    print("Assignments:", assignments)
