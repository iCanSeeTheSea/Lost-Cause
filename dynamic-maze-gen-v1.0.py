# comparing different algorithms

import random, time, pygame
pygame.init()



# generating nodes based on chosen size
maxX = int(input('max value for X: '))
maxY = int(input('max value for Y: '))



def original_algorithm():
    global maxX, maxY

    # each "point" in the maze
    nodes = []

    for x in range(1,maxX+1):
        for y in range(1,maxY+1):
            nodes.append((x, y))

    adjacent_nodes = ((-1, 0), (1,0), (0,1), (0, -1))

    # using tuples to avoid accidental overwrites


    # hold data on which nodes are visited, and in what order
    spanning_tree = []

    # node to start on
    current_node = (1,1)

    start_time = time.time()

    # creates the maze until all nodes are visited
    while nodes:

        # removes current node from stack
        # print(current_node)
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
            # when branch meets a dead end, backtrack through the spanning tree to find an available node
            for index in range(len(spanning_tree) -1, -1, -1): # (going from the end of spanning tree backwards)
                item = spanning_tree[index]
                check_node = item[1]
                for dx, dy in adjacent_nodes:
                    if (check_node[0] + dx, check_node[1] + dy) in nodes:
                        next_node = check_node; break
                else:
                    continue
                break
        
        current_node = next_node

    # calculating time taken to run 
    end_time = time.time()-start_time
    print((str(end_time)[:-(len(str(end_time).split('.')[1])-2)]) + 's')

    return spanning_tree


def recursive_backtacking():
    global maxX, maxY

    nodes = []

    for x in range(1,maxX+1):
        for y in range(1,maxY+1):
            nodes.append((x, y))

    adjacent_nodes = ((-1, 0), (1,0), (0,1), (0, -1))

    stack = []
    spanning_tree = []

    start_time = time.time()

    next_node = (1,1)

    while True:

        current_node = next_node
        stack.append(current_node)

        #print(current_node)
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
            for index in range(len(stack)-1, -1, -1):
                check_node = stack[index]
                for dx, dy in adjacent_nodes:
                    if (check_node[0] + dx, check_node[1] + dy) in nodes:
                        next_node = check_node; break
                else:
                    try:
                        stack.remove(check_node) # using stack to keep track of which nodes to/ not to visit again
                    except ValueError:
                        pass
                    continue
                break
        
        if len(stack) == 0:
            end_time = time.time()-start_time
            print((str(end_time)[:-(len(str(end_time).split('.')[1])-2)]) + 's')
            return spanning_tree

spanning_tree = recursive_backtacking()
    
screen = pygame.display.set_mode([(maxX*20)-10,(maxY*20)-10])

screen.fill((0,0,0))
pygame.draw.rect(screen, (255,255,255), pygame.Rect(0, 0, 10, 10))

for coord_set in spanning_tree:
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((coord_set[0][0]-1)*20, (coord_set[0][1]-1)*20, 10, 10))
    # finding mid-points between current and previous nodes to remove wall
    join_x = ((coord_set[1][0] - coord_set[0][0])/2) + coord_set[0][0] 
    join_y = ((coord_set[1][1] - coord_set[0][1])/2) + coord_set[0][1]
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((join_x-1)*20, (join_y-1)*20, 10, 10))
    

# pygame stuff
running = True
while running:

    for  event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()