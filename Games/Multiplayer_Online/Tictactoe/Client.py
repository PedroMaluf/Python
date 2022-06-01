import pygame
from Network import Network
import socket
pygame.font.init()

width = 500
height = 500
wn = pygame.display.set_mode((width,height))
pygame.display.set_caption('Client')


class Button:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(wn, game, player):
    global wins, ties

    wn.fill((0,0,0))

    if not (game.connected()):
        font = pygame.font.SysFont('Arial', 40)
        text = font.render('Wait for Player...', 1, (255,255,255), True)
        wn.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        dis = 100

        for x in range(2):
            pygame.draw.line(wn,(255,255,255),(200+dis*x,100),(200+dis*x,400))
            pygame.draw.line(wn,(255,255,255),(100,200+dis*x),(400,200+dis*x))

        font = pygame.font.SysFont('Arial', 40)

        if player == 0:
            text1 = font.render('X', 1, (255,255,255), True)
            text2 = font.render('O', 1, (255,255,255), True)
            other_player = 1
        else:
            text1 = font.render('O', 1, (255,255,255), True)
            text2 = font.render('X', 1, (255,255,255), True)
            other_player = 0


        for (i,j) in game.moves[player]:
            wn.blit(text1,(150+100*i - text1.get_width()/2, 150+100*j - text1.get_height()/2))
        
        for (i,j) in game.moves[other_player]:
            wn.blit(text2,(150+100*i - text2.get_width()/2, 150+100*j - text2.get_height()/2))


        font = pygame.font.SysFont('Arial', 30)
        textwins = font.render('Wins: ' + str(wins[player]), 1,(255,255,255))

        if player == 0:
            other_player = 1
            if game.p1Went:
                textturn = font.render('Opponent turn', 1,(255,255,255))
            else:
               textturn = font.render('Your turn', 1,(255,255,255))
        else:
            other_player = 0
            if game.p2Went:
                textturn = font.render('Opponent turn', 1,(255,255,255))
            else:
               textturn = font.render('Your turn', 1,(255,255,255))

        textlost = font.render('Lost: ' + str(wins[other_player]), 1,(255,255,255))
        textties = font.render('Ties: ' + str(ties), 1,(255,255,255))

        wn.blit(textturn, (250 - textturn.get_width()/2,40))
        wn.blit(textwins, (50 - textwins.get_width()/2,10))
        wn.blit(textlost, (250 - textlost.get_width()/2,10))
        wn.blit(textties, (450 - textties.get_width()/2,10))
    
    pygame.display.update()

    

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + ',' + str(tup[1])
    

btns = [Button(100,100), Button(200,100), Button(300,100), Button(100,200), Button(200,200), Button(300,200), Button(100,300), Button(200,300), Button(300,300)]
wins = [0,0]


def main():
    global ties, btns

    flag = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    ties = 0


    while flag:
        clock.tick(60)

        try:
            game = n.send('get')
        except:
            flag = False
            break

        if len(game.moves[0]) + len(game.moves[1]) == 9 or game.winner() != -1:
            redrawWindow(wn, game, player)
            pygame.time.delay(500)

            font = pygame.font.SysFont('Arial', 90)

            if player == game.winner():
                message = 'You won!'
                wins[player] += 1
            elif game.winner() == -1:
                message = 'Tie'
                ties += 1
            else:
                if player == 0:
                    other_player = 1
                else:
                    other_player = 0

                message = 'You lost!'
                wins[other_player] += 1

            text = font.render(message, 1, (255,0,0))
            wn.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

            try:
                game = n.send('reset')
                btns = [Button(100,100), Button(200,100), Button(300,100), Button(100,200), Button(200,200), Button(300,200), Button(100,300), Button(200,300), Button(300,300)]
            except socket.error as e:
                print(e)
                flag = False
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for buttons in btns:
                    if buttons.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                game = n.send(make_pos((buttons.x/100 - 1, buttons.y/100 - 1)))
                        else:
                            if not game.p2Went:
                                game = n.send(make_pos((buttons.x/100 - 1, buttons.y/100 - 1)))                 

        for i, buttons in enumerate(btns):
            if ((int(buttons.x/100 - 1),int(buttons.y/100 - 1)) in game.moves[0]) or ((int(buttons.x/100 - 1),int(buttons.y/100 - 1)) in game.moves[1]):
                        del btns[i]
        
        redrawWindow(wn, game, player)


def menu_screen():
    flag = True
    clock = pygame.time.Clock()

    wn.fill((0,0,0))
    while flag:
        clock.tick(60)
        wn.fill((0,0,0))
        font = pygame.font.SysFont('Arial', 40)
        text = font.render('Click anywhere to connect', 1, (255,255,255))
        wn.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                flag = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                flag = False    


    main()

while True:
    menu_screen()