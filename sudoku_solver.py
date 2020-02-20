import numpy as np
from random import randint
from copy import deepcopy
import cv2
import utils
import grid

# Global variables
sudoku_grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 0, 9]]
counter = 0
solutions = []


def is_possible(y, x, n):
    global sudoku_grid
    for i in range(0, 9):
        if sudoku_grid[y][i] == n:
            return False
    for j in range(0, 9):
        if sudoku_grid[j][x] == n:
            return False
    x0 = (x//3)*3
    y0 = (y//3)*3
    for k in range(0, 3):
        for l in range(0, 3):
            if sudoku_grid[y0+k][x0+l] == n:
                return False
    return True


def solve_recursion():
    global sudoku_grid, counter, solutions
    for y in range(9):
        for x in range(9):
            if sudoku_grid[y][x] == 0:
                for n in range(1, 10):
                    if is_possible(y, x, n):
                        sudoku_grid[y][x] = n
                        solve_recursion()
                        sudoku_grid[y][x] = 0
                return
    counter += 1
    solutions.append(deepcopy(sudoku_grid))


def main():
    global sudoku_grid, counter, solutions
    model = utils.load_mnist_model()
    img = cv2.imread("./SudokuOnline/puzzle1.jpg")

    sudoku_grid = grid.recognize_grid(model, img)

    solve_recursion()
    print("There are {} possible solutions".format(counter))
    if len(solutions) > 0:
        print("Random solution:")
        print(np.matrix(solutions[randint(0, counter - 1)]))


if __name__ == "__main__":
    main()

