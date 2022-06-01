import random
import pygame
import tkinter as tk
from tkinter import messagebox

#Classe das formas
class Formas(object):
    body = []

    def __init__(self, pos):
        self.rows = 20
        self.columns = 10
        self.dirnx = 0
        self.forma = random.choice(['O','I','S','Z','L','J','T'])

        if self.forma == 'O':
            self.head = Cube(pos,(255,215,0))
            self.body.append(self.head)
            for i in range(2):
                for j in range(2):
                    if i == 0 and j == 0:
                        continue
                    self.body.append(Cube((self.head.pos[0] + i, self.head.pos[1] + j),(255,215,0)))
        elif self.forma == 'I':
            self.head = Cube(pos, (51,161,201))
            self.body.append(self.head)
            for i in range(3):
                self.body.append(Cube((self.head.pos[0], self.head.pos[1] + i+1), (51,161,201)))
        elif self.forma == 'S':
            self.head = Cube(pos,(255,0,0))
            self.body.append(self.head)
            self.body.append(Cube((self.head.pos[0] - 1, self.head.pos[1]),(255,0,0)))
            self.body.append(Cube((self.head.pos[0] - 1, self.head.pos[1] + 1),(255,0,0)))
            self.body.append(Cube((self.head.pos[0] - 2, self.head.pos[1] + 1),(255,0,0)))
        elif self.forma == 'Z':
            self.head = Cube(pos,(48,128,20))
            self.body.append(self.head)
            self.body.append(Cube((self.head.pos[0] + 1, self.head.pos[1]),(48,128,20)))
            self.body.append(Cube((self.head.pos[0] + 1, self.head.pos[1] + 1),(48,128,20)))
            self.body.append(Cube((self.head.pos[0] + 2, self.head.pos[1] + 1),(48,128,20)))
        elif self.forma == 'L':
            self.head = Cube(pos,(255,128,0))
            self.body.append(self.head)
            self.body.append(Cube((self.head.pos[0], self.head.pos[1] + 1),(255,128,0)))
            self.body.append(Cube((self.head.pos[0], self.head.pos[1] + 2),(255,128,0)))
            self.body.append(Cube((self.head.pos[0] + 1, self.head.pos[1] + 2),(255,128,0)))
        elif self.forma == 'J':
            self.head = Cube(pos,(255,131,250))
            self.body.append(self.head)
            self.body.append(Cube((self.head.pos[0], self.head.pos[1] + 1),(255,131,250)))
            self.body.append(Cube((self.head.pos[0], self.head.pos[1] + 2),(255,131,250)))
            self.body.append(Cube((self.head.pos[0] - 1, self.head.pos[1] + 2),(255,131,250)))
        elif self.forma == 'T':
            self.head = Cube(pos,(85,26,139))
            self.body.append(self.head)
            self.body.append(Cube((self.head.pos[0] + 1, self.head.pos[1]),(85,26,139)))
            self.body.append(Cube((self.head.pos[0] + 2, self.head.pos[1]),(85,26,139)))
            self.body.append(Cube((self.head.pos[0] + 1, self.head.pos[1] + 1),(85,26,139)))


    def giraforma(self, fundo):
        ver = True

        while ver:
            x = self.body[0].pos[0]
            y = self.body[0].pos[1]
            voltax = 0
            voltay = 0
            cx = []
            cy = []
            cont_fundos = 0

            if self.forma != 'O':
                for i, c in enumerate(self.body):
                    cx.append(c.pos[0])
                    cy.append(c.pos[1])
                    c.pos = (x - (cy[i] - y),y + (cx[i] - x))
                    encostando_fundos = 0
                    if c.pos[0] < 0:
                        voltax = max(0 - c.pos[0], voltax)
                    elif c.pos[0] > self.columns - 1:
                        voltax = min(self.columns - 1 - c.pos[0], voltax)
                    elif c.pos[1] > self.rows - 1:
                        voltay = min(self.rows - 1 - c.pos[1], voltay)

                    for j, cf in enumerate(fundo.body):
                        if c.pos == cf.pos and c.pos[0] > cx[i]:
                            voltax += -1
                        elif c.pos == cf.pos and c.pos[0] < cx[i]:
                            voltax += 1

                if voltax != 0 or voltay !=0:
                    for i, c in enumerate(self.body):
                        c.pos = (cx[i] + voltax, cy[i] + voltay)
                else:
                    ver = False

            else:
                ver = False



    def moveforma(self, fundo):
        self.dirnx = 0
        giro = 0
        desce = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT] and self.dirnx != 1:
                    self.dirnx = -1
                elif keys[pygame.K_RIGHT] and self.dirnx != -1:
                    self.dirnx = 1
                elif keys[pygame.K_UP]:
                    giro = 1
                elif keys[pygame.K_DOWN]:
                    desce = 1

        for i, c in enumerate(self.body):
            if c.pos[0] <= 0 and self.dirnx == -1:
                self.dirnx = 0
            elif c.pos[0] >= self.columns - 1 and self.dirnx == 1:
                self.dirnx = 0
            for j, cf in enumerate(fundo.body):
                if c.pos[0] - 1 == cf.pos[0] and c.pos[1] == cf.pos[1] and self.dirnx == -1:
                    self.dirnx = 0
                elif c.pos[0] + 1 == cf.pos[0] and c.pos[1] == cf.pos[1] and self.dirnx == 1:
                    self.dirnx = 0


        for c in self.body:
            c.movecubeprolado(self.dirnx)

        if giro == 1:
            self.giraforma(fundo)

        if desce == 1:
            self.movebaixo(fundo)


    def movebaixo(self, fundo):
        auxbaixo = 0

        for c in self.body:
            for cf in fundo.body:
                if c.pos[0] == cf.pos[0] and c.pos[1] == cf.pos[1] - 1:
                    auxbaixo = 1

        if auxbaixo == 0:
            for c in self.body:
                c.movecubeprabaixo()


    def draw(self, surface):
        for i, c in enumerate(self.body):
                c.drawCube(surface)

    def reset(self, pos):
        self.body = []
        self.rows = 20
        self.columns = 10
        self.dirnx = 0
        self.forma = random.choice(['O','I','S','Z','L','J','T'])

        if self.forma == 'O':
            self.head = Cube(pos,(255,215,0))
            self.body.append(self.head)
            for i in range(2):
                for j in range(2):
                    if i == 0 and j == 0:
                        continue
                    self.body.append(Cube((self.head.pos[0] + i, self.head.pos[1] + j),(255,215,0)))
        elif self.forma == 'I':
            self.head = Cube(pos, (51,161,201))
            self.body.append(self.head)
            for i in range(3):
                self.body.append(Cube((self.head.pos[0], self.head.pos[1] + i+1), (51,161,201)))
        elif self.forma == 'S':
            self.head = Cube(pos,(255,0,0))
            self.body.append(self.head)
            self.body.append(Cube((self.head.pos[0] - 1, self.head.pos[1]),(255,0,0)))
            self.body.append(Cube((self.head.pos[0] - 1, self.head.pos[1] + 1),(255,0,0)))
            self.body.append(Cube((self.head.pos[0] - 2, self.head.pos[1] + 1),(255,0,0)))
        elif self.forma == 'Z':
            self.head = Cube(pos,(48,128,20))
            self.body.append(self.head)
            self.body.append(Cube((self.head.pos[0] + 1, self.head.pos[1]),(48,128,20)))
            self.body.append(Cube((self.head.pos[0] + 1, self.head.pos[1] + 1),(48,128,20)))
            self.body.append(Cube((self.head.pos[0] + 2, self.head.pos[1] + 1),(48,128,20)))
        elif self.forma == 'L':
            self.head = Cube(pos,(255,128,0))
            self.body.append(self.head)
            self.body.append(Cube((self.head.pos[0], self.head.pos[1] + 1),(255,128,0)))
            self.body.append(Cube((self.head.pos[0], self.head.pos[1] + 2),(255,128,0)))
            self.body.append(Cube((self.head.pos[0] + 1, self.head.pos[1] + 2),(255,128,0)))
        elif self.forma == 'J':
            self.head = Cube(pos,(255,131,250))
            self.body.append(self.head)
            self.body.append(Cube((self.head.pos[0], self.head.pos[1] + 1),(255,131,250)))
            self.body.append(Cube((self.head.pos[0], self.head.pos[1] + 2),(255,131,250)))
            self.body.append(Cube((self.head.pos[0] - 1, self.head.pos[1] + 2),(255,131,250)))
        elif self.forma == 'T':
            self.head = Cube(pos,(85,26,139))
            self.body.append(self.head)
            self.body.append(Cube((self.head.pos[0] + 1, self.head.pos[1]),(85,26,139)))
            self.body.append(Cube((self.head.pos[0] + 2, self.head.pos[1]),(85,26,139)))
            self.body.append(Cube((self.head.pos[0] + 1, self.head.pos[1] + 1),(85,26,139)))


