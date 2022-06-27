from dataclasses import dataclass
import random
import time
from PIL import Image
from pathlib import Path
from string import hexdigits
from base64 import b64decode, b64encode


@dataclass
class Node:
    __pos: list

    def __post_init__(self):
        self._top = "1"
        self._bottom = "1"
        self._left = "1"
        self._right = "1"

        self._row = self.__pos[0]
        self._column = self.__pos[1]

    def _wallValueChecker(self, value):
        if value == "1" or value == "0":
            return True
        else:
            raise ValueError("wall value should be either \"1\" or \"0\"")

    def wallsFromBinary(self, wallBin):
        self._top = wallBin[0]
        self._bottom = wallBin[1]
        self._left = wallBin[2]
        self._right = wallBin[3]

    def debug(self):
        return [self.__pos, (self._top, self._bottom, self._left, self._right), self.key]

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, value):
        if self._wallValueChecker(value):
            self._top = value

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, value):
        if self._wallValueChecker(value):
            self._bottom = value

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        if self._wallValueChecker(value):
            self._left = value

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        if self._wallValueChecker(value):
            self._right = value

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @property
    def key(self):
        wallsStr = self._top + self._bottom + self._left + self._right
        return hex(int(wallsStr, 2))[2:]


class Maze:
    def __init__(self, maxX, maxY):
        # 2D list to store node objects - index matches coordinate in the maze
        self._list = [[None for _ in range(maxX)] for _ in range(maxY)]

    def insert(self, nodeObj):
        row = nodeObj.row
        column = nodeObj.column
        # maze starts at 1,1 but list indexing starts at [0][0]
        self._list[row - 1][column - 1] = nodeObj

    def node(self, coord):
        node = self._list[coord[0] - 1][coord[1] - 1]  # Changed
        return node


