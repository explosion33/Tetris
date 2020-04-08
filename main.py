import os
import sys
import ctypes
import pygame
from pygame.locals import *
from random import randint

class Block (object):
    """
    Block (data,color,pos): handles block graphics and position\n
    data  : a 2D aray with 1's & 0's (1=block) or "random" for random generation\n
    color : (r,g,b)\n
    pos   : [x,y] where to render the block (from top left)\n
    """
    def __init__(self,data, color, pos):
        self.color = color
        self.pos = pos

        if data == "random":
            self.data = self.randomData()
        else:
            self.data = data
    
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
    
    def getAbsPos(self, grid):
        """
        getAbsPos (grid): returns the position of each individual block in a Block on the grid\n
        grid : grid data ex| 18x18 full of zeros
        """
        pos = []
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.data[y][x] == 1:
                    x1 = self.pos[0] + x
                    y1 = self.pos[1] + y
                    pos.append((x1,y1))
                else:
                    pos.append(None)
        return pos

    def randomData(self):
        datas = [
            [[1,1,1,1]],
            [[1,0,0],[1,1,1]],
            [[0,0,1],[1,1,1]],
            [[1,1],[1,1]],
            [[0,1,1],[1,1,0]],
            [[0,1,0],[1,1,1]],
            [[1,1,0],[0,1,1]],
        ] #all posible cominations

        x = len(datas)
        x = randint(0,x-1)
        return datas[x]

    def rotate(self, grid):
        w,h = self.size

        newData = []        
        for x in range(w):
            t = []
            for y in range(h):
                t.append(self.data[y][x])
            t = t[::-1]
            newData.append(t)
        data = self.data
        self.data = newData
        self.size = (h,w)

        x1,y1 = self.pos
        x = w-h
        if x != 0:
            k = x 
            p=x
            if k < 0: k = k*-1
        
            u=0
            if x == 3: u = 1
            elif x == -3: u = -1

            n = int(x/k)
            self.pos = [self.pos[0] + n, self.pos[1] + u]

        badPosition = False
        positions = self.getAbsPos(grid)
        for pos in positions:
            if pos:
                x,y = pos
                try:
                    if grid[y][x] == 1:
                        badPosition = True
                except:
                    badPosition = True
                if x < 0:
                    badPosition = True

        if badPosition:
            self.data = data
            self.size = (w,h)
            self.pos = [x1,y1]

    def floor(self, grid):

        x,y = self.pos
        touch = False
        while not touch:
            if self.pos[1] + self.size[1] < len(grid):
                positions = self.getAbsPos(grid)
                for pos in positions:
                    if pos:
                        dwn = (pos[0], pos[1] + 1)
                        try:
                            if grid[dwn[1]][dwn[0]] == 1:
                                if dwn[0] >= 0 and dwn[1] >= 0:
                                    touch = True
                        except:
                            pass

            else: #touching bottom
                touch = True
            self.pos[1] += 1
        self.pos[1] -= 1

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

def placeBlocks(block, NextBlock):
    """
    placeBlocks (block): places block on the screen, removes player control from the block and stores its collision data (updates score too)\n
    block : a Block object\n
    returns: a new block for the player to control
    """
    global grid
    global gridW
    global hard
    global score

    positions = block.getAbsPos(grid)

    for pos in positions:
        if pos:
            grid[pos[1]][pos[0]] = 1

            if pos[1] <= 0:
                loose()

    if hard:
        score += len(block.data)*2
    else:
        score += len(block.data)

    data = "random"
    block = Block(data, (200,200,200), [0,0])
    data = block.data
    pos = [randint(0, size[0]/gridW - len(data[0])), 0-len(data)]
    block.pos = pos
    return NextBlock, block

def loose():
    global grid
    global block
    global score
    global highScore
    global numLines
    global speedMult

    grid = []
    w = int(size[0]/gridW)
    h = int(size[1]/gridW)

    for y in range(h):
        temp = []
        for x in range(w):
            temp.append(0)
        grid.append(temp)
        temp = []
    
    data = "random"
    block = Block(data, (200,200,200), [0,0])
    data = block.data
    pos = [randint(0, size[0]/gridW - len(data[0])), 0-len(data)]
    block.pos = pos

    if score > highScore:
        highScore = score
        f = open(find_data_file("hs.txt"), "w")
        f.write(str(highScore))
    print("score", score)
    score = 0
    numLines = 0
    speedMult = 1


pygame.init()

size = (300,720)
gridW = 30
panelSize = 300

grid = []
w = int(size[0]/gridW)
h = int(size[1]/gridW)

for y in range(h):
    temp = []
    for x in range(w):
        temp.append(0)
    grid.append(temp)
    temp = []


# makes two Surfaces one as the screen the other as a mimic screen
# this is useful for post-process scaling
screen = pygame.display.set_mode((size[0] + panelSize,720))
display = pygame.Surface(size)
display.fill((22,22,22))
screen.fill((222,222,222))
screen.blit(display,(0,0))
pygame.display.flip()

pygame.display.set_caption('Tetris')

#creates the first block
data = "random"
block = Block(data, (200,200,200), [0,0])
data = block.data
pos = [randint(0, size[0]/gridW - len(data[0])), 0-len(data)]
block.pos = pos

