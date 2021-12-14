from PIL import Image
from pathlib import Path
import generateMaze

SIDELEN = 5

spanning_tree = generateMaze.mazeGen(SIDELEN,SIDELEN)

mazePath = Path('static/img/maze/')

width = 400
height = 300

base = mazePath / 'base.png'
img = Image.open(base)

tile = mazePath / 'no-walls.png'
tileImg = Image.open(tile)

img = img.resize((SIDELEN*32*2,SIDELEN*32*2))

for node in spanning_tree:
    img.paste(tileImg, (node[0][0]-1*32, node[0][1]-1*32))
    # join_x = ((node[1][0] - node[0][0])/2) + node[0][0] 
    # join_y = ((node[1][1] - node[0][1])/2) + node[0][1]
    # img.paste(tileImg, (join_x-1*32, join_y-1*32))

img.show()
