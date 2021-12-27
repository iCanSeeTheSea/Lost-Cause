from app import app, generateMaze, drawMaze
from flask import render_template


@app.route('/')
def index():
    return render_template('public/index.html')


@app.route('/play')
def about():
    spanning_tree = generateMaze.mazeGen(20, 20)
    drawMaze.mazeImgGen(20, spanning_tree)
    return render_template('public/play.html', spanningTree=spanning_tree)
