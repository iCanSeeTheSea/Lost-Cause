# primms 

import random, time, pygame
pygame.init()

def mazeGen(m, maxX, maxY):
    nodes = []
    colour = [255, 255, 255]
    step = 2
    count = 0

    for x in range(1, maxX+1):
        for y in range(1, maxY+1):
            nodes.append((x, y))

    adjacent_nodes = ((-1, 0), (1, 0), (0, 1), (0, -1))

    frontiers = []

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
        
        # print(current_node)
        try:
            nodes.remove(current_node)
        except ValueError:
            pass

        # finding possible next nodes by comparing each position adjacent to the current node to the unused nodes
        for dx, dy in adjacent_nodes:
            if (current_node[0] + dx, current_node[1] + dy) in nodes:
                frontiers.append(
                    [(current_node[0] + dx, current_node[1] + dy), current_node])
        
        if frontiers:
            # choosing a random (adjacent) node to go next
        
            next_node = random.choice(frontiers)
            frontiers.remove(next_node)
            for node in frontiers:
                if node[0] == next_node[0]:
                    frontiers.remove(node)
            prev_node = next_node[1]
            next_node = next_node[0]
            spanning_tree.append((next_node, prev_node))
            
            # visualisation
            rColour = tuple(colour)
            pygame.draw.rect(screen, rColour, pygame.Rect(
                (next_node[0]-1)*(m*2), (next_node[1]-1)*(m*2), m, m))
            # finding mid-points between current and previous nodes to remove wall
            join_x = ((prev_node[0] - next_node[0])/2) + next_node[0]
            join_y = ((prev_node[1] - next_node[1])/2) + next_node[1]
            pygame.draw.rect(screen, rColour, pygame.Rect(
                (join_x-1)*(m*2), (join_y-1)*(m*2), m, m))
            
            # colours
            if count%((maxX*maxY)//10 + (maxX*maxY)//100) == 0:
                colour[step] -= 20; colour[step-1] -= 20
                if colour[step] < 50: colour[step] = 250; step += 1
                if colour[step-1] < 50: colour[step-1] = 250
                if step > 2: step = 0
            count += 1

        else:
            end_time = time.perf_counter()-start_time
            print(
                (str(end_time)[:-(len(str(end_time).split('.')[1])-2)]) + 's')
            #print(spanning_tree)
            break
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()

mazeGen(4,100,100)