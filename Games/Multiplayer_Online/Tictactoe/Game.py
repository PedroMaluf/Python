import pygame


class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = True
        self.ready = False
        self.id = id
        self.moves = [[], []]

    def get_player_move(self, p):
        return self.moves[p]
    
    def play(self, player, move):

        self.moves[player].append(move)

        if player == 0:
            self.p1Went = True
            self.p2Went = False
        else:
            self.p2Went = True
            self.p1Went = False
    
    def connected(self):
        return self.ready

    def winner(self):

        p1 = self.moves[0]
        p2 = self.moves[1]

        winner = -1

        for i in range(3):
            if ((i,0) in p1) and ((i,1) in p1) and ((i,2) in p1):
                winner = 0
            elif ((i,0) in p2) and ((i,1) in p2) and ((i,2) in p2):
                winner = 1
            elif ((0,i) in p1) and ((1,i) in p1) and ((2,i) in p1):
                winner = 0
            elif ((0,i) in p2) and ((1,i) in p2) and ((2,i) in p2):
                winner = 1
        
        if (((0,0) in p1) and ((1,1) in p1) and ((2,2) in p1)) or (((0,2) in p1) and ((1,1) in p1) and ((2,0) in p1)):
            winner = 0
        elif (((0,0) in p2) and ((1,1) in p2) and ((2,2) in p2)) or (((0,2) in p2) and ((1,1) in p2) and ((2,0) in p2)):
            winner = 0
        
        return winner

    def reset(self):
        self.moves=[[],[]]

