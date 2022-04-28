import random
import time
from PIL import Image
from pathlib import Path
from base64 import b64decode


class Node:
    def __init__(self, node: list, walls: dict):
        self._id = node
        self._walls = walls

        # generates a unique identifier based on the adjacent walls
        self._key = hex(int(str(walls["top"]) +
                        str(walls["bottom"]) +
                        str(walls["left"]) + str(walls["right"]), 2))[2:]

    def key(self):
        return self._key

    def getWalls(self):
        return self._walls

    def top(self):
        return self._walls["top"]

    def bottom(self):
        return self._walls["bottom"]

    def left(self):
        return self._walls["left"]

    def right(self):
        return self._walls["right"]

    def row(self):
        return self._id[0]

    def column(self):
        return self._id[1]


class AdjacencyList:
    def __init__(self, maxX, maxY):
        # 2D list to store node objects - index matches coordinate in the maze
        self._list = [[None for _ in range(maxX)] for _ in range(maxY)]

    def insert(self, node):
        row = node.row()
        column = node.column()
        # maze starts at 1,1 but list indexing starts at [0][0]
        self._list[row-1][column-1] = node

    def get(self, row, column):
        node = self._list[row-1][column-1]
        return node


class MazeGenerator:
    def __init__(self, maxX, maxY):
        self._adjacencyList = AdjacencyList(maxX, maxY)

        self._nodes = []

        for x in range(1, maxX+1):
            for y in range(1, maxY+1):
                self._nodes.append([x, y])
        self._save_nodes = self._nodes.copy()

        self._adjacent_nodes = ((-1, 0), (1, 0), (0, 1), (0, -1))

        self._maxX = maxX
        self._maxY = maxY

        # number corresponds to hex value of the node's key
        self._tileNames = {'0': 'no-walls.png', '1': 'right-wall.png', '2': 'left-wall.png', '3': 'left-right-wall.png',
                           '4': 'bottom-wall.png', '5': 'bottom-right-corner.png', '6': 'bottom-left-corner.png', '7': 'bottom-dead.png', '8': 'top-wall.png',
                           '9': 'top-right-corner.png', 'a': 'top-left-corner.png', 'b': 'top-dead.png', 'c': 'top-bottom-wall.png', 'd': 'right-dead.png',
                           'e': 'left-dead.png', 'f': 'all-walls.png'}

    def _drawMaze(self):

        mazePath = Path('app/static/img/maze/')

        base = mazePath / 'base.png'
        img = Image.open(base)

        img = img.resize((self._maxX*32*2-32, self._maxY*32*2-32))
        # tiles are 32x32

        debug = Image.open(mazePath / 'debug-tile.png')

        mazeHex = ''

        for row in range(1, self._maxY+1):
            for column in range(1, self._maxX+1):
                node = self._adjacencyList.get(row, column)

                adjNodes = []
                # getting the list of adjacent nodes from the dictionary
                if node.top() == 0:
                    adjNodes.append([node.row(), node.column()-1])
                if node.bottom() == 0:
                    adjNodes.append([node.row(), node.column()+1])
                if node.left() == 0:
                    adjNodes.append([node.row()-1, node.column()])
                if node.right() == 0:
                    adjNodes.append([node.row()+1, node.column()])

                # pasting the correct image (correspoding with the walls list) onto the main background image
                tile = mazePath / self._tileNames[node.key()]
                tileImg = Image.open(tile)

                img.paste(tileImg, ((node.row()-1)*64, (node.column()-1)*64))

                for adjNode in adjNodes:
                    # figuring out where to place adjacent corridors based
                    join_x = ((adjNode[0] - node.row())/2) + node.row()
                    join_y = ((adjNode[1] - node.column())/2) + node.column()

                    # pasting corridors joining the nodes

                    if join_y-int(join_y) != 0:
                        tile = mazePath / 'left-right-wall.png'

                    elif join_x-int(join_x) != 0:
                        tile = mazePath / 'top-bottom-wall.png'

                    tileImg = Image.open(tile)
                    img.paste(tileImg, (int((join_x-1)*64), int((join_y-1)*64)))

                mazeHex += node.key()

        img.save(mazePath / "fullmaze.png")

        print(mazeHex)

        return mazeHex

        # recursive backtracking | 19/09/21
    def recursiveBacktracking(self):

        stack = []
        start_time = time.time()
        next_node = [1, 1]

        while True:

            current_node = next_node
            stack.append(current_node)

            try:
                self._nodes.remove(current_node)
            except ValueError:  # raised if current node already not in self._nodes  - this is fine
                pass

            possible_nodes = []

            # finding possible next nodes by comparing each position adjacent to the current node to the unused nodes
            for dx, dy in self._adjacent_nodes:
                if [current_node[0] + dx, current_node[1] + dy] in self._nodes:
                    possible_nodes.append(
                        [current_node[0] + dx, current_node[1] + dy])
            if possible_nodes:
                # choosing a random (adjacent) node to go next
                next_node = random.choice(possible_nodes)
                pair = [next_node, current_node]

                # updating (or adding if not already) nodes to adjacencyList
                for index, node in enumerate(pair):
                    if not self._adjacencyList.get(node[0], node[1]):
                        walls = {'top': True, 'bottom': True,
                                 'left': True, 'right': True}
                    else:
                        nodeObj = self._adjacencyList.get(node[0], node[1])
                        walls = nodeObj.getWalls()

                    # ! finishing changing walls dict to bools

                    # working out which wall to remove
                    adjNode = pair[index-1]
                    xDiff = node[0] - adjNode[0]
                    yDiff = node[1] - adjNode[1]
                    if yDiff > 0:
                        walls['top'] = False
                    elif yDiff < 0:
                        walls['bottom'] = False
                    if xDiff > 0:
                        walls['left'] = False
                    elif xDiff < 0:
                        walls['right'] = False

                    nodeObj = Node(node, walls)
                    self._adjacencyList.insert(nodeObj)

            else:
                # checking each node from the stack for possible nodes, if there are none, removing it
                for index in range(len(stack)-1, -1, -1):
                    check_node = stack[index]
                    for dx, dy in self._adjacent_nodes:
                        if [check_node[0] + dx, check_node[1] + dy] in self._nodes:
                            next_node = check_node
                            break
                    else:
                        try:
                            # using stack to keep track of which nodes to/ not to visit again
                            stack.remove(check_node)
                        except ValueError:
                            pass
                        continue
                    break

            if len(stack) == 0:
                break

        # end_time = time.time()-start_time
        # print((str(end_time)[:-(len(str(end_time).split('.')[1])-2)]) + 's')

        return self._drawMaze()


class Base64Converter(MazeGenerator):
    def __init__(self, base64String):
        # get width and height from start of base 64 num
        maxX = int(base64String[0:2])
        maxY = int(base64String[2:4])
        base64String = base64String[4:]

        # inherit attributes
        super().__init__(maxX, maxY)

        # convert the rest of the base 64 into hex
        self._hexString = b64decode(base64String).hex()

    def mazeFromHex(self):
        # each hex digit corresponds to one of the nodes
        for index, node in enumerate(self._nodes):
            hex = self._hexString[index]
            # converts the hex digit to binary
            wallBin = bin(int(hex, 16))[2:].zfill(4)
            walls = {'top': int(wallBin[0]), 'bottom': int(wallBin[1]),
                     'left': int(wallBin[2]), 'right': int(wallBin[3])}

            nodeObj = Node(node, walls)
            self._adjacencyList.insert(nodeObj)

        return self._drawMaze()
