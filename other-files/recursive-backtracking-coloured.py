# recursive backtracking | 19/09/21

import random
import time
import pygame
pygame.init()



def mazeGen(m, maxX, maxY):
    nodes = []
    colour = [255, 255, 255]
    step = 0

    for x in range(1, maxX+1):
        for y in range(1, maxY+1):
            nodes.append((x, y))

    adjacent_nodes = ((-1, 0), (1, 0), (0, 1), (0, -1))

    stack = []
    spanning_tree = []

    # initialising pygame window
    screen = pygame.display.set_mode([(maxX*(m*2))-m, (maxY*(m*2))-m])
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, m, m))

    start_time = time.perf_counter()

    next_node = (1, 1)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

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
            
            # visualisation
            rColour = tuple(colour)
            pygame.draw.rect(screen, rColour, pygame.Rect(
                (next_node[0]-1)*(m*2), (next_node[1]-1)*(m*2), m, m))
            # finding mid-points between current and previous nodes to remove wall
            join_x = ((current_node[0] - next_node[0])/2) + next_node[0]
            join_y = ((current_node[1] - next_node[1])/2) + next_node[1]
            pygame.draw.rect(screen, rColour, pygame.Rect(
                (join_x-1)*(m*2), (join_y-1)*(m*2), m, m))

        else:
            # checking each node from the stack for possible nodes, if there are none, removing it
            for index in range(len(stack)-1, -1, -1):
                check_node = stack[index]
                for dx, dy in adjacent_nodes:
                    if (check_node[0] + dx, check_node[1] + dy) in nodes:
                        next_node = check_node
                        colour[step] -= 20; colour[step-1] -= 20
                        if colour[step] < 50: colour[step] = 250; step += 1
                        if colour[step-1] < 50: colour[step-1] = 250
                        if step > 2: step = 0
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

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()


mazeGen(m=20, maxX=20, maxY=20)
