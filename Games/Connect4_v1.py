import pygame
import time
import tkinter as tk
from tkinter import messagebox

rows = 7
columns = 7
width = 700
height = 700

class Cube(object):
    width = 700
    height = 700

    def __init__(self, start, color):
        self.pos = start
        self.color = color
        self.rows = 6
        self.columns = 7

    def movecubeprabaixo(self):
        self.pos = (self.pos[0], self.pos[1] + 1)

    def drawCube(self, surface):
        dis = self.width // self.columns
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis + 1, j*dis + 1, dis - 2, dis - 2))


def drawgrind(surface):
    squares_width = width // columns
    x = 0
    y = 0

    for _ in range(columns):
        x = x + squares_width
        pygame.draw.line(surface, (255,255,255), (x,0),(x,height))

    for _ in range(rows):
        y = y + squares_width
        pygame.draw.line(surface, (255,255,255), (0,y),(width,y))


def message_box(subject, content):
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def drawarrow(surface, color, pos):
    dis = width // rows
    centre = dis // 2

    pygame.draw.line(surface, color, (pos*dis + centre, 1),(pos*dis + centre, dis - 1),5)
    pygame.draw.line(surface, color, (pos*dis + centre, dis - 1),(pos*dis + 1 + centre/2, centre*3/2),5)
    pygame.draw.line(surface, color, (pos*dis + centre, dis - 1),((1 + pos)*dis - 1 - centre/2, centre*3/2),5)

def redrawWindow(surface, color, posseta, pospecas1, pospecas2, pos):
    surface.fill((0,0,0))
    drawgrind(surface)
    drawarrow(surface, color, posseta)
    for (i,j) in pospecas1:
        Cube((i,j), (255,215,0)).drawCube(surface)
    for (i,j) in pospecas2:
        Cube((i,j), (51,161,201)).drawCube(surface)
    if pos != -1:
        Cube((posseta, pos), color).drawCube(surface)
    pygame.display.update()


def vencedor(surface, cubovitoria, player):
    for (i,j) in cubovitoria:
        Cube((i,j), (255,0,0)).drawCube(surface)
        time.sleep(0.5)
        pygame.display.update()

    message_box('Ganhou!', 'Jogador {} venceu'.format(player))

def reset():
    return 0, [],[],[],[]


def main():
    wn = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()
    flag = True

    aux = 0
    pospecas1 = []
    pospecas2 = []
    colunas_completas = []
    cubovitoria = []

    while flag:
        if aux % 2 == 0:
            color = (255,215,0)
            player = 'AMARELO'
            pospecas = pospecas1
        else:
            color = (51,161,201)
            player = 'AZUL'
            pospecas = pospecas2

        posseta = 3
        down = False

        while not down:
            andadireita = False
            andaesquerda = False
            redrawWindow(wn, color, posseta, pospecas1, pospecas2, -1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                keys = pygame.key.get_pressed()

                for key in keys:
                    if keys[pygame.K_LEFT] and posseta > 0:
                        andaesquerda = True
                    elif keys[pygame.K_RIGHT] and posseta < columns - 1:
                        andadireita = True
                    elif keys[pygame.K_DOWN] and posseta not in colunas_completas:
                        down = True
            if andadireita:
                posseta += 1
            elif andaesquerda:
                posseta += -1

        for j in range(6):
            redrawWindow(wn, color, posseta, pospecas1, pospecas2, j + 1)
            time.sleep(0.5)
            if (posseta, j + 2) in pospecas1 or (posseta, j + 2) in pospecas2 or j + 2 == rows:
                if j == 0:
                    colunas_completas.append(posseta)
                if player == 'AMARELO':
                    pospecas1.append((posseta, j + 1))
                else:
                    pospecas2.append((posseta, j + 1))
                break

        aux += 1

        for i in range(7):
            na_coluna = 0
            for y in range(6):
                if na_coluna == 3:
                    vencedor(wn, cubovitoria, player)
                    aux, pospecas1, pospecas2, colunas_completas, cubovitoria = reset()
                    redrawWindow(wn, color, posseta, pospecas1, pospecas2, -1)
                    break
                j = y + 1
                if (i,j) in pospecas and (i,j + 1) in pospecas:
                    if na_coluna == 0:
                        cubovitoria.append((i,j))
                    cubovitoria.append((i,j + 1))
                    na_coluna += 1
                else:
                    na_coluna = 0
                    cubovitoria = []

        for y in range(6):
            j = y + 1
            na_linha = 0
            for i in range(7):
                if na_linha == 3:
                    vencedor(wn, cubovitoria, player)
                    aux, pospecas1, pospecas2, colunas_completas, cubovitoria = reset()
                    redrawWindow(wn, color, posseta, pospecas1, pospecas2, -1)
                    break
                elif (i,j) in pospecas and (i + 1,j) in pospecas:
                    if na_linha == 0:
                        cubovitoria.append((i,j))
                    cubovitoria.append((i + 1,j))
                    na_linha += 1
                else:
                    na_linha = 0
                    cubovitoria = []

        for i in range(7):
            for y in range(6):
                na_diagonaldir = 0
                if na_diagonaldir == 3:
                    vencedor(wn, cubovitoria, player)
                    aux, pospecas1, pospecas2, colunas_completas, cubovitoria = reset()
                    redrawWindow(wn, color, posseta, pospecas1, pospecas2, -1)
                    break
                j = y + 1
                for x in range(4):
                    if na_diagonaldir == 3:
                        break
                    elif (i,j) in pospecas and (i + 1 + x, j + 1 + x) in pospecas:
                        if na_diagonaldir == 0:
                            cubovitoria.append((i,j))
                        cubovitoria.append((i + 1 + x, j + 1 + x))
                        na_diagonaldir += 1
                    else:
                        na_diagonaldir = 0
                        cubovitoria = []

        for i in range(7):
            for y in range(6):
                na_diagonalesq = 0
                if na_diagonalesq == 3:
                    vencedor(wn, cubovitoria, player)
                    aux, pospecas1, pospecas2, colunas_completas, cubovitoria = reset()
                    redrawWindow(wn, color, posseta, pospecas1, pospecas2, -1)
                    break
                j = y + 1
                for x in range(4):
                    if na_diagonalesq == 3:
                        break
                    elif (i,j) in pospecas and (i - 1 - x, j - 1 - x) in pospecas:
                        if na_diagonalesq == 0:
                            cubovitoria.append((i,j))
                        cubovitoria.append((i - 1 - x, j - 1 - x))
                        na_diagonalesq += 1
                    else:
                        na_diagonalesq = 0
                        cubovitoria = []

        if len(pospecas1) + len(pospecas2) == 42:
            message_box('Empatou...', 'Jogar de novo')
            aux, pospecas1, pospecas2, colunas_completas, cubovitoria = reset()
            redrawWindow(wn, color, posseta, pospecas1, pospecas2, -1)


main()
