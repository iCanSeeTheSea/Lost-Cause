
var myGamePiece;

function startGame() {
    myGameArea.start();
    myGamePiece = new component(10, 10, "red", 2, 2);
}

var myGameArea = {
    canvas : document.createElement("canvas"),
    start : function() {
<<<<<<< HEAD
        this.canvas.width = 500;
=======
        this.canvas.width = 480;
>>>>>>> 4d4efbe25e3dda38055ec8325c63ebc38ece0f91
        this.canvas.height = 500;
        this.context = this.canvas.getContext("2d");
        document.body.insertBefore(this.canvas, document.body.childNodes[0]);
        this.interval = setInterval(updateGameArea, 20);
        window.addEventListener('keydown', function (event) {
            myGameArea.keys = (myGameArea.keys || []);
            myGameArea.keys[event.keyCode] = true;
            console.log(event.keyCode)
            console.log(myGameArea.keys)
        })
        window.addEventListener('keyup', function (event) {
<<<<<<< HEAD
            myGameArea.keys[event.keyCode] = (event.type == "keydown");            
=======
            myGameArea.keys[event.keyCode] = false;            
>>>>>>> 4d4efbe25e3dda38055ec8325c63ebc38ece0f91
        })
    }, 
    clear : function(){
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
}

function component(width, height, color, x, y) {
    this.gamearea = myGameArea;
    this.width = width;
    this.height = height;
    this.speedX = 0;
    this.speedY = 0;    
    this.x = x;
    this.y = y;    
    this.update = function() {
        ctx = myGameArea.context;
        ctx.fillStyle = color;
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }
    this.newPos = function() {
        this.x += this.speedX;
        this.y += this.speedY;        
    }    
}

function updateGameArea() {
    myGameArea.clear();
    myGamePiece.speedX = 0;
    myGamePiece.speedY = 0;
<<<<<<< HEAD
    if (myGameArea.keys && myGameArea.keys[87] && !(myGamePiece.y <= 0)) {myGamePiece.speedY = -2; } // w
    if (myGameArea.keys && myGameArea.keys[65] && !(myGamePiece.x <= 0)) {myGamePiece.speedX = -2; } // a
    if (myGameArea.keys && myGameArea.keys[83] && !(myGamePiece.y >= myGameArea.canvas.height - 10)) {myGamePiece.speedY = 2; } // s
    if (myGameArea.keys && myGameArea.keys[68] && !(myGamePiece.x >= myGameArea.canvas.height - 10)) {myGamePiece.speedX = 2; } // d
=======
    if (myGameArea.keys && myGameArea.keys == 87) {myGamePiece.speedY = -1; } // w
    if (myGameArea.keys && myGameArea.keys == 65) {myGamePiece.speedX = -1; } // a
    if (myGameArea.keys && myGameArea.keys == 83) {myGamePiece.speedY = 1; } // s
    if (myGameArea.keys && myGameArea.keys == 68) {myGamePiece.speedX = 1; } // d
    console.log(myGamePiece.speedX, myGamePiece.speedY)
>>>>>>> 4d4efbe25e3dda38055ec8325c63ebc38ece0f91
    myGamePiece.newPos();
    myGamePiece.update();
}