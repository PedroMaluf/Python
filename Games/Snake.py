import math
import random
import pygame
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk


class Cube(object):
    width = 500

    def __init__(self, start, rows, dirnx = 1, dirny = 0, color = (255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
        self.rows = rows

    def movecube(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def drawCube(self, surface, eyes = False):
        dis = self.width // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis + 1, j*dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis//2
            radius = 3
            if self.dirny == -1:
                circleMiddle = (i*dis+centre-dis//4,j*dis+dis*3/4)
                circleMiddle2 = (i*dis + dis -dis//4, j*dis+dis*3/4)
                pygame.draw.line(surface, (255,0,0), (i*dis + centre, j*dis),(i*dis + centre, j*dis - dis/4))
                pygame.draw.line(surface, (255,0,0), (i*dis + centre, j*dis - dis/4),(i*dis + centre - dis/8, j*dis - dis*3/8))
                pygame.draw.line(surface, (255,0,0), (i*dis + centre, j*dis - dis/4),(i*dis + centre + dis/8, j*dis - dis*3/8))
            elif self.dirny == 1:
                circleMiddle = (i*dis+centre-dis//4,j*dis+dis/4)
                circleMiddle2 = (i*dis + dis -dis//4, j*dis+dis/4)
                pygame.draw.line(surface, (255,0,0), (i*dis + centre, (j+1)*dis),(i*dis + centre, (j+1)*dis + dis/4))
                pygame.draw.line(surface, (255,0,0), (i*dis + centre, (j+1)*dis + dis/4),(i*dis + centre - dis/8, (j+1)*dis + dis*3/8))
                pygame.draw.line(surface, (255,0,0), (i*dis + centre, (j+1)*dis + dis/4),(i*dis + centre + dis/8, (j+1)*dis + dis*3/8))
            elif self.dirnx == -1:
                circleMiddle = (i*dis+dis*3/4,j*dis+centre-dis//4)
                circleMiddle2 = (i*dis + dis*3/4, j*dis+dis -dis//4)
                pygame.draw.line(surface, (255,0,0), (i*dis, j*dis + centre),(i*dis - dis/4, j*dis + centre))
                pygame.draw.line(surface, (255,0,0), (i*dis - dis/4, j*dis + centre),(i*dis - dis*3/8, j*dis + centre - dis/8))
                pygame.draw.line(surface, (255,0,0), (i*dis - dis/4, j*dis + centre),(i*dis - dis*3/8, j*dis + centre + dis/8))
            elif self.dirnx == 1:
                circleMiddle = (i*dis+dis/4,j*dis+centre-dis//4)
                circleMiddle2 = (i*dis + dis/4, j*dis+dis -dis//4)
                pygame.draw.line(surface, (255,0,0), ((1+i)*dis, j*dis + centre),((1+i)*dis + dis/4, j*dis + centre))
                pygame.draw.line(surface, (255,0,0), ((1+i)*dis + dis/4, j*dis + centre),((1+i)*dis + dis*3/8, j*dis + centre - dis/8))
                pygame.draw.line(surface, (255,0,0), ((1+i)*dis + dis/4, j*dis + centre),((1+i)*dis + dis*3/8, j*dis + centre + dis/8))

            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos, rows):
        self.rows = rows
        self.color = color
        self.head = Cube(pos, self.rows)
        self.body.append(self.head)
        self.dirnx = 1
        self.dirny = 0

        for i in range(4):
            self.inibody = Cube((pos[0] - 1 - i, pos[1]), self.rows)
            self.body.append(self.inibody)


    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT] and self.dirnx != 1:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT] and self.dirnx != -1:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP] and self.dirny != 1:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN] and self.dirny != -1:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]

            if p in self.turns:
                turn = self.turns[p]
                c.movecube(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else :
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                else:
                    c.movecube(c.dirnx, c.dirny)


    def reset(self, pos):
        self.body = []
        self.turns = {}
        self.head = Cube(pos, self.rows)
        self.body.append(self.head)
        self.dirnx = 1
        self.dirny = 0

        for i in range(4):
            self.inibody = Cube((pos[0] - 1 - i, pos[1]), self.rows)
            self.body.append(self.inibody)


    def addCube(self):
        tail = self.body[-1]

        self.body.append(Cube((tail.pos[0] - tail.dirnx, tail.pos[1] - tail.dirny), self.rows))
        self.body[-1].dirnx = tail.dirnx
        self.body[-1].dirny = tail.dirny

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.drawCube(surface, True)
            else:
                c.drawCube(surface)



def randomSnack(snake):
    global rows
    positions = snake.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break

    return (x,y)

def redrawWindow(surface):
    global width, rows, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.drawCube(surface)
    drawgrind(width, rows, surface)
    pygame.display.update()


def drawgrind(width, rows, surface):
    squares_width = width // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + squares_width
        y = y + squares_width
        pygame.draw.line(surface, (255,255,255), (x,0),(x,width))
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
    global width, rows, s, snack, entry, win
    rows = int(entry.get())
    width = 500
    win.destroy()
    if rows < 5:
        message_box('Muito pequeno!', 'Escolha outro tamanho')
        box()
        wn.destroy()
    wn = pygame.display.set_mode((width,width))
    s = Snake((255,0,0),(rows // 2,rows // 2), rows)
    snack = Cube(randomSnack(s), rows, color = (0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()

        if snack.pos == s.body[0].pos:
            s.addCube()
            snack = Cube(randomSnack(s), rows, color = (0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                message_box('You lost!', 'Try again')
                snack = Cube(randomSnack(s), rows, color = (0, 255, 0))
                s.reset((rows // 2,rows // 2))
                break

        if len(s.body)+1 == rows**2:
            message_box('You won!', 'Play again')
            snack = Cube(randomSnack(s), rows, color = (0, 255, 0))
            s.reset((rows // 2,rows // 2))


        redrawWindow(wn)

def box():
    global entry, win
    win= Tk()

    #Set the geometry of Tkinter frame
    win.geometry("200x150")

    #Initialize a Label to display the User Input
    label=Label(win, text="", font=("Courier 8 bold"))
    label.pack()
    label.configure(text='Qual o tamanho dos lados?')

    #Create an Entry widget to accept User Input
    entry= Entry(win, width= 40)
    entry.focus_set()
    entry.pack()

    #Create a Button to validate Entry Widget
    ttk.Button(win, text= "Okay",width= 20, command= main).pack(pady=20)

    win.mainloop()

box()
