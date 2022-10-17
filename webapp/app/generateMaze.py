from dataclasses import dataclass
import random
import time
from PIL import Image
from pathlib import Path


@dataclass
class Node:
    __pos: list

    def __post_init__(self):
        # pre-defining parameters after initialisation to be defined later
        self._top = self._bottom = self._left = self._right = "1"

        self._row = self.__pos[0]
        self._column = self.__pos[1]

    def _wall_value_checker(self, value):
        if value == "1" or value == "0":
            return True
        else:
            raise ValueError("wall value should be either \"1\" or \"0\"")

    def debug(self):
        return [self.__pos, (self._top, self._bottom, self._left, self._right), self.key]

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, value):
        if self._wall_value_checker(value):
            self._top = value

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, value):
        if self._wall_value_checker(value):
            self._bottom = value

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        if self._wall_value_checker(value):
            self._left = value

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        if self._wall_value_checker(value):
            self._right = value

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @property
    def key(self):
        # key for each node is a 4 digit binary string
        return self._top + self._bottom + self._left + self._right


class Maze:
    def __init__(self, max_x, max_y):
        # 2D list to store node objects - index matches coordinate in the maze
        self._max_x = max_x
        self._max_y = max_y
        self._nodeList = [[None for _ in range(max_x)] for _ in range(max_y)]
        self._binary_list = ['' for _ in range(max_y * max_x)]

    def insert(self, node_object):
        row = node_object.row
        column = node_object.column
        # maze starts at 1,1 but list indexing starts at [0][0]
        self._nodeList[row - 1][column - 1] = node_object
        # calculates relative position
        self._binary_list[
            self._max_x * (row - 1) + (
                    column - 1)] = f'{node_object.top}{node_object.bottom}{node_object.left}{node_object.right}'

    def node(self, coord):
        node = self._nodeList[coord[0] - 1][coord[1] - 1]
        return node

    # storing the sequence of node keys as a property that the seed generator can access
    @property
    def binary_string(self):
        return ''.join(self._binary_list)


class MazeGenerator:
    def __init__(self, max_x, max_y):
        self._maze = Maze(max_x, max_y)

        self._nodes = []

        # nodes is a 2D list, [row][column]
        for row in range(1, max_y + 1):
            for column in range(1, max_x + 1):
                self._nodes.append([row, column])
        self._saveNodes = self._nodes.copy()

        # allows easy calculation of the nodes around any given node
        self._adjacentCoords = ((-1, 0), (1, 0), (0, 1), (0, -1))

        self._max_x = max_x
        self._max_y = max_y

        # number corresponds to binary value of the node's key
        self._tileNames = {'0000': 'no-walls.png', '0001': 'right-wall.png', '0010': 'left-wall.png',
                           '0011': 'left-right-wall.png',
                           '0100': 'bottom-wall.png', '0101': 'bottom-right-corner.png',
                           '0110': 'bottom-left-corner.png',
                           '0111': 'bottom-dead.png', '1000': 'top-wall.png',
                           '1001': 'top-right-corner.png', '1010': 'top-left-corner.png', '1011': 'top-dead.png',
                           '1100': 'top-bottom-wall.png', '1101': 'right-dead.png',
                           '1110': 'left-dead.png', '1111': 'all-walls.png'}

    def draw_maze(self, binary_string):

        maze_path = Path('app/static/img/maze/')

        base = maze_path / 'base.png'
        img = Image.open(base)

        # tiles are 32x32
        img = img.resize((self._max_x * 32 * 2 - 32, self._max_y * 32 * 2 - 32))

        # debug = Image.open(maze_path / 'debug-tile.png')

        for row in range(1, self._max_y + 1):
            for column in range(1, self._max_x + 1):
                if binary_string:
                    # uses the binary_string if generating from a seed
                    wall_string = binary_string[:4]
                    binary_string = binary_string[4:]
                    node = Node([row, column])
                    node.top = wall_string[0]
                    node.bottom = wall_string[1]
                    node.left = wall_string[2]
                    node.right = wall_string[3]
                    self._maze.insert(node)
                else:
                    node = self._maze.node([row, column])

                adjacent_nodes = []
                # getting the list of adjacent nodes from the dictionary
                if node.top == "0":
                    adjacent_nodes.append([row - 1, column])
                if node.bottom == "0":
                    adjacent_nodes.append([row + 1, column])
                if node.left == "0":
                    adjacent_nodes.append([row, column - 1])
                if node.right == "0":
                    adjacent_nodes.append([row, column + 1])

                # pasting the correct image (corresponding with the walls list) onto the main background image
                tile = maze_path / self._tileNames[node.key]
                tile_image = Image.open(tile)

                img.paste(tile_image, ((column - 1) * 64, (row - 1) * 64))

                for adjacent_node in adjacent_nodes:
                    # figuring out where to place adjacent corridors based
                    join_y = ((adjacent_node[0] - node.row) / 2) + node.row
                    join_x = ((adjacent_node[1] - node.column) / 2) + node.column

                    # pasting corridors joining the nodes

                    if join_y - int(join_y) != 0:
                        tile = maze_path / 'left-right-wall.png'  # vertical corridor

                    elif join_x - int(join_x) != 0:
                        tile = maze_path / 'top-bottom-wall.png'  # horizontal corridor

                    tile_image = Image.open(tile)
                    img.paste(tile_image, (int((join_x - 1) * 64), int((join_y - 1) * 64)))

        print(self._maze.binary_string)
        return img

    # recursive backtracking | 19/09/21

    def recursive_backtracking(self):

        stack = []
        start_time = time.time()
        next_position = [1, 1]

        while True:

            current_position = next_position
            stack.append(current_position)

            try:
                self._nodes.remove(current_position)
            except ValueError:
                # value error is raised if the current position has already been removed
                # occurs after maze reaches a dead end and backtracks
                pass

            possible_coordinates = []

            # finding possible next nodes by comparing each position adjacent to the current node to the unused nodes
            for dy, dx in self._adjacentCoords:
                if [current_position[0] + dy, current_position[1] + dx] in self._nodes:
                    possible_coordinates.append(
                        [current_position[0] + dy, current_position[1] + dx])
            if possible_coordinates:
                # choosing a random (adjacent) node to go next
                next_position = random.choice(possible_coordinates)
                pair = [next_position, current_position]

                # updating (or adding if not already) nodes in maze
                for index, coord in enumerate(pair):
                    if not self._maze.node(coord):
                        node = Node(coord)
                    else:
                        node = self._maze.node(coord)

                    # working out which wall to remove
                    adjacent_node = pair[index - 1]
                    y_difference = coord[0] - adjacent_node[0]
                    x_difference = coord[1] - adjacent_node[1]
                    if y_difference > 0:
                        node.top = '0'
                    elif y_difference < 0:
                        node.bottom = '0'
                    if x_difference > 0:
                        node.left = '0'
                    elif x_difference < 0:
                        node.right = '0'

                    self._maze.insert(node)

            else:
                # checking each node from the stack for possible nodes, if there are none, removing it
                for index in range(len(stack) - 1, -1, -1):
                    check_position = stack[index]
                    for dy, dx in self._adjacentCoords:
                        if [check_position[0] + dy, check_position[1] + dx] in self._nodes:
                            next_position = check_position
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

        return self._maze


