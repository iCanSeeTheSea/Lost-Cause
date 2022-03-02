# recursive backtracking | 19/09/21

import random
import time

# generating nodes based on chosen size
# maxX = 20
# maxY = 20


def recursiveBacktracking(maxX, maxY):

    nodes = []

    for x in range(1, maxX+1):
        for y in range(1, maxY+1):
            nodes.append([x, y])
    save_nodes = nodes.copy()

    adjacent_nodes = ((-1, 0), (1, 0), (0, 1), (0, -1))

    stack = []
    spanning_tree = []
    start_time = time.time()
    next_node = [1, 1]

    while True:

        current_node = next_node
        stack.append(current_node)

        try:
            nodes.remove(current_node)
        except ValueError:
            pass

        possible_nodes = []

        # finding possible next nodes by comparing each position adjacent to the current node to the unused nodes
        for dx, dy in adjacent_nodes:
            if [current_node[0] + dx, current_node[1] + dy] in nodes:
                possible_nodes.append(
                    [current_node[0] + dx, current_node[1] + dy])
        if possible_nodes:
            # choosing a random (adjacent) node to go next
            next_node = random.choice(possible_nodes)
            spanning_tree.append([next_node, current_node])
        else:
            # checking each node from the stack for possible nodes, if there are none, removing it
            for index in range(len(stack)-1, -1, -1):
                check_node = stack[index]
                for dx, dy in adjacent_nodes:
                    if [check_node[0] + dx, check_node[1] + dy] in nodes:
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

    return adjacencyListGen(spanning_tree, save_nodes)

def primms(maxX, maxY):
    
    nodes = []

    for x in range(1, maxX+1):
        for y in range(1, maxY+1):
            nodes.append([x, y])
    save_nodes = nodes.copy()


    adjacent_nodes = ((-1, 0), (1, 0), (0, 1), (0, -1))

    frontiers = []
    prev_nodes = []

    spanning_tree = []

    #start_time = time.perf_counter()

    next_node = [1, 1]
    
    while True:

        
        current_node = next_node
        
        # print(current_node)
        try:
            nodes.remove(current_node)
        except ValueError:
            pass

        # finding possible next nodes by comparing each position adjacent to the current node to the unused nodes
        for dx, dy in adjacent_nodes:
            proposedNode = [current_node[0] + dx, current_node[1] + dy]
            if proposedNode in nodes and proposedNode not in frontiers:
                frontiers.append(proposedNode)
                prev_nodes.append(current_node)
        
        if frontiers:
            # choosing a random (adjacent) node to go next

            index = random.randint(0,len(frontiers)-1)
            next_node = frontiers.pop(index)
            prev_node = prev_nodes.pop(index)
            
            spanning_tree.append((next_node, prev_node))

        else:
            #end_time = time.perf_counter()-start_time
            #print((str(end_time)[:-(len(str(end_time).split('.')[1])-2)]) + 's')

            break

    return adjacencyListGen(spanning_tree, save_nodes)


# TODO comments in here!
# TODO use an object for the tree and possibly send it as a json file

    
def adjacencyListGen(spanning_tree, nodes):
    adjacencyDict = {}
    for node in nodes:
        walls = [1, 1, 1, 1]
        for pair in spanning_tree:
            if pair[1] == node:
                adjNode = pair[0]
            elif pair[0] == node:
                adjNode = pair[1]
            else:
                continue
            # top, bottom, left, right
            # wall = 1
            xDiff = node[0] - adjNode[0]
            yDiff = node[1] - adjNode[1]
            if yDiff > 0:
                walls[0] = 0
            elif yDiff < 0:
                walls[1] = 0
            if xDiff > 0:
                walls[2] = 0
            elif xDiff < 0:
                walls[3] = 0
        adjacencyDict[str(node)] = walls
    return adjacencyDict
