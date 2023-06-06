''' Intelligent Systems class's main project

    Developed by:
        Carlos Fortín
        Mauricio Aguilera
        Jamil García
'''
import pygame
import sys
import math


pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Predefined some colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Screen information
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

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

    def __str__(self):
        retStr = str(self.x) + ',' + str(self.y) + '\n'
        for key in self.neigbors.keys():
            if self.neigbors[key] is not None:
                retStr += '\t' + key + ': ' + str(self.neigbors[key].x) + ', ' + str(self.neigbors[key].y) + '\n'
            else:
                retStr += '\t' + key + ': ' + 'None\n'

        return retStr


class Pacman():
    def __init__(self, xcoor, ycoor):
        self.x = xcoor
        self.y = ycoor

    def move(self):
        pass

    def transpose(self):
        self.x = self.x * gridW + (gridW/2)
        self.y = self.y * gridH + (gridH/2)

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, YELLOW, pygame.Rect(self.x, self.y, pacmanW, pacmanH))


class Ghost():
    def __init__(self):
        pass

    def move():
        pass

    def draw():
        pass


# Level related globals
mapGrid = []
mapGraph = Graph()
pacman = Pacman


# Pathfinding method that will be shared by both PAC-MAN's
# AI and the different ghosts. It might end up being an
# A* implementation.
#
# params:
#     origin: an (x, y) tuple representing the element's starting
#             position
#
#     destiny: an (x, y) tuple representing the element's goal
def pathfind(origin, destiny):
    pass


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
                mapGrid[i].append(' ')
                pacman = Pacman(j, i)
            elif line[j] != '\n':
                mapGrid[i].append(line[j])

    updateDrawindDims()


def isWalkable(tile):
    if tile == '.' or tile == '*' or tile == '#':
        return True
    return False


def findFirstWalkable():
    tempNode = Node
    firstNode = (-1, -1)

    for i in range(len(mapGrid)):
        if firstNode[0] == -1 and firstNode[1] == -1:
            for j in range(len(mapGrid[0])):
                if isWalkable(mapGrid[i][j]):
                    firstNode = (i, j)
                    break

    mapGraph.addNode(Node(firstNode[1], firstNode[0], mapGrid[firstNode[0]][firstNode[1]] == '.', mapGrid[firstNode[0]][firstNode[1]] == '*'))
    tempNode = mapGraph.getNode(firstNode[1], firstNode[0])
    return tempNode


def createMapGraph(node):
    i = node.y
    j = node.x

    if i - 1 >= 0 and isWalkable(mapGrid[i - 1][j]) and mapGraph.getNode(j, i - 1) is None:
        currNode = Node(j, i - 1, mapGrid[i - 1][j] == '.', mapGrid[i - 1][j] == '*')
        currNode.setNeighbor(node, 'down')
        mapGraph.addNode(currNode)
        createMapGraph(currNode)

    if i + 1 < len(mapGrid) and isWalkable(mapGrid[i + 1][j]) and mapGraph.getNode(j, i + 1) is None:
        currNode = Node(j, i + 1, mapGrid[i + 1][j] == '.', mapGrid[i + 1][j] == '*')
        currNode.setNeighbor(node, 'up')
        mapGraph.addNode(currNode)
        createMapGraph(currNode)

    if j - 2 >= 0 and isWalkable(mapGrid[i][j - 2]) and mapGraph.getNode(j - 2, i) is None:
        currNode = Node(j - 2, i, mapGrid[i][j - 2] == '.', mapGrid[i][j - 2] == '*')
        currNode.setNeighbor(node, 'right')
        mapGraph.addNode(currNode)
        createMapGraph(currNode)

    if j + 2 < len(mapGrid[0]) and isWalkable(mapGrid[i][j + 2]) and mapGraph.getNode(j + 2, i) is None:
        currNode = Node(j + 2, i, mapGrid[i][j + 2] == '.', mapGrid[i][j + 2] == '*')
        currNode.setNeighbor(node, 'left')
        mapGraph.addNode(currNode)
        createMapGraph(currNode)

    if i - 1 >= 0 and isWalkable(mapGrid[i - 1][j]) and mapGraph.getNode(j, i - 1) is not None:
        node.setNeighbor(mapGraph.getNode(j, i - 1), 'up')

    if i + 1 < len(mapGrid) and isWalkable(mapGrid[i + 1][j]) and mapGraph.getNode(j, i + 1) is not None:
        node.setNeighbor(mapGraph.getNode(j, i + 1), 'down')

    if j - 2 >= 0 and isWalkable(mapGrid[i][j - 2]) and mapGraph.getNode(j - 2, i) is not None:
        node.setNeighbor(mapGraph.getNode(j - 2, i), 'left')

    if j + 2 < len(mapGrid[0]) and isWalkable(mapGrid[i][j + 2]) and mapGraph.getNode(j + 2, i) is not None:
        node.setNeighbor(mapGraph.getNode(j + 2, i), 'right')


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
                pygame.draw.arc(DISPLAYSURF, BLUE, [(j * gridW - (gridW * 0.4)) - 2, (i * gridH + (gridH/2)), gridW, gridH], 0, pi / 2, 3)
            if mapGrid[i][j] == '{':
                pygame.draw.arc(DISPLAYSURF, BLUE, [(j * gridW + (gridW/2)), (i * gridH + (gridH/2)), gridW, gridH], pi / 2, pi, 3)
            if mapGrid[i][j] == '(':
                pygame.draw.arc(DISPLAYSURF, BLUE, [(j * gridW + (gridW/2)), (i * gridH - (gridH* 0.4)), gridW, gridH], pi, 3 * pi / 2, 3)
            if mapGrid[i][j] == ')':
                pygame.draw.arc(DISPLAYSURF, BLUE, [(j * gridW - (gridW * 0.4)) - 2, (i * gridH - (gridH * 0.4)), gridW, gridH], 3 * pi / 2, 2 * pi, 3)
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


def main():
    loadMap('./levels/level3.txt')
    createMapGraph(findFirstWalkable())
    # mapGraph.print()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            DISPLAYSURF.fill(BLACK)
            drawMap()
            pacman.draw()
            pygame.display.update()
            FramePerSec.tick(FPS)


if __name__ == '__main__':
    main()
