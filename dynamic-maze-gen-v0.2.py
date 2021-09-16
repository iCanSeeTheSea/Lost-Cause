# proof of concept 2: expandable grid, preliminary visualisation | 16/09/21

# closer to a recursive backtracker

import random, time

start_time = time.time()

# each "point" in the maze
nodes = []

# generating nodes based on chosen size
maxX = int(input('max value for X: '))
maxY = int(input('max value for Y: '))

for x in range(1,maxX+1):
    for y in range(1,maxY+1):
        nodes.append((x, y))

adjacent_nodes = ((-1, 0), (1,0), (0,1), (0, -1))

# using tuples to avoid accidental overwrites

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
    except ValueError:
        pass

    possible_nodes = []

    # finding possible next nodes by comparing each position adjacent to the current node to the unused nodes
    for dx, dy in adjacent_nodes:
        if (current_node[0] + dx, current_node[1] + dy) in nodes:
            possible_nodes.append((current_node[0] + dx, current_node[1] + dy))

    if possible_nodes:
        # choosing a random (adjacent) node to go next
        next_node = random.choice(possible_nodes)
        spanning_tree.append((next_node, current_node))
    else:
        print('new branch')
        # when branch meets a dead end, backtrack through the spanning tree to find an available node
        for index in range(len(spanning_tree) -1, -1, -1): # (going from the end of spanning tree backwards)
            item = spanning_tree[index]
            check_node = item[1]
            for x, y in adjacent_nodes:
                if (check_node[0] +x, check_node[1] + y) in nodes:
                    next_node = check_node
    
    current_node = next_node

print(spanning_tree)

if maxX*maxY == len(spanning_tree)+1:
    print('YAY')
else:
    print('a sad feeling :(')

end_time = time.time()-start_time
print((str(end_time)[:-(len(str(end_time).split('.')[1])-2)]) + 's')