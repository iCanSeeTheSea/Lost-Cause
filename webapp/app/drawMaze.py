from PIL import Image
from pathlib import Path
import json


# [top, bottom, left, right]
# number corresponds to decimal value when walls dict is interpreted as binary
tileNames = {0: 'no-walls.png', 1: 'right-wall.png', 2: 'left-wall.png', 3: 'left-right-wall.png',
             4: 'bottom-wall.png', 5: 'bottom-right-corner.png', 6: 'bottom-left-corner.png', 7: 'bottom-dead.png', 8: 'top-wall.png',
             9: 'top-right-corner.png', 10: 'top-left-corner.png', 11: 'top-dead.png', 12: 'top-bottom-wall.png', 13: 'right-dead.png',
             14: 'left-dead.png', 15: ''}


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
    
    for strNode, walls in spanning_tree.items():

        # turning dictionary keys (stored as strings) into  lists
        separated = strNode.split(',')
        node = [getIntFromString(separated[0]), getIntFromString(separated[1])]

        # getting the list of adjacent nodes from the dictionary
        adjNodes = []

        if walls['top'] == 1:
            adjNodes.append([node[0], node[1]-1])
        if walls['bottom'] == 1:
            adjNodes.append([node[0], node[1]+1])
        if walls['left'] == 1:
            adjNodes.append([node[0]-1, node[1]])
        if walls['right'] == 1:
            adjNodes.append([node[0]+1, node[1]])

        print(node, adjNodes, walls, walls['top'])
        
        # pasting the correct image (correspoding with the walls list) onto the main background image

        key = (walls['top'] * 8) + (walls['bottom'] * 4) + (walls['left'] * 2) + (walls['right'])
                    
        tile = mazePath / tileNames[key]
        tileImg = Image.open(tile)
        img.paste(tileImg, ((node[0]-1)*64, (node[1]-1)*64))

        
        for adjNode in adjNodes:
            # figuring out where to place adjacent corridors based
            join_x = ((adjNode[0] - node[0])/2) + node[0]
            join_y = ((adjNode[1] - node[1])/2) + node[1]

            # pasting corridors joinging the nodes, and saving their data to the dictionary
            
            if join_y-int(join_y) != 0:
                tile = mazePath / 'left-right-wall.png'
                joinNodesDict[str([int(join_x), join_y])] = {'top': 0,'bottom': 0,'left': 1,'right': 1}
            elif join_x-int(join_x) != 0:
                tile = mazePath / 'top-bottom-wall.png'
                joinNodesDict[str([join_x, int(join_y)])] = {'top': 1,'bottom': 1,'left': 0,'right': 0}
            
            tileImg = Image.open(tile)
            img.paste(tileImg, (int((join_x-1)*64), int((join_y-1)*64)))

    img.save(mazePath / "fullmaze.png")

    spanning_tree.update(joinNodesDict)

    json_data = json.dumps(spanning_tree, indent = 3)
    with open('app/spanning-tree.json', 'w') as file:
        file.write(json_data)   

    #print(spanning_tree)
    
    return spanning_tree

