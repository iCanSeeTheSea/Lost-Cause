


var mapSize;
var spanningTree;
function getMazeData(spanning_tree, map_size) {
    mapSize = map_size;
    spanningTree = spanning_tree
}
console.log(spanningTree)
console.log(mapSize)
var mapMulti = (mapSize * 30) / 4;
console.log(mapMulti)


var held_directions = [];
var character = document.querySelector('.character');
var map = document.querySelector(".map");
var x = 21;
var y = 33;
var speed = 1;

const roundTileCoord = function(tileCoord) {
    if (tileCoord - Math.floor(tileCoord) > 0.5){
        tileCoord = Math.floor(tileCoord) + 0.5
    } else {
        tileCoord = Math.floor(tileCoord)
    }
    return tileCoord
}

const placeCharacter = function () {
    var pixelSize = parseInt(
        getComputedStyle(document.documentElement).getPropertyValue('--pixel-size')
    );
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
    mapMulti = 150;

    
    var currentTileX = ((x)/128)+1; 
    var currentTileY = ((y)/128)+1;

    var currentTile = [roundTileCoord(currentTileX), roundTileCoord(currentTileY)]
    console.log(x, y, currentTile);



    if (x < 0) { x = 0; } // left
    if (x > 16 * mapMulti - 32) { x = 16 * mapMulti - 32; } // right
    if (y < 0) { y = 0; } // top
    if (y > 16 * mapMulti - 24) { y = 16 * mapMulti - 24; } // bottom


    if (mapX < 112) { mapX = 112; } // left
    if (mapX > (16 * mapMulti) - 112) { mapX = (16 * mapMulti) - 112; } // right
    if (mapY < 112) { mapY = 112; } // tops
    if (mapY > (16 * mapMulti) - 112) { mapY = (16 * mapMulti) - 112; } // bottom
    let camera_top = pixelSize * 112;
    let camera_left = pixelSize * 112;
    map.style.transform = `translate3d( ${-mapX * pixelSize + camera_left}px, ${-mapY * pixelSize + camera_top}px, 0 )`;
    character.style.transform = `translate3d( ${x * pixelSize}px, ${y * pixelSize}px, 0 )`;


}

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