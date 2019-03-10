from math import floor


def fillMiddle(text, width, background_character):
    '''
    Returns the 'text' field in the middle of 'width' filling remained
    characters with 'background_character'.

    :param text: text wanted to be in the middle of 'width' string
    :param width: width of the string
    :param background_character: fill character for the rest of the string
    :return: result
    '''
    textWidth = len(text)
    w_ = width - textWidth
    w = floor(w_ / 2)
    s = ""
    if (w_ % 2) == 0:
        # pair
        for i in range(0, w):
            s = s + background_character
        return s + text + s
    else:
        for i in range(0, w):
            s = s + background_character
        return s + background_character + text + s

    return "(PRINT_ERROR)"

def convertAssignmentToBoard(assignment, size):
    '''
    Converts the solvedGroups into board.
    board = easy to read for human structure
    '''
    # Initialize printed size x size board:
    board = [[0 for i in range(0, size + 1)] for i in range(0, size + 1)]

    for item in assignment:
        idx = 0
        for i in item:
            x = i[0]
            y = i[1]
            board[x][y] = assignment[item][idx]
            idx = idx + 1

    return board

def convertAssignmentToBoardIds(assignment, size):
    '''
        Converts the solvedGroups into id board.
        BoardIds = easy to read for human structure
        '''
    # Initialize printed size x size board:
    cellIds = [[0 for i in range(0, size + 1)] for i in range(0, size + 1)]

    count = 0
    for item in assignment:
        idx = 0
        for i in item:
            x = i[0]
            y = i[1]
            cellIds[x][y] = count + 1
        count = count + 1

    return cellIds

def printSimpleBoard(board, size):
    '''
    Printss a simple board.
    '''
    for i in range(1, size + 1):
        for j in range(1, size + 1):
            print(board[j][i], end=" ")
        print()
    print()

def printBoardIds(cellIds, size):
    '''
    Printss a simple board with cell's id.
    '''
    for i in range(1, size + 1):
        for j in range(1, size + 1):
            print(cellIds[j][i], end=" ")
        print()
    print()

def printUnsolvedBoard(meta, size):
    '''
    Prints the unsolved Board, ready to solve for human.
    '''
    # no board because no solution
    cellIds = convertAssignmentToBoardIds(assignment, size)

    # width = 0;
    # for i in range(1, size + 1):
    #     for j in range(1, size + 1):
    #         w = len(str(board[j][i]))
    #         if( w > width ):
    #             width = w

    # SETTINGS:

    width = 10  # default: 10
    height = 3  # default: 3
    background_char = " "  # default: " "
    left_spacing = "    "  # left spacing fot the operator and target number   default: "   "
    # tip: use "" for small width
    vdso = " "  # vertical_divider_symbol_open    default:   "|"    favorite:  " "
    vdsw = "|"  # vertical_divider_symbol_wall    default:   "l"    favorite:  "|"
    hdso = " "  # horizontal_divider_symbol_open  default:   "-"    favorite:  " "
    hdsw = "-"  # horizontal_divider_symbol_wall  default:   "="    favorite:  "-"

    lf = "|"  # right_closing_line_feed         default:   " "    favorite:  "|"

    # Used to be user if only once is the Operator and Target Printed
    groupOpAndTarget = [False for i in range(0, size * size)]  # size*size = Max possible ID numbers

    for i in range(1, size + 1):
        # Print line vertical divider
        # k iterates through columns on {i} row
        for k in range(1, size + 1):
            # print(vdso, end="")             #
            # for kk in range(0, width):     # old: without group separator
            #     print(hdso, end="")         #
            vertical_symbol = hdso
            try:
                if cellIds[k][i - 1] != cellIds[k][i]:  # checking upper cell (i,j are swapped)
                    vertical_symbol = hdsw
            finally:
                no_variable = 0

            for kk in range(0, width + 1):
                # leave the separator on the first last character because of the board border
                if kk == 0:  # or (k == size and kk == width):  # first or last
                    print(hdsw, end="")
                else:
                    print(vertical_symbol, end="")
        print(vdso)

        # Print vertical Cell lines
        # line number = height
        for h in range(0, height):

            for j in range(1, size + 1):
                horizontal_symbol = vdso

                try:
                    if cellIds[j - 1][i] != cellIds[j][i]:  # checking upper cell (i,j are swapped)
                        horizontal_symbol = vdsw
                finally:
                    no_variable = 0

                print(horizontal_symbol, end="")
                # cell width = width
                s = ""
                for w in range(0, width):
                    s = s + background_char

                # Modify S int to print inside

                # in the first line (target + operator):
                if h == 0:
                    # only print once / group
                    idd = cellIds[j][i]
                    if not groupOpAndTarget[idd]:  # ..[currentID]
                        groupOpAndTarget[cellIds[j][i]] = True
                        operator = "o"
                        target = "t"
                        # ind current cell data
                        for data in meta:  # throug operation_groups
                            for point in data:  # trough operation_group cells
                                if point[0] == j and point[1] == i:  # if cell is the current printing chell
                                    operator = meta[data][0]
                                    target = str(meta[data][1])

                        display = target + " " + operator + left_spacing
                        s = fillMiddle(display, width, background_char)

                # in the middle line (result):
                # if h == floor(height / 2):
                 #    s = fillMiddle(str(board[j][i]), width, background_char)

                print(s, end="")
            print(vdso, end="")
            print(lf)

    # Print last line vertical divider
    for k in range(0, size):
        print("|", end="")
        for kk in range(0, width):
            print(hdsw, end="")
    print("|")

    print("\n")

