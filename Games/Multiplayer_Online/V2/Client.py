import pygame
from Network import Network
from Player import Player

width = 500
height = 500

wn = pygame.display.set_mode((width,height))
pygame.display.set_caption('Client')


def redrawWindow(wn, player, player2):
    wn.fill((0,0,0))
    player.draw(wn)
    player2.draw(wn)
    pygame.display.update()


def main():
    flag = True
    n = Network()

    p = n.getP()

    clock = pygame.time.Clock()

    while flag:
        clock.tick(60)
        p2 = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                pygame.quit()

        p.move()
        redrawWindow(wn, p, p2)


main()