# recursive backtracking | 19/09/21

import random
import time
import math


def mazeGen(side):
    dead_ends = 1
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
            dead_ends += 1
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
            # end_time = time.perf_counter()-start_time
            # print(
            #     (str(end_time)[:-(len(str(end_time).split('.')[1])-2)]) + 's')
            # print(spanning_tree)
            if str(dead_ends) in dead_end_dict:
                dead_end_dict[str(dead_ends)] += 1
            else:
                dead_end_dict[str(dead_ends)] = 1
            break


tests = 100000
for i in range(25, 26):
    print(i)
    dead_end_dict = {}
    mean = 0
    deviation = 0

    start_time = time.perf_counter()
    for n in range(tests):
        mazeGen(i)
    print(f"{i}: ")
    for k in range(1, len(dead_end_dict)**2):
        if str(k) in dead_end_dict:
            freq = dead_end_dict[str(k)]
            mean += k*freq
            deviation += freq*(k**2)
            # print(f"  {k}:  {dead_end_dict[str(k)]}")
    mean /= tests
    deviation = math.sqrt((deviation/tests) - mean**2)
    percent = (mean/i**2) * 100
    end_time = time.perf_counter()-start_time
    print(
        (str(end_time)[:-(len(str(end_time).split('.')[1])-2)]) + 's')
    print(
        f"mean - {mean}, standard deviation - {deviation}, percent - {percent}")