def printSolvedBoard(meta, assignment, size):
    '''
    Prints the solved Board, human readable.
    '''
    board = convertAssignmentToBoard(assignment, size)
    cellIds = convertAssignmentToBoardIds(assignment, size)

    # width = 0;
    # for i in range(1, size + 1):
    #     for j in range(1, size + 1):
    #         w = len(str(board[j][i]))
    #         if( w > width ):
    #             width = w

    # SETTINGS:

    width = 10  # default: 10
    height = 3  # default: 3
    background_char = " "  # default: " "
    left_spacing = "    "  # left spacing fot the operator and target number   default: "   "
    # tip: use "" for small width
    vdso = " "  # vertical_divider_symbol_open    default:   "|"    favorite:  " "
    vdsw = "|"  # vertical_divider_symbol_wall    default:   "l"    favorite:  "|"
    hdso = " "  # horizontal_divider_symbol_open  default:   "-"    favorite:  " "
    hdsw = "-"  # horizontal_divider_symbol_wall  default:   "="    favorite:  "-"

    lf = "|"  # right_closing_line_feed         default:   " "    favorite:  "|"

    # Used to be user if only once is the Operator and Target Printed
    groupOpAndTarget = [False for i in range(0, size * size)]  # size*size = Max possible ID numbers

    for i in range(1, size + 1):
        # Print line vertical divider
        # k iterates through columns on {i} row
        for k in range(1, size + 1):
            # print(vdso, end="")             #
            # for kk in range(0, width):     # old: without group separator
            #     print(hdso, end="")         #
            vertical_symbol = hdso
            try:
                if cellIds[k][i - 1] != cellIds[k][i]:  # checking upper cell (i,j are swapped)
                    vertical_symbol = hdsw
            finally:
                no_variable = 0

            for kk in range(0, width + 1):
                # leave the separator on the first last character because of the board border
                if kk == 0:  # or (k == size and kk == width):  # first or last
                    print(hdsw, end="")
                else:
                    print(vertical_symbol, end="")
        print(vdso)

        # Print vertical Cell lines
        # line number = height
        for h in range(0, height):

            for j in range(1, size + 1):
                horizontal_symbol = vdso

                try:
                    if cellIds[j - 1][i] != cellIds[j][i]:  # checking upper cell (i,j are swapped)
                        horizontal_symbol = vdsw
                finally:
                    no_variable = 0

                print(horizontal_symbol, end="")
                # cell width = width
                s = ""
                for w in range(0, width):
                    s = s + background_char

                # Modify S int to print inside

                # in the first line (target + operator):
                if h == 0:
                    # only print once / group
                    idd = cellIds[j][i]
                    if not groupOpAndTarget[idd]:  # ..[currentID]
                        groupOpAndTarget[cellIds[j][i]] = True
                        operator = "o"
                        target = "t"
                        # ind current cell data
                        for data in meta:  # throug operation_groups
                            for point in data:  # trough operation_group cells
                                if point[0] == j and point[1] == i:  # if cell is the current printing chell
                                    operator = meta[data][0]
                                    target = str(meta[data][1])

                        display = target + " " + operator + left_spacing
                        s = fillMiddle(display, width, background_char)

                # in the middle line (result):
                if h == floor(height / 2):
                    s = fillMiddle(str(board[j][i]), width, background_char)

                print(s, end="")
            print(vdso, end="")
            print(lf)

    # Print last line vertical divider
    for k in range(0, size):
        print("|", end="")
        for kk in range(0, width):
            print(hdsw, end="")
    print("|")

    print("\n")