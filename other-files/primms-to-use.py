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

    return adjacencyListGen(spanning_tree, save_nodes, maxX, maxY)