class SeedGenerator:
    def __init__(self):
        self._mazeGenerator = None
        self._seed = None
        self._maze = None
        self._height = None
        self._width = None

        # base 64 conversion tables
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
                      '000111': 'H', '001000': 'I', '001001': 'J', '001010': 'K', '001011': 'L', '001100': 'M',
                      '001101': 'N',
                      '001110': 'O', '001111': 'P', '010000': 'Q', '010001': 'R', '010010': 'S', '010011': 'T',
                      '010100': 'U',
                      '010101': 'V', '010110': 'W', '010111': 'X', '011000': 'Y', '011001': 'Z', '011010': 'a',
                      '011011': 'b',
                      '011100': 'c', '011101': 'd', '011110': 'e', '011111': 'f', '100000': 'g', '100001': 'h',
                      '100010': 'i',
                      '100011': 'j', '100100': 'k', '100101': 'l', '100110': 'm', '100111': 'n', '101000': 'o',
                      '101001': 'p',
                      '101010': 'q', '101011': 'r', '101100': 's', '101101': 't', '101110': 'u', '101111': 'v',
                      '110000': 'w',
                      '110001': 'x', '110010': 'y', '110011': 'z', '110100': '0', '110101': '1', '110110': '2',
                      '110111': '3',
                      '111000': '4', '111001': '5', '111010': '6', '111011': '7', '111100': '8', '111101': '9',
                      '111110': '-',
                      '111111': '_'}

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, seed):
        self._seed = seed

    @property
    def height(self):
        return self.height

    @height.setter
    def height(self, height):
        if len(str(height)) < 2:
            self._height = int('0' + str(height))
        else:
            self._height = height

    @property
    def width(self):
        return self.width

    @width.setter
    def width(self, width):
        if len(str(width)) < 2:
            self._width = int('0' + str(width))
        else:
            self._width = width

    def create_base_64_seed(self):
        self._mazeGenerator = MazeGenerator(self._height, self._width)

        self._maze = self._mazeGenerator.recursive_backtracking()
        image = self._mazeGenerator.draw_maze('')

        # turns the width and height of the maze into two bytes
        size_binary = str(bin(self._height))[2:].zfill(8) + str(bin(self._width))[2:].zfill(8)
        binary_string = size_binary + self._maze.binary_string

        padding = 0
        # one '=' is added for every byte of padding
        while len(binary_string) % 24 != 0:
            binary_string += '0'
            padding += 1
        padding //= 8

        # splits binary_string every 6 characters for easier conversion to base 64
        binary_list = [binary_string[i:i + 6] for i in range(0, len(binary_string), 6)]

        base_64_string = ''
        for value in binary_list:
            base_64_string += self._to64[value]
        base_64_string += '=' * padding

        print(base_64_string)
        self._seed = base_64_string
        return image

    def draw_maze_from_seed(self):
        # removing padding before conversion
        base_64_string = self._seed.rstrip('=')
        binary_string = ''

        for value in base_64_string:
            binary_string += self._toBinary[value]

        # splitting converted string into height, width, and binary_string
        padding = self._seed.count('=')
        self._height = int(binary_string[:8], 2)
        self._width = int(binary_string[8:16], 2)
        binary_string = binary_string[16:-padding * 8]

        if self._mazeGenerator is None:
            self._mazeGenerator = MazeGenerator(self._height, self._width)
        return self._mazeGenerator.draw_maze(binary_string)
