from PIL import Image
from pathlib import Path


# [top, bottom, left, right]
tileNames = {'[0, 0, 0, 0]': 'no-walls.png', '[0, 0, 0, 1]': 'right-wall.png', '[0, 0, 1, 0]': 'left-wall.png', '[0, 0, 1, 1]': 'left-right-wall.png',
             '[0, 1, 0, 0]': 'bottom-wall.png', '[0, 1, 0, 1]': 'bottom-right-corner.png', '[0, 1, 1, 0]': 'bottom-left-corner.png', '[0, 1, 1, 1]': 'bottom-dead.png', '[1, 0, 0, 0]': 'top-wall.png',
             '[1, 0, 0, 1]': 'top-right-corner.png', '[1, 0, 1, 0]': 'top-left-corner.png', '[1, 0, 1, 1]': 'top-dead.png', '[1, 1, 0, 0]': 'top-bottom-wall.png', '[1, 1, 0, 1]': 'right-dead.png',
             '[1, 1, 1, 0]': 'left-dead.png', '[1, 1, 1, 1]': ''}


def getIntFromString(section):
    s = ''
    for char in section:
        try:
            i = int(char)
            s += char
        except ValueError:
            pass
    return int(s)
            
        

def mazeImgGen(SIDELEN, spanning_tree):
    mazePath = Path('app/static/img/maze/')

    width = 400
    height = 300

    base = mazePath / 'base.png'
    img = Image.open(base)

    img = img.resize((SIDELEN*32*2-32, SIDELEN*32*2-32))
    # tiles are 32x32

    joinNodesDict = {}
    
    for strNode in spanning_tree:

        # turning dictionary keys (stored as strings) into  lists
        separated = strNode.split(',')
        node = [getIntFromString(separated[0]), getIntFromString(separated[1])]

        # getting the list of adjacent nodes from the dictionary
        adjNodes = []
        for index, wall in enumerate(spanning_tree[strNode][1]):
            if not wall:
                if index == 0:
                    adjNodes.append([node[0], node[1]-1])
                elif index == 1:
                    adjNodes.append([node[0], node[1]+1])
                elif index == 2:
                    adjNodes.append([node[0]-1, node[1]])
                elif index == 3:
                    adjNodes.append([node[0]+1, node[1]])
                
        
        # pasting the correct image (correspoding with the walls list) onto the main background image
        tile = mazePath / tileNames[str(spanning_tree[strNode][1])]
        tileImg = Image.open(tile)
        img.paste(tileImg, ((node[0]-1)*64, (node[1]-1)*64))

        
        for adjNode in adjNodes:
            # figuring out where to place adjacent corridors based
            join_x = ((adjNode[0] - node[0])/2) + node[0]
            join_y = ((adjNode[1] - node[1])/2) + node[1]

            # pasting corridors joinging the nodes, and saving their data to the dictionary
            if join_y-int(join_y) != 0:
                tile = mazePath / 'left-right-wall.png'
                joinNodesDict[str([int(join_x), join_y])] = [[], [0, 0, 1, 1]]
            elif join_x-int(join_x) != 0:
                tile = mazePath / 'top-bottom-wall.png'
                joinNodesDict[str([join_x, int(join_y)])] = [[], [1, 1, 0, 0]]
            
            tileImg = Image.open(tile)
            img.paste(tileImg, (int((join_x-1)*64), int((join_y-1)*64)))

    img.save(mazePath / "fullmaze.png")

    spanning_tree.update(joinNodesDict)
    
    return spanning_tree

