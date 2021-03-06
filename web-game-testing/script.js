
var myGamePiece;
var myObstacles = [];
var myMaze = [];
var spanningTree = [];
myMaze.push(new component(15, 15, "red", 0, 0))
myMaze.push(new component(15, 15, "green", 585, 570))

const xhttp = new XMLHttpRequest();

xhttp.onload = function(){
    spanningTree = (xhttp.responseText).split("\r\n")
    for (i = 0; i < spanningTree.length; i++){
        spanningTree[i] = spanningTree[i].split(",")
    }
    for (i = 0; i < spanningTree.length; i++){
        for (n = 0; n<4; n++){
            spanningTree[i][n] = parseInt(spanningTree[i][n])
        }
    }
}
xhttp.open("GET", "spanning-tree.txt");
xhttp.send()



function startGame() {
    myGameArea.start();
    myGamePiece = new component(10, 10, "red", 2, 2);
    var x, y;
    for (i = 0; i < myObstacles.length; i ++) {
      if (myGamePiece.crashWith(myObstacles[i])) {
        myGameArea.stop();
        return;
      }
    }
    
    // obstacles
    x = 50;
    y = 0;
    //myObstacles.push(new component(50, 50, "black", x, y));
    for (i = 0; i < myObstacles.length; i ++) {
        myObstacles[i].update();
    }

    // maze
    for (i = 0; i < spanningTree.length; i++){
        coordSet = spanningTree[i];
        x = (coordSet[0]-1)*30;
        y = (coordSet[1]-1)*30;
        myMaze.push(new component(15, 15, "white", x, y));
        x = ((coordSet[2] - coordSet[0]) / 2 + coordSet[0])-1;
        y = ((coordSet[3] - coordSet[1]) / 2 + coordSet[1])-1;
        myMaze.push(new component(15, 15, "white", x*30, y*30));
    }
    for (m =0; m < myMaze.length; m ++){
        myMaze[m].update();
    }
}

var myGameArea = {
    canvas : document.createElement("canvas"),
    start : function() {
        this.canvas.width = 600;
        this.canvas.height = 600;
        this.context = this.canvas.getContext("2d");
        document.body.insertBefore(this.canvas, document.body.childNodes[0]);
        this.frameNo = 0;        
        this.interval = setInterval(updateGameArea, 20);
        window.addEventListener('keydown', function (event) {
            myGameArea.keys = (myGameArea.keys || []);
            myGameArea.keys[event.keyCode] = true;
        })
        window.addEventListener('keyup', function (event) {
            myGameArea.keys[event.keyCode] = (event.type == "keydown");            
        })
    }, 
    stop : function(){
        clearInterval(this.interval)
        console.log("stopped")
    }
}

function everyinterval(n){
    if ((myGameArea.frameNo/n)%1 == 0) {return true;}
    return false;
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
    this.crashWith = function(otherobj) {
        var myleft = this.x;
        var myright = this.x + (this.width);
        var mytop = this.y;
        var mybottom = this.y + (this.height);
        var otherleft = otherobj.x;
        var otherright = otherobj.x + (otherobj.width);
        var othertop = otherobj.y;
        var otherbottom = otherobj.y + (otherobj.height);
        var crash = true;
        if ((mybottom < othertop) ||
        (mytop > otherbottom) ||
        (myright < otherleft) ||
        (myleft > otherright)) {
          crash = false;
        }
        return crash;
    }    
}

function updateGameArea() {
    myGameArea.frameNo ++;
    myGamePiece.speedX = 0;
    myGamePiece.speedY = 0;
    if (myGameArea.keys && myGameArea.keys[87] && 
        !(myGamePiece.y <= 0)) {myGamePiece.speedY = -2; } // w
    if (myGameArea.keys && myGameArea.keys[65] && 
        !(myGamePiece.x <= 0)) {myGamePiece.speedX = -2; } // a
    if (myGameArea.keys && myGameArea.keys[83] && 
        !(myGamePiece.y >= myGameArea.canvas.height - 10)) {myGamePiece.speedY = 2; } // s
    if (myGameArea.keys && myGameArea.keys[68] && 
        !(myGamePiece.x >= myGameArea.canvas.height - 10)) {myGamePiece.speedX = 2; } // d
    myGamePiece.newPos();
    myGamePiece.update();
    if (myGamePiece.x >= 585 && myGamePiece.y >= 570 && myGamePiece.y <= 585){
        element = document.getElementById("wellDone");
        element.style.visibility = 'visible';
    } else {
        element = document.getElementById("wellDone");
        element.style.visibility = 'hidden'
    }
}