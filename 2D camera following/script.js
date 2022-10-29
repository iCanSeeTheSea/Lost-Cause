var character = document.querySelector(".character");
var map = document.querySelector(".map");

//start in the middle of the map
var x = 90;
var y = 34;
var heldDirections = []; //State of which arrow keys we are holding down
var speed = 1; //How fast the character moves in pixels per frame

const placeCharacter = () => {

   var pixelSize = parseInt(
      getComputedStyle(document.documentElement).getPropertyValue('--pixel-size')
   );

   const held_direction = heldDirections[0];
   console.log(heldDirections)
   console.log(held_direction)
   if (held_direction) {
      if (held_direction === directions.right) { x += speed; }
      if (held_direction === directions.left) { x -= speed; }
      if (held_direction === directions.down) { y += speed; }
      if (held_direction === directions.up) { y -= speed; }
      character.setAttribute("facing", held_direction);
      character.setAttribute("walking", held_direction ? "true" : "false");
   }
   // character.setAttribute("walking", held_direction ? "true" : "false");

   //Limits (gives the illusion of walls)
   var leftLimit = -8;
   var rightLimit = (16 * 11) + 8;
   var topLimit = -8 + 32;
   var bottomLimit = (16 * 7);
   if (x < leftLimit) { x = leftLimit; }
   if (x > rightLimit) { x = rightLimit; }
   if (y < topLimit) { y = topLimit; }
   if (y > bottomLimit) { y = bottomLimit; }


   var camera_left = pixelSize * 66;
   var camera_top = pixelSize * 42;

   map.style.transform = `translate3d( ${-x * pixelSize + camera_left}px, ${-y * pixelSize + camera_top}px, 0 )`;
   character.style.transform = `translate3d( ${x * pixelSize}px, ${y * pixelSize}px, 0 )`;
}


//Set up the game loop
const step = () => {
   placeCharacter();
   window.requestAnimationFrame(() => {
      step();
   })
}
step(); //kick off the first step!



/* Direction key state */
const directions = {
   up: "up",
   down: "down",
   left: "left",
   right: "right",
}
const keys = {
   38: directions.up,
   37: directions.left,
   39: directions.right,
   40: directions.down,
}
document.addEventListener("keydown", (e) => {
   var dir = keys[e.which];
   if (dir && heldDirections.indexOf(dir) === -1) {
      heldDirections.unshift(dir)
   }
})

document.addEventListener("keyup", (e) => {
   var dir = keys[e.which];
   var index = heldDirections.indexOf(dir);
   if (index > -1) {
      heldDirections.splice(index, 1)
   }
});
