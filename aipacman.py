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
SCREEN_WIDTH = 800
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
    def __init__(self, xcoor, ycoor):
        self.x = xcoor
        self.y = ycoor
        self.dirs = ['up', 'right', 'down', 'left']
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

    def changeDir(self):
        keys = pygame.key.get_pressed()

        prevDir = self.currDir

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

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, YELLOW, pygame.Rect(self.x, self.y, pacmanW, pacmanH))


class Ghost():
    def __init__(self, x, y, color, level, cDir):
        self.destinList = []
        self.x = x
        self.y = y
        self.color = color
        self.level = level
        self.dirs = ['up', 'right', 'down', 'left']
        self.currDir = None

    def move(self):
        global pacman

        speed = 3

        if len(self.destinList) < 1:
            self.destinList = pathfind(mapGraph.getNode(int(self.x/gridW), int(self.y/gridH)), mapGraph.getNode(int(pacman.x/gridW), int(pacman.y/gridH)))

        # pygame.draw.rect(DISPLAYSURF, YELLOW, pygame.Rect(rx * gridW, ry * gridH, pointW, pointH))

        if len(self.destinList) != 0 and mapGraph.getNode(int(self.x/gridW), int(self.y/gridH)) == self.destinList[0][1]:
            nDir = self.destinList[0][0]
            if nDir is not None:
                self.currDir = nDir
            del self.destinList[0]
            nx, ny = int(self.x/gridW), int(self.y/gridH)
            self.x = nx * gridW + (gridW - pacmanW)/2
            self.y = ny * gridH + (gridH - pacmanH)/2

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

        if self.currDir == 'up':
            self.y -= speed
        elif self.currDir == 'right':
            self.x += speed
        elif self.currDir == 'down':
            self.y += speed
        elif self.currDir == 'left':
            self.x -= speed

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


# Pathfinding method that will be shared by both PAC-MAN's
# AI and the different ghosts. It might end up being an
# A* implementation.
#
# params:
#     origin: an (x, y) tuple representing the element's starting
#             position
#
#     destiny: an (x, y) tuple representing the element's goal
#
#     weightfn: a function to determine the weight of each node,
#               defaults to None, so every node weights the same.
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
                cost = pathCost[currNode] + weightfn(mapGraph.getNode(nextNode.x, nextNode.y))
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
    if tile == ' ' and j - 1 > 0 and j + 1 < len(mapGrid[0]) and ((mapGrid[i][j-1] == '.' or mapGrid[i][j+1] == '.') or (mapGrid[i][j-1] == '#' or mapGrid[i][j+1] == '#')):
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


rx, ry = -1, -1


def main():
    loadMap('./levels/level3.txt')
    createMapGraph(findFirstPill())
    red = Ghost(4, 2, RED, 1, 2)
    red.transpose()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                rnode = mapGraph.nodes[random.randint(0, len(mapGraph.nodes))]
                global rx
                global ry
                rx = rnode.x
                ry = rnode.y
                print('Going to:', rx, ry)

        DISPLAYSURF.fill(BLACK)
        drawMap()
        pacman.changeDir()
        pacman.move()
        pacman.draw()

        # for node in mapGraph.nodes:
        #     pygame.draw.rect(DISPLAYSURF, RED, pygame.Rect(node.x * gridW+(gridW/2), node.y * gridH+(gridH/2), pointW*4, pointH*2))

        red.move()
        red.draw()
        pygame.display.update()
        FramePerSec.tick(FPS)


if __name__ == '__main__':
    main()
