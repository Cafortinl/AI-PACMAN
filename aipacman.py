'''
    Intelligent Systems class's main project

    Developed by:
        Carlos Fortín
        Mauricio Aguilera
        Jamil García
'''


class Pacman():
    def __init__(self, ycoor, xcoor):
        self.x = xcoor
        self.y = ycoor
        print('PAC-MAN created at:', self.x, self.y)

    def move():
        pass


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
    for i in range(len(mapGrid)):
        for j in range(len(mapGrid[0])):
            if i == pacman.y and j == pacman.x:
                print('<', end='')
            else:
                print(mapGrid[i][j], end='')

        print()


def main():
    loadMap('./levels/level2.txt')
    drawMap()


if __name__ == '__main__':
    main()
