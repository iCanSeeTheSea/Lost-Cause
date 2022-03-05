// debug
console.log(mazeHex)
console.log(mapSize)

// get the correct multiplier for the collisions depending on the size of the maze
var mapMulti = (mapSize * 32) / 4;
console.log(mapMulti)

var spanningTree = [];

// converting hex back into the spanning tree
var index = 0
for (let row = 1; row <= mapSize; row++ ){
    var rowList = []
    for (let column = 1; column <= mapSize; column++){

        // each hex character corresponds to one node of the maze
        hex = mazeHex[index]
        
        walls = {top: 1, bottom: 1, left: 1, right: 1}

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


var root = document.querySelector(':root');
root.style.setProperty('--map_multiplier', mapMulti);

// initial variable declarations
var held_directions = [];
var character = document.querySelector('.character');
var map = document.querySelector(".map");
var x = 16;
var y = 27;
var speed = 1;
var walls;

/*
20: 123
^ - 1
15: 124
^ - 2.5
10: 126.5
^ - 6.5
5: 133
3: 145
*/

// correct position? scaling? of player? walls?
// var posCorrectDict = { 20: 123, 15: 124, 10: 126.5, 5: 133, 3: 145 }
// var positionCorrector = posCorrectDict[mapSize];
// console.log(mapSize, positionCorrector)

var positionCorrector = 132

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

    // getting the pixel size being used from the css
    var pixelSize = parseInt(
        getComputedStyle(document.documentElement).getPropertyValue('--pixel-size')
    );

    var originalX = x;
    var originalY = y;

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


    
    // work out which tile in the spanning tree the player is in
    let currentTileX = roundTileCoord(((x) / positionCorrector) + 1);
    let currentTileY = roundTileCoord(((y) / positionCorrector) + 1);
    console.log(x, y, currentTileX, currentTileY)

    // debug
    //console.log(x, y, currentTileX, currentTileY, "[" + currentTileX.toString() + ", " + currentTileY.toString() + "]", spanningTree["[" + currentTileX.toString() + ", " + currentTileY.toString() + "]"]);


    // get the coordinates of the tile and data from spanning tree
    let tileOriginX = (currentTileX - 1) * positionCorrector;
    let tileOriginY = (currentTileY - 1) * positionCorrector;


    if (Math.floor(currentTileX) != currentTileX || Math.floor(currentTileY) != currentTileY){
        // store previous node to know where its walls where
    }
    

    if (spanningTree[currentTileX-1][currentTileY-1]) {
        walls = spanningTree[currentTileX-1][currentTileY-1]
    }


    //console.log(x, y,'|', currentTileX, currentTileY,'|', tileOriginX, tileOriginY, '|', walls);

    // if (x < 0) { x = 0; } // left
    // if (x > 16 * mapMulti - 32) { x = 16 * mapMulti - 32; } // right
    // if (y < 0) { y = 0; } // top
    // if (y > 16 * mapMulti - 24) { y = 16 * mapMulti - 24; } // bottom

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
        } else if (walls.right == 0 && y > tileOriginY + 37) {
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
    if (y > tileOriginY + 37) {
        if (walls.bottom == 1) {
            y = originalY;
        } else if (walls.bottom == 0 && x > tileOriginX + 32) {
            y = originalY;
        }
    }

    // smooth camera movement - moves the map against the player if the player is in the centre of the map
    if (mapX < 112) { mapX = 112; } // left
    if (mapX > (16 * mapMulti) - 112) { mapX = (16 * mapMulti) - 112; } // right
    if (mapY < 112) { mapY = 112; } // tops
    if (mapY > (16 * mapMulti) - 112) { mapY = (16 * mapMulti) - 112; } // bottom
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
}

const arrowKeys = {
    'ArrowUp': directions.up,
    'ArrowLeft': directions.left,
    'ArrowRight': directions.right,
    'ArrowDown': directions.down,
}

// event listeners for keys being pressed and released
document.addEventListener('keydown', function (e) {
    let dir = keys[e.key];
    if (dir && held_directions.indexOf(dir) === -1) {
        held_directions.unshift(dir);
    }
})

document.addEventListener('keyup', function (e) {
    let dir = keys[e.key];
    let index = held_directions.indexOf(dir);
    if (index > -1) {
        held_directions.splice(index, 1)
    }
})