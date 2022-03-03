from app import app, generateMaze, drawMaze
from flask import render_template


@app.route('/')
def index():
    return render_template('public/index.html')


@app.route('/play')
def about():
    map_size = 20
    mazeHex = generateMaze.recursiveBacktracking(map_size, map_size)
    return render_template('public/play.html', mazeHex=mazeHex, mapSize=map_size)
