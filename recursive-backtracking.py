# recursive backtracking | 19/09/21

import random, time, pygame
pygame.init()

# generating nodes based on chosen size
maxX = 50
maxY = 50

nodes = []

for x in range(1,maxX+1):
    for y in range(1,maxY+1):
        nodes.append((x, y))

adjacent_nodes = ((-1, 0), (1,0), (0,1), (0, -1))

stack = []
spanning_tree = []

screen = pygame.display.set_mode([(maxX*20)-10,(maxY*20)-10])

screen.fill((0,0,0))
pygame.draw.rect(screen, (255,255,255), pygame.Rect(0, 0, 10, 10))

start_time = time.time()

next_node = (1,1)

while True:

    for  event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

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
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((next_node[0]-1)*20, (next_node[1]-1)*20, 10, 10))
        # finding mid-points between current and previous nodes to remove wall
        join_x = ((current_node[0] - next_node[0])/2) + next_node[0] 
        join_y = ((current_node[1] - next_node[1])/2) + next_node[1]
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((join_x-1)*20, (join_y-1)*20, 10, 10))

    else:
        # checking each node from the stack for possible nodes, if there are none, removing it
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
        break

# pygame stuff
running = True
while running:

    for  event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()