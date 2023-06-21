'''
    Intelligent Systems class's main project

    Developed by:
        Carlos Fortín
        Mauricio Aguilera
        Jamil García
'''
import pygame
import sys


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

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("AI-PACMAN")


class Pacman():
    def __init__(self, ycoor, xcoor):
        self.x = xcoor
        self.y = ycoor


class Ghost():
    def __init__(self):
        pass

    def move():
        pass


# Level related globals
mapGrid = []
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

def move():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman.x -= 1
    if keys[pygame.K_RIGHT]:
        pacman.x += 1
    if keys[pygame.K_UP]:
        pacman.y -= 1
    if keys[pygame.K_DOWN]:
        pacman.y += 1
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
                pacman = Pacman(i, j)
            elif line[j] != '\n':
                mapGrid[i].append(line[j])


def drawMap():

    gridW = SCREEN_WIDTH/len(mapGrid[0])
    gridH = SCREEN_HEIGHT/len(mapGrid)
    pmW = gridW / 2
    pmH = gridH / 2
    piW = gridW / 4
    piH = gridH / 4

    # Temporal code, just for tests. Eventually we'll draw images containing sprites.
    for i in range(len(mapGrid)):
        for j in range(len(mapGrid[0])):
            if i == pacman.y and j == pacman.x:
                pygame.draw.rect(DISPLAYSURF, YELLOW, pygame.Rect(j * gridW + (gridW - pmW)/2, i * gridH + (gridH - pmH)/2, pmW, pmH))
            elif mapGrid[i][j] == '.':
                pygame.draw.rect(DISPLAYSURF, WHITE, pygame.Rect(j * gridW + (gridW - piW)/2, i * gridH + (gridH - piH)/2, piW, piH))
            else:
                pygame.draw.rect(DISPLAYSURF, BLUE, pygame.Rect(j * gridW, i * gridH, gridW, gridH))


def main():
    loadMap('./levels/level2.txt')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            move()
            DISPLAYSURF.fill(BLACK)
            drawMap()
            pygame.display.update()
            FramePerSec.tick(FPS)
        


if __name__ == '__main__':
    main()
