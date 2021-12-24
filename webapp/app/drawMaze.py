from PIL import Image
from pathlib import Path

def mazeImgGen(SIDELEN, spanning_tree):
    mazePath = Path('static/img/maze/')

    width = 400
    height = 300

    base = mazePath / 'base.png'
    img = Image.open(base)

    tile = mazePath / 'no-walls.png'
    tileImg = Image.open(tile)

    img = img.resize((SIDELEN*32*2-32,SIDELEN*32*2-32))
    # tiles are 32x32

    for node in spanning_tree:
        adjNodes = spanning_tree[node]
        img.paste(tileImg, ((node[0]-1)*64, (node[1]-1)*64))
        for adjNode in adjNodes:
            join_x = ((adjNode[0] - node[0])/2) + node[0] 
            join_y = ((adjNode[1] - node[1])/2) + node[1]
            img.paste(tileImg, (int((join_x-1)*64), int((join_y-1)*64)))


    img.save(mazePath / "fullmaze.png")