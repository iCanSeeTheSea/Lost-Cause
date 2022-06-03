# recursive backtracking | 19/09/21

from platform import node
import random
import time
import pygame
pygame.init()


def chooseColour(node):
    if 0 <= node[1] < 10 or 40 <= node[1]:
        colour = (85, 205, 252)
    elif 10 <= node[1] < 20 or 30 <= node[1] < 40:
        colour = (247, 168, 184)
    elif 20 <= node[1] < 30:
        colour = (255, 255, 255)
    return colour


def mazeGen(m, maxX, maxY):
    nodes = []
    step = 0

    for x in range(1, maxX+1):
        for y in range(1, maxY+1):
            nodes.append((x, y))

    adjacent_nodes = ((-1, 0), (1, 0), (0, 1), (0, -1))

    stack = []
    spanning_tree = []

    start_time = time.time()

    next_node = (1, 1)
    colour = chooseColour(next_node)

    # initialising pygame window
    screen = pygame.display.set_mode([(maxX*(m*2))-m, (maxY*(m*2))-m])
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, colour, pygame.Rect(0, 0, m, m))

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
            colour = chooseColour(next_node)
            pygame.draw.rect(screen, colour, pygame.Rect(
                (next_node[0]-1)*(m*2), (next_node[1]-1)*(m*2), m, m))
            # finding mid-points between current and previous nodes to remove wall
            join_x = ((current_node[0] - next_node[0])/2) + next_node[0]
            join_y = ((current_node[1] - next_node[1])/2) + next_node[1]
            colour = chooseColour([join_x, join_y])
            pygame.draw.rect(screen, colour, pygame.Rect(
                (join_x-1)*(m*2), (join_y-1)*(m*2), m, m))

        else:
            # checking each node from the stack for possible nodes, if there are none, removing it
            for index in range(len(stack)-1, -1, -1):
                check_node = stack[index]
                for dx, dy in adjacent_nodes:
                    if (check_node[0] + dx, check_node[1] + dy) in nodes:
                        next_node = check_node
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
            end_time = time.time()-start_time
            print(
                (str(end_time)[:-(len(str(end_time).split('.')[1])-2)]) + 's')
            break

    running = True
    # while running:

    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False

    pygame.display.flip()

    time.sleep(0.5)

    pygame.quit()


mazeGen(m=5, maxX=120, maxY=50)
