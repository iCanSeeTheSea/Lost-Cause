
function displayMaze(spanningTree) {
    console.log(spanningTree)
}

let held_directions = [];
let character = document.querySelector('.character');
var map = document.querySelector(".map");
let x = 15;
let y = 15;
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
    let mapMulti = 10;

    if (charX < 0 + 5) { charX = 0 + 5; } // left
    if (charX > 15.5 * mapMulti - 5) { charX = 15.5 * mapMulti - 5; } // right
    if (charY < 0 + 5) { charY = 0 + 5; } // top
    if (charY > 15.5 * mapMulti - 5) { charY = 15.5 * mapMulti - 5; } // bottom

    if (mapX < 6.2 * mapMulti) { mapX = 6.2 * mapMulti; } // left
    if (mapX > 7.8 * mapMulti) { mapX = 7.8 * mapMulti; } // right
    if (mapY < 6.2 * mapMulti) { mapY = 6.2 * mapMulti; } // top
    if (mapY > 7.8 * mapMulti) { mapY = 7.8 * mapMulti; } // bottom
    var camera_top = pixelSize * mapMulti * 6.2;
    let camera_left = pixelSize * mapMulti * 6.2;
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