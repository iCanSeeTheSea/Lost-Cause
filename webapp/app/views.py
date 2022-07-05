from app import app, generateMaze
from flask import render_template, redirect
from base64 import b64encode

seedGenerator = generateMaze.SeedGenerator()


@app.route('/')
def index():
    return render_template('public/index.html')


@app.route('/play')
def play():
    seedGenerator.height = 10
    seedGenerator.width = 10
    seedGenerator.createBase64Seed()

    return redirect(f'/play/{seedGenerator.seed}')


@app.route('/play/<string:seed>')
def playFromSeed(seed):
    if seedGenerator.seed != seed:
        seedGenerator.seed = seed
        seedGenerator.drawMazeFromSeed()

    return render_template('public/play.html', mazeSeed=seedGenerator.seed)
