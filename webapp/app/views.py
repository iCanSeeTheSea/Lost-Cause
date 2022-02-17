from app import app, generateMaze, drawMaze
from flask import render_template


@app.route('/')
def index():
    return render_template('public/index.html')


@app.route('/play')
def about():
    map_size = 10
    spanning_tree = generateMaze.mazeGen(map_size, map_size)
    spanning_tree = drawMaze.mazeImgGen(map_size, spanning_tree)
    return render_template('public/play.html', spanningTree=spanning_tree, mapSize=map_size)