#classe do que já chegou no fundo
class Fundo(object):
    body = []

    def addCube(self, forma):
        for i in forma.body:
            self.body.append(i)

    def deleterow(self):
        pass

    def drawfundo(self, surface):
        for i, c in enumerate(self.body):
                c.drawCube(surface)

    def resetfundo(self):
        self.body = []

    def deleta_linha(self, row):
        for i, c in enumerate(self.body):
            if c.pos[1] == row:
                del self.body[i]

        for c in self.body:
            if c.pos[1] <= row:
                c.movecubeprabaixo()


#Classe de cada cubo
class Cube(object):
    width = 400
    height = 800

    def __init__(self, start, color, dirnx = 0):
        self.pos = start
        self.dirnx = 0
        self.color = color
        self.rows = 20
        self.columns = 10

    def movecubeprolado(self, dirnx):
        self.dirnx = dirnx
        self.pos = (self.pos[0] + self.dirnx, self.pos[1])

    def movecubeprabaixo(self):
        self.pos = (self.pos[0], self.pos[1] + 1)

    def drawCube(self, surface):
        dis = self.width // self.columns
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis + 1, j*dis + 1, dis - 2, dis - 2))


#Atualiza o desenho
def redrawWindow(surface):
    global width, height, rows, columns, f, fundo
    surface.fill((0,0,0))
    f.draw(surface)
    fundo.drawfundo(surface)
    drawgrind(surface)
    pygame.display.update()


