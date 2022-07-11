// debug
console.log(mazeSeed)
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

const toBinary = {'A': '000000', 'B': '000001', 'C': '000010', 'D': '000011', 'E': '000100', 'F': '000101',
                    'G': '000110', 'H': '000111',
                    'I': '001000', 'J': '001001', 'K': '001010', 'L': '001011', 'M': '001100', 'N': '001101',
                    'O': '001110', 'P': '001111',
                    'Q': '010000', 'R': '010001', 'S': '010010', 'T': '010011', 'U': '010100', 'V': '010101',
                    'W': '010110', 'X': '010111',
                    'Y': '011000', 'Z': '011001', 'a': '011010', 'b': '011011', 'c': '011100', 'd': '011101',
                    'e': '011110', 'f': '011111',
                    'g': '100000', 'h': '100001', 'i': '100010', 'j': '100011', 'k': '100100', 'l': '100101',
                    'm': '100110', 'n': '100111',
                    'o': '101000', 'p': '101001', 'q': '101010', 'r': '101011', 's': '101100', 't': '101101',
                    'u': '101110', 'v': '101111',
                    'w': '110000', 'x': '110001', 'y': '110010', 'z': '110011', '0': '110100', '1': '110101',
                    '2': '110110', '3': '110111',
                    '4': '111000', '5': '111001', '6': '111010', '7': '111011', '8': '111100', '9': '111101',
                    '-': '111110', '_': '111111'}

class Node{
    constructor(y, x, walls) {
        this.x = x;
        this.y = y;
        this.top = walls.top;
        this.bottom = walls.bottom;
        this.left = walls.left;
        this.right = walls.right;
    }

    wallString(){
        return this.top.toString() + this.bottom.toString() + this.left.toString() + this.right.toString();
    }

    position(){
        return {y: this.y, x: this.x}
    }
    
}

class HorizontalEdge extends Node{
    constructor(y, x) {
        let walls = { top: 1, bottom: 1, left: 0, right: 0 }
        super(y, x, walls);
    }
}

class VerticalEdge extends Node{
    constructor(y, x) {
        let walls = { top: 0, bottom: 0, left: 1, right: 1 }
        super(y, x, walls);
    }
}


class Maze {

    constructor(seed) {
        this.seed = seed;

        let base64String = this.seed.replace(/=/g, '')
        console.log(base64String)
        let binaryString = ''
        for (let i = 0; i < base64String.length; i++){
            binaryString += toBinary[base64String[i]]
        }
        let padding = (this.seed.length - base64String.length)*8
        this.height = parseInt(binaryString.slice(0,8), 2);
        this.width = parseInt(binaryString.slice(8,16), 2);
        binaryString = binaryString.slice(16, binaryString.length - padding)
        console.log(binaryString,this.height, this.width)

        this.adjacencyList = [];

        // populating tree
        let index = 0;
        for (let row = 1; row <= this.height; row++) {
            let rowList = [];
            for (let column = 1; column <= this.width; column++) {
                let bin = binaryString.slice(0,4)
                let walls = {top: parseInt(bin[0]), bottom: parseInt(bin[1]), left: parseInt(bin[2]), right: parseInt(bin[3])}
                let node = new Node(row, column, walls);
                rowList.push(node)
                binaryString = binaryString.slice(4)
                index += 1
            }
            this.adjacencyList.push(rowList)
        }
    }

    getNodeFromCoordinate(y, x){
        return this.adjacencyList[y - 1][x - 1]
    }

    // getNode(currentTile, prevTile){
    //     let node = currentTile;
    //     // if the next node is going to be between two nodes
    //     if (Math.floor(currentTile.x) !== currentTile.x && prevTile.x !== currentTile.x) {
    //         node = HorizontalEdge(currentTile.y, currentTile.x)
    //
    //     } else if (Math.floor(currentTile.y) !== currentTile.y && prevTile.y !== currentTile.y) {
    //         node = VerticalEdge(currentTile.y, currentTile.x)
    //
    //     } else if (prevTile.y !== currentTile.y || prevTile.x !== currentTile.x) {
    //         node = this.adjacencyList[currentTile.y - 1][currentTile.x - 1]
    //     }
    //     return node
    // }

    checkTileInMaze(tile){
        if (tile.x % 1 === 0 && tile.y % 1 === 0 && 0 < tile.x <= this.width && 0 < tile.y <= this.height){
            return true;
        }
        if (tile.y % 1 !== 0 && tile.x % 1 === 0){
            let adjTile = this.getNode({y:Math.floor(tile.y), x:tile.x})
            if (adjTile.bottom === 0){
                return true
            }
        }
        if (tile.x % 1 !== 0 && tile.y % 1 === 0){
            let adjTile = this.getNode({y:tile.y, x:Math.floor(tile.x)})
            if (adjTile.right === 0){
                return true
            }
        }
        return false
    }

