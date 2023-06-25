''' Intelligent Systems class's main project

    Developed by:
        Carlos Fortín
        Mauricio Aguilera
        Jamil García
'''
import pygame
import sys
import math
import heapq
import random
import json


pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()
index=0

# Predefined some colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
CYAN = (0,200,200)

# Screen information
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# Drawing information
gridW = 0
gridH = 0
pacmanW = 0
pacmanH = 0
pointW = 0
pointH = 0

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("AI-PACMAN")
pi = math.pi


class Graph():
    def __init__(self):
        self.nodes = []
        self.nodeDict = {}

    def addNode(self, node):
        self.nodes.append(node)
        key = str(node.x) + ',' + str(node.y)
        self.nodeDict[key] = self.nodes.index(node)

    def getNode(self, x, y):
        key = str(x) + ',' + str(y)
        if key in self.nodeDict:
            return self.nodes[self.nodeDict[key]]
        else:
            return None

    def setNode(self, x, y, node):
        key = str(x) + ',' + str(y)
        if key in self.nodeDict:
            self.nodes[self.nodeDict[key]] = node

    def print(self):
        for node in self.nodes:
            print(node)

#class to load spritesheets of the assets, needs the spritesheet as a png and the corresponding json
class Spritesheet():
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close
        
    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w,h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet,(0,0),(x, y, w, h))
        return sprite
    
    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite['x'], sprite['y'], sprite['w'], sprite['h']
        image = self.get_sprite(x, y, w, h)
        return image
        
        

class Node():
    def __init__(self, x, y, hasPill, hasSuperPill):
        self.x = x
        self.y = y
        self.hasPill = hasPill
        self.hasSuperPill = hasSuperPill
        self.neigbors = {'up': None, 'down': None, 'right': None, 'left': None}

    def setNeighbor(self, node, direction):
        self.neigbors[direction] = node

    def getNeighbors(self):
        return self.neigbors

    def getReachableNeighbors(self):
        return {k: v for k, v in self.neigbors.items() if v is not None}

    def __str__(self):
        retStr = str(self.x) + ',' + str(self.y) + '\n'
        for key in self.neigbors.keys():
            if self.neigbors[key] is not None:
                retStr += '\t' + key + ': ' + str(self.neigbors[key].x) + ', ' + str(self.neigbors[key].y) + '\n'
            else:
                retStr += '\t' + key + ': ' + 'None\n'

        return retStr

    def getName(self):
        return str(self.x) + ', ' + str(self.y)


