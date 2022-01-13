from PIL import Image
from pathlib import Path

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

    for strNode in spanning_tree:
        separated = strNode.split(',')
        node = [getIntFromString(separated[0]), getIntFromString(separated[1])]
        adjNodes = spanning_tree[strNode][0]
        tile = mazePath / tileNames[str(spanning_tree[strNode][1])]
        tileImg = Image.open(tile)
        img.paste(tileImg, ((node[0]-1)*64, (node[1]-1)*64))
        for adjNode in adjNodes:
            join_x = ((adjNode[0] - node[0])/2) + node[0]
            join_y = ((adjNode[1] - node[1])/2) + node[1]
            if join_y-int(join_y) != 0:
                tile = mazePath / 'left-right-wall.png'
            elif join_x-int(join_x) != 0:
                tile = mazePath / 'top-bottom-wall.png'
            tileImg = Image.open(tile)
            img.paste(tileImg, (int((join_x-1)*64), int((join_y-1)*64)))

    img.save(mazePath / "fullmaze.png")
