// debug
console.log(mazeHex)
console.log(mapWidth, mapHeight)


var spanningTree = [];

// converting hex back into the spanning tree
var index = 0
for (let row = 1; row <= mapWidth; row++) {
    var rowList = []
    for (let column = 1; column <= mapHeight; column++) {

        // each hex character corresponds to one node of the maze
        hex = mazeHex[index]

        walls = { top: 1, bottom: 1, left: 1, right: 1 }

        // converting hex to binary, nibble will represent the walls of the node
        bin = (parseInt(hex, 16).toString(2)).padStart(4, '0')
        walls.top = parseInt(bin[0])
        walls.bottom = parseInt(bin[1])
        walls.left = parseInt(bin[2])
        walls.right = parseInt(bin[3])

        rowList.push(walls)

        index += 1
    }
    spanningTree.push(rowList)
}

console.log(spanningTree)

// setting css properties to correct values
var root = document.querySelector(':root');
root.style.setProperty('--map-width', mapWidth); 
root.style.setProperty('--map-height', mapHeight); 


// initial variable declarations
var held_directions = [];
var character = document.querySelector('.character');
var map = document.querySelector(".map");
var x = 16;
var y = 27;
var currentTileX = 1
var currentTileY = 1
var speed = 1;
var walls = spanningTree[currentTileX - 1][currentTileY - 1];

// function to round a number to the nearest 0.5
const roundTileCoord = function (tileCoord) {
    if (tileCoord - Math.floor(tileCoord) > 0.5) {
        tileCoord = Math.floor(tileCoord) + 0.5
    } else {
        tileCoord = Math.floor(tileCoord)
    }
    return tileCoord
}

// deterimes where the character (and maze) is positioned every frame
const placeCharacter = function () {

    // getting the pixel size being used from the css - varies depending on how large the browser window is
    let pixelSize = parseInt(
        getComputedStyle(document.documentElement).getPropertyValue('--pixel-size')
    );

    let positionCorrector = 128

    // storing position from previous frame in case new position is blocked 
    let originalX = x;
    let originalY = y;

    // work out which direction the user wants to move the player
    const held_direction = held_directions[0];
    if (held_direction) {
        if (held_direction === directions.right) { x += speed; }
        if (held_direction === directions.left) { x -= speed; }
        if (held_direction === directions.down) { y += speed; }
        if (held_direction === directions.up) { y -= speed; }
        character.setAttribute("facing", held_direction);
        character.setAttribute("walking", "true");
    } else {
        character.setAttribute("walking", "false");
    }

    let mapX = x;
    let mapY = y;


    // store previous node to know where its walls where
    let prevTileX = currentTileX;
    let prevTileY = currentTileY;

    // work out which tile in the spanning tree the player is in
    currentTileX = roundTileCoord((x / positionCorrector) + 1);
    currentTileY = roundTileCoord((y / positionCorrector) + 1);


    // if the next node is going to be between two nodes
    if (Math.floor(currentTileX) != currentTileX && prevTileX != currentTileX) {
        walls = { top: 1, bottom: 1, left: 0, right: 0 }

    } else if (Math.floor(currentTileY) != currentTileY && prevTileY != currentTileY) {
        walls = { top: 0, bottom: 0, left: 1, right: 1 }

    } else if (prevTileX != currentTileX || prevTileY != currentTileY) {
        walls = spanningTree[currentTileX - 1][currentTileY - 1]
    }
    // debug
    console.log(x, y, currentTileX, currentTileY)

    // get the coordinates of the tile and data from spanning tree
    let tileOriginX = (currentTileX - 1) * positionCorrector;
    let tileOriginY = (currentTileY - 1) * positionCorrector;

    // maze wall collisions
    // top, bottom, left, right

    // left
    if (x < tileOriginX + 1) {
        if (walls.left == 1) {
            x = originalX;
        } else if (walls.left == 0 && y < tileOriginY + 1) {
            // space for corner correction
            x = originalX;
        }
    }
    // right
    if (x > tileOriginX + 32) {
        if (walls.right == 1) {
            x = originalX;
        } else if (walls.right == 0 && y > tileOriginY + 41) {
            x = originalX;
        }
    }
    // top
    if (y < tileOriginY + 1) {
        if (walls.top == 1) {
            y = originalY;
        } else if (walls.top == 0 && x < tileOriginX + 1) {
            y = originalY;
        }
    }
    // bottom
    if (y > tileOriginY + 41) {
        if (walls.bottom == 1) {
            y = originalY;
        } else if (walls.bottom == 0 && x > tileOriginX + 32) {
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