#Desenha as linhas e colunas
def drawgrind(surface):
    global width, height, rows, columns
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


def main():
    global width, height, rows, columns, f, fundo
    rows = 20
    columns = 10
    width = 400
    height = 800

    #Cria janela
    wn = pygame.display.set_mode((width,height))
    f = Formas((columns // 2, -4))
    fundo = Fundo()
    clock = pygame.time.Clock()
    flag = True

    aux = 0
    scorepecas = 0
    scoreslinhas = 0

    while flag:
        pygame.time.delay(80)
        clock.tick(10)
        f.moveforma(fundo)

        for i in range(len(f.body)):
            if f.body[i].pos[1] + 1 == rows:
                fundo.addCube(f)
                f.reset((columns // 2, -4))
                scorepecas += 1

            for j in range(len(fundo.body)):
                if f.body[i].pos[0] == fundo.body[j].pos[0] and f.body[i].pos[1] + 1 == fundo.body[j].pos[1]:
                    fundo.addCube(f)
                    f.reset((columns // 2, -4))
                    scorepecas += 1

        for row in range(rows):
            controw = 0
            for i in range(len(fundo.body)):
                if fundo.body[i].pos[1] == row:
                    controw += 1

            if controw >= columns:
                fundo.deleta_linha(row)
                scoreslinhas += 1
                row += -1

        redrawWindow(wn)

        for j in range(len(fundo.body)):
            if fundo.body[j].pos[1] == 0:
                message_box('Perdeu!', 'Peças: {}\nLinhas: {}'.format(scorepecas, scoreslinhas))
                scorepecas = 0
                scoreslinhas = 0
                f.reset((columns // 2, -4))
                fundo.resetfundo()
                break

        if aux % 3 == 0:
            f.movebaixo(fundo)

        aux += 1


main()
