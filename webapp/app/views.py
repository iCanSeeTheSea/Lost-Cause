from app import app, generateMaze
from flask import render_template, redirect, send_from_directory, request, session
import os
from time import time
from PIL import Image

app.secret_key = os.urandom(12).hex()
maze_image_dir = os.path.join(app.root_path, "mazeimages")
seed_generator = generateMaze.SeedGenerator()


def save_maze_image(maze_image):
    """
    It deletes all the files in the maze_image_dir directory, then saves the maze_image parameter as a PNG file in the
    maze_image_dir directory

    :param maze_image: the image of the maze
    """
    for file in os.scandir(maze_image_dir):
        os.remove(file)
    session['image name'] = f"maze{str(time()).split('.')[0]}.png"
    maze_image.save(os.path.join(maze_image_dir, session['image name']))


def add_maze_to_session(seed):
    """
    If the session doesn't have a key called 'maze list', create it and set it to an empty list. If the seed isn't already
    in the list, add it

    :param seed: the seed for the maze
    """
    if 'maze list' not in session:
        session['maze list'] = []
    if seed not in session['maze list']:
        session['maze list'].append(seed)


@app.route('/')
def index():
    """
    The function `index()` returns the rendered template `public/index.html`
    :return: The index.html file is being returned.
    """
    return render_template('public/index.html')


@app.route('/mazeimages/<string:file_name>')
def get_maze_image(file_name):
    """
    It returns the image file from the maze_image_dir directory

    :param file_name: The name of the file to be sent
    :return: The image of the maze.
    """
    return send_from_directory(maze_image_dir, file_name)


@app.route('/play', methods=['GET'])
def play_with_size():
    """
    It takes in the height and width of the maze, creates a maze with those dimensions, and then redirects the user to the
    play page for that maze
    :return: A redirect to the play page with the seed as a parameter.
    """

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
    """
    It loads the maze image and adds its name to the session if it's not already there, then renders the play page

    :param seed: the seed for the maze
    :return: The play.html template is being returned.
    """
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
    """
    This function is called when the user completes the game. It sets the session variable 'game complete' to 1, and then
    renders the gamecomplete.html template.
    :return: The gamecomplete.html page is being returned.
    """
    session['game complete'] = 1
    print(session['maze list'])
    return render_template('public/gamecomplete.html', mazeList=session['maze list'])
