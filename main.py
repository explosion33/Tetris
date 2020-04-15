import os
import sys
import pygame
from pygame.locals import *
from random import randint
import ast

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

        self.size = [len(self.data[0]), len(self.data)]
    
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


class Button():
    """
    Button() : creates a clickable button\n
    images : a list of two strings\n
    text : text for the image\n
    color : text color for image\n
    pos : topleft of image\n
    action : optional function to run on click\n
    args : optional args for function
    """
    def __init__(self, images, text, color, pos, action=None, args=None, centered=None):
        self.images = images
        self.activeImage = self.images[0]
        self.text = text
        self.color = color
        self.pos = pos
        self.action = action
        self.args = args

        self.Surface = self.draw()

        if centered:
            self.pos = self.getCenter()

    def draw(self):
        f = pygame.font.SysFont("", 40, True)


        img = pygame.image.load(find_data_file(self.activeImage))
        text = f.render(self.text, True, self.color)
        img.blit(text, (img.get_width()/2 - text.get_width()/2, img.get_height()/2 - text.get_height()/2))

        return img

    def tick(self):
        if pygame.mouse.get_pressed()[0]:
            if self.Surface.get_rect(topleft=self.pos).collidepoint(pygame.mouse.get_pos()):
                self.activeImage = self.images[1]
                
                print(self.action)

                if self.action:
                    if self.args:
                        self.action(self.args)
                    else:
                        self.action()
        else:
            self.activeImage = self.images[0]

    def getCenter(self):
        """
        getCenter() : returns the pos for the object to be centered on its pos
        """

        x,y = self.pos
        h = self.Surface.get_height()
        w = self.Surface.get_width()

        return (x-w/2, y-h/2)

class toggleButton(Button):
    def __init__(self, images, text, color, pos, action=None, args=None, centered=None):
        self.state = 0
        self.pressed = False
        super(toggleButton, self).__init__(images, text, color, pos, action, args, centered)
    
    def tick(self):
        if pygame.mouse.get_pressed()[0]:
            if self.Surface.get_rect(topleft=self.pos).collidepoint(pygame.mouse.get_pos()):
                if self.state == 0 and not self.pressed:
                    self.pressed = True
                    self.state = 1
                    self.activeImage = self.images[1]
                
                    if self.action:
                        if self.args:
                            self.action(self.args)
                        else:
                            self.action()
                if self.state == 1 and not self.pressed:
                    self.pressed = True
                    self.state = 0
                    self.activeImage = self.images[0]
        else:
            self.pressed = False


class textInput():
    def __init__(self, size, text, color, pos, id=None):
        self.size = size
        self.text = text
        self.savedText = text
        self.color = color
        self.pos = pos

        self.Surface = self.draw()
        self.state = 0

        self.blinkIter = 0

        self.id = id

    def draw(self):
        text = self.text
        if self.text == "":
            text = self.savedText

        f = pygame.font.SysFont("", self.size, True)
        text = f.render(text, True, self.color)

        if self.text == "":
            box = pygame.Surface((text.get_width(), text.get_height()), pygame.SRCALPHA)
            box.fill((0,0,0,0))

            bar = pygame.Surface((text.get_width(), 2))

            dur = 60

            if self.blinkIter <= dur:
                box.blit(bar, (0, text.get_width()))
            elif self.blinkIter > dur*2:
                self.blinkIter = 0
            
            self.blinkIter += 1

            text = box

        self.Surface = text
        return text

    def getKeys(self):
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


    def tick(self):
        hit = self.Surface.get_rect(center=self.pos).collidepoint(pygame.mouse.get_pos())
        pressed = pygame.mouse.get_pressed()[0]

        #pygame.draw.rect(screen, (255,0,0), self.Surface.get_rect(center=self.pos))

        if pressed:
            if hit:
                if self.state == 0:
                    self.state = 1
                    self.text = ""
            else:
                self.text = self.savedText
                self.state = 0

        if self.state == 1:
            keys = self.getKeys()
            if keys:
                self.text = keys[0]
                self.savedText = self.text
                self.state = 0


    def getCenter(self):
        w,h = self.Surface.get_size()

        x,y = self.pos

        x -= w/2
        y -= h/2

        return (x,y)



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
    score = 0
    numLines = 0
    speedMult = 1

def menu(arg):
    global mode
    if arg == "exit":
        sys.exit()
    elif arg == "start":
        mode = "game"
    elif arg == "settings":
        mode = "settings"

