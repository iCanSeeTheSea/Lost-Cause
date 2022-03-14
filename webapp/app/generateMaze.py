
import random
import time
from PIL import Image
from pathlib import Path


class Node:
    def __init__(self, node, walls):
        self._id = node
        self._top = walls['top']
        self._bottom = walls['bottom']
        self._left = walls['left']
        self._right = walls['right']
        self._key = str(hex(int(str(self._top) + str(self._bottom) +
                        str(self._left) + str(self._right), 2)))[2:]

    def __getattribute__(self, name):
        return super().__getattribute__(name)

    def getWalls(self):
        walls = {'top': self._top, 'bottom': self._bottom,
                 'left': self._left, 'right': self._right}
        return walls


class AdjacencyList:
    def __init__(self, maxX, maxY):
        # creating empty list the correct size for the maze
        self._list = [[None for _ in range(maxX)] for _ in range(maxY)]

    def insert(self, node):
        row = node._id[0]
        column = node._id[1]
        # maze starts at 1,1 but list indexing starts at [0][0]
        self._list[row-1][column-1] = node

    def get(self, row, column):
        node = self._list[row-1][column-1]
        return node

    def __getattribute__(self, name):
        return super().__getattribute__(name)


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
                           'e': 'left-dead.png', 'f': ''}

    def __getattribute__(self, name):
        return super().__getattribute__(name)

    def drawMaze(self):

        mazePath = Path('app/static/img/maze/')

        base = mazePath / 'base.png'
        img = Image.open(base)

        img = img.resize((self._maxX*32*2-32, self._maxY*32*2-32))
        # tiles are 32x32

        mazeHex = ''

        for row in range(1, self._maxY+1):
            for column in range(1, self._maxX+1):
                node = self._adjacencyList.get(row, column)

                # getting the list of adjacent nodes from the dictionary
                adjNodes = []

                if node._top == 0:
                    adjNodes.append([node._id[0], node._id[1]-1])
                if node._bottom == 0:
                    adjNodes.append([node._id[0], node._id[1]+1])
                if node._left == 0:
                    adjNodes.append([node._id[0]-1, node._id[1]])
                if node._right == 0:
                    adjNodes.append([node._id[0]+1, node._id[1]])

                # pasting the correct image (correspoding with the walls list) onto the main background image
                tile = mazePath / self._tileNames[node._key]
                tileImg = Image.open(tile)
                img.paste(tileImg, ((node._id[0]-1)*64, (node._id[1]-1)*64))

                for adjNode in adjNodes:
                    # figuring out where to place adjacent corridors based
                    join_x = ((adjNode[0] - node._id[0])/2) + node._id[0]
                    join_y = ((adjNode[1] - node._id[1])/2) + node._id[1]

                    # pasting corridors joinging the nodes, and saving their data to the dictionary

                    if join_y-int(join_y) != 0:
                        tile = mazePath / 'left-right-wall.png'

                    elif join_x-int(join_x) != 0:
                        tile = mazePath / 'top-bottom-wall.png'

                    tileImg = Image.open(tile)
                    img.paste(tileImg, (int((join_x-1)*64), int((join_y-1)*64)))

                # saving hex keys to a string
                mazeHex += node._key

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
            except ValueError:
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

                # updating (or adding) nodes to adjacencyList
                '''
                when a pair would be added to the spanning tree -> 
                for both nodes:
                    - check their index in adjacency list
                    - if its not there:
                            make it
                    - update which wall is removed
                        
                '''
                for index, node in enumerate(pair):
                    if not self._adjacencyList.get(node[0], node[1]):
                        walls = {'top': 1, 'bottom': 1, 'left': 1, 'right': 1}
                    else:
                        nodeObj = self._adjacencyList.get(node[0], node[1])
                        walls = nodeObj.getWalls()

                    # working out which wall to remove
                    adjNode = pair[index-1]
                    xDiff = node[0] - adjNode[0]
                    yDiff = node[1] - adjNode[1]
                    if yDiff > 0:
                        walls['top'] = 0
                    elif yDiff < 0:
                        walls['bottom'] = 0
                    if xDiff > 0:
                        walls['left'] = 0
                    elif xDiff < 0:
                        walls['right'] = 0

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

        return self.drawMaze()


class base64Converter(MazeGenerator):
    def __init__(self, maxX, maxY, base64String):
        super().__init__(maxX, maxY)
        self._base64String = base64String
