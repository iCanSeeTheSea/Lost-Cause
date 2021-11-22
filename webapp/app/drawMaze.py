from PIL import Image
from pathlib import Path

# mazePath = Path('static/img/maze/')

width = 400
height = 300
#img = Image.new(mode='RGB', size=(width, height), color=(0, 16, 41))

# base = mazePath / 'base.png'
img = Image.open('base.png')

img.show()
