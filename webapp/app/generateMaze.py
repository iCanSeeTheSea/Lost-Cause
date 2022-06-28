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
        self._binaryString = ''

    def insert(self, nodeObj):
        row = nodeObj.row
        column = nodeObj.column
        # maze starts at 1,1 but list indexing starts at [0][0]
        self._list[row - 1][column - 1] = nodeObj
        self._binaryString += f'{nodeObj.top}{nodeObj.bottom}{nodeObj.left}{nodeObj.right}'

    def node(self, coord):
        node = self._list[coord[0] - 1][coord[1] - 1]  # Changed
        return node

    @property
    def binaryString(self):
        return self._binaryString

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

        return(self._maze)


class SeedGenerator:
    def __init__(self, height, width):
        self._height = self._twoDigitNumber(height)
        self._width = self._twoDigitNumber(width)
        self._mazeGenerator = MazeGenerator(self._height, self._width, '')
        self._mazeHex = ''
        self._seed = None
        self._maze = None

        self._toBinary = {'A': '000000', 'B': '000001', 'C': '000010', 'D': '000011', 'E': '000100', 'F': '000101',
                    'G': '000110', 'H': '000111',
                    'I': '001000', 'J': '001001', 'K': '001010', 'L': '001011', 'M': '001100', 'N': '001101',
                    'O': '001110', 'P': '001111',
                    'Q': '010000', 'R': '010001', 'S': '010010', 'T': '010011', 'U': '010100', 'V': '010101',
                    'W': '010110', 'X': '010111',
                    'Y': '011000', 'Z': '011001', 'a': '011010', 'b': '011011', 'c': '011100', 'd': '011101',
                    'e': '011110', 'f': '011111',
                    'g': '100000', 'h': '100001', 'i': '100010', 'j': '100011', 'k': '100100', 'l': '100101',
                    'm': '100110', 'n': '100111',
                    'o': '101000', 'p': '101001', 'q': '101010', 'r': '101011', 's': '101100', 't': '101101',
                    'u': '101110', 'v': '101111',
                    'w': '110000', 'x': '110001', 'y': '110010', 'z': '110011', '0': '110100', '1': '110101',
                    '2': '110110', '3': '110111',
                    '4': '111000', '5': '111001', '6': '111010', '7': '111011', '8': '111100', '9': '111101',
                    '-': '111110', '_': '111111'}

        self._to64 = {'000000': 'A', '000001': 'B', '000010': 'C', '000011': 'D', '000100': 'E', '000101': 'F',
                '000110': 'G',
                '000111': 'H', '001000': 'I', '001001': 'J', '001010': 'K', '001011': 'L', '001100': 'M', '001101': 'N',
                '001110': 'O', '001111': 'P', '010000': 'Q', '010001': 'R', '010010': 'S', '010011': 'T', '010100': 'U',
                '010101': 'V', '010110': 'W', '010111': 'X', '011000': 'Y', '011001': 'Z', '011010': 'a', '011011': 'b',
                '011100': 'c', '011101': 'd', '011110': 'e', '011111': 'f', '100000': 'g', '100001': 'h', '100010': 'i',
                '100011': 'j', '100100': 'k', '100101': 'l', '100110': 'm', '100111': 'n', '101000': 'o', '101001': 'p',
                '101010': 'q', '101011': 'r', '101100': 's', '101101': 't', '101110': 'u', '101111': 'v', '110000': 'w',
                '110001': 'x', '110010': 'y', '110011': 'z', '110100': '0', '110101': '1', '110110': '2', '110111': '3',
                '111000': '4', '111001': '5', '111010': '6', '111011': '7', '111100': '8', '111101': '9', '111110': '-',
                '111111': '_'}

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
        self._maze = self._mazeGenerator.recursiveBacktracking()
        self._mazeGenerator.drawMaze()
        sizeBin = str(bin(int(self._height)))[2:].zfill(8) + str(bin(int(self._width)))[2:].zfill(8)
        print(sizeBin)
        binaryString = self._maze.binaryString

        padding = 0
        while len(binaryString) % 24 != 0:
            binaryString += '0'
            padding += 1
        padding //= 8

        binaryList = [binaryString[i:i + 6] for i in range(0, len(binaryString), 6)]

        base64String = ''
        for value in binaryList:
            base64String += self._to64[value]
        base64String += '=' * padding

        print(base64String)
        self._seed = base64String


    def drawMazeFromSeed(self, seed):
        self._seed = seed
        hexString = str(b64decode(self._seed))
        self._height = hexString[:2]
        self._width = hexString[2:4]
        self._mazeHex = hexString[4:]
        self._mazeGenerator.mazeHex = self._mazeHex
        self._mazeGenerator.drawMaze()



