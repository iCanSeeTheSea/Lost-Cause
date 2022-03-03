from app import app, generateMaze, drawMaze
from flask import render_template


@app.route('/')
def index():
    return render_template('public/index.html')


@app.route('/play')
def about():
    map_size = 20
    spanning_tree = generateMaze.recursiveBacktracking(map_size, map_size)
    return render_template('public/play.html', spanningTree=spanning_tree, mapSize=map_size)