class MazeGenerator:
    def __init__(self, maxX, maxY, mazeHex):
        self._maze = Maze(maxX, maxY)

        self._nodes = []

        for row in range(1, maxY + 1):
            for column in range(1, maxX + 1):
                self._nodes.append([row, column])
        self._saveNodes = self._nodes.copy()

        self._adjacentCoords = ((-1, 0), (1, 0), (0, 1), (0, -1))

        self._maxX = maxX
        self._maxY = maxY
        self._mazeHex = mazeHex

        # number corresponds to hex value of the node's key
        self._tileNames = {'0': 'no-walls.png', '1': 'right-wall.png', '2': 'left-wall.png', '3': 'left-right-wall.png',
                           '4': 'bottom-wall.png', '5': 'bottom-right-corner.png', '6': 'bottom-left-corner.png',
                           '7': 'bottom-dead.png', '8': 'top-wall.png',
                           '9': 'top-right-corner.png', 'a': 'top-left-corner.png', 'b': 'top-dead.png',
                           'c': 'top-bottom-wall.png', 'd': 'right-dead.png',
                           'e': 'left-dead.png', 'f': 'all-walls.png'}

    @property
    def mazeHex(self):
        return self._mazeHex

    @mazeHex.setter
    def mazeHex(self, mazeHex):
        self._mazeHex = mazeHex

    def drawMaze(self):

        mazePath = Path('app/static/img/maze/')

        base = mazePath / 'base.png'
        img = Image.open(base)

        img = img.resize((self._maxX * 32 * 2 - 32, self._maxY * 32 * 2 - 32))
        # tiles are 32x32

        # debug = Image.open(mazePath / 'debug-tile.png')

        count = 0
        print(self._mazeHex)
        drawMazeFromHex = False
        if self._mazeHex:
            drawMazeFromHex = True

        for row in range(1, self._maxY + 1):
            for column in range(1, self._maxX + 1):
                if drawMazeFromHex:
                    node = Node([row, column])
                    tileHex = self._mazeHex[count]
                    tileBin = str(bin(int(tileHex, 16))[2:].zfill(4))
                    node.top = tileBin[0]
                    node.bottom = tileBin[1]
                    node.left = tileBin[2]
                    node.right = tileBin[3]
                else:
                    node = self._maze.node([row, column])

                adjNodes = []
                # getting the list of adjacent nodes from the dictionary
                if node.top == "0":
                    adjNodes.append([row - 1, column])
                if node.bottom == "0":
                    adjNodes.append([row + 1, column])
                if node.left == "0":
                    adjNodes.append([row, column - 1])
                if node.right == "0":
                    adjNodes.append([row, column + 1])

                # pasting the correct image (corresponding with the walls list) onto the main background image
                tile = mazePath / self._tileNames[node.key]
                tileImg = Image.open(tile)

                img.paste(tileImg, ((column - 1) * 64, (row - 1) * 64))

                for adjNode in adjNodes:
                    # figuring out where to place adjacent corridors based
                    join_y = ((adjNode[0] - node.row) / 2) + node.row
                    join_x = ((adjNode[1] - node.column) / 2) + node.column

                    # pasting corridors joining the nodes

                    if join_y - int(join_y) != 0:
                        tile = mazePath / 'left-right-wall.png'  # vertical corridor

                    elif join_x - int(join_x) != 0:
                        tile = mazePath / 'top-bottom-wall.png'  # horizontal corridor

                    tileImg = Image.open(tile)
                    img.paste(tileImg, (int((join_x - 1) * 64), int((join_y - 1) * 64)))

                self._mazeHex += node.key
                count += 1

        img.save(mazePath / 'fullmaze.png')

        print(self._mazeHex)

    # recursive backtracking | 19/09/21

    def recursiveBacktracking(self):

        stack = []
        start_time = time.time()
        nextPos = [1, 1]

        while True:

            currentPos = nextPos
            stack.append(currentPos)

            try:
                self._nodes.remove(currentPos)
            except ValueError:  # value error is raised if the current position has already been removed - occurs after maze reaches a dead end and backtracks
                pass

            possibleCoords = []

            # finding possible next nodes by comparing each position adjacent to the current node to the unused nodes
            for dy, dx in self._adjacentCoords:
                if [currentPos[0] + dy, currentPos[1] + dx] in self._nodes:
                    possibleCoords.append(
                        [currentPos[0] + dy, currentPos[1] + dx])
            if possibleCoords:
                # choosing a random (adjacent) node to go next
                nextPos = random.choice(possibleCoords)
                pair = [nextPos, currentPos]

                # updating (or adding if not already) nodes in maze
                for index, coord in enumerate(pair):
                    if not self._maze.node(coord):
                        node = Node(coord)
                    else:
                        node = self._maze.node(coord)

                    # working out which wall to remove
                    adjNode = pair[index - 1]
                    yDiff = coord[0] - adjNode[0]
                    xDiff = coord[1] - adjNode[1]
                    if yDiff > 0:
                        node.top = '0'
                    elif yDiff < 0:
                        node.bottom = '0'
                    if xDiff > 0:
                        node.left = '0'
                    elif xDiff < 0:
                        node.right = '0'

                    self._maze.insert(node)

            else:
                # checking each node from the stack for possible nodes, if there are none, removing it
                for index in range(len(stack) - 1, -1, -1):
                    checkPos = stack[index]
                    for dy, dx in self._adjacentCoords:
                        if [checkPos[0] + dy, checkPos[1] + dx] in self._nodes:
                            nextPos = checkPos
                            break
                    else:
                        try:
                            # using stack to keep track of which nodes to/ not to visit again
                            stack.pop()
                        except ValueError:
                            pass
                        continue
                    break

            if len(stack) == 0:
                break

        # end_time = time.time()-start_time
        # print((str(end_time)[:-(len(str(end_time).split('.')[1])-2)]) + 's')


class SeedGenerator:
    def __init__(self, height, width):
        self._height = self._twoDigitNumber(height)
        self._width = self._twoDigitNumber(width)
        self._mazeGenerator = MazeGenerator(self._height, self._width, '')
        self._mazeHex = ''
        self._seed = None

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, seed):
        self._seed = seed

    def _twoDigitNumber(self, number):
        if len(str(number)) < 2:
            return int('0' + str(number))
        return number

    def createBase64Seed(self):
        self._mazeGenerator.recursiveBacktracking()
        self._mazeGenerator.drawMaze()
        self._mazeHex = f'{self._height}{self._width}{self._mazeGenerator.mazeHex}'
        mazeHexBytes = self._mazeHex.encode()
        self._seed = b64encode(mazeHexBytes)
        print(self._seed)

    def drawMazeFromSeed(self, seed):
        self._seed = seed
        hexString = str(b64decode(self._seed))
        self._height = hexString[:2]
        self._width = hexString[2:4]
        self._mazeHex = hexString[4:]
        self._mazeGenerator.mazeHex = self._mazeHex
        self._mazeGenerator.drawMaze()



