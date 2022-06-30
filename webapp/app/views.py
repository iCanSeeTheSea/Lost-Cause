from app import app, generateMaze
from flask import render_template
from base64 import b64encode


@app.route('/')
def index():
    return render_template('public/index.html')


@app.route('/play')
def about():
    map_height = 10
    map_width = 10
    seedGenerator = generateMaze.SeedGenerator(map_height, map_width)
    seedGenerator.createBase64Seed()
    seedGenerator.drawMazeFromSeed()

    return render_template('public/play.html', mazeSeed=seedGenerator.seed)
