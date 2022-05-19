from jogadordavelha import RealPlayer, PCPlayer, PCPlayerHARD
import time

class JogoVelhas:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| '+' | '.join(row)+' |')
        print('')

    @staticmethod
    def print_board_nums():
        number_board = [[str(i)for i in range(j*3, (1+j)*3)] for j in range(3)]
        for row in number_board:
            print('| '+' | '.join(row)+' |')
        print('')

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        self.board[square] = letter
        if self.winner(square, letter):
            self.current_winner = letter
        return True

    def winner(self, square, letter):
        row_ind = square // 3
        col_ind = square % 3

        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([x == letter for x in row]):
            return True

        col = [self.board[col_ind+i*3] for i in range(3)]
        if all([x == letter for x in col]):
            return True

        if square % 2 ==0:
            diag1 = [self.board[i] for i in [0,4,8]]
            if all([x == letter for x in diag1]):
                return True

            diag2 = [self.board[i] for i in [2,4,6]]
            if all([x == letter for x in diag2]):
                return True

        return False

def play(game, xplayer, oplayer, print_game = True):
    if print_game:
        game.print_board_nums()

    letter = 'X'

    while game.empty_squares():
        if letter == 'O':
            square = oplayer.get_move(game)
        else:
            square = xplayer.get_move(game)

        if game.make_move(square, letter):
            if print_game:
                game.print_board()

            if game.current_winner:
                if print_game:
                    print(letter + ' ganho!')
                return letter

            letter = 'O' if letter == 'X' else 'X'
            #time.sleep(1)

    if print_game:
        print('empate')

if __name__ == '__main__':
    player1 = int(input("Quem vai ser o Player 1?\n1 - Pessoa\n2 - PC Aleatorio\n3 - PC HARD\nDigite a opção desejada: "))
    player2 = int(input("Quem vai ser o Player 1?\n1 - Pessoa\n2 - PC Aleatorio\n3 - PC HARD\nDigite a opção desejada: "))

    xplayer = RealPlayer('X') if player1 == 1 else PCPlayer('X') if player1 == 2 else PCPlayerHARD('X')
    oplayer = RealPlayer('O') if player2 == 1 else PCPlayer('O') if player2 == 2 else PCPlayerHARD('O')

    t = JogoVelhas()
    play(t, xplayer, oplayer, print_game = True)
        
