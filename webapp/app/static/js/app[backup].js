// debug
console.log(mazeHex)
console.log(mapWidth, mapHeight)


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

    getWalls(currentTileX, currentTileY, prevTileX, prevTileY, walls){
        // if the next node is going to be between two nodes
        if (Math.floor(currentTileX) !== currentTileX && prevTileX !== currentTileX) {
            walls =  { top: 1, bottom: 1, left: 0, right: 0 }

        } else if (Math.floor(currentTileY) !== currentTileY && prevTileY !== currentTileY) {
            walls =  { top: 0, bottom: 0, left: 1, right: 1 }

        } else if (prevTileX !== currentTileX || prevTileY !== currentTileY) {
            walls = this.adjacencyList[currentTileY - 1][currentTileX - 1]
        }
        return walls
    }

    output(){
        console.log(this.adjacencyList)
    }

}

const maze = new Maze(mapHeight, mapWidth, mazeHex)
maze.output()

// setting css properties to correct values
let root = document.querySelector(':root');
root.style.setProperty('--map-width', mapWidth); 
root.style.setProperty('--map-height', mapHeight); 


// initial variable declarations
let held_directions = [];
let character = document.querySelector('.character');
let map = document.querySelector(".map");
let x = 16;
let y = 27;
let prevTileX = 0;
let prevTileY = 0;
let currentTileX = 1
let currentTileY = 1
let speed = 1;
let walls = maze.getWalls(currentTileX, currentTileY, prevTileX, prevTileY);
const mazeScale = 128

// function to round a number to the nearest 0.5
const roundTileCoord = function (tileCoord) {
    if (tileCoord - Math.floor(tileCoord) > 0.5) {
        tileCoord = Math.floor(tileCoord) + 0.5
    } else {
        tileCoord = Math.floor(tileCoord)
    }
    return tileCoord
}

// determines where the character (and maze) is positioned every frame
const placeCharacter = function () {

    // getting the pixel size being used from the css - varies depending on how large the browser window is
    let pixelSize = parseInt(
        getComputedStyle(document.documentElement).getPropertyValue('--pixel-size')
    );

    // storing position from previous frame in case new position is blocked 
    let originalX = x;
    let originalY = y;

    // work out which direction the user wants to move the player
    const held_direction = held_directions[0];
    if (held_direction) {
        switch (held_direction) {
            case directions.right:
                x += speed;
                break;
            case directions.left:
                x -= speed;
                break;
            case directions.down:
                y += speed;
                break;
            case directions.up:
                y -= speed;
                break;
        }
        character.setAttribute("facing", held_direction);
        character.setAttribute("walking", "true");
    } else {
        character.setAttribute("walking", "false");
    }

    let mapX = x;
    let mapY = y;


    // store previous node to know where its walls where
    prevTileX = currentTileX;
    prevTileY = currentTileY;

    // work out which tile in the spanning tree the player is in
    currentTileX = roundTileCoord((x / mazeScale) + 1);
    currentTileY = roundTileCoord((y / mazeScale) + 1);

    walls = maze.getWalls(currentTileX, currentTileY, prevTileX, prevTileY, walls)

    // debug
    console.log(y, x, currentTileY, currentTileX, walls)

    // get the coordinates of the tile and data from spanning tree
    let tileOriginX = (currentTileX - 1) * mazeScale;
    let tileOriginY = (currentTileY - 1) * mazeScale;

    // maze wall collisions
    // top, bottom, left, right

    // left
    if (x < tileOriginX + 1) {
        if (walls.left === 1) {
            x = originalX;
        } else if (walls.left === 0 && y < tileOriginY + 1) {
            // space for corner correction
            x = originalX;
        }
    }
    // right
    if (x > tileOriginX + 32) {
        if (walls.right === 1) {
            x = originalX;
        } else if (walls.right === 0 && y > tileOriginY + 41) {
            x = originalX;
        }
    }
    // top
    if (y < tileOriginY + 1) {
        if (walls.top === 1) {
            y = originalY;
        } else if (walls.top === 0 && x < tileOriginX + 1) {
            y = originalY;
        }
    }
    // bottom
    if (y > tileOriginY + 41) {
        if (walls.bottom === 1) {
            y = originalY;
        } else if (walls.bottom === 0 && x > tileOriginX + 32) {
            y = originalY;
        }
    }
    

    let imgWidth = (mapWidth * 128) - 64
    let imgHeight = (mapHeight * 128) - 64
    
    // smooth camera movement - moves the map against the player while the player is in the centre of the map
    if (mapX < 112) { mapX = 112; } // left
    if (mapX > imgWidth - 112) { mapX = imgWidth - 112; } // right
    if (mapY < 112) { mapY = 112; } // tops
    if (mapY > imgHeight - 112) { mapY = imgHeight - 112; } // bottom
    let camera_top = pixelSize * 112;
    let camera_left = pixelSize * 112;

    // moving the map and player
    map.style.transform = `translate3d( ${-mapX * pixelSize + camera_left}px, ${-mapY * pixelSize + camera_top}px, 0 )`;
    character.style.transform = `translate3d( ${x * pixelSize}px, ${y * pixelSize}px, 0 )`;


}

// steps through every frame
const step = function () {
    placeCharacter()
    window.requestAnimationFrame(function () {
        step()
    })
}
step()

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