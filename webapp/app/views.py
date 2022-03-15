from app import app, generateMaze
from flask import render_template
import base64

@app.route('/')
def index():
    return render_template('public/index.html')


@app.route('/play')
def about():
    map_size = 20
    mazeGenerator = generateMaze.MazeGenerator(map_size, map_size)
    mazeHex = mazeGenerator.recursiveBacktracking()
    
    mazeB64 = f'{b64encode(bytes(map_size))}{b64encode(bytes(map_size))}{b64encode(bytes.fromhex(mazeHex))}'
    print(mazeB64)
    
    base64Converter = generateMaze.Base64Converter(mazeB64)
    mazeHex = base64Converter.mazeFromHex()
    
    return render_template('public/play.html', mazeHex=mazeHex, mapSize=map_size)