    getNode(currentTile){
        if (this.checkTileInMaze(currentTile)) {
            if (currentTile.x % 1 !== 0) {
                return new HorizontalEdge(currentTile.y, currentTile.x)
            } else if (currentTile.y % 1 !== 0) {
                return new VerticalEdge(currentTile.y, currentTile.x)
            } else {
                return this.adjacencyList[currentTile.y - 1][currentTile.x - 1]
            }
        }
        return false
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
        this.prevTile = {y: 0, x:0};
        this.currentTile = {y: 0, x:0};
        this.tileOrigin = {y: 0, x:0}
        this.determineCurrentTile()
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
        this.prevTile = this.currentTile;

        // work out which tile in the spanning tree the entity is in
        this.currentTile.x = this.roundTileCoord((this.x / mazeScale) + 1);
        this.currentTile.y = this.roundTileCoord((this.y / mazeScale) + 1);

        this.currentTile = maze.getNode(this.currentTile, this.prevTile)
    }

    checkCollision(originalX, originalY) {
        // maze wall collisions
        // top, bottom, left, right

        this.determineCurrentTile()

        // left
        if (this.x < this.tileOriginX + 1) {
            if (this.currentTile.left === 1) {
                this.x = originalX;
            } else if (this.currentTile.left === 0 && this.y < this.tileOriginY + 1) {
                // corner correction
                this.x = originalX;
            }
        }
        // right
        if (this.x > this.tileOriginX + 32) {
            if (this.currentTile.right === 1) {
                this.x = originalX;
            } else if (this.currentTile.right === 0 && this.y > this.tileOriginY + 41) {
                this.x = originalX;
            }
        }
        // top
        if (this.y < this.tileOriginY + 1) {
            if (this.currentTile.top === 1) {
                this.y = originalY;
            } else if (this.currentTile.top === 0 && this.x < this.tileOriginX + 1) {
                this.y = originalY;
            }
        }
        // bottom
        if (this.y > this.tileOriginY + 41) {
            if (this.currentTile.bottom === 1) {
                this.y = originalY;
            } else if (this.currentTile.bottom === 0 && this.x > this.tileOriginX + 32) {
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

    getCurrentTile(){
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
            // * this will need to move to Entity
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
        if (this.path.length > 0){
            return
        }
        this.targetTile = player.getCurrentTile()
        let min = {y: this.currentTile.y - this.range/2, x: this.currentTile.x - this.range/2};
        let max = {y: this.currentTile.y + this.range/2, x: this.currentTile.x + this.range/2};
        if (min.y <= this.targetTile.y <= max.y && min.x <= this.targetTile.x <= max.x){
            let nodesInRange = [];
            let positionsInRange = [];
            console.log('search start', this.currentTile);
            // ! plan this properly
            for (let row = min.y; row <= max.y; row += 0.5){
                for (let column = min.x; column <= max.x; column += 0.5){
                    let node = maze.getNode({row, column})
                    if (node){
                        nodesInRange.push(node);
                        positionsInRange.push(node.position());
                    }
                }
            }
            let checkTile = this.targetTile;
            let checkPosition = checkTile.position;
            let visitedNodes = []
            let visitedPositions = []
            while(true){
                console.log(checkTile, checkPosition, this.path)
                if (checkTile === this.currentTile){
                    // has found player
                    break;
                }
                let index = positionsInRange.indexOf(checkPosition);
                positionsInRange.splice(index);
                nodesInRange.splice(index);
                let nextPosition = checkPosition;
                let direction = false;
                if (checkTile.top === 0){
                    nextPosition.y -= 0.5;
                    direction = "down";
                    checkTile.top = 1;
                } else if (checkTile.bottom === 0){
                    nextPosition.y += 0.5;
                    direction = "up";
                    checkTile.bottom = 1;
                } else if (checkTile.left === 0){
                    nextPosition.x -= 0.5;
                    direction = "right";
                    checkTile.left = 1;
                } else if (checkTile.right === 0){
                    nextPosition.x += 0.5;
                    direction = "left";
                    checkTile.right = 1;
                }
                if (nextPosition in positionsInRange){
                    this.path.push(direction);
                    visitedNodes.push(checkTile)
                    visitedPositions.push(checkPosition)
                    checkPosition = nextPosition;
                    index = positionsInRange.indexOf(checkPosition)
                    checkTile = nodesInRange[index]
                } else {
                    // can't find player
                    this.path.pop()
                    checkTile = visitedNodes.pop()
                    checkPosition = visitedPositions.pop()
                }
            }
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
            if (Math.abs(this.currentTile.x - this.prevTile.x) === 0.5 || Math.abs(this.currentTile.y - this.prevTile.y) === 0.5) {
                this.target = {y: this.tileOriginX + 20, x: this.tileOriginY + 15}
            }
        }
        this.self.style.transform = `translate3d( ${this.x * pixelSize}px, ${this.y * pixelSize}px, 0 )`;
    }
}

const maze = new Maze(mazeSeed)
maze.output()

let player = new Player()

let enemy = new Enemy(3)
enemy.spawn(2, 2)

// setting css properties to correct values
let root = document.querySelector(':root');
root.style.setProperty('--map-width', maze.width);
root.style.setProperty('--map-height', maze.height);

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
    // enemy.move(pixelSize)

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