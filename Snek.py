from cmath import rect
from lib2to3.pytree import convert
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


#Class cube
#Basic game object for both sacks and sneks
#uses X Y coordinates to record and update its position
class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(100,0,255)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
 
    #move using standard x y coordinates
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    
    #draw the square at the curent position
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
 
        #pygame definitions of cube 
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
       
 
 
#Class snek or "snake" for the less cultured
#A series of connected cubes that extends as the game is played
#and has a constant momentumn
class snek(object):
    body = []
    turns = {}
    #define snek using cubes
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
    
    #move snek
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
 
            keys = pygame.key.get_pressed()

            #definitions of arrow keys as game controls
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        #Pressing keys changes cube positions
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)
       
    #reset snek for new games
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
 
    #make more snek
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
 
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
 
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
       
    #draw snek
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)
 
 

       
#redrawWindow
#update the game window to reflect changes in game state
def redrawWindow(surface):
    global rows, width, s, snack
    #fancy grass jpg background converted as per pygame recomendations
    background_image = pygame.image.load("grass.jpg").convert()
    #build background image
    surface.blit(background_image, [0, 0])
    s.draw(surface)
    snack.draw(surface)
    pygame.display.update()
    
 
#ramdomSnack
#pick an unoccupied square at random and put a snack there
def randomSnack(rows, item):
 
    positions = item.body
 
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
       
    return (x,y)
 
#Message box for loosing game state and try again
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
 
 
def main():
    #global varibles that define key game elements
    global width, rows, s, snack
    width = 500
    rows = 20
    
    #Call key varibles for game loop

    #win defines game window
    win = pygame.display.set_mode((width, width))
    #s adds a snek to gamestate
    s = snek((255,0,0), (10,10))
    #snack adds a snack to gamestate
    snack = cube(randomSnack(rows, s), color=(0,255,0))
    #flag starts and stops game loop
    flag = True

    
    
    #set clock
    clock = pygame.time.Clock()
   
   
    while flag:
        #primary game loop
        #move the snek around to eat snacks
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        #if you eat a snack your snek grows by 1 cube
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))
        #secondary game loop
        #if you eat yourself the game is over
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                #score prints in terminal using body legenth as score
                print('Score: ', len(s.body))
                #play again message
                message_box('You Lost!', 'Play again...')
                #reset button
                s.reset((10,10))
                break
 
        #update game state   
        redrawWindow(win)
 
       
    pass
 
 
 
main()