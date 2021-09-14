# proof of concept 1: 3x3 grid, no visualisation | 21.08.21

from random import randint

# each "point" in the maze
nodes = [[1,1],[1,2],[1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3]] # ISSUE 1: large maze will end up with huge list - auto generate?

total_nodes = len(nodes)

# hold data on which nodes are visited, and in what order
spanning_tree = []

# node to start on
current_node = [1,1]



# creates the maze until all nodes are visited
while len(spanning_tree) < total_nodes:

    # removes current node from stack
    nodes.remove(current_node)

    print('nodes:', nodes)
    
    possible_nodes = []

    for node in nodes:
        # try-except to account for index error when searching for nodes outside maze
        try:
            # finding nodes next to current_node, 1 space above or below, or 1 space either side
            if (node[0]+1 == current_node[0] or node[0]-1 == current_node[0]) and node[1] == current_node[1]:
                possible_nodes.append(node)
            elif (node[1]+1 == current_node[1] or node[1]-1 == current_node[1]) and node[0] == current_node[0]:
                possible_nodes.append(node)
            else:
                pass
        except:
            pass


    # randomly choosing the next node, unless there is only 1 option
    if len(possible_nodes) > 1:
        next_node = possible_nodes[randint(0, len(possible_nodes))-1]
    elif len(possible_nodes) == 1:
        next_node = possible_nodes[0]
    elif possible_nodes == []:
        # when the branch has met a dead end, look for a new branch
        for item in spanning_tree:
            check_node = item[1]
            for node in nodes:
                try:
                    '''
                    if (node[0]+1 == check_node[0] or node[0]-1 == check_node[0]) and node[1] == check_node[1]:
                        next_node = check_node; print(check_node, next_node, node); break
                    elif (node[1]+1 == check_node[1] or node[1]-1 == check_node[1]) and node[0] == check_node[0]:
                        next_node = check_node; print(check_node, next_node, node); break
                    '''
                    if node[0]+1 == check_node[0] and node[1] == check_node[1]:
                        check_node[0] -= 1
                        next_node = check_node
                    elif node[0]-1 == check_node[0] and node[1] == check_node[1]:
                        check_node[0] += 1
                        next_node = check_node
                    elif node[1]+1 == check_node[1] and node[0] == check_node[0]:
                        check_node[1] -= 1
                        next_node = check_node
                    elif node[1]-1 == check_node[1] and node[0] == check_node[0]:
                        check_node[1] += 1
                        next_node = check_node
                except:
                    print('ERROR')

                
            
    print('current:', current_node)
    print('possible:', possible_nodes)
    print('next:', next_node)
    spanning_tree.append([next_node, current_node])
    print('tree:', spanning_tree, '\n')

    current_node = next_node

print(spanning_tree)
