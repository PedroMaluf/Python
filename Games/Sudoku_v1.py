import re
import sys
sys.setrecursionlimit(2000)

def find_next_empty(puzzle):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == -1:
                return i, j

    return None, None


def valorpermitido(puzzle, chute, row, col):
    if chute in puzzle[row]:
        return False

    if chute in [puzzle[i][col] for i in range(9)]:
        return False

    for i in range(row - (row % 3), row + 3 - (row % 3)):
        for j in range(col - (col % 3), col + 3 - (col % 3)):
            if i == row and j == col:
                continue
            if chute == puzzle[i][j]:
                return False

    return True


def resolve_sudoku(puzzle, posicoespreocupadas):
    row, col = find_next_empty(puzzle)

    if row is None:
        return True

    for chute in range(1, 10):
        if valorpermitido(puzzle, chute, row, col):
            puzzle[row][col] = chute
            if resolve_sudoku(puzzle, posicoespreocupadas):
                return True
        puzzle[row][col] = -1


    return False


if __name__ =='__main__':

    #ganhou = False

    #while not ganhou:

        #puzzle = [[-1 for _ in range(9)] for _ in range(9)]
    preocupados = [[None for _ in range(9)] for _ in range(9)]

    puzzle = [
        [3, 9, -1,   -1, 5, -1,   -1, -1, -1],
        [-1, -1, -1,   2, -1, -1,   -1, -1, 5],
        [-1, -1, -1,   7, 1, 9,   -1, 8, -1],

        [-1, 5, -1,   -1, 6, 8,   -1, -1, -1],
        [2, -1, 6,   -1, -1, 3,   -1, -1, -1],
        [-1, -1, -1,   -1, -1, -1,   -1, -1, 4],

        [5, -1, -1,   -1, -1, -1,   -1, -1, -1],
        [6, 7, -1,   1, -1, 5,   -1, 4, -1],
        [1, -1, 9,   -1, -1, -1,   2, -1, -1]
    ]

    for i in range(1,10):
        for j in range(1,10):
    #            print('Digite o valor (',i,',',j,'):')
    #            puzzle[i - 1][j - 1] = int(input())
            if puzzle[i - 1][j - 1] != -1:
                preocupados[i - 1][j - 1] = 1
    print(resolve_sudoku(puzzle, preocupados))

    print('Resolvido!')

    for i in range(9):
        for j in range(9):
            print(puzzle[i][j],' ', end = '')
        print('\n')
