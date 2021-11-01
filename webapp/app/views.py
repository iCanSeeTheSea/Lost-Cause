from app import app
from flask import render_template
from app import generateMaze

@app.route('/')
def index():
    return render_template('public/index.html')

@app.route('/play')
def about():
    spanning_tree = generateMaze.mazeGen(20,20)
    return render_template('public/play.html', spanningTree=spanning_tree)