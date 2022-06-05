// debug
console.log(mazeHex)
console.log(mapWidth, mapHeight)
const mazeScale = 128

// mapping keys to movement directions
const directions = {
    up: "up",
    down: "down",
    left: "left",
    right: "right",
}
const keys = {
    'w': directions.up,
    'a': directions.left,
    'd': directions.right,
    's': directions.down,
    'ArrowUp': directions.up,
    'ArrowLeft': directions.left,
    'ArrowRight': directions.right,
    'ArrowDown': directions.down,
}


class Maze {

    constructor(mapHeight, mapWidth, mazeHex) {
        this.adjacencyList = [];
        this.height = mapHeight;
        this.width = mapWidth;
        this.mazeHex = mazeHex;
        this.createTree()
        }

    createTree() {
        // converting hex back into the spanning tree
        let index = 0;
        for (let row = 1; row <= mapHeight; row++) {
            let rowList = [];
            for (let column = 1; column <= mapWidth; column++) {

                // each hex character corresponds to one node of the maze
                let hex = this.mazeHex[index]

                let walls = {top: 1, bottom: 1, left: 1, right: 1}

                // converting hex to binary, nibble will represent the walls of the node
                let bin = (parseInt(hex, 16).toString(2)).padStart(4, '0')
                walls.top = parseInt(bin[0])
                walls.bottom = parseInt(bin[1])
                walls.left = parseInt(bin[2])
                walls.right = parseInt(bin[3])

                rowList.push(walls)

                index += 1
            }
            this.adjacencyList.push(rowList)
        }
    }

    getWalls(currentTile, prevTile, walls){
        // if the next node is going to be between two nodes
        if (Math.floor(currentTile.x) !== currentTile.x && prevTile.x !== currentTile.x) {
            walls =  { top: 1, bottom: 1, left: 0, right: 0 }

        } else if (Math.floor(currentTile.y) !== currentTile.y && prevTile.y !== currentTile.y) {
            walls =  { top: 0, bottom: 0, left: 1, right: 1 }

        } else if (prevTile.y !== currentTile.y || prevTile.x !== currentTile.x) {
            walls = this.adjacencyList[currentTile.y - 1][currentTile.x - 1]
        }
        return walls
    }

    output(){
        console.log(this.adjacencyList)
    }

}

class Entity {
    constructor(y, x, identifier) {
        this.x = x;
        this.y = y;
        this.speed = 0;
        this.prevTile = {y: 0, x: 0};
        this.currentTile = {y: 0, x:0};
        this.tileOrigin = {y: 0, x: 0};
        this.determineCurrentTile()
        this.walls = maze.getWalls(this.currentTile, this.prevTile);
        this.self = document.querySelector(identifier);
    }

    // function to round a number to the nearest 0.5
    roundTileCoord(tileCoord) {
        if (tileCoord - Math.floor(tileCoord) > 0.5) {
            tileCoord = Math.floor(tileCoord) + 0.5
        } else {
            tileCoord = Math.floor(tileCoord)
        }
        return tileCoord
    }

    determineCurrentTile(){
        // store previous node to know where its walls where
        this.prevTile.y = this.currentTile.y
        this.prevTile.x = this.currentTile.x;

        // work out which tile in the spanning tree the entity is in
        this.currentTile.x = this.roundTileCoord((this.x / mazeScale) + 1);
        this.currentTile.y = this.roundTileCoord((this.y / mazeScale) + 1);
    }

    determineWalls() {
        this.determineCurrentTile()
        return maze.getWalls(this.currentTile, this.prevTile, this.walls)
    }

    checkCollision(originalX, originalY) {
        // maze wall collisions
        // top, bottom, left, right

        this.walls = this.determineWalls()

        // left
        if (this.x < this.tileOriginX + 1) {
            if (this.walls.left === 1) {
                this.x = originalX;
            } else if (this.walls.left === 0 && this.y < this.tileOriginY + 1) {
                // corner correction
                this.x = originalX;
            }
        }
        // right
        if (this.x > this.tileOriginX + 32) {
            if (this.walls.right === 1) {
                this.x = originalX;
            } else if (this.walls.right === 0 && this.y > this.tileOriginY + 41) {
                this.x = originalX;
            }
        }
        // top
        if (this.y < this.tileOriginY + 1) {
            if (this.walls.top === 1) {
                this.y = originalY;
            } else if (this.walls.top === 0 && this.x < this.tileOriginX + 1) {
                this.y = originalY;
            }
        }
        // bottom
        if (this.y > this.tileOriginY + 41) {
            if (this.walls.bottom === 1) {
                this.y = originalY;
            } else if (this.walls.bottom === 0 && this.x > this.tileOriginX + 32) {
                this.y = originalY;
            }
        }
    }

