import pygame
from Network import Network
pygame.font.init()

width = 700
height = 700
wn = pygame.display.set_mode((width,height))
pygame.display.set_caption('Client')


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, wn):
        pygame.draw.rect(wn, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('Arial', 40)
        text = font.render(self.text, 1, (255,255,255))
        wn.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(wn, game, player):
    global btns, wins, ties

    wn.fill((128,128,128))

    if not (game.connected()):
        font = pygame.font.SysFont('Arial', 40)
        text = font.render('Wait for Player...', 1, (255,255,255), True)
        wn.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont('Arial', 40)
        text = font.render('Your move', 1, (255,255,255), True)
        wn.blit(text, (80,200))

        text = font.render('Opponents', 1, (255,255,255), True)
        wn.blit(text, (620 - text.get_width(),200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        text1 = font.render('Waiting...', 1,(0,0,0))
        text2 = font.render('Waiting...', 1,(0,0,0))

        if game.bothWent() and player == 0:
            text1 = font.render(move1, 1,(0,0,0))
            text2 = font.render(move2, 1,(0,0,0))
        elif game.bothWent() and player == 1:
            text1 = font.render(move2, 1,(0,0,0))
            text2 = font.render(move1, 1,(0,0,0))
        elif player == 0 and game.p1Went:
            text1 = font.render(move1, 1,(0,0,0))
            text2 = font.render('Waiting...', 1,(0,0,0))
        elif (player == 0 and game.p2Went) or (player == 1 and game.p1Went):
            text1 = font.render('Waiting...', 1,(0,0,0))
            text2 = font.render('Locked in', 1,(0,0,0))
        elif player == 1 and game.p2Went:
            text1 = font.render(move2, 1,(0,0,0))
            text2 = font.render('Waiting...', 1,(0,0,0))

        wn.blit(text1, (80,250))
        wn.blit(text2, (620 - text.get_width(),250))

        for buttons in btns:
            buttons.draw(wn)


        textwins = font.render('Wins: ' + str(wins[player]), 1,(0,0,0))

        if player == 0:
            other_player = 1
        else:
            other_player = 0

        textlost = font.render('Lost: ' + str(wins[other_player]), 1,(0,0,0))
        textties = font.render('Ties: ' + str(ties), 1,(0,0,0))

        wn.blit(textwins, (50,10))
        wn.blit(textlost, (250,10))
        wn.blit(textties, (450,10))
    
    pygame.display.update()

    

btns = [Button('Rock', 50, 500,(0,0,0)), Button('Scissors', 250, 500,(255,0,0)), Button('Paper', 450, 500,(0,255,0))]
wins = [0,0]


def main():
    global ties

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

        if game.bothWent():
            redrawWindow(wn, game, player)
            pygame.time.delay(500)

            try:
                game = n.send('reset')
            except:
                flag = False
                break

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
                                game = n.send(buttons.text)

                        else:
                            if not game.p2Went:
                                game = n.send(buttons.text)
        
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