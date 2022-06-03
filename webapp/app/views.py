from app import app, generateMaze
from flask import render_template
from base64 import b64encode


@app.route('/')
def index():
    return render_template('public/index.html')


@app.route('/play')
def about():
    map_height = 4
    map_width = 10
    mazeGenerator = generateMaze.MazeGenerator(map_width, map_height)
    mazeHex = mazeGenerator.recursiveBacktracking()

    # mazeB64 = f'{map_size}{map_size}{str(b64encode(bytes.fromhex(mazeHex)))[2:-1]}'
    # print(mazeB64)
    # base64Converter = generateMaze.Base64Converter(mazeB64)
    # mazeHex = base64Converter.mazeFromHex()

    return render_template('public/play.html', mazeHex=mazeHex, mapWidth=map_width, mapHeight=map_height)
