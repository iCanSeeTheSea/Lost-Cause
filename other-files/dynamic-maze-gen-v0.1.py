# proof of concept 1: 3x3 grid, no visualisation | 21.08.21 -> 16/09/21

# drunkards walk algorithm

from random import randint

# each "point" in the maze
nodes = [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3)] # ISSUE 1: large maze will end up with huge list - auto generate?

adjacent_nodes = ((-1, 0), (1,0), (0,1), (0, -1))

# using tuples to avoid accidental overwrites

total_nodes = len(nodes)

# hold data on which nodes are visited, and in what order
spanning_tree = []

# node to start on
current_node = (1,1)

# creates the maze until all nodes are visited
while len(nodes) > 0:

    # removes current node from stack
    print(current_node)
    try:
        nodes.remove(current_node)
    except ValueError:
        pass

    possible_nodes = []

    # finding possible next nodes by comparing each position adjacent to the current node to the unused nodes
    for x, y in adjacent_nodes:
        if (current_node[0] + x, current_node[1] + y) in nodes:
            possible_nodes.append((current_node[0] + x, current_node[1] + y))

    if len(possible_nodes) > 0:
        # choosing a random (adjacent) node to go next
        next_node = possible_nodes[randint(0, len(possible_nodes)-1)]
        spanning_tree.append((next_node, current_node))
    else:
        print('new branch')
        # when branch meets a dead end, look through the spanning tree to find an available node
        for item in spanning_tree:
            check_node = item[1]
            for x, y in adjacent_nodes:
                if (check_node[0] +x, check_node[1] + y) in nodes:
                    next_node = check_node
    
    current_node = next_node

print(spanning_tree)