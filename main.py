import os
import sys
import ctypes
import pygame
from pygame.locals import *
from random import randint

class Block (object):
    """
    Block (data,color,pos): handles block graphics and position\n
    data  : a 2D aray with 1's & 0's (1=block)\n
    color : (r,g,b)\n
    pos   : [x,y] where to render the block (from top left)\n
    """
    def __init__(self,data, color, pos):
        self.data = data
        self.color = color
        self.pos = pos
    
    def draw(self, gridSize, borderLen):
        """
        draw (gridSize, borderLen): returns a Surface of the specified block\n
        gridSize  : the global grid size for the game (int)\n
        borderLen : the width of the border between individual grids (int)\n
        """
        data = self.data
        self.size = [len(data[0]), len(data)]

        cube = pygame.Surface((gridSize,gridSize))
        cubeC = pygame.Surface((gridSize-(borderLen*2),gridSize-(borderLen*2)))
        cubeC.fill(self.color)
        cube.fill((20,20,20))
        cube.blit(cubeC, (borderLen, borderLen))

        surface = pygame.Surface((self.size[0]*gridSize, self.size[1]*gridSize))


        colorNew = (255 - self.color[0],255 - self.color[1],255 - self.color[2])
        surface.fill(colorNew)
        
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                val = data[y][x]
                if val == 1:
                    surface.blit(cube,(gridSize*x, gridSize*y))
        surface.set_colorkey(colorNew)
        return surface
    

def find_data_file(filename):
    """
    find_data_file (filename) : Finds the absolute position of a file for when the game is compiled into an exe
    filename : string including for filename "example.txt"
    """
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)

def getKeys():
    """
    getkeys (): returns a list of all the keys currently being pressed
    """
    current_keys = {'a': 97, 'b': 98, 'c': 99, 'd': 100, 'e': 101, 'f': 102, 'g': 103, 'h': 104, 'i': 105, 'j': 106, 'k': 107, 'l': 108, 'm': 109,
    'n': 110, 'o': 111, 'p': 112, 'q': 113, 'r': 114, 's': 115, 't': 116, 'u': 117, 'v': 118, 'w': 119, 'x': 120, 'y': 121, 'z': 122, '[': 91, ']': 93, '\\': 92, '.': 46, '/': 47, ';': 59, "'": 39, 'backspace': 8, 'delete': 127, 'home': 278, 'end': 279, 'return': 13, 'insert': 277, 'page up': 280, 'right shift': 303, 'up': 273, 'page down': 281, 'right': 275, 'down': 274, 'left': 276,
    'right ctrl': 305, 'menu': 319, 'right alt': 307, 'space': 32, 'left alt': 308, 'left ctrl': 306, 'left shift': 304, 'caps lock': 301, 'tab': 301, '`': 301, '1': 301, '2': 301, '3': 301, '4':
    301, '5': 301, '6': 301, '7': 301, '8': 301, '9': 301, '0': 301, '-': 301, '=': 301, 'escape': 301, 'f1': 301, 'f2': 301, 'f3':
    301, 'f4': 301, 'f5': 301, 'f6': 287, 'f7': 301, 'f8': 301, 'f9': 301, 'f10': 301, 'f11': 301, 'f12': 301, '0': 48, '1': 49, '2': 50, '3': 51, '4': 52, '5': 53, '6': 54, '7': 55, '8': 56, '9': 57}
    
    if pygame.key.get_focused() == True:
        bools = pygame.key.get_pressed()
        out = []
        for i in range(0,len(bools)):
            if bools[i] == 1:
                try:
                    out.append(list(current_keys.keys())[list(current_keys.values()).index(i)])
                except(ValueError):
                    pass
        return out
    return []


pygame.init()

size = (900,900)
gridW = 50

# makes two Surfaces one as the screen the other as a mimic screen
# this is useful for post-process scaling
screen = pygame.display.set_mode(size)
display = screen
display.fill((0,255,0))
screen.fill((255,255,255))
screen.blit(display,(0,0))
pygame.display.flip()

pygame.display.set_caption('Tetris')

#creates the first block
data = [[1,0],[1,1]]
pos = [randint(0, size[1]/gridW - len(data[0])), 0-len(data)]
block = Block(data, (200,200,200), pos)
blocks = [] #list of "placed blocks"

#timers for controled movement
lastTime = 0  #user Controls
lastTime2 = 0 #down

display.fill((0,255,0))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    #draws active block
    b = block.draw(gridW, 2)
    display.blit(b, (block.pos[0]*50, block.pos[1]*50))

    #draws inactive blocks
    for i in blocks:
        k = i[1]
        display.blit(i[0],(k[0]*50,k[1]*50))

    #refreshes the screen
    screen.blit(display, (0,0))
    pygame.display.flip()
    display.fill((0,255,0))

    #user input
    keys = getKeys()
    if pygame.time.get_ticks() - lastTime > 200:
        if keys:
            lastTime = pygame.time.get_ticks()
        if "a" in keys:
            if block.pos[0] != 0:
                    block.pos[0] -= 1

        elif "d" in keys:
            if block.pos[0] + block.size[0] != size[0]/gridW:
                block.pos[0] += 1

        if "s" in keys:
            if block.pos[1] + block.size[1] < size[1]/gridW:
                block.pos[1] += 1

    #Gravity
    if pygame.time.get_ticks() - lastTime2 > 500:
        lastTime2 = pygame.time.get_ticks()
        if block.pos[1] + block.size[1] < size[1]/gridW:
            block.pos[1] += 1
        else:
            blocks.append([b,block.pos])
            data = [[1]]
            pos = [randint(0, size[1]/gridW - len(data[0])), 0-len(data)]
            block = Block(data, (200,200,200), pos)
    