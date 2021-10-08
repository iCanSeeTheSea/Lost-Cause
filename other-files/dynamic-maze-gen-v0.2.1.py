# proof of concept 2: expandable grid, preliminary visualisation | 18/09/21

# closer to a recursive backtracker

import random, time, pygame
pygame.init()

# each "point" in the maze
nodes = []

# generating nodes based on chosen size
maxX = 50
maxY = 50 

for x in range(1,maxX+1):
    for y in range(1,maxY+1):
        nodes.append((x, y))


screen = pygame.display.set_mode([(maxX*20)-10,(maxY*20)-10])

screen.fill((0,0,0))
pygame.draw.rect(screen, (255,255,255), pygame.Rect(0, 0, 10, 10))

# saving nodes before they are removed
all_nodes = tuple(nodes)

adjacent_nodes = ((-1, 0), (1,0), (0,1), (0, -1))

# using tuples to avoid accidental overwrites

total_nodes = len(nodes)

start_time = time.time()

# hold data on which nodes are visited, and in what order
spanning_tree = []

# node to start on
current_node = (1,1)

# creates the maze until all nodes are visited
while nodes:

    for  event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

    # removes current node from stack
    # print(current_node) | ENABLE FOR DEGUBBING
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
        
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((next_node[0]-1)*20, (next_node[1]-1)*20, 10, 10))
        # finding mid-points between current and previous nodes to remove wall
        join_x = ((current_node[0] - next_node[0])/2) + next_node[0] 
        join_y = ((current_node[1] - next_node[1])/2) + next_node[1]
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((join_x-1)*20, (join_y-1)*20, 10, 10))
        # time.sleep(0.00025)

    else:
        # print('new branch') | ENABLE FOR DEBUGGING
        # when branch meets a dead end, backtrack through the spanning tree to find an available node 
        for index in range(len(spanning_tree) -1, -1, -1): # (going from the end of spanning tree backwards)
            item = spanning_tree[index]
            check_node = item[1]
            for x, y in adjacent_nodes:
                if (check_node[0] +x, check_node[1] + y) in nodes: # WILL CHECK EVERY UNUSED NODE FOR AN AVAILABLE ONE, EVEN IF THERE ARE NONE
                    next_node = check_node; break
            else:
                continue
            # breaks both loops when next node is found
            break
    
    current_node = next_node

# calculating time taken to run 
end_time = time.time()-start_time
print((str(end_time)[:-(len(str(end_time).split('.')[1])-2)]) + 's')

# print(spanning_tree) | ENABLE FOR DEBUGGING


# pygame stuff
running = True
while running:

    for  event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()