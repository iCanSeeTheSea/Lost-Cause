# peer checked and improved code | DO NOT USE DIRECTLY

import random

# each "point" in the maze
nodes = [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3)] # ISSUE 1: large maze will end up with huge list - auto generate?

adjacent_nodes = ((-1, 0), (1, 0), (0, -1), (0, 1))

total_nodes = len(nodes)

# hold data on which nodes are visited, and in what order
spanning_tree = []

# node to start on
current_node = (1,1)

# creates the maze until all nodes are visited
while nodes:

    # removes current node from stack
    print(current_node)
    try:
        nodes.remove(current_node)
    except ValueError: # only passes on the expected error
        pass
    
    possible_nodes = []

    # checking nodes with a different in x by 1 and/or a difference in y by 1
    for dx, dy in adjacent_nodes:
        if (current_node[0] + dx, current_node[1] + dy) in nodes:
            possible_nodes.append((current_node[0] + dx, current_node[1] + dy))

    # choosing a random next node 
    if possible_nodes:
        next_node = random.choice(possible_nodes)
        spanning_tree.append((next_node, current_node))
    else:
        print('Jumped branch')
        # when the branch has met a dead end, look for a new branch
        for item in spanning_tree:
            check_node = item[1]
            for dx, dy in adjacent_nodes:
                if (check_node[0] + dx, check_node[1] + dy) in nodes:
                    next_node = check_node

    current_node = next_node

print(spanning_tree)
