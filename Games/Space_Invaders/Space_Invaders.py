import pygame
import time
import random
import tkinter as tk
from tkinter import messagebox

#Player object
class Player():
    def __init__(self, x, y, height, width, img, vel):
        self.x = x
        self.y = y
        self.width = width
        self.heigth = height
        self.img = img
        self.vel = vel
    
    def drawplayer(self, wn):
        wn.blit(self.img,(self.x,self.y))
    
    def playermove(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.x > 0:
                self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            if self.x < self.width - self.img.get_width():
                self.x += self.vel

#Invader object
class Invader():
    def __init__(self, x, y, img, vel, type):
        self.x = x
        self.y = y
        self.img = img
        self.vel = vel
        self.type = type
    
    #If the invader is supose to have a shield (type S) we draw the shield
    def drawinvader(self, wn):
        if self.img !=  None:
            if self.type == 'S':
                pygame.draw.circle(wn,(0,255,0),(self.x + self.img.get_width()/2,self.y + self.img.get_width()/2),23)
            wn.blit(self.img,(self.x,self.y))
    
    def invaderdown(self):
        self.y += self.vel
    
    def invaderside(self,lado):
        self.x += self.vel*lado

#Shots object
class Shot():
    def __init__(self, x, y, img, vel, type):
        self.x = x
        self.y = y
        self.vel = vel
        self.img = img
        self.type = type
    
    def drawshot(self, wn):
        wn.blit(self.img,(self.x - self.img.get_width()/2,self.y))
    
    #If the player has unlocked the tripleshot he should shot 2 more shots diagonally
    def shotmove(self):
        if self.type == None:
            self.y -= self.vel
        elif self.type == 'L':
            self.y -= self.vel
            self.x -= 1
        elif self.type == 'R':
            self.y -= self.vel
            self.x += 1
        else:
            self.y += self.vel #If the shot came from a invader it is suppose to go down instead of going up


def redrawWindow(wn, player, invaders,shots,shield_ready, shield_active, count_shield, level):
    wn.fill((0,0,0))
    
    for inv in invaders:
        inv.drawinvader(wn)
    
    for shot in shots:
        shot.drawshot(wn)

    if level > 3:
        if shield_ready:
            pygame.draw.rect(wn,(0,255,0),(player.x, player.y+75, 60, 20)) #The shield load bar will turn green when fully loaded
        elif shield_active:
            pygame.draw.circle(wn,(0,255,0),(player.x + player.img.get_width()/2,player.y + player.img.get_width()/2),38) #Draw the shield
            pygame.draw.rect(wn,(255,0,0),(player.x, player.y+75, 60 - (1/3)*count_shield, 20)) #The shield load bar will progressively deploy until de shield stop working
        else:
            pygame.draw.rect(wn,(0,0,255),(player.x, player.y+75, (1/3)*count_shield, 20)) #The shield load bar will progressively increase until de shield is ready to be used 
    
    player.drawplayer(wn)

    pygame.display.update()

#Show a message box
def message_box(subject, content):
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

#reset for new level
def reset(wn,width,height,level,player):
    
    #first screen showing the level and new upgrades
    wn.fill((0,0,0))
    font = pygame.font.SysFont('Arial', 80)
    text = font.render('LEVEL ' + str(level), 1, (255,255,255))
    wn.blit(text, (width/2 - text.get_width()/2,height/2 - text.get_height()/2))
    
    if level == 6:
        subtext = font.render('shot rate up', 1, (255,255,255))
        wn.blit(subtext, (width/2 - subtext.get_width()/2,10 + height/2 + text.get_height()/2))
    elif level == 4:
        subtext = font.render('shield unlocked', 1, (255,255,255))
        wn.blit(subtext, (width/2 - subtext.get_width()/2,10 + height/2 + text.get_height()/2))
    elif level == 8:
        subtext = font.render('tripleshot unlocked', 1, (255,255,255))
        wn.blit(subtext, (width/2 - subtext.get_width()/2,10 + height/2 + text.get_height()/2))
    elif level == 12:
        subtext = font.render('speed up', 1, (255,255,255))
        wn.blit(subtext, (width/2 - subtext.get_width()/2,10 + height/2 + text.get_height()/2))

    pygame.display.update() 
    time.sleep(1)


    #Reset all parameters and lists
    aux = 0
    lado = 1
    shottime = 20
    press = True
    shots = []
    invaderImg = pygame.image.load('C:\\PY\\Estudospy\\Games\\Space_Invaders\\UFO.png')
    invaderImg = pygame.transform.scale(invaderImg,(40,40))
    bomberImg = pygame.image.load('C:\\PY\\Estudospy\\Games\\Space_Invaders\\bomber.png')
    bomberImg = pygame.transform.scale(bomberImg,(40,40))
    invaders = []
    player.vel = 3
    shield_active = False
    shield_ready = True
    count_shield = 0
    pressshield = True
    rate = 25


    #The number of invaders rows increase with every 2 levels
    row = level // 2 + 4

    #Will randomly assign positions for a number of shielded invaders and bombers invaders, this invaders increase in number with each level, without repeating positions
    pos_ok = False
    while not pos_ok:
        ver = True

        shielders = level // 2
        shielders_pos = []

        for _ in range(shielders*5):
            shielders_pos.append((random.choice(range(11)),random.choice(range(row))))

        bombers = level // 3
        bombers_pos = []

        for _ in range(bombers*5):
            bombers_pos.append((random.choice(range(11)),random.choice(range(row))))

        for bombers_aux in bombers_pos:
            if bombers_aux in shielders_pos:
                ver = False

        for i in range(bombers):
            for j in range(bombers):
                if i == j:
                    continue
                elif bombers_pos[i] == bombers_pos[j]:
                    ver = False

        for i in range(shielders):
            for j in range(shielders):
                if i == j:
                    continue
                elif shielders_pos[i] == shielders_pos[j]:
                    ver = False
        
        pos_ok = ver

    for i in range(11):
        for j in range(row):
            if (i,j) in bombers_pos:
                invaders.append(Invader(20 + 100*i, 20 + 60*j,bomberImg,20,'B'))
            elif (i,j) in shielders_pos:
                invaders.append(Invader(20 + 100*i, 20 + 60*j,invaderImg,20,'S'))
            else:
                invaders.append(Invader(20 + 100*i, 20 + 60*j,invaderImg,20,None))
    
    return aux, lado, shottime, press, shots, invaders, shield_active, shield_ready, count_shield, pressshield, rate

def main():

    level = 13
    width = 1200
    height = 900

    #Create window
    pygame.init()
    wn = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Space Invaders')
    icon = pygame.image.load('C:\PY\Estudospy\Games\Space_Invaders\spaceship.png')
    pygame.display.set_icon(icon)

    #Create player
    playerImg = pygame.image.load('C:\PY\Estudospy\Games\Space_Invaders\spaceship.png')
    playerImg = pygame.transform.scale(playerImg,(60,60))
    p = Player(width/2 - playerImg.get_width()/2,height - 100,height,width,playerImg,3)

    #Load images
    deathImg = pygame.image.load('C:\PY\Estudospy\Games\Space_Invaders\dead.png')
    deathImg = pygame.transform.scale(deathImg,(60,60))

    bombImg = pygame.image.load('C:\\PY\\Estudospy\\Games\\Space_Invaders\\bomb.png')
    bombImg = pygame.transform.scale(bombImg,(30,30))

    explosion = pygame.image.load('C:\\PY\\Estudospy\\Games\\Space_Invaders\\explosion.png')
    explosion = pygame.transform.scale(explosion,(40,40))
    explosion_bombs = pygame.transform.scale(explosion,(30,30))

    shotImg = pygame.image.load('C:\\PY\\Estudospy\\Games\\Space_Invaders\\bullet.png')
    shotImg = pygame.transform.scale(shotImg,(30,30))
    shotImg = pygame.transform.rotate(shotImg,90)

    #Create first level
    aux, lado, shottime, press, shots, invaders, shield_active, shield_ready, count_shield, pressshield, rate = reset(wn,width,height,level,p)

    clock = pygame.time.Clock()
    flag = True

    while flag:
        aux += 1
        count_shield += 1
        clock.tick(60)

        #Close window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False

        #Increase rate of fire after level 5
        if level > 5:
            rate = 10

        #Increase player speed after level 11
        if level > 11:
            p.vel = 6

        #Allow player to fire in a certain rate, but he can't hold SPACE to fire
        if shottime >= rate and press:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if level > 7: #Allow player to fire two more shots after level 7
                    shots.append(Shot(p.x + playerImg.get_width()/2,p.y,shotImg,3,'L'))
                    shots.append(Shot(p.x + playerImg.get_width()/2,p.y,shotImg,3,'R'))
                shots.append(Shot(p.x + playerImg.get_width()/2,p.y,shotImg,3,None))
                shottime = 0
                press = False
        else:
            shottime += 1

        keys = pygame.key.get_pressed()
        if not keys[pygame.K_SPACE]:
            press = True

        #Allow player to use the shield after level 3, but he can't hold UP to activate the shield automatically
        if level > 3:
            if shield_ready and pressshield:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    shield_active = True
                    shield_ready = False
                    count_shield = 0
                    pressshield = False
            
            elif shield_active:
                if count_shield == 180:
                    count_shield = 0
                    shield_active = False
            else:
                if count_shield == 180:
                    shield_ready = True

            keys = pygame.key.get_pressed()
            if not keys[pygame.K_UP]:
                pressshield = True

        #Move the invaders, for every 7 steps to the side they go 1 step down them go side in the other direction
        if aux % max((18 - level),1) == 0:
            if aux % (max((18 - level),1)*7) == 0:
                lado = -lado
                for inv in invaders:
                    inv.invaderdown()
            else:
                for inv in invaders:
                    inv.invaderside(lado)
                    
       
        for inv in invaders:

            #Remove the invader from the invader list if it has been destroyed in the last loop
            if inv.img == explosion:
                        invaders.remove(inv)
                        continue
            
            #If the invader is a bomber fire by a random chance a bomb
            if inv.type == 'B' and random.random() < 0.001:
                shots.append(Shot(inv.x + inv.img.get_width()/2,inv.y +  inv.img.get_height(),bombImg,3,'B'))

            #Destroy the invader if the player touch it and the shield is active
            if shield_active and inv.y <= p.y + p.img.get_height() and  inv.y + inv.img.get_height() >= p.y and inv.x <= p.x + p.img.get_width() and  inv.x + inv.img.get_width() >= p.x and inv.img != explosion:
                inv.img = explosion
                inv.type = None
                continue

            for shot in shots:

                #Remove the shot from the shots list if it has been destroyed in the last loop
                if shot.img == explosion_bombs:
                    shots.remove(shot)
                    continue
            
                #Remove the shot from the shots list if it went out of the window range
                if shot.x < -50 or shot.x > width or shot.y < - 50 or shot.y > height:
                    shots.remove(shot)
                    continue
                
                #Destroy the invader if it was hit by a player's shot or destroy his shield if the invader is a shielded one. It destroy the player's shot also
                if shot.type != 'B' and inv.img != explosion and inv.y <= shot.y + shot.img.get_height() and  inv.y + inv.img.get_height() >= shot.y and inv.x <= shot.x + shot.img.get_width() and  inv.x + inv.img.get_width() >= shot.x:
                    if inv.type != 'S':
                        inv.img = explosion
                        shots.remove(shot)
                        continue
                    elif inv.type == 'S':
                        inv.type = None
                        shots.remove(shot)
                        continue
                
                #Destroy the bomb if it was hit by a player's shot. It destroy the player's shot also
                for bomb in shots:
                    if (shield_active and bomb.type == 'B' and bomb.img != explosion_bombs and p.img != explosion_bombs and bomb.y <= p.y + p.img.get_height() and  bomb.y + bomb.img.get_height() >= p.y and bomb.x <= p.x + p.img.get_width() and  bomb.x + bomb.img.get_width() >= p.x) or (shot.type != 'B' and bomb.type == 'B' and bomb.img != explosion_bombs and shot.img != explosion_bombs and bomb.y <= shot.y + shot.img.get_height() and  bomb.y + bomb.img.get_height() >= shot.y and bomb.x <= shot.x + shot.img.get_width() and  bomb.x + bomb.img.get_width() >= shot.x):
                        bomb.img = explosion_bombs
                        bomb.vel = 0
                        shots.remove(shot)

        #Move all the shots
        for shot in shots:        
            shot.shotmove()
        
        #Move the player
        p.playermove()

        redrawWindow(wn, p, invaders,shots,shield_ready, shield_active, count_shield, level)

        #Verify if the player has won or lose and show a corresponding message, then it reset the game for the next level or back to level 1
        if len(invaders) == 0:
            if level == 14:
                message_box('NO MORE LEVELS!','Play again')
                level = 1
                p.img = playerImg
                p.x = width/2 - playerImg.get_width()/2
                aux,lado,shottime,press,shots,invaders, shield_active, shield_ready, count_shield, pressshield, rate = reset(wn,width,height,level,p)
            else:
                message_box('LEVEL CLEANED!','Next level')
                level += 1
                p.img = playerImg
                p.x = width/2 - playerImg.get_width()/2
                shield_active = False
                shield_ready = True
                aux,lado,shottime,press,shots,invaders, shield_active, shield_ready, count_shield, pressshield, rate = reset(wn,width,height,level,p)
                redrawWindow(wn, p, invaders,shots,shield_ready, shield_active, count_shield, level)
        
        for inv in invaders:
            if inv.y >= height and not shield_active:
                p.img = deathImg
                redrawWindow(wn, p, invaders,shots,shield_ready, shield_active, count_shield, level)
                time.sleep(1)
                
                message_box('YOU LOST!','Try again')
                level = 1
                p.img = playerImg
                p.x = width/2 - playerImg.get_width()/2
                shield_active = False
                shield_ready = True
                aux,lado,shottime,press,shots,invaders, shield_active, shield_ready, count_shield, pressshield, rate = reset(wn,width,height,level,p)
                redrawWindow(wn, p, invaders,shots,shield_ready, shield_active, count_shield, level)
                break

        for shot in shots:
            if shot.img == bombImg and p.y <= shot.y + shot.img.get_height() and  p.y + p.img.get_height() >= shot.y and p.x <= shot.x + shot.img.get_width() and  p.x + p.img.get_width() >= shot.x and not shield_active:
                p.img = deathImg
                shots.remove(shot)
                redrawWindow(wn, p, invaders,shots,shield_ready, shield_active, count_shield, level)
                time.sleep(1)
                
                message_box('YOU LOST!','Try again')
                level = 1
                p.img = playerImg
                p.x = width/2 - playerImg.get_width()/2
                shield_active = False
                shield_ready = True
                aux,lado,shottime,press,shots,invaders, shield_active, shield_ready, count_shield, pressshield, rate = reset(wn,width,height,level,p)
                redrawWindow(wn, p, invaders,shots,shield_ready, shield_active, count_shield, level)
                break

main()
