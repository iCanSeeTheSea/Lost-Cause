
function displayMaze(spanningTree) {
    console.log(spanningTree);
}

var mapSize;
function getMapSize(map_size) {
    mapSize = map_size;
}


let held_directions = [];
let character = document.querySelector('.character');
var map = document.querySelector(".map");
let x = 14;
let y = 14;
let speed = 1;

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
        character.setAttribute("walking", held_direction ? "true" : "false");
    }

    let charX = x;
    let charY = y;
    let mapX = x;
    let mapY = y;
    var mapMulti = 100;

    //! here, the mulitplier is 16x whatever the grid size is multiplied by in the css, -5
    if (charX < 0) { charX = 0; } // left
    if (charX > 16 * mapMulti - 5) { charX = 16 * mapMulti - 5; } // right
    if (charY < 0) { charY = 0; } // top
    if (charY > 16 * mapMulti - 5) { charY = 16 * mapMulti - 5; } // bottom

    if (mapX < 100) { mapX = 100; } // left
    if (mapX > (16 * mapMulti) - 100) { mapX = (16 * mapMulti) - 100; } // right
    if (mapY < 100) { mapY = 100; } // top
    if (mapY > (16 * mapMulti) - 100) { mapY = (16 * mapMulti) - 100; } // bottom
    var camera_top = pixelSize * 100;
    let camera_left = pixelSize * 100;
    map.style.transform = `translate3d( ${-mapX * pixelSize + camera_left}px, ${-mapY * pixelSize + camera_top}px, 0 )`;
    character.style.transform = `translate3d( ${charX * pixelSize}px, ${charY * pixelSize}px, 0 )`;

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