# BackTracking
KenKenPuzzle
As in Sudoku, the goal of each puzzle is to fill a grid with digits –– 1 through 4 for a 4×4 grid, 1 through 5 for a 5×5, 1 through 6 for a 6×6, etc. –– so that no digit appears more than once in any row or any column (a Latin square). Grids range in size from 3×3 to 9×9. Additionally, KenKen grids are divided into heavily outlined groups of cells –– often called “cages” –– and the numbers in the cells of each cage must produce a certain “target” number when combined using a specified mathematical operation (one of addition, subtraction, multiplication or division). For example, a linear three-cell cage specifying addition and a target number of 6 in a 4×4 puzzle must be satisfied with the digits 1, 2, and 3. Digits may be repeated within a cage, as long as they are not in the same row or column. No operation is relevant for a single-cell cage: placing the "target" in the cell is the only possibility (thus being a "free space"). The target number and operation appear in the upper left-hand corner of the cage.

In the English-language KenKen books of Will Shortz, the issue of the non-associativity of division and subtraction is addressed by restricting clues based on either of those operations to cages of only two cells in which the numbers may appear in any order. Hence if the target is 1 and the operation is - (subtraction) and the number choices are 2 and 3, possible answers are 2,3 or 3,2. Some puzzle authors have not done this and have published puzzles that use more than two cells for these operations.

# Measurements
Considering that we generate the KenKen board randomly for every instance of the program, we couldn't measure the performance of different algorithms under exactly the same conditions, so we chose to measure the performance of ten instances and publish their average for different board sizes. The performance is measured in the total number of assignments made during the whole running time of an algorithm.
The benchmarks are obtained using:
 - the simple backtracing algorithm that solves the puzzle
 - the backtracking algorithm that uses Minimum Remaining Values and Forward Checking
 - the backtracking algorithm that uses Minimum Remaining Values and Arc Consitency - 3
 
 