class Pacman():
    currDir = ''
    def __init__(self, xcoor, ycoor):
        self.x = xcoor
        self.y = ycoor
        self.prevX = self.x
        self.prevY = self.y
        # self.dirs = ['up', 'right', 'down', 'left']
        self.currDir = None
        self.speed = 3

    def move(self):
        if self.currDir == 'up':
            self.y -= self.speed
            if mapGraph.getNode(int(self.x/gridW), int(self.y/gridH)) is None:
                self.y += self.speed
                nx, ny = int(self.x/gridW), int(self.y/gridH)
                self.x = nx * gridW + (gridW - pacmanW)/2
                self.y = ny * gridH + (gridH - pacmanH)/2
                self.currDir = None
        elif self.currDir == 'right':
            self.x += self.speed
            if mapGraph.getNode(int(self.x/gridW), int(self.y/gridH)) is None:
                self.x -= self.speed
                nx, ny = int(self.x/gridW), int(self.y/gridH)
                self.x = nx * gridW + (gridW - pacmanW)/2
                self.y = ny * gridH + (gridH - pacmanH)/2
                self.currDir = None
        elif self.currDir == 'down':
            self.y += self.speed
            if mapGraph.getNode(int(self.x/gridW), int(self.y/gridH)) is None:
                self.y -= self.speed
                nx, ny = int(self.x/gridW), int(self.y/gridH)
                self.x = nx * gridW + (gridW - pacmanW)/2
                self.y = ny * gridH + (gridH - pacmanH)/2
                self.currDir = None
        elif self.currDir == 'left':
            self.x -= self.speed
            if mapGraph.getNode(int(self.x/gridW), int(self.y/gridH)) is None:
                self.x += self.speed
                nx, ny = int(self.x/gridW), int(self.y/gridH)
                self.x = nx * gridW + (gridW - pacmanW)/2
                self.y = ny * gridH + (gridH - pacmanH)/2
                self.currDir = None

        currNode = mapGraph.getNode(int(self.x/gridW), int(self.y/gridH))
        if currNode is not None:
            self.prevX = currNode.x
            self.prevY = currNode.y
        else:
            print('Pacman in illegal position')

    def changeDir(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.currDir = 'left'
            
        if keys[pygame.K_RIGHT]:
            self.currDir = 'right'
        if keys[pygame.K_UP]:
            self.currDir = 'up'
        if keys[pygame.K_DOWN]:
            self.currDir = 'down'

        # node = mapGraph.getNode(int(self.x/gridW), int(self.y/gridH))

        # if node is None:
        #     if self.currDir == 'up':
        #         self.y += self.speed
        #     elif self.currDir == 'right':
        #         self.x -= self.speed
        #     elif self.currDir == 'down':
        #         self.y -= self.speed
        #     elif self.currDir == 'left':
        #         self.x += self.speed

        # if self.currDir not in list(node.getReachableNeighbors().keys()):
        #     self.currDir = prevDir

        # if self.currDir != prevDir:
        #     nx, ny = int(self.x/gridW), int(self.y/gridH)
        #     self.x = nx * gridW + (gridW - pacmanW)/2
        #     self.y = ny * gridH + (gridH - pacmanH)/2

    def transpose(self):
        self.x = self.x * gridW + (gridW/2)
        self.y = self.y * gridH + (gridH/2)
        self.prevX = int(self.x/gridW)
        self.prevY = int(self.y/gridH)

    def draw(self, sprites):
        DISPLAYSURF.blit(sprites, (self.x, self.y))
        
    def getDir(self):
        return self.currDir
        


class Ghost():
    def __init__(self, x, y, color, level, cDir, target):
        self.destinList = []
        self.x = x
        self.y = y
        self.color = color
        self.level = level
        self.dirs = ['up', 'right', 'down', 'left']
        self.currDir = None
        self.targetfn = target

    def move(self):
        global pacman

        speed = 3

        px, py = self.targetfn()

        if euclideanDistance(int(self.x/gridW), px, int(self.y/gridH), py) > 5:
            self.destinList.clear()
            self.destinList = pathfind(mapGraph.getNode(int(self.x/gridW), int(self.y/gridH)), mapGraph.getNode(px, py), ghostPathWeightFunction)

        if len(self.destinList) != 0 and mapGraph.getNode(int(self.x/gridW), int(self.y/gridH)) == self.destinList[0][1]:
            nDir = self.destinList[0][0]
            if nDir is not None:
                self.currDir = nDir
            else:
                i = int(self.y/gridH)
                j = int(self.x/gridW)

                if self.currDir == 'up':
                    i -= 1
                elif self.currDir == 'right':
                    j += 1
                elif self.currDir == 'down':
                    i += 1
                elif self.currDir == 'left':
                    j -= 1

                self.destinList.append((self.currDir, mapGraph.getNode(int(self.x/gridW), int(self.y/gridH))))

            del self.destinList[0]

        if self.currDir == 'up':
            self.y -= speed
            if mapGraph.getNode(int(self.x/gridW), int(self.y/gridH)) is None:
                self.y += speed
                nx, ny = int(self.x/gridW), int(self.y/gridH)
                self.x = nx * gridW + (gridW - pacmanW)/2
                self.y = ny * gridH + (gridH - pacmanH)/2
                self.currDir = None
        elif self.currDir == 'right':
            self.x += speed
            if mapGraph.getNode(int(self.x/gridW), int(self.y/gridH)) is None:
                self.x -= speed
                nx, ny = int(self.x/gridW), int(self.y/gridH)
                self.x = nx * gridW + (gridW - pacmanW)/2
                self.y = ny * gridH + (gridH - pacmanH)/2
                self.currDir = None
        elif self.currDir == 'down':
            self.y += speed
            if mapGraph.getNode(int(self.x/gridW), int(self.y/gridH)) is None:
                self.y -= speed
                nx, ny = int(self.x/gridW), int(self.y/gridH)
                self.x = nx * gridW + (gridW - pacmanW)/2
                self.y = ny * gridH + (gridH - pacmanH)/2
                self.currDir = None
        elif self.currDir == 'left':
            self.x -= speed
            if mapGraph.getNode(int(self.x/gridW), int(self.y/gridH)) is None:
                self.x += speed
                nx, ny = int(self.x/gridW), int(self.y/gridH)
                self.x = nx * gridW + (gridW - pacmanW)/2
                self.y = ny * gridH + (gridH - pacmanH)/2
                self.currDir = None

        # prevDir = self.currDir
        # currNode = mapGraph.getNode(int(self.x/gridW), int(self.y/gridH))
        # bestDist = manhattanDistance(currNode.x, pacman.x, currNode.y, pacman.y)
        # reachables = currNode.getReachableNeighbors()

        # for neighbor in reachables.keys():
        #     node = reachables[neighbor]
        #     print(bestDist,end=' ')
        #     if manhattanDistance(node.x, pacman.x, node.y, pacman.y) < bestDist and (prevDir is None or abs(self.dirs.index(prevDir) - self.dirs.index(neighbor)) != 2):
        #         print('vs', manhattanDistance(node.x, pacman.x, node.y, pacman.y))
        #         bestDist = manhattanDistance(node.x, pacman.x, node.y, pacman.y)
        #         self.currDir = neighbor

        # if self.currDir not in reachables.keys():
        #     self.currDir = list(reachables.keys())[random.randint(0, len(reachables.keys()) - 1)]

        # if self.currDir != prevDir:
        #     nx, ny = int(self.x/gridW), int(self.y/gridH)
        #     self.x = nx * gridW + (gridW - pacmanW)/2
        #     self.y = ny * gridH + (gridH - pacmanH)/2

        #if self.currDir == 'up':
        #    self.y -= speed
        #elif self.currDir == 'right':
        #    self.x += speed
        #elif self.currDir == 'down':
        #    self.y += speed
        #elif self.currDir == 'left':
        #    self.x -= speed

    def rotate(self, rotDir):
        '''
        self.dirs.index(self.currDir) + rotDir -> new index relative to the original position
        + len(self.dirs) -> offsets negative values
        % len(self.dirs) -> makes it so the new index is inside the list's range
        '''
        self.currDir = self.dirs[((self.dirs.index(self.currDir) + rotDir) + len(self.dirs)) % len(self.dirs)]

    def transpose(self):
        self.x = self.x * gridW + (gridW/2)
        self.y = self.y * gridH + (gridH/2)

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, self.color, pygame.Rect(self.x, self.y, pacmanW, pacmanH))


