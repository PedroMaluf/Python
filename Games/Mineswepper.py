import random
import re

class fakeBoard:
    def __init__(self, dim_size):
        self.dim_size = dim_size


        self.dug = set()

    def make_new_board(self):

        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]


        return board


    def __str__(self):
        # this is a magic function where if you call print on this object,
        # it'll print out what this function returns!
        # return a string that shows the board to the player

        # first let's create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


class Board:
    def __init__(self, dim_size, num_bombs, initrow, initcol):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        self.board = self.make_new_board(initrow, initcol)
        self.assing_values_to_board()

        self.dug = set()

    def make_new_board(self, initrow, initcol):

        first_move = False

        while not first_move:
            board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
            bomb_planted = 0
            while bomb_planted < self.num_bombs:
                rowloc = random.randint(0, self.dim_size - 1)  # we want the number of times dim_size goes into loc to tell us what row to look at
                colloc = random.randint(0, self.dim_size - 1)

                if board[rowloc][colloc] == 'B':
                    continue
                board[rowloc][colloc] = 'B'
                bomb_planted += 1
            if board[initrow][initcol] != 'B':
                first_move = True
        return board

    def assing_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == 'B':
                    continue
                self.board[r][c] = self.get_num_bombs_around(r, c)

    def get_num_bombs_around(self, r, c):
        num_bombs_around = 0
        for auxr in range(max(0, r - 1), min(self.dim_size - 1, r + 1)+1):
            for auxc in range(max(0, c - 1), min(self.dim_size - 1, c + 1)+1):
                if auxr == r and auxc == c:
                    continue
                if self.board[auxr][auxc] == 'B':
                    num_bombs_around += 1
        return num_bombs_around

    def dig(self, row, col):
        self.dug.add((row,col))

        if self.board[row][col] == 'B':
            return False
        elif self.board[row][col] > 0:
            return True

        for auxr in range(max(0, row - 1), min(self.dim_size - 1, row + 1)+1):
            for auxc in range(max(0, col - 1), min(self.dim_size - 1, col + 1)+1):
                if (auxr, auxc) in self.dug:
                    continue
                self.dig(auxr, auxc)
        return True


    def __str__(self):
        # this is a magic function where if you call print on this object,
        # it'll print out what this function returns!
        # return a string that shows the board to the player

        # first let's create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

def play(dim_size, num_bombs):

    fakeboard = fakeBoard(dim_size)
    print(fakeboard)

    aux = False

    while not aux:
        user_input = re.split(',(\\s)*', input('Onde vc quer cavar?\nDigite como \"linha,coluna\":'))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= dim_size or col < 0 or col >= dim_size:
            print('Num pode essa possição não')
            continue
        aux = True


    board = Board(dim_size, num_bombs, row, col)

    safe = board.dig(row, col)

    while len(board.dug) < dim_size**2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input('Onde vc quer cavar?\nDigite como \"linha,coluna\":'))
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= dim_size or col < 0 or col >= dim_size:
            print('Num pode essa possição não')
            continue

        safe = board.dig(row,col)
        if not safe:
            print('\n\nOlha a bomba!\n\nPERDEU!\n')
            board.dug = [(r,c) for r in range(dim_size) for c in range(dim_size)]
            print(board)
            break

    if safe:
        print('GANHO!!')
        board.dug = [(r,c) for r in range(dim_size) for c in range(dim_size)]
        print(board)

if __name__ =='__main__':

    ver = False

    while not ver:
        tamanho = int(input('Qual o tamanho dos lados do campo?'))
        bombas = int(input('Quantas bombas?'))

        if bombas < tamanho**2:
            ver = True
        else:
            print('Tem muita bomba ai')


    play(tamanho, bombas)