data = "random"
nextBlock = Block(data, (200,200,200), [0,0])
data = nextBlock.data
pos = [randint(0, size[0]/gridW - len(data[0])), 0-len(data)]
nextBlock.pos = pos

#timers for controled movement
lastTime = 0  #user Controls
lastTime2 = 0 #down
gTime = 500

speedMult = 1

#keeps tracks of whoch keys were pushed in order to implemet one action for push
pushedKeys = []

#scoring
hard = False    #wether or not a block was hard dropped
score = 0

f = open(find_data_file("hs.txt"), "r")
highScore = int(f.read())
f.close()

numLines = 0

b1 = "b.png"
b2 = "b.png"



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    #LEFT SIDE OF SCREEN

    #draws active block
    b = block.draw(gridW, 2)
    display.blit(b, (block.pos[0]*gridW, block.pos[1]*gridW))

    #draws inactive blocks
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 1:
                b = Block([[1]], (200,200,200), [x,y])
                w,h = b.pos
                display.blit(b.draw(gridW, 2), (w*gridW,h*gridW))

    #RIGHT SIDE OF SCREEN

    f = pygame.font.SysFont("", 60, True)
    sc = f.render(str(score), True, (22,22,22))
    w = sc.get_width()

    Highsc = f.render(str(highScore), True, (22,22,22))
    w2 = Highsc.get_width()
    h2 = Highsc.get_height()

    screen.blit(sc, (size[0] + panelSize/2 -w/2, 20))
    screen.blit(Highsc, (size[0] + panelSize/2 -w2/2, size[1]-20-h2))

    f = pygame.font.SysFont("", 40, True)

    btn1 = pygame.image.load(find_data_file(b1))
    btn1T = f.render("RESTART", True, (222,222,222))
    btn1.blit(btn1T, (btn1.get_width()/2 - btn1T.get_width()/2, btn1.get_height()/2 - btn1T.get_height()/2))
    screen.blit(btn1, (size[0] + panelSize/2 -btn1.get_width()/2, 400))

    if pygame.mouse.get_pressed()[0]:
        if btn1.get_rect(topleft=(size[0] + panelSize/2 -btn1.get_width()/2, 400)).collidepoint(pygame.mouse.get_pos()):
            b1 = "bP.png"
            loose()
    else:
        b1 = "b.png"
        b2 = "b.png"

    nb = nextBlock.draw(gridW, 2)
    screen.blit(nb, (size[0] + panelSize/2 -nb.get_width()/2, 200))





    #refreshes the screen
    screen.blit(display, (0,0))
    pygame.display.flip()
    display.fill((22,22,22))
    screen.fill((222,222,222))

    #user input
    keys = getKeys()
    if pygame.time.get_ticks() - lastTime > 150: #timer based
        if keys:
            lastTime = pygame.time.get_ticks()
        if "a" in keys:
            if block.pos[0] != 0:
                positions = block.getAbsPos(grid)
                rouch = False
                for pos in positions:
                    if pos:
                        x,y = pos
                        x -= 1
                        if grid[y][x] == 1:
                            touch = True

                if not touch:
                    block.pos[0] -= 1

        elif "d" in keys:
            if block.pos[0] + block.size[0] != size[0]/gridW:
                positions = block.getAbsPos(grid)
                rouch = False
                for pos in positions:
                    if pos:
                        x,y = pos
                        x += 1
                        if grid[y][x] == 1:
                            touch = True

                if not touch:
                    block.pos[0] += 1

        if "s" in keys:
            gTime = 100/speedMult
        else:
            gTime = 500/speedMult

    #one input for key push
    if "r" in keys:
        if "r" not in pushedKeys:
            block.rotate(grid)
            pushedKeys.append("r")
    
    if "space" in keys:
        if "space" not in pushedKeys:
            block.floor(grid)
            pushedKeys.append("space")
            hard = True

    for key in pushedKeys:
        if key not in keys:
            pushedKeys.remove(key)

    #Gravity
    if pygame.time.get_ticks() - lastTime2 > gTime/speedMult:
        lastTime2 = pygame.time.get_ticks()
        if block.pos[1] + block.size[1] < size[1]/gridW:
            positions = block.getAbsPos(grid)
            touch = False
            for pos in positions:
                if pos:
                    dwn = (pos[0], pos[1] + 1)
                    try:
                        if grid[dwn[1]][dwn[0]] == 1:
                            if dwn[0] >= 0 and dwn[1] >= 0:
                                touch = True
                    except:
                        pass
            if not touch:
                block.pos[1] += 1
            else:
                block, nextBlock = placeBlocks(block, nextBlock)

        else: #touching bottom
            block, nextBlock = placeBlocks(block, nextBlock)

    #row clear Detection
    row = []
    for y in range(len(grid)):
        all1 = True
        for x in range(len(grid[0])):
            if grid[y][x] == 0:
                all1 = False
        if all1:
            row.append(y)

    for t in row:

        x = grid.pop(t)
        grid = grid[::-1]

        ls = []
        for i in range(len(x)):
            ls.append(0)

        grid.append(ls)
        grid = grid[::-1]

    #add score for row clear
    m = len(row)
    numLines += m
    if m == 1:
        m = 40
    elif m == 2:
        m = 100
    elif m == 3:
        m = 300
    elif m == 4:
        m = 1200
    score += m
    print(numLines, speedMult)

    if numLines > 0:
        x = int((numLines - 10)/20)/10
        speedMult = x +1