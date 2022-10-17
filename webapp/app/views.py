from app import app, generateMaze
from flask import render_template, redirect, send_from_directory
import os
from PIL import Image
from pathlib import Path
from base64 import b64encode

seedGenerator = generateMaze.SeedGenerator()


def save_maze_image(maze_image):
    maze_image.save(os.path.join(app.root_path, "mazeimages", f"{seedGenerator.seed}.png"))


@app.route('/')
def index():
    return render_template('public/index.html')


@app.route('/mazeimages/<string:file_name>')
def get_maze_image(file_name):
    return send_from_directory(os.path.join(app.root_path, "mazeimages"), file_name)


@app.route('/play')
def play():
    seedGenerator.height = 3
    seedGenerator.width = 3
    maze_image = seedGenerator.create_base_64_seed()
    save_maze_image(maze_image)

    return redirect(f'/play/{seedGenerator.seed}')


@app.route('/play/<string:seed>')
def play_from_seed(seed):
    if seedGenerator.seed != seed:
        seedGenerator.seed = seed
        path = os.path.join(app.root_path, "mazeimages", f"{seed}.png")
        if not os.path.exists(path):
            maze_image = seedGenerator.draw_maze_from_seed()
            save_maze_image(maze_image)

    return render_template('public/play.html', mazeSeed=seedGenerator.seed)
