from app import app, generateMaze
from flask import render_template, redirect, send_from_directory, request, session, Response
import os
from time import time
from PIL import Image
from pathlib import Path
from base64 import b64encode

app.secret_key = os.urandom(12).hex()
maze_image_dir = os.path.join(app.root_path, "mazeimages")
seed_generator = generateMaze.SeedGenerator()


def save_maze_image(maze_image):
    for file in os.scandir(maze_image_dir):
        os.remove(file)
    session['image name'] = f"maze{str(time()).split('.')[0]}.png"
    maze_image.save(os.path.join(maze_image_dir, session['image name']))


def add_maze_to_session(seed):
    if 'maze list' not in session:
        session['maze list'] = []
    if seed not in session['maze list']:
        session['maze list'].append(seed)


@app.route('/')
def index():
    return render_template('public/index.html')


@app.route('/mazeimages/<string:file_name>')
def get_maze_image(file_name):
    return send_from_directory(maze_image_dir, file_name)


@app.route('/play', methods=['GET'])
def play_with_size():

    args = request.args.to_dict()

    if 'maxEnemies' in args:
        session['max enemies'] = int(args['maxEnemies'])
    if 'maxLocks' in args:
        session['max locks'] = int(args['maxLocks'])

    seed_generator.height = int(args['height'])
    seed_generator.width = int(args['width'])
    maze_image = seed_generator.create_base_64_seed()
    save_maze_image(maze_image)
    add_maze_to_session(seed_generator.seed)

    return redirect(f"/play/{seed_generator.seed}")


@app.route('/play/<string:seed>')
def play_from_seed(seed):
    if seed_generator.seed != seed:
        seed_generator.seed = seed
        maze_image = seed_generator.draw_maze_from_seed()
        save_maze_image(maze_image)
        add_maze_to_session(seed)

    if 'game complete' not in session:
        session['game complete'] = 0

    if session['game complete']:
        level = "custom"
    else:
        level = str(len(session['maze list']))

    if 'max enemies' not in session:
        session['max enemies'] = -1
    if 'max locks' not in session:
        session['max locks'] = -1

    return render_template('public/play.html', level=level, maxEnemies=session["max enemies"], maxLocks=session["max locks"], mazeImage=session['image name'], mazeSeed=seed_generator.seed, gameComplete=session['game complete'])


@app.route('/gamecomplete')
def game_complete():
    session['game complete'] = 1
    print(session['maze list'])
    return render_template('public/gamecomplete.html', mazeList=session['maze list'])
