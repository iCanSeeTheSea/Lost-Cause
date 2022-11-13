from dataclasses import dataclass
import random
import time
from PIL import Image
from pathlib import Path


@dataclass
class Node:
    __pos: list

    def __post_init__(self):
        """
        The function takes the position of the cell and assigns it to the row and column variables
        """
        self._top = self._bottom = self._left = self._right = "1"

        self._row = self.__pos[0]
        self._column = self.__pos[1]

    def _wall_value_checker(self, value):
        """
        It checks if the value of a wall is either "1" or "0"

        :param value: the value of the cell
        :return: a boolean value.
        """
        if value == "1" or value == "0":
            return True
        else:
            raise ValueError("wall value should be either \"1\" or \"0\"")

    def debug(self):
        """
        It returns a list of the position of the node, the node's walls, and the object's key
        :return: The position of the node, the boundaries of the node, and the key of the node.
        """
        return [self.__pos, (self._top, self._bottom, self._left, self._right), self.key]

    def setWallsFromKey(self, key):
        self.top = key[0]
        self.bottom = key[1]
        self.left = key[2]
        self.right = key[3]

    @property
    def top(self):
        """
        getter for property "top"
        :return: the value of the top wall
        """
        return self._top

    @top.setter
    def top(self, value):
        """
        This function checks if the value is a valid wall value, and if it is, it sets the top wall to that value

        :param value: The value of the wall
        """
        if self._wall_value_checker(value):
            self._top = value

    @property
    def bottom(self):
        """
        getter for property "bottom"
        :return: The value for the bottom wall
        """
        return self._bottom

    @bottom.setter
    def bottom(self, value):
        """
        It checks if the value is a valid wall value and if it is, it sets the bottom wall to that value.

        :param value: The value of the wall
        """
        if self._wall_value_checker(value):
            self._bottom = value

    @property
    def left(self):
        """
        getter for property "left"
        :return: The value for the left wall
        """
        return self._left

    @left.setter
    def left(self, value):
        """
        This function takes in a value and checks if it is a valid wall value. If it is, it sets the left wall value to the
        value

        :param value: The value of the wall
        """
        if self._wall_value_checker(value):
            self._left = value

    @property
    def right(self):
        """
        getter for property "right"
        :return: The value for the right wall
        """
        return self._right

    @right.setter
    def right(self, value):
        """
        This function checks if the value is a valid wall value, and if it is, it sets the right wall to that value

        :param value: The value of the wall
        """
        if self._wall_value_checker(value):
            self._right = value

    @property
    def row(self):
        """
        getter for property "row"
        :return: The row the node is in
        """
        return self._row

    @property
    def column(self):
        """
        getter for property "column"
        :return: The column the node is in
        """
        return self._column

    @property
    def key(self):
        """
        The key for each node is a 4 digit binary string, where the first two digits are the top and bottom edges, and the
        last two digits are the left and right edges.
        :return: A 4 digit binary string.
        """
        return self._top + self._bottom + self._left + self._right


class Maze:
    def __init__(self, max_y, max_x):
        """
        It creates a 2D list of node objects, where the index of the list matches the coordinate in the maze

        :param max_y: The height of the maze
        :param max_x: The width of the maze
        """
        self._max_x = max_x
        self._max_y = max_y
        self._node_list = [[None for _ in range(max_x)] for _ in range(max_y)]
        self._binary_list = ['' for _ in range(max_y * max_x)]

    def insert(self, node_object):
        """
        The function takes a node object and inserts it into the node list and binary list

        :param node_object: the node object to be inserted into the maze
        """
        row = node_object.row
        column = node_object.column
        # maze starts at 1,1 but list indexing starts at [0][0]
        self._node_list[row - 1][column - 1] = node_object
        # calculates relative position
        self._binary_list[(self._max_x * (row - 1)) + (column - 1)] = f'{node_object.top}{node_object.bottom}{node_object.left}{node_object.right}'

    def node(self, coord):
        """
        It returns the node at the given coordinate

        :param coord: The coordinate of the node you want to get
        :return: The node at the given coordinates.
        """
        node = self._node_list[coord[0] - 1][coord[1] - 1]
        return node

    @property
    def binary_string(self):
        """
        It takes a list of strings, and joins them together into one string
        :return: The binary string is being returned.
        """
        return ''.join(self._binary_list)


