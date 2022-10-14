from app import app, generateMaze
from flask import render_template, redirect
import os
from pathlib import Path
from base64 import b64encode

seedGenerator = generateMaze.SeedGenerator()


@app.route('/')
def index():
    return render_template('public/index.html')


@app.route('/play')
def play():
    seedGenerator.height = 3
    seedGenerator.width = 3
    seedGenerator.create_base_64_seed()

    return redirect(f'/play/{seedGenerator.seed}')


@app.route('/play/<string:seed>')
def play_from_seed(seed):
    if seedGenerator.seed != seed:
        path = Path("/static/img/maze/")
        print(path / f"{seedGenerator.seed}.png")
        if os.path.exists(path / f"{seedGenerator.seed}.png"):
            os.remove(path / f"{seedGenerator.seed}.png")
        seedGenerator.seed = seed
        seedGenerator.draw_maze_from_seed()

    return render_template('public/play.html', mazeSeed=seedGenerator.seed)
