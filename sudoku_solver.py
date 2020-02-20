import numpy as np
from random import randint
from copy import deepcopy


def is_possible(y, x, n):
    global grid
    for i in range(0, 9):
        if grid[y][i] == n:
            return False
    for j in range(0, 9):
        if grid[j][x] == n:
            return False
    x0 = (x//3)*3
    y0 = (y//3)*3
    for k in range(0, 3):
        for l in range(0, 3):
            if grid[y0+k][x0+l] == n:
                return False
    return True


def solve_recursion():
    global grid, counter, solutions
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if is_possible(y, x, n):
                        grid[y][x] = n
                        solve_recursion()
                        grid[y][x] = 0
                return
    counter += 1
    solutions.append(deepcopy(grid))


## Global var
counter = 0
solutions = []
grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 0, 9]]

## Main
solve_recursion()
print("There are {} possible solutions".format(counter))
print("Random solution:")
print(np.matrix(solutions[randint(0, counter-1)]))