class MazeGenerator:
    def __init__(self, max_y, max_x):
        """
        The function takes in the dimensions of the maze and creates a 2D list of Nodes

        :param max_y: the number of rows in the maze
        :param max_x: the number of columns in the maze
        """
        self._maze = Maze(max_y, max_x)

        self._nodes = []

        # nodes is a 2D list, [row][column]
        for row in range(1, max_y + 1):
            for column in range(1, max_x + 1):
                self._nodes.append([row, column])

        # allows easy calculation of the nodes around any given node
        self._adjacent_coords = ((-1, 0), (1, 0), (0, 1), (0, -1))

        self._max_x = max_x
        self._max_y = max_y

        # number corresponds to binary value of the node's key
        self._tile_names = {'0000': 'no-walls.png', '0001': 'right-wall.png', '0010': 'left-wall.png',
                            '0011': 'left-right-wall.png',
                            '0100': 'bottom-wall.png', '0101': 'bottom-right-corner.png',
                            '0110': 'bottom-left-corner.png',
                            '0111': 'bottom-dead.png', '1000': 'top-wall.png',
                            '1001': 'top-right-corner.png', '1010': 'top-left-corner.png', '1011': 'top-dead.png',
                            '1100': 'top-bottom-wall.png', '1101': 'right-dead.png',
                            '1110': 'left-dead.png', '1111': 'all-walls.png'}

    def draw_maze(self, binary_string):
        """
        It takes a binary string, and uses it to generate a maze image

        :param binary_string: the binary string of the maze
        :return: The image of the maze.
        """

        maze_path = Path('app/static/img/maze/')

        base = maze_path / 'base.png'
        img = Image.open(base)

        # tiles are 32x32
        img = img.resize((self._max_x * 64 - 32, self._max_y * 64 - 25))

        # debug = Image.open(maze_path / 'debug-tile.png')

        for row in range(0, self._max_y):
            for column in range(0, self._max_x):

                key = binary_string[:4]
                binary_string = binary_string[4:]

                # pasting the correct image (corresponding with the walls list) onto the main background image
                tile = maze_path / self._tile_names[key]
                tile_image = Image.open(tile)
                img.paste(tile_image, (column * 64, row * 64))

                if key[1] == "0":
                    tile = maze_path / 'left-right-wall.png'  # vertical corridor
                    tile_image = Image.open(tile)
                    img.paste(tile_image, (column * 64, (row * 64) + 32))

                if key[3] == "0":
                    tile = maze_path / 'top-bottom-wall.png'  # horizontal corridor
                    tile_image = Image.open(tile)
                    img.paste(tile_image, ((column * 64) + 32, row * 64))

        return img

    def recursive_backtracking(self):
        """
        The function starts at a random node, and then checks all adjacent nodes to see if they have been visited. If they
        have not, it chooses one at random and removes the wall between the two nodes. If they have been visited, it
        backtracks to the last node that had an unvisited adjacent node
        :return: A maze object
        """

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
            for dy, dx in self._adjacent_coords:
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
                    elif x_difference > 0:
                        node.left = '0'
                    elif x_difference < 0:
                        node.right = '0'

                    self._maze.insert(node)

            else:
                # checking each node from the stack for possible nodes, if there are none, removing it
                for index in range(len(stack) - 1, -1, -1):
                    check_position = stack[index]
                    for dy, dx in self._adjacent_coords:
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
        """
        Defines variables to be used by SeedGenerator
        """
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
        """
        getter for seed of the maze.
        :return: The seed is being returned.
        """
        return self._seed

    @seed.setter
    def seed(self, seed):
        """
        The function takes in a seed and sets the seed for the maze

        :param seed: The seed for the maze
        """
        self._seed = seed

    @property
    def height(self):
        """
        getter for height of the maze.
        :return: The height of the maze
        """
        return self.height

    @height.setter
    def height(self, height):
        """
        If the height is less than 10, add a 0 to the front of the height

        :param height: The height of the maze
        """
        if len(str(height)) < 2:
            self._height = int('0' + str(height))
        else:
            self._height = height

    @property
    def width(self):
        """
        getter for the width of the maze.
        :return: The width of the maze
        """
        return self.width

    @width.setter
    def width(self, width):
        """
        If the width less than 10, add a 0 to the front of the width

        :param width: The width of the maze
        """
        if len(str(width)) < 2:
            self._width = int('0' + str(width))
        else:
            self._width = width

    def create_base_64_seed(self):
        """
        It takes the maze's width and height, turns them into two bytes, adds them to the maze's binary string, pads the
        binary string with zeros until it's a multiple of 24, splits the binary string into 6 character chunks, and then
        converts each chunk into a base 64 character
        :return: The image of the maze is being returned.
        """
        self._mazeGenerator = MazeGenerator(self._height, self._width)

        self._maze = self._mazeGenerator.recursive_backtracking()
        image = self._mazeGenerator.draw_maze(self._maze.binary_string)

        # turns the width and height of the maze into two bytes
        size_binary = str(bin(self._height))[2:].zfill(8) + str(bin(self._width))[2:].zfill(8)
        binary_string = size_binary + self._maze.binary_string

        padding = 0
        # one '=' is added for every byte of padding
        while len(binary_string) % 24 != 0:
            binary_string += '0'
            padding += 1
        padding //= 4

        # splits binary_string every 6 characters for easier conversion to base 64
        binary_list = [binary_string[i:i + 6] for i in range(0, len(binary_string), 6)]

        base_64_string = ''
        for value in binary_list:
            base_64_string += self._to64[value]
        base_64_string += '=' * padding

        self._seed = base_64_string
        return image

    def draw_maze_from_seed(self):
        """
        It takes a base64 encoded string, converts it to binary, and then uses the binary string to draw a maze

        :return: The image for the maze is being returned.
        """
        # removing padding before conversion
        base_64_string = self._seed.rstrip('=')
        binary_string = ''

        for value in base_64_string:
            binary_string += self._toBinary[value]

        # splitting converted string into height, width, and binary_string
        padding = self._seed.count('=')
        self._height = int(binary_string[:8], 2)
        self._width = int(binary_string[8:16], 2)
        if padding:
            binary_string = binary_string[16:-padding * 8]
        else:
            binary_string = binary_string[16:]

        self._mazeGenerator = MazeGenerator(self._height, self._width)

        image = self._mazeGenerator.draw_maze(binary_string)

        return image