# Level related globals
mapGrid = []
mapGraph = Graph()
pacman = Pacman


def euclideanDistance(x1, x2, y1, y2):
    return math.sqrt(((x1 - x2)**2) + ((y1 - y2)**2))


def manhattanDistance(x1, x2, y1, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def straightenVisitOrder(visitOrder, origin, destiny):
    path = []
    dirArr = [None]

    currNode = destiny

    if destiny not in visitOrder:
        return []

    while currNode is not None:
        path.append(currNode)
        nNode = visitOrder[currNode]
        if nNode is None:
            break
        nNNeighbors = nNode.getNeighbors()
        dirArr.append(list(nNNeighbors.keys())[list(nNNeighbors.values()).index(currNode)])
        currNode = nNode

    path.reverse()
    dirArr.reverse()

    return list(path), list(dirArr)


def pruneVisitOrder(visitOrder, dirs):
    nVisitOrder = []
    lastDir = None

    for k in range(len(visitOrder)):
        newDir = dirs[k]

        if lastDir is None or lastDir != newDir:
            lastDir = newDir
            nVisitOrder.append((lastDir, visitOrder[k]))
        else:
            continue

    return nVisitOrder


def pathfind(origin, destiny, weightfn=None):
    frontier = []
    visitOrder = {}
    pathCost = {}

    insertCounter = 0
    heapq.heappush(frontier, (0, insertCounter, origin))
    visitOrder[origin] = None
    pathCost[origin] = 0

    while len(frontier) > 0:
        currNode = heapq.heappop(frontier)[2]

        if currNode == destiny:
            break

        for k in currNode.getReachableNeighbors().keys():
            nextNode = currNode.getNeighbors()[k]

            if weightfn is not None:
                cost = pathCost[currNode] + weightfn(currNode, mapGraph.getNode(nextNode.x, nextNode.y), k)
            else:
                cost = pathCost[currNode] + 1

            if nextNode not in pathCost or cost < pathCost[nextNode]:
                pathCost[nextNode] = cost
                nodePriority = cost + manhattanDistance(nextNode.x, destiny.x, nextNode.y, destiny.y)
                insertCounter += 1
                heapq.heappush(frontier, (nodePriority, insertCounter, nextNode))
                visitOrder[nextNode] = currNode

    retTuple = straightenVisitOrder(visitOrder, origin, destiny)
    visitOrder, visitDirs = retTuple[0], retTuple[1]
    visitOrder = pruneVisitOrder(visitOrder, visitDirs)
    return visitOrder


def ghostPathWeightFunction(currNode, nextNode, currDir):
    dirs = ['up', 'right', 'down', 'left']

    nDir = list(currNode.getNeighbors().keys())[list(currNode.getNeighbors().values()).index(nextNode)]

    if currDir is None or abs(dirs.index(currDir) - dirs.index(nDir)) != 2:
        return 1
    else:
        return float('inf')


def loadMap(levelPath):
    level = open(levelPath, 'r')

    metadataStr = level.readline()
    dimArr = metadataStr.split(',')

    global mapGrid
    global pacman

    for i in range(int(dimArr[0])):
        mapGrid.append([])
        line = level.readline()

        for j in range(int(dimArr[1])):
            if line[j] == 'P':
                mapGrid[i].append('.')
                pacman = Pacman(j, i)
            elif line[j] != '\n':
                mapGrid[i].append(line[j])

    updateDrawindDims()


def isWalkable(i, j):
    tile = mapGrid[i][j]
    if tile == '.' or tile == '*' or tile == '#':
        return True
    if tile == ' ' and j - 1 > 0 and j + 1 < len(mapGrid[0]) and ((mapGrid[i][j-1] == '.' or mapGrid[i][j+1] == '.') or (mapGrid[i][j-1] == '#' or mapGrid[i][j+1] == '#') or (mapGrid[i][j-1] == '*' or mapGrid[i][j+1] == '*')):
        return True
    return False


def findFirstPill():
    tempNode = Node
    firstNode = (-1, -1)

    for i in range(len(mapGrid)):
        if firstNode[0] == -1 and firstNode[1] == -1:
            for j in range(len(mapGrid[0])):
                if mapGrid[i][j] == '.':
                    print('fount at', i, ',', j)
                    firstNode = (i, j)
                    break

    mapGraph.addNode(Node(firstNode[1], firstNode[0], mapGrid[firstNode[0]][firstNode[1]] == '.', mapGrid[firstNode[0]][firstNode[1]] == '*'))
    tempNode = mapGraph.getNode(firstNode[1], firstNode[0])
    return tempNode


def createMapGraph(node):
    i = node.y
    j = node.x

    if i - 1 >= 0 and isWalkable(i - 1, j) and mapGraph.getNode(j, i - 1) is None:
        currNode = Node(j, i - 1, mapGrid[i - 1][j] == '.', mapGrid[i - 1][j] == '*')
        currNode.setNeighbor(node, 'down')
        mapGraph.addNode(currNode)
        createMapGraph(currNode)

    if i + 1 < len(mapGrid) and isWalkable(i + 1, j) and mapGraph.getNode(j, i + 1) is None:
        currNode = Node(j, i + 1, mapGrid[i + 1][j] == '.', mapGrid[i + 1][j] == '*')
        currNode.setNeighbor(node, 'up')
        mapGraph.addNode(currNode)
        createMapGraph(currNode)

    if j - 1 >= 0 and isWalkable(i, j - 1) and mapGraph.getNode(j - 1, i) is None:
        currNode = Node(j - 1, i, mapGrid[i][j - 1] == '.', mapGrid[i][j - 1] == '*')
        currNode.setNeighbor(node, 'right')
        mapGraph.addNode(currNode)
        createMapGraph(currNode)

    if j + 1 < len(mapGrid[0]) and isWalkable(i, j + 1) and mapGraph.getNode(j + 1, i) is None:
        currNode = Node(j + 1, i, mapGrid[i][j + 1] == '.', mapGrid[i][j + 1] == '*')
        currNode.setNeighbor(node, 'left')
        mapGraph.addNode(currNode)
        createMapGraph(currNode)

    if i - 1 >= 0 and isWalkable(i - 1, j) and mapGraph.getNode(j, i - 1) is not None:
        node.setNeighbor(mapGraph.getNode(j, i - 1), 'up')

    if i + 1 < len(mapGrid) and isWalkable(i + 1, j) and mapGraph.getNode(j, i + 1) is not None:
        node.setNeighbor(mapGraph.getNode(j, i + 1), 'down')

    if j - 1 >= 0 and isWalkable(i, j - 1) and mapGraph.getNode(j - 1, i) is not None:
        node.setNeighbor(mapGraph.getNode(j - 1, i), 'left')

    if j + 1 < len(mapGrid[0]) and isWalkable(i, j + 1) and mapGraph.getNode(j + 1, i) is not None:
        node.setNeighbor(mapGraph.getNode(j + 1, i), 'right')


def updateDrawindDims():
    global gridW
    gridW = SCREEN_WIDTH/len(mapGrid[0])
    global gridH
    gridH = SCREEN_HEIGHT/len(mapGrid)
    global pacmanW
    pacmanW = gridW / 2
    global pacmanH
    pacmanH = gridH / 2
    global pointW
    pointW = gridW / 4
    global pointH
    pointH = gridH / 4
    pacman.transpose()


def drawMap():
    # Temporal code, just for tests. Eventually we'll draw images containing sprites.
    for i in range(len(mapGrid)):
        for j in range(len(mapGrid[0])):
            if mapGrid[i][j] == '.':
                pygame.draw.rect(DISPLAYSURF, WHITE, pygame.Rect(j * gridW+(gridW/2), i * gridH+(gridH/2), pointW*2, pointH))
            if mapGrid[i][j] == '*':
                pygame.draw.rect(DISPLAYSURF, WHITE, pygame.Rect(j * gridW+(gridW/2), i * gridH+(gridH/2), pointW*4, pointH*2))
            if mapGrid[i][j] =='|':
                pygame.draw.line(DISPLAYSURF, BLUE, [j * gridW+(gridW/2), i * gridH], [j * gridW+(gridW/2), i * gridH + gridH], 5)
            if mapGrid[i][j] == '_':
                pygame.draw.line(DISPLAYSURF, BLUE, [j * gridW, i * gridH+(gridH/2)], [j * gridW +gridW*2, i * gridH+(gridH/2)], 5)
            # if i == pacman.y and j == pacman.x:
            #     pygame.draw.rect(DISPLAYSURF, YELLOW, pygame.Rect(j * gridW+(gridW/2), i * gridH+(gridH/2), pacmanW, pacmanH))
            if mapGrid[i][j] == '}':
                pygame.draw.arc(DISPLAYSURF, BLUE, [(j * gridW - (gridW * 0.4)) - 2, (i * gridH + (gridH/2)), gridW*1.3, gridH], 0, pi / 2, 5)
            if mapGrid[i][j] == '{':
                pygame.draw.arc(DISPLAYSURF, BLUE, [(j * gridW + (gridW/2)), (i * gridH + (gridH/2)), gridW*3, gridH], pi / 2, pi, 5)
            if mapGrid[i][j] == '(':
                pygame.draw.arc(DISPLAYSURF, BLUE, [(j * gridW + (gridW/2)), (i * gridH - (gridH* 0.4)), gridW*3, gridH], pi, 3 * pi / 2, 5)
            if mapGrid[i][j] == ')':
                pygame.draw.arc(DISPLAYSURF, BLUE, [(j * gridW - (gridW * 0.4)) - 2, (i * gridH - (gridH * 0.4)), gridW*1.3, gridH], 3 * pi / 2, 2 * pi, 5)
            if mapGrid[i][j] =='+':
                pygame.draw.line(DISPLAYSURF, WHITE, (j * gridW, i * gridH + (gridH/2)), (j * gridW + gridW*2, i * gridH + (gridH/2)), 3)
            '''
            if i == pacman.y and j == pacman.x:
                pygame.draw.rect(DISPLAYSURF, YELLOW, pygame.Rect(j * gridW + (gridW - pacmanW)/2, i * gridH + (gridH - pacmanH)/2, pacmanW, pacmanH))
            elif mapGrid[i][j] == '.':
                pygame.draw.rect(DISPLAYSURF, WHITE, pygame.Rect(j * gridW + (gridW - pointW)/2, i * gridH + (gridH - pointH)/2, pointW, pointH))
            else:
                pygame.draw.rect(DISPLAYSURF, BLUE, pygame.Rect(j * gridW, i * gridH, gridW, gridH))
            '''


rx, ry = -1, -1


def redTarget():
    return pacman.prevX, pacman.prevY


def pinkTarget():
    x, y = pacman.prevX, pacman.prevY
    pmDir = pacman.currDir
    if pmDir is not None and mapGraph.getNode(x, y).getNeighbors()[pmDir] is not None:
        if pmDir == 'up':
            y -= 1
        elif pmDir == 'right':
            x += 1
        elif pmDir == 'down':
            y += 1
        elif pmDir == 'left':
            x -= 1

    return x, y

def cyanTarget():
    x, y = pacman.prevX, pacman.prevY
    pmDir = pacman.currDir
    if pmDir is not None and mapGraph.getNode(x, y).getNeighbors()[pmDir] is not None:
        if pmDir == 'up':
            y -= 1
        elif pmDir == 'right':
            x += 1
        elif pmDir == 'down':
            y += 1
        elif pmDir == 'left':
            x -= 1
    tempx, tempy = (x)+(x-int(red.x/gridW)), (y)+(y-int(red.y/gridH))
    if mapGraph.getNode(tempx, tempy) is not None:
        x, y = tempx, tempy
        print('Blinky: '+str([int(red.x/gridW),int(red.y/gridH)])+' Pacman: '+str([pacman.prevX, pacman.prevY])+' Inky: '+str([x,y]))
    return x, y

def orangeTarget():
    pass
# def to update the sprites used by pac-man
def updateSprite():
    if(pacman.currDir=='left'):
        sprite_pacman = [spritesheet.parse_sprite('pac-man_left1.png'), spritesheet.parse_sprite('pac-man_left2.png'),
                 spritesheet.parse_sprite('pac-man_full.png'), spritesheet.parse_sprite('pac-man_left2.png')]
    elif(pacman.currDir=='down'):
        sprite_pacman = [spritesheet.parse_sprite('pac-man_down1.png'), spritesheet.parse_sprite('pac-man_down2.png'),
                 spritesheet.parse_sprite('pac-man_full.png'), spritesheet.parse_sprite('pac-man_down2.png')]   
    elif(pacman.currDir=='up'):
        sprite_pacman = [spritesheet.parse_sprite('pac-man_up1.png'), spritesheet.parse_sprite('pac-man_up2.png'),
                 spritesheet.parse_sprite('pac-man_full.png'), spritesheet.parse_sprite('pac-man_up2.png')]
    else:
        sprite_pacman = [spritesheet.parse_sprite('pac-man_right1.png'), spritesheet.parse_sprite('pac-man_right2.png'),
                 spritesheet.parse_sprite('pac-man_full.png'), spritesheet.parse_sprite('pac-man_right2.png')]
    return sprite_pacman

spritesheet = Spritesheet('sprites/pacman.png')


def main():
    global index
    global sprite_pacman
    global red
    sprite_pacman = [spritesheet.parse_sprite('pac-man_right1.png'), spritesheet.parse_sprite('pac-man_right2.png'),
                 spritesheet.parse_sprite('pac-man_full.png'), spritesheet.parse_sprite('pac-man_right2.png')]
    loadMap('./levels/level3.txt')
    createMapGraph(findFirstPill())
    red = Ghost(4, 2, RED, 1, 2, redTarget)
    yellow = Ghost(54, 2, GREEN, 1, 2, pinkTarget)
    cyan = Ghost(54, 4, CYAN, 1, 2, cyanTarget)
    red.transpose()
    yellow.transpose()
    cyan.transpose()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        DISPLAYSURF.fill(BLACK)
        drawMap()
        red.move()
        yellow.move()
        cyan.move()
        red.draw()
        yellow.draw()
        cyan.draw()
        pacman.changeDir()
        pacman.move()
        pacman.draw(updateSprite()[index])
        index = (index+1) % len(sprite_pacman)

        # for node in mapGraph.nodes:
        #     pygame.draw.rect(DISPLAYSURF, RED, pygame.Rect(node.x * gridW+(gridW/2), node.y * gridH+(gridH/2), pointW*4, pointH*2))

        pygame.display.update()
        FramePerSec.tick(FPS)


if __name__ == '__main__':
    main()
