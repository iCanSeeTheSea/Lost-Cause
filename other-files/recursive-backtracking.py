# recursive backtracking | 19/09/21

import random
import time



def mazeGen(side):
    nodes = []

    for x in range(1, side+1):
        for y in range(1, side+1):
            nodes.append((x, y))

    adjacent_nodes = ((-1, 0), (1, 0), (0, 1), (0, -1))

    stack = []
    spanning_tree = []

    start_time = time.perf_counter()

    next_node = (1, 1)

    while True:

        current_node = next_node
        stack.append(current_node)

        # print(current_node)
        try:
            nodes.remove(current_node)
        except ValueError:
            pass

        possible_nodes = []

        # finding possible next nodes by comparing each position adjacent to the current node to the unused nodes
        for dx, dy in adjacent_nodes:
            if (current_node[0] + dx, current_node[1] + dy) in nodes:
                possible_nodes.append(
                    (current_node[0] + dx, current_node[1] + dy))

        if possible_nodes:
            # choosing a random (adjacent) node to go next
        
            next_node = random.choice(possible_nodes)
            spanning_tree.append((next_node, current_node))


        else:
            # checking each node from the stack for possible nodes, if there are none, removing it
            for index in range(len(stack)-1, -1, -1):
                check_node = stack[index]
                for dx, dy in adjacent_nodes:
                    if (check_node[0] + dx, check_node[1] + dy) in nodes:
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
            end_time = time.perf_counter()-start_time
            print(
                (str(end_time)[:-(len(str(end_time).split('.')[1])-2)]) + 's')
            break

mazeGen(100)