    move(direction) {
        // storing position from previous frame in case new position is blocked
        let originalX = this.x;
        let originalY = this.y;

        // get the coordinates of the tile and data from spanning tree
        this.tileOriginX = (this.currentTile.x - 1) * mazeScale;
        this.tileOriginY = (this.currentTile.y - 1) * mazeScale;

        switch (direction) {
            case directions.right:
                this.x += this.speed;
                break;
            case directions.left:
                this.x -= this.speed;
                break;
            case directions.down:
                this.y += this.speed;
                break;
            case directions.up:
                this.y -= this.speed;
                break;
        }
        this.checkCollision(originalX, originalY)
    }

    getTilePosition(){
        return this.currentTile
    }

}

class Player extends Entity {
    constructor() {
        super(27, 16, '.character');
        this.speed = 1
        this.map = document.querySelector('.map')
    }

    move(pixelSize){
        let mapX = this.x;
        let mapY = this.y;

        //console.log(this.y, this.x, this.currentTileY, this.currentTileX, this.walls)

        let held_direction = held_directions[0];
        if (held_direction){
            super.move(held_direction)
            this.self.setAttribute("facing", held_direction)
            this.self.setAttribute("walking", "true");
        } else {
            this.self.setAttribute("walking", "false");
        }

        // smooth camera movement - moves the map against the player while the player is in the centre of the map
        if (mapX < 112) { mapX = 112; } // left
        if (mapX > imgWidth - 112) { mapX = imgWidth - 112; } // right
        if (mapY < 112) { mapY = 112; } // tops
        if (mapY > imgHeight - 112) { mapY = imgHeight - 112; } // bottom
        let camera_top = pixelSize * 112;
        let camera_left = pixelSize * 112;

        // moving the map and player
        this.map.style.transform = `translate3d( ${-mapX * pixelSize + camera_left}px, ${-mapY * pixelSize + camera_top}px, 0 )`;
        this.self.style.transform = `translate3d( ${this.x * pixelSize}px, ${this.y * pixelSize}px, 0 )`;

        }
}

class Enemy extends Entity {
    constructor(range) {
        super(0, 0, '.enemy');
        this.speed = 1;
        this.range = range
        this.path = [];
        this.target = {};
        this.targetTile = {};
    }

    spawn(tileY, tileX){
        this.x = (tileX -1) * mazeScale + 20
        this.y = (tileY -1) * mazeScale + 40
        this.currentTile = this.prevTile = {y: tileY, x: tileX}
    }

    pathFind(){
        this.targetTile = player.getTilePosition()
        // TODO use getter
        let walls = player.walls()
        let min = {y: this.currentTile.y - this.range/2, x: this.currentTile.x - this.range/2};
        let max = {y: this.currentTile.y + this.range/2, x: this.currentTile.x + this.range/2};

        if (min.y <= this.targetTile.y <= max.y && min.x <= this.targetTile.x <= max.x){
            let checkTile = this.targetTile
            let prevCheckTile = checkTile
            let tilesInRange = []
            let adjacentTiles = []
            let visitedTiles = []
            this.path = []
            console.log('search start', this.currentTile, this.walls)

            for (let row = min.y; row <= max.y; row += 0.5){
                for (let column = min.x; column <= max.x; column += 0.5){

                }
            }


            while (checkTile !== this.currentTile){


            }
        }
    }