def settingsMenu(arg):
    global mode
    if arg == "back":
        mode = "menu"
        print(settings)

        f = open(find_data_file("settings.txt"), "w")
        f.write(str(settings))

pygame.init()

size = (300,720)
gridW = 30
panelSize = 300

w = int(size[0]/gridW)
h = int(size[1]/gridW)

grid = []
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


f = open(find_data_file("settings.txt"))
r = f.read()

settings = ast.literal_eval(r)
print(settings)

restartBtn = Button(["b.png", "bP.png"], "RESTART", (222,222,222), (3/2*panelSize, 400), loose)
restartBtn.pos = restartBtn.getCenter()

startBtn = Button(["b.png", "bP.png"], "START", (222,222,222), (3/2*panelSize, 100), menu, "start", centered=True)
settingsBtn = Button(["b.png", "bP.png"], "SETTINGS", (222,222,222), (3/2*panelSize, 300), menu, "settings", centered=True)
ScoresBtn = Button(["b.png", "bP.png"], "SCORES", (222,222,222), (3/2*panelSize, 200), menu, "scores", centered=True)
ExitBtn = Button(["b.png", "bP.png"], "EXIT", (222,222,222), (3/2*panelSize, 400), menu, "exit", centered=True)

logo = pygame.image.load("logo.png")

menuBtns = [startBtn, settingsBtn, ScoresBtn, ExitBtn]

backBtn = Button(["b.png", "bP.png"], "BACK", (222,222,222), (3/2*panelSize, 600), settingsMenu, "back", centered=True)
showGrid = toggleButton(["c.png", "cP.png"], "", (222,222,222), (3/2*panelSize + 60, 410), centered=True)
leftIn = textInput(40, settings["left"], (22,22,22), (7/4*panelSize - 20,50))
RightIn = textInput(40, settings["right"], (22,22,22), (7/4*panelSize - 20,50))
SpeedIn = textInput(40, settings["speed"], (22,22,22), (7/4*panelSize - 20,50))
DropIn = textInput(40, settings["drop"], (22,22,22), (7/4*panelSize - 20,50))
RotateIn = textInput(40, settings["rotate"], (22,22,22), (7/4*panelSize - 20,50))

inputs = []

x = 50
for i in ["left", "right", "speed", "drop", "rotate"]:
    inputs.append(textInput(40, settings[i], (22,22,22), (7/4*panelSize - 20,x), i))
    x += 50

mode = "menu"




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    if mode == "game":
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

        screen.blit(restartBtn.draw(), restartBtn.pos)
        restartBtn.tick()

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
            if settings["left"] in keys:
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

            elif settings["right"] in keys:
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

            if settings["speed"] in keys:
                gTime = 100/speedMult
            else:
                gTime = 500/speedMult

        #one input for key push
        if settings["rotate"] in keys:
            if settings["rotate"] not in pushedKeys:
                block.rotate(grid)
                pushedKeys.append(settings["rotate"])
        
        if settings["drop"] in keys:
            if settings["drop"] not in pushedKeys:
                block.floor(grid)
                pushedKeys.append(settings["drop"])
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

        if numLines > 0:
            x = int((numLines - 10)/10)/10
            speedMult = x +1

    if mode == "menu":

        for btn in menuBtns:
            screen.blit(btn.draw(), btn.pos)
            btn.tick()

        screen.blit(logo, (panelSize*3/2 - logo.get_width()/2, 450))
        


        #refreshes the screen
        screen.blit(display, (0,0))
        pygame.display.flip()
        display.fill((22,22,22))
        screen.fill((222,222,222))

    if mode == "settings":

        f = pygame.font.SysFont("", 35, True)

        GRD = f.render("Show Grid: ", True, (22,22,22))

        screen.blit(GRD, (panelSize+15, 400))

        screen.blit(backBtn.draw(), backBtn.pos)
        backBtn.tick()

        screen.blit(showGrid.draw(), showGrid.pos)
        showGrid.tick()

        for i in inputs:

            t = f.render(i.id, True, (22,22,22))

            screen.blit(t, (panelSize+15, i.getCenter()[1]))

            screen.blit(i.draw(), i.getCenter())
            i.tick()

            settings[i.id] = i.savedText

        settings["grid"] = showGrid.state

        #refreshes the screen
        screen.blit(display, (0,0))
        pygame.display.flip()
        display.fill((22,22,22))
        screen.fill((222,222,222))