    // ! doesnt work
    depthFirstSearch(checkTile, prevCheckTile, walls, depth){
        walls = maze.getWalls(checkTile, prevCheckTile, walls);
        console.log(prevCheckTile, checkTile, this.targetTile, walls, depth, this.path)
        if (depth < this.range) {
            if (this.walls.top === 0 && prevCheckTile.y >= checkTile.y) {
                if (checkTile.y - 0.5 === this.targetTile.y) {
                    return true;
                } else if (this.depthFirstSearch({y: checkTile.y - 0.5, x: checkTile.x}, checkTile, walls,+ 0.5)) {
                    this.path.unshift(directions.up)
                    return true
                }
            }
            if (this.walls.bottom === 0 && prevCheckTile.y <= checkTile.y) {
                if (checkTile.y + 0.5 === this.targetTile.y) {
                    return true;
                } else if(this.depthFirstSearch({y: checkTile.y + 0.5, x: checkTile.x}, checkTile, walls,depth + 0.5)){
                    this.path.unshift(directions.down)
                    return true
                }
            }
            if (this.walls.left === 0 && prevCheckTile.x >= checkTile.x) {
                if (checkTile.x - 0.5 === this.targetTile.x) {
                    return true;
                } else if(this.depthFirstSearch({y: checkTile.y, x: checkTile.x - 0.5}, checkTile, walls,depth + 0.5)) {
                    this.path.unshift(directions.left)
                    return true
                }
            }
            if (this.walls.right === 0 && prevCheckTile.x <= checkTile.x) {
                if (checkTile.x + 0.5 === this.targetTile.x) {
                    return true;
                } else if(this.depthFirstSearch({y: checkTile.y, x: checkTile.x + 0.5}, checkTile, walls,depth + 0.5)) {
                    this.path.unshift(directions.right)
                    return true
                }
            }
            return false
        } else {
            return false
        }
    }

    move(pixelSize){
        //console.log(this.y, this.x, this.currentTileY, this.currentTileX, this.walls, this.target, this.path)
        if (this.target !== {}) {
            // move towards target
            if (this.x > this.target.x) {
                let direction = directions.left
            } else if (this.x < this.target.x) {
                let direction = directions.right
            } else if (this.y > this.target.y) {
                let direction = directions.up
            } else if (this.y < this.target.y) {
                let direction = directions.down
            } else {
                this.target = {};
                this.path.shift();
            }
        }
        if (this.targetTile.x === this.currentTileX && this.targetTile.y === this.currentTileY){
            // set player as target
        } else if (!this.path){
            // random movement
        } else {
            // move to next tile
            super.move(this.path[0]);
            if (Math.abs(this.currentTileX - this.prevTileX) === 0.5 || Math.abs(this.currentTileY - this.prevTileY) === 0.5) {
                this.target = {y: this.tileOriginX + 20, x: this.tileOriginY + 15}
            }
        }
        this.self.style.transform = `translate3d( ${this.x * pixelSize}px, ${this.y * pixelSize}px, 0 )`;
    }
}

const maze = new Maze(mapHeight, mapWidth, mazeHex)
maze.output()

let player = new Player()

let enemy = new Enemy(3)
enemy.spawn(2, 2)

// setting css properties to correct values
let root = document.querySelector(':root');
root.style.setProperty('--map-width', mapWidth);
root.style.setProperty('--map-height', mapHeight);

// initial variable declarations
let held_directions = [];
const imgWidth = (maze.width * mazeScale) - 64
const imgHeight = (maze.height * mazeScale) - 64

// determines where the character (and maze) is positioned every frame
const gameLoop = function () {

    // getting the pixel size being used from the css - varies depending on how large the browser window is
    let pixelSize = parseInt(
        getComputedStyle(document.documentElement).getPropertyValue('--pixel-size')
    );

    player.move(pixelSize)

    enemy.pathFind();
    enemy.move(pixelSize)

}

// steps through every frame
const step = function () {
    gameLoop()
    window.requestAnimationFrame(function () {
        step()
    })
}
step()



// event listeners for keys being pressed and released
document.addEventListener('keydown', function (e) {
    let dir = keys[e.key];
    // adds last key pressed to the start of the held_directions array
    if (dir && held_directions.indexOf(dir) === -1) {
        held_directions.unshift(dir);
    }
})

document.addEventListener('keyup', function (e) {
    let dir = keys[e.key];
    let index = held_directions.indexOf(dir);
    // removes key from help_directions when it stops being pressed
    if (index > -1) {
        held_directions.splice(index, 1)
    }
})