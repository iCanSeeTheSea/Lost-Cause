// debug
console.log(mazeSeed);
const mazeScale = 128;
let pixelSize = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--pixel-size'));

// mapping keys to movement directions
const directions = {
    up: "up",
    down: "down",
    left: "left",
    right: "right"
}

const directionKeys = {
    'w': directions.up,
    'a': directions.left,
    'd': directions.right,
    's': directions.down,
    'ArrowUp': directions.up,
    'ArrowLeft': directions.left,
    'ArrowRight': directions.right,
    'ArrowDown': directions.down,
    'W': directions.up,
    'A': directions.left,
    'S': directions.down,
    'D': directions.right
}

// mapping keys to inventory slots
const inventoryKeys = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5
}

// mapping keys to commands
const commands = {
    'e': 'interact',
    'E': 'interact',
    'q': 'drop',
    'Q': 'drop',
    'r': 'attack',
    'R': 'attack'
}

// base 64 to binary conversion table
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


/*  A class that holds a list of objects of the same type */
class ObjectGroup{
    /**
     * The constructor function takes an objectType as an argument and sets the objectType property of the object to the
     * objectType argument. It also sets the objectList property of the object to an empty array
     * @param objectType - This is the type of object that the list will contain.
     */
    constructor(objectType) {
        this.objectType = objectType;
        this.objectList = [];
    }

    /**
     * This function returns the object at the specified index in the objectList array
     * @param index - The index of the object you want to get.
     * @returns The object at the index of the objectList array.
     */
    get(index){
        return this.objectList[index];
    }

    /**
     *  Adds an object to the object list and returns a reference to it
     * @param object - The object to be added to the group.
     * @returns A reference to the object that was just added to the object list.
     */
    push(object){
        this.objectList.push(object);
        return new ObjectGroupReference(object.type, this.objectList.length-1, this);
    }
}


/* A reference to an object in an object group */
class ObjectGroupReference{
    /**
     * This function is a constructor for the object type "ObjectPropertiesSection"
     * @param objectType - The type of the object.
     * @param index - The index of the object in the object group.
     * @param objectGroup - The name of the object group that the object belongs to.
     */
    constructor(objectType, index, objectGroup) {
        this.objectType = objectType;
        this._index = index;
        this._objectGroup = objectGroup;
    }

    /**
     * It returns the object at the current index.
     * @returns The object at the current index.
     */
    getSelf(){
        return this._objectGroup.get(this._index);
    }
}


/* It's a class that represents an item in the game */
class Item{
    /**
     * It creates a new item entity with the type and id of the item
     * @param type - The type of the item.
     * @param id - The id of the item.
     */
    constructor(type, id) {
        this.type = type;
        this.entity = new ItemEntity(0, 0);
        this.id = id;
        this.entity.self.id = type;
    }

    /**
     * The function place() takes two arguments, y and x, and moves the entity to the y and x coordinates
     * @param y - The y coordinate of the tile to move to.
     * @param x - The x coordinate of the tile to move to.
     */
    place(y, x){
        this.entity.move(y, x);
    }

    /**
     * When the player picks up the item, the item is removed from the game.
     */
    take(){
        this.entity.remove();
    }

    /**
     * The update function is called every frame and updates the position of the entity
     */
    update(){
        this.entity.updatePosition();
    }
}


/* The Lock class is a subclass of the Item class, and it has a locked property that is set to true by default. */
class Lock extends Item{
    /**
     * The constructor function calls the constructor of the parent to store thr type and create an ItemEntity
     */
    constructor() {
        super('lock')
        this.locked = true;
    }

    /**
     * When the user opens the lock, the lock disappears.
     */
    unlock(){
        this.locked = false;
        this.entity.self.outerHTML = "";
    }
}


/* It's a dictionary that stores nodes, and it also stores the keys in a list */
class NodeList{
    /**
     * The constructor function creates a new object, and sets the object's dict property to an empty object, and sets the
     * object's _keys property to an empty array.
     */
    constructor() {
        this.dict = {};
        this._positions = [];
    }

    /**
     * It takes a position object and returns a string that represents the position
     * @param position - The position of the tile.
     * @returns A string that is the key for the position object.
     */
    getKeyFromPos(position){
        return 'y' + String(position.y) + 'x' + String(position.x);
    }

    /**
     * It pushes a node into the grid.
     * @param node - The node to be added to the open list.
     */
    push(node){
        let position = node.position();
        this.dict[this.getKeyFromPos(position)] = node;
        this._positions.unshift(node.position());
    }

    /**
     * If there are keys in the dictionary, remove the first key from the list of keys, delete the key from the dictionary,
     * and return the position of the key
     * @returns The position of the first element in the array.
     */
    pop(){
        if (this._positions){
            let position = this._positions.shift();
            let key = this.getKeyFromPos(position);
            delete this.dict[key];
            return position;
        } else {
            return undefined;
        }
    }

    /**
     * It deletes the position from the dictionary and the list of positions
     * @param position - The position of the object to be deleted.
     * @returns The value of the key at the position in the array.
     */
    delete(position){
        let key = this.getKeyFromPos(position);
        delete this.dict[key];
        this._positions = this._positions.filter(function(e) { return e !== position});
    }

    /**
     * It checks if the position is in the dictionary.
     * @param position - The position of the tile you want to check.
     * @returns A boolean value.
     */
    contains(position){
        let key = this.getKeyFromPos(position)
        return key in this.dict;
    }

    /**
     * If the position is in the maze, return the node at that position
     * @param position - The position of the node you want to get.
     * @returns The node at the given position.
     */
    getNode(position){
        if (this.contains(position)){
            return this.dict[this.getKeyFromPos(position)]
        }
        return undefined
    }

}


/* A Node is a square that has a position and walls */
class Node{
    /**
     * The constructor function creates a node object with the given x and y coordinates, and the given walls
     * @param y - The y coordinate of the node
     * @param x - The x coordinate of the node
     * @param walls - an object with the following properties:
     */
    constructor(y, x, walls) {
        this.type = 'node'
        this.x = x;
        this.y = y;
        this.top = walls.top;
        this.bottom = walls.bottom;
        this.left = walls.left;
        this.right = walls.right;
        this.contains = undefined;
    }

    /**
     * It returns an object with the properties y and x, which are set to the values of this.y and this.x
     * @returns The object {y: this.y, x: this.x} is being returned.
     */
    position(){
        return {y: this.y, x: this.x};
    }
}


/* A horizontal edge is a node with walls on the top and bottom, but not on the left or right. */
class HorizontalEdge extends Node{
    /**
     * The constructor function for the Edge class takes two arguments, y and x, and sets the wall properties to
     * pre-determined values
     * @param y - The y coordinate of the cell
     * @param x - The x coordinate of the cell
     */
    constructor(y, x) {
        let walls = { top: 1, bottom: 1, left: 0, right: 0 };
        super(y, x, walls);
        this.type = 'edge';
    }
}


/* VerticalEdge is a Node with a left and right wall. */
class VerticalEdge extends Node{
    /**
     * The constructor function for the Edge class takes two arguments, y and x, and sets the wall properties to
     * pre-determined values
     * @param y - The y coordinate of the cell
     * @param x - The x coordinate of the cell
     */
    constructor(y, x) {
        let walls = { top: 0, bottom: 0, left: 1, right: 1 };
        super(y, x, walls);
        this.type = 'edge';
    }
}


/* A 2D array of tiles */
class Maze {

    /**
     * It takes a base64 string, converts it to binary, and then uses the first 16 bits to determine the height and width
     * of the maze
     * @param seed - the seed string that is used to generate the maze
     */
    constructor(seed) {
        this.seed = seed;
        this._usedEdges = {};
        this.nodes = new NodeList();

        // separating dimensions from seed and converting to binary
        let base64String = this.seed.replace(/=/g, '');
        let binaryString = '';
        for (let i = 0; i < base64String.length; i++){
            binaryString += toBinary[base64String[i]];
        }
        let padding = (this.seed.length - base64String.length)*8;
        this.height = parseInt(binaryString.slice(0,8), 2);
        this.width = parseInt(binaryString.slice(8,16), 2);
        this.binaryString = binaryString.slice(16, binaryString.length - padding);
        console.log(binaryString,this.height, this.width);
    }


    /**
     * If the coordinates are in the maze, or are within the bounds of the maze and are a valid edge, returns true
     * if the coordinates are outside the bounds of the maze, or are not a valid edge, returns false
     * @param y - the y coordinate of the tile
     * @param x - the x coordinate of the tile
     * @returns A boolean value.
     */
    checkTileInMaze(y, x) {
        if (this.nodes.contains({y: y, x: x})) {
            return true;
        } else if ((1 > x || x > this.width) || (1 > y || y > this.height)){
            // if the coordinates are outside the maze
            return false;
        } else if (y % 1 !== 0 && x % 1 === 0){
            let adjTile = this.nodes.getNode({y: Math.floor(y), x: x});
            if (adjTile.bottom === 0){
                // if the y coordinate .5, and the tile above has no bottom wall
                return true;
            }
        } else if (x % 1 !== 0 && y % 1 === 0){
            let adjTile = this.nodes.getNode({ y: y, x: Math.floor(x)});
            if (adjTile.right === 0){
                // if the x coordinate is .5 and the tile to the left has no right wall
                return true;
            }
        }
        return false;
    }

    /**
     * If the tile is an edge, and it doesn't contain a piece, then delete it from the used edges object. Otherwise, add it
     * to the used edges object
     * @param tile - the tile object that is being checked
     */
    checkUsedEdge(tile){
        if (tile.type === 'edge'){
            if (tile.contains === undefined){
                // concatenate y and x values to create a unique key for any edge
                delete this._usedEdges[String(tile.y)+String(tile.x)];
            } else {
                this._usedEdges[String(tile.y)+String(tile.x)] = tile;
            }
        }
    }

    /**
     * If the tile is in the maze, return the node at that location. If the tile is not in the maze, return false
     * @param y - The y coordinate of the node you want to get.
     * @param x - The x coordinate of the node you want to get.
     * @returns A node or edge object.
     */
    getTile(y, x){
        if (this.checkTileInMaze(y, x)) {
            if (x % 1 === 0 && y % 1 === 0){
                return this.nodes.getNode({y: y, x: x});
            } else {
                let edgeUsed = this._usedEdges[String(y)+String(x)];
                if (edgeUsed !== undefined){
                    return edgeUsed;
                } else {
                    if (x % 1 !== 0) {
                        return new HorizontalEdge(y, x);
                    } else if (y % 1 !== 0) {
                        return new VerticalEdge(y, x);
                    }
                }
            }
        }
        return false;
    }

    /**
     * The output function will print out the adjacency list to the console
     */
    output(){
        console.log(this.nodes);
    }
}


/* It's a class that represents an entity in the game */
class Entity {
    /**
     * The constructor function is used to create a new object with the properties of the class
     * @param x - The x coordinate of the entity.
     * @param y - The y coordinate of the entity
     */
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this._speed = 0;
        this._prevTile = {y: 0, x:0};
        this._currentTile = {y: 0, x:0};
        this._tileOrigin = {y: 0, x:0};
        this.moveDirections = [];
        this._attackCooldown = 0;
        this._attackDamage = 0;
    }

    /**
     * If the decimal portion of the tile coordinate is greater than 0.5, round down to the nearest half-tile. Otherwise,
     * round down to the nearest tile
     * @param tileCoord - The tile coordinate to round.
     * @returns The rounded tile coordinate.
     */
    roundTileCoord(tileCoord) {
        if (tileCoord - Math.floor(tileCoord) > 0.5) {
            tileCoord = Math.floor(tileCoord) + 0.5;
        } else {
            tileCoord = Math.floor(tileCoord);
        }
        return tileCoord;
    }

    /**
     * The function determines the current tile the entity is in by rounding the entity's x and y coordinates to the
     * nearest tile
     */
    determineCurrentTile(){
        // store previous node to know where its walls where
        this._prevTile.x = this._currentTile.x;
        this._prevTile.y = this._currentTile.y

        // work out which tile in the spanning tree the entity is in
        let x = this.roundTileCoord((this.x / mazeScale) + 1);
        let y = this.roundTileCoord((this.y / mazeScale) + 1);

        this._currentTile = game.maze.getTile(y, x);
        this.determineTileOrigin();
    }

    /**
     * This function determines the origin of the tile that the entity is currently on
     */
    determineTileOrigin(){
        // get the coordinates of the tile and data from spanning tree
        this._tileOrigin.x = (this._currentTile.x - 1) * mazeScale;
        this._tileOrigin.y = (this._currentTile.y - 1) * mazeScale;
    }

    /**
     * If the entity is within the bounds of a tile, check if the entity is colliding with a wall. If so, move the entity
     * back to their original position
     * @param originalX - the original x position of the entity before the move
     * @param originalY - the original y position of the entity before the move
     */
    checkCollision(originalX, originalY) {
        // maze wall collisions
        // top, bottom, left, right

        this.determineCurrentTile();

        // left
        if (this.x < this._tileOrigin.x + 3) {
            if (this._currentTile.left === 1) {
                this.x = originalX;
            } else if (this._currentTile.left === 0 && (this.y > this._tileOrigin.y + 46 || this.y < this._tileOrigin.y + 5)) {
                // corner correction
                this.y = originalY;
            }
        }
        // right
        if (this.x > this._tileOrigin.x + 45) {
            if (this._currentTile.right === 1) {
                this.x = originalX;
            } else if (this._currentTile.right === 0 && (this.y > this._tileOrigin.y + 46 || this.y < this._tileOrigin.y + 5)) {
                this.y = originalY;
            }
        }
        // top
        if (this.y < this._tileOrigin.y + 5) {
            if (this._currentTile.top === 1) {
                this.y = originalY;
            } else if (this._currentTile.top === 0 && (this.x < this._tileOrigin.x + 3|| this.x > this._tileOrigin.x + 45)) {
                this.x = originalX;
            }
        }
        // bottom
        if (this.y > this._tileOrigin.y + 46) {
            if (this._currentTile.bottom === 1) {
                this.y = originalY;
            } else if (this._currentTile.bottom === 0 && (this.x < this._tileOrigin.x + 3|| this.x > this._tileOrigin.x + 45)) {
                this.x = originalX;
            }
        }
    }

    /**
     * If the entity is moving, check if the new position is blocked, and if not, move the entity to the new position
     */
    move() {
        if (this.moveDirections.length > 0){

            
            // storing position from previous frame in case new position is blocked
            let originalX = this.x;
            let originalY = this.y;


            this.determineCurrentTile();

            for (let i = 0; i < this.moveDirections.length; i++) {
                switch (this.moveDirections[i]) {
                    case directions.right:
                        this.x += this._speed;
                        break;
                    case directions.left:
                        this.x -= this._speed;
                        break;
                    case directions.down:
                        this.y += this._speed;
                        break;
                    case directions.up:
                        this.y -= this._speed;
                        break;
                }
            }

            this.checkCollision(originalX, originalY);
            // animations change based on HTML attributes
            this.self.setAttribute("facing", this.moveDirections[0]);
            this.self.setAttribute("walking", "true");

        } else {
            this.self.setAttribute("walking", "false");
        }
    }

    /**
     * This function returns the current tile
     * @returns The current tile that the entity is on.
     */
    getCurrentTile(){
        return this._currentTile;
    }

    /**
     * If the entity is not currently attacking, set the attacking attribute to true, set the facing attribute to the
     * direction of the target, damage the target, and set the attacking attribute to false after the attack cooldown.
     * @param target - The target to attack.
     */
    attack(target){
        if (this.self.getAttribute("attacking") !== "true"){
            this.self.setAttribute("attacking", "true");
            if (target.x <= this.x){
                this.self.setAttribute("facing", "left");
            } else if (target.x > this.x) {
                this.self.setAttribute("facing", "right");
            }
            target.damage(this._attackDamage)
            window.setTimeout(function (self){
                self.setAttribute("attacking", "false");
            }, this._attackCooldown, this.self);
        }
    }
}


/* It's a class that represents an item in the game */
class ItemEntity extends Entity{
    /**
     * The constructor function sets the object's x and y coordinates, determines
     * the current tile, and creates a div element for the object
     */
    constructor() {
        super(20, 28);
        this.determineCurrentTile();
        this.self = document.createElement("div");
        this.self.className = "item";
    }

    /**
     * It takes the entity's x and y coordinates, and determines which tile in the spanning tree the entity is in
     * @param y - the y coordinate of the entity
     * @param x - the x coordinate of the entity
     */
    determineCurrentTile(y, x){
        // work out which tile in the spanning tree the entity is in
        let tileX = this.roundTileCoord((x / mazeScale) + 1);
        let tileY = this.roundTileCoord((y / mazeScale) + 1);

        this.determineTileOrigin(tileY, tileX);
    }

    /**
     * "Given a tile's coordinates, determine the coordinates of the tile's origin."
     *
     * @param tileY - the y coordinate of the tile
     * @param tileX - the x coordinate of the tile
     */
    determineTileOrigin(tileY, tileX){
        // get the coordinates of the tile and data from spanning tree
        this._tileOrigin.x = (tileX - 1) * mazeScale;
        this._tileOrigin.y = (tileY - 1) * mazeScale;
    }

    /**
     * > The function places the object on the map
     */
    place(){
        this.y = this._tileOrigin.y+32;
        this.x = this._tileOrigin.x+24;
        game.map.appendChild(this.self);
        this.updatePosition();
    }

    /**
     * The function determines the tile's origin and then places the tile
     * @param tileY - The y coordinate of the tile you want to spawn on.
     * @param tileX - The x coordinate of the tile you want to spawn on.
     */
    spawn(tileY, tileX){
        this.determineTileOrigin(tileY, tileX);
        this.place();
    }

    /**
     * The function move() takes in two parameters, y and x, and then determines the current tile,
     * and then calls the function place().
     * @param y - the y coordinate of the tile you want to move to
     * @param x - The x coordinate of the tile you want to move to.
     */
    move(y, x){
        this.determineCurrentTile(y, x);
        this.place();
    }

    /**
     * This function updates the position of the item on the screen.
     */
    updatePosition(){
        this.self.style.transform = `translate3d( ${this.x * pixelSize}px, ${this.y * pixelSize}px, 0 )`;
    }


    /**
     * Remove the element from the DOM.
     */
    remove(){
        this.self.outerHTML = "";
    }
}


/* It's a class that represents an enemy in the game */
class Enemy extends Entity {
    /**
     * The constructor function is used to create a new enemy object
     * @param id - The id of the enemy.
     */
    constructor(id) {
        super(27, 16);
        this.id = id;
        this._speed = 7/8;
        this._range = 3;
        this._maxHealth = 10;
        this._health = this._maxHealth;
        this._attackCooldown = 1000;
        this._attackDamage = 1;
        this._path = [];
        this._target = {y: -1, x: -1};
        this._targetTile = {};
        this.self = document.createElement("div");
        this.self.className = "enemy";
        this.self.id = `enemy-${this.id}`;
    }

    /**
     * The spawn function is called when the enemy is created, and it sets the enemy's position on the map, and creates the
     * enemy's health bar
     * @param tileY - The y coordinate of the tile you want the enemy to spawn on.
     * @param tileX - The x coordinate of the tile you want the enemy to spawn on.
     */
    spawn(tileY, tileX){
        this.self.setAttribute("attacking", "false")

        this.x = (tileX -1) * mazeScale + 20;
        this.y = (tileY -1) * mazeScale + 40;
        this._currentTile = {y: tileY, x: tileX};
        game.map.appendChild(this.self)

        let spriteSheet = document.createElement("div");
        spriteSheet.className = "enemy-spritesheet";
        this.self.appendChild(spriteSheet);

        this.self.style.transform = `translate3d( ${this.x * pixelSize}px, ${this.y * pixelSize}px, 0 )`;
        this.healhBar = new HealthBar(this.self.id, this._maxHealth);
    }

    /**
     * The function takes in a number, subtracts that number from the enemy's health, and if the enemy's health is less
     * than or equal to 0, it removes the enemy from the game
     * @param damageTaken - The amount of damage the enemy takes.
     */
    damage(damageTaken){
        this._health -= damageTaken
        if (this._health <= 0){
            this._health = 0;
            this.self.outerHTML = "";
            game.player.enemiesKilled += 1;
            for (let index = 0; index < game.enemyGroup.objectList.length; index++){
                let enemy = game.enemyGroup.objectList[index];
                if (enemy.id === this.id){
                    console.log(enemy, game.enemyGroup.objectList);
                    game.enemyGroup.objectList.splice(index, 1);
                    break;
                }
            }
        }
        this.healhBar.update(this._health);
    }

    /**
     * The enemy finds a path to the player by checking the tiles around it and moving in the direction of the player
     */
    pathFind(){
        //console.log(this.targetTile)
        let targetPosition = this._targetTile.position();
        if (this._path.length > 0 || (targetPosition.y === this._currentTile.y && targetPosition.x === this._currentTile.x)){
            return;
        }
        let min = {y: this._currentTile.y - this._range/2, x: this._currentTile.x - this._range/2};
        let max = {y: this._currentTile.y + this._range/2, x: this._currentTile.x + this._range/2};

        // enemy should only find a path if the target is within its range
        if (min.y <= this._targetTile.y && this._targetTile.y <= max.y && min.x <= this._targetTile.x && this._targetTile.x <= max.x){

            let nodesInRange = new NodeList();
            //console.log('search start', this.currentTile, this.targetTile.position());

            for (let row = min.y; row <= max.y; row += 0.5){
                for (let column = min.x; column <= max.x; column += 0.5){
                    let node = game.maze.getTile(row, column);
                    if (node){
                        nodesInRange.push(node);
                    }
                }
            }
            // recursive backtracking starts at target for better efficiency
            // * explain in design
            let checkTile = this._targetTile;
            let checkPosition = checkTile.position();
            let visitedNodes = new NodeList();

            while(true){
                if (checkPosition.y === this._currentTile.y && checkPosition.x === this._currentTile.x){
                    // has found player
                    //console.log('player found', this.path)
                    break;
                }

                // ensures a node is not checked twice
                nodesInRange.delete(checkPosition);
                let nextPosition = checkPosition;
                let direction = "";

                // if the player is in an adjacent tile, the correct direction is known
                if (nextPosition.x === this._currentTile.x && nextPosition.y + 0.5 === this._currentTile.y){
                    nextPosition.y += 0.5;
                    direction = "up";

                } else if (nextPosition.x === this._currentTile.x && nextPosition.y - 0.5 === this._currentTile.y){
                    nextPosition.y -= 0.5;
                    direction = "down";

                } else if (nextPosition.y === this._currentTile.y && nextPosition.x - 0.5 === this._currentTile.x){
                    nextPosition.x -= 0.5;
                    direction = "right";

                } else if (nextPosition.y === this._currentTile.y && nextPosition.x + 0.5 === this._currentTile.x){
                    nextPosition.x += 0.5;
                    direction = "left";

                // when the player is not in an adjacent tile, tiles are checked using recursive backtracking
                } else if (checkTile.top === 0 && nodesInRange.contains({y: nextPosition.y - 0.5, x: nextPosition.x})){
                    nextPosition.y -= 0.5;
                    direction = "down";

                } else if (checkTile.bottom === 0 && nodesInRange.contains({y: nextPosition.y + 0.5, x: nextPosition.x})){
                    nextPosition.y += 0.5;
                    direction = "up";

                } else if (checkTile.left === 0 && nodesInRange.contains({y: nextPosition.y, x: nextPosition.x - 0.5})){
                    nextPosition.x -= 0.5;
                    direction = "right";

                } else if (checkTile.right === 0 && nodesInRange.contains({y: nextPosition.y, x: nextPosition.x + 0.5})){
                    nextPosition.x += 0.5;
                    direction = "left";

                } else {
                    // can't find player
                    if (this._path.length !== 0) {
                        this._path.shift();
                        checkPosition = visitedNodes.pop();
                    } else {
                        break;
                    }
                }
                if (nodesInRange.contains(nextPosition)){
                    this._path.unshift(direction);
                    visitedNodes.push(checkTile);
                    checkPosition = nextPosition;
                    checkTile = nodesInRange.dict[nodesInRange.getKeyFromPos(checkPosition)];
                }
            }
        }
    }

    /**
     * If the player is on the same tile as the enemy, move towards the player. If the player is not on the same tile as
     * the enemy, move towards the next tile in the path
     */
    move(){
        this.determineTileOrigin();
        this._targetTile = game.player.getCurrentTile();

        if (this._targetTile.x === this._currentTile.x && this._targetTile.y === this._currentTile.y) {
            // set player as target
            this._target.x = game.player.x;
            this._target.y = game.player.y;

        } else {
            this.pathFind();
        }

        if (this._target.x !== -1 && this._target.y !== -1) {
            // move towards target
            this.moveDirections = [];
            if (this.x - 2 > this._target.x) {
                this.moveDirections.push(directions.left);
            } else if (this.x + 2 < this._target.x) {
                this.moveDirections.push(directions.right);
            }
            if (this.y - 2 > this._target.y) {
                this.moveDirections.push(directions.up);
            } else if (this.y + 2 < this._target.y) {
                this.moveDirections.push(directions.down);
            }
            if (this.moveDirections.length > 0) {
                super.move();
            } else {
                this._target.x = this._target.y = -1;
                this._path.shift();
            }
        }
        if (this._path.length > 0 && this._target.x === -1 && this._target.y === -1){
            // move to next tile
            this.moveDirections = [];
            this.moveDirections.push(this._path[0]);
            super.move();
            if (this._currentTile.x !== this._prevTile.x || this._currentTile.y !== this._prevTile.y) {
                this._target = {y: this._tileOrigin.y + 25, x: this._tileOrigin.x + 25};
            }
        }
        this.self.style.transform = `translate3d( ${this.x * pixelSize}px, ${this.y * pixelSize}px, 0 )`;
    }

    /**
     * If the distance between the player and the enemy is less than 5, then the enemy will attack the player
     */
    attack(){
        let distance = Math.sqrt(Math.abs(this.x - game.player.x) **2 + Math.abs(this.y  - game.player.y )**2);
        if (distance < 5) {
            super.attack(game.player);
        }
    }
}


/* It's a class that represents the Player in the game */
class Player extends Entity {
    /**
     * The constructor function is used to set the character's starting position, health, speed, attack damage, and attack
     * cooldown
     */
    constructor() {
        super(27, 16);
        this._prevTile = {y:0, x:0};
        this._maxHealth = game.maze.height * game.maze.width;
        this._health = this._maxHealth;
        this._currentTile = game.maze.getTile(1, 1);
        this._speed = 1;
        this._attackCooldown = 200;
        this._attackDamage = 5;
        this.inventory = new Inventory();
        this.self = document.querySelector('.character');
        this._healthBar = new HealthBar('character-1', this._maxHealth);
        this.enemiesKilled = 0;
        this.locksOpened = 0;
        }

    /**
     * The function takes a command as a parameter, and then executes the command
     * @param command - The command to execute.
     */
    executeCommand(command){
        switch (command){
            case 'interact':
                this.interact();
                break;
            case 'drop':
                this.drop();
                break;
            case 'attack':
                this.attack();
                break;
        }
    }

    /**
     * If the player is standing on a tile that contains an object, and that object is a lock, then if the player has a key
     * in their inventory, the lock is unlocked, the key is removed from the inventory, and the lock is removed from the
     * tile. If the player is standing on a tile that contains an object, and that object is not a lock, and there is
     * space in the player's inventory, then the object is added to the player's inventory, and the object is removed
     * from the tile
     */
    interact(){
        if (this._currentTile.contains !== undefined){
            if (this._currentTile.contains.objectType === 'lock'){
                let lock = this._currentTile.contains.getSelf();
                let itemReference = this.inventory.getItemFromSlot(game.activeInventorySlot);
                if (itemReference.objectType === 'key'){
                    lock.unlock();
                    this._currentTile.contains = undefined;
                    this.inventory.removeItem(game.activeInventorySlot);
                    this.locksOpened += 1;
                    game.checkWinCondition();
                }
            } else {
                let itemReference = this._currentTile.contains;
                if (this.inventory.checkSlotsAvailable()){
                    this.inventory.insertItem(itemReference, game.activeInventorySlot);
                    this._currentTile.contains.getSelf().take()
                    this._currentTile.contains = undefined;
                    game.maze.checkUsedEdge(this._currentTile);
                }
            }
        }
    }

    /**
     * If the player is holding a sword, find the closest enemy and attack it
     */
    attack(){
        if (this.inventory.getItemFromSlot(game.activeInventorySlot).objectType === 'sword'){
            let closestEnemy = game.enemyGroup.objectList[0];
            let closestDistance = 10;
            let enemyInRange = false;
            for (const enemy of game.enemyGroup.objectList) {
                let targetTile = enemy.getCurrentTile()
                if (targetTile.x === this._currentTile.x && targetTile.y === this._currentTile.y) {
                    let distance = Math.sqrt(Math.abs(this.x - enemy.x) **2 + Math.abs(this.y  - enemy.y )**2);
                    if (distance < closestDistance){
                        closestDistance = distance;
                        closestEnemy = enemy;
                        enemyInRange = true;
                    }
                }
            }
            if (enemyInRange) {
                super.attack(closestEnemy);
            }
        }
    }

    /**
     * If the player is holding an item and the tile they're on doesn't already have an item on it, then drop the item on
     * the tile
     */
    drop(){
        if (this.inventory.getItemFromSlot(game.activeInventorySlot) !== undefined && this._currentTile.contains === undefined){
            this._currentTile.contains = this.inventory.removeItem(game.activeInventorySlot);
            this._currentTile.contains.getSelf().place(this.y, this.x);
            game.maze.checkUsedEdge(this._currentTile);
        }
    }

    /**
     * The damage function takes in a number and subtracts it from the player's health. If the player's health is less than
     * or equal to zero, the player's health is set to zero and the game ends
     * @param damageTaken - The amount of damage the player takes.
     */
    damage(damageTaken){
        this._health -= damageTaken;
        if (this._health <= 0){
            this._health = 0;
            game.gameEnd(false);
        }
        this._healthBar.update(this._health);
    }

    /**
     * The player moves, and the map moves with the player - the player is always in the centre of the camera, unless
     * the player reaches the edge of the map
     */
    move(){
        let mapX = this.x;
        let mapY = this.y;

        this.moveDirections = game.heldDirections;
        super.move();

        let widthM = game.imgWidth;
        let heightM = game.imgHeight;
        // smooth camera movement - moves the map against the player while the player is in the centre of the map
        if (mapX < 112) { mapX = 112; } // left
        if (mapX > widthM - 112) { mapX = widthM - 112; } // right
        if (mapY < 112) { mapY = 112; } // tops
        if (mapY > heightM - 112) { mapY = heightM - 112; } // bottom
        let camera_top = pixelSize * 112;
        let camera_left = pixelSize * 112;

        // moving the map and player
        game.map.style.transform = `translate3d( ${-mapX * pixelSize + camera_left}px, ${-mapY * pixelSize + camera_top}px, 0 )`;
        this.self.style.transform = `translate3d( ${this.x * pixelSize}px, ${this.y * pixelSize}px, 0 )`;
    }
}


/* It's a container for items that can be picked up and used by the player */
class Inventory {
    /**
     * It creates a new empty array with 5 elements, and assigns it to the _contents property of the object
     */
    constructor(){
        this._size = 5;
        this._slotsAvailable = 5;
        this._contents = [undefined, undefined, undefined, undefined, undefined];
    }

    /**
     * Sets the id of the slot element of the DOM specified to the type specified
     *
     * @param slot - The id of the slot you want to change.
     * @param type - The type of item you want to set the slot to.
     */
    _setDocumentInventorySlot(slot, type){
        let slotView = document.getElementById(slot).firstElementChild;
        if (type !== null){
            slotView.id = type;
        } else {
            slotView.id = "";
        }
    }

    /**
     * It returns true if the number of slots available is not equal to zero
     * @returns whether there are slots available or not
     */
    checkSlotsAvailable(){
        return this._slotsAvailable !== 0;
    }

    /**
     * If the slot is not undefined, return the item in that slot. Otherwise, return false
     * @param slot - The slot number of the item you want to get.
     * @returns The item in the slot.
     */
    getItemFromSlot(slot){
        if (this._contents[slot] !== undefined){
            return this._contents[slot];
        } else {
            return false;
        }
    }

    /**
     * If the inventory is not full, the item is added to the first empty slot. If the inventory is full, the item is
     * not added
     * @param itemReference - This is the item object that is being added to the inventory.
     * @param activeSlot - The slot that the player is currently hovering over.
     */
    insertItem(itemReference, activeSlot) {
        if (this.checkSlotsAvailable()) {
            let slot = '';
            for (let index = 0; index < this._size; index++) {
                if (this._contents[index] === undefined) {
                    this._contents[index] = itemReference;
                    slot = 'slot-' + index.toString();
                    this._slotsAvailable -= 1;
                    break;
                }
            }
            this._setDocumentInventorySlot(slot, itemReference.objectType);
        }
    }

    /**
     * This function removes an item from the inventory and returns a reference to the item.
     * @param activeSlot - The slot number of the item to be removed.
     * @returns The reference to the item being removed
     */
    removeItem(activeSlot){
        let itemReference = this._contents[activeSlot];
        this._contents[activeSlot] = undefined;
        this._setDocumentInventorySlot('slot-' + activeSlot.toString(), null);
        this._slotsAvailable += 1;
        return itemReference;
    }
}


/* It's a class that represents a healthbar in the game */
class HealthBar{
    /**
     * The constructor function creates a div element with the class name "health_bar" and appends it to the parent element
     * @param parentId - The id of the element that the health bar will be appended to.
     * @param maxHealth - The maximum health of the entity.
     */
    constructor(parentId, maxHealth) {
        this._maxHealth = maxHealth;
        let parent = document.getElementById(parentId);
        this._self = document.createElement("div");
        this._self.className = "health_bar";
        parent.appendChild(this._self);
        this.update(maxHealth);
    }

    /**
     * It updates the health bar.
     * @param health - The current health of the entity.
     */
    update(health){
        this._self.style.width= `${(health/this._maxHealth) * 50}%`;
    }
}


/* It's a class that handles the game logic */
class GameController{
    /**
     * It creates a new game object, and initializes all the variables that will be used throughout the game.
     */
    constructor() {
        this._gameOver = false;

        this.itemGroup = new ObjectGroup('item');
        this.lockGroup = new ObjectGroup('lock');
        this.enemyGroup = new ObjectGroup('enemy');

        this.heldDirections = [];
        this.activeInventorySlot = 0;
        document.getElementById(`slot-${this.activeInventorySlot}`).style.backgroundImage = "url(/static/img/active_slot.png)";

        this.map = document.querySelector('.map');
        this.endScreen = document.querySelector('.end-screen');
        this.level = document.querySelector('.level');

        this.timeElapsed = 0;
        setInterval(function(){
            game.timeElapsed += 1;
        }, 1000, );

        this._timerStatus = document.querySelector(".time-elapsed");
        this._locksStatus = document.querySelector(".locks-remaining");
        this._enemiesStatus = document.querySelector(".enemies-defeated");
    }

    /**
     * It updates the game status text on the screen
     */
    _updateGameStatus(){
        let minutes = Math.floor(this.timeElapsed /60);
        let seconds = Math.floor((this.timeElapsed/60 - minutes)*60);
        if (String(seconds).length < 2){
            seconds = `0${seconds}`;
        }

        this._timerStatus.textContent = `time elapsed: ${minutes}:${seconds}`;
        this._locksStatus.textContent = `Locks remaining: ${this.lockGroup.objectList.length - this.player.locksOpened}`;
        this._enemiesStatus.textContent = `Enemies defeated: ${this.player.enemiesKilled}`;
    }

    /**
     * It changes the background image of the active inventory slot to a different image
     * @param slot - The slot number to set as active.
     */
    setActiveInventorySlot(slot){
        if (this.activeInventorySlot !== slot){
            let prevSlot = this.activeInventorySlot;
            this.activeInventorySlot = slot;
            let slotView = document.getElementById(`slot-${slot}`);
            let prevSlotView = document.getElementById(`slot-${prevSlot}`);
            slotView.style.backgroundImage = "url(/static/img/active_slot.png)";
            prevSlotView.style.backgroundImage = "none";
        }
    }

    /**
     * If any of the locks are locked, return false. Otherwise, end the game and return true
     * @returns whether the game has been won or not
     */
    checkWinCondition() {
        for (const lock of this.lockGroup.objectList){
            if (lock.locked){
                return false;
            }
        }
        this.gameEnd(true);
        return true;
    }

    /**
     * This function loops through the enemySpawnPositions array and creates a new enemy object for each position in the
     * array
     */
    spawnEnemies(){
        let id = 0;
        for (const coord of this.enemySpawnPositions){
            id += 1;
            let enemy = new Enemy(id);
            this.enemyGroup.push(enemy);
            enemy.spawn(coord.y,  coord.x);
        }
    }

    /**
     * The function creates a new player, creates a new sword, adds the sword to the item group, and then adds the sword to
     * the player's inventory
     */
    spawnPlayer(){
        this.player = new Player();
        let sword = new Item('sword', 1);
        let swordReference = this.itemGroup.push(sword);
        this.player.inventory.insertItem(swordReference, 0);
    }

    /**
     * It takes a binary string and converts it into a 2D array of nodes, each of which has a top, bottom, left, and right
     * wall
     */
    defineMaze(){
        this.maze = new Maze(mazeSeed);

        // populating tree and calculating enemy spawn positions
        let enemyNumber = Math.floor(3**(((this.maze.height*this.maze.width)**(1/2))/5));
        if (enemyNumber > maxEnemies && maxEnemies !== -1){
            enemyNumber = maxEnemies;
        }
        let enemySpawnSpacing = Math.floor((this.maze.height*this.maze.width)/enemyNumber);
        if (enemyNumber === 0){
            enemySpawnSpacing = 0;
        }

        let index = 0;
        let deadEndCodes = ['0111', '1011', '1101', '1110'];
        this.deadEndPositions = [];
        let corridorCodes = ['1010', '0101'];

        this.enemySpawnPositions = [];

        for (let row = 1; row <= this.maze.height; row++) {
            for (let column = 1; column <= this.maze.width; column++) {

                let bin = this.maze.binaryString.slice(0,4);

                // checking if the node is either a dead end or a node to be used to an enemy spawn
                if (deadEndCodes.includes(bin)){
                    this.deadEndPositions.push({y:row, x:column});
                } else if (!corridorCodes.includes(bin) && (index%(enemySpawnSpacing-Math.floor(enemySpawnSpacing/2)) === 0) && enemyNumber !==  0){
                    this.enemySpawnPositions.push({y:row, x:column});
                }

                let walls = {top: parseInt(bin[0]), bottom: parseInt(bin[1]), left: parseInt(bin[2]), right: parseInt(bin[3])};
                let node = new Node(row, column, walls);

                this.maze.nodes.push(node);
                this.maze.binaryString = this.maze.binaryString.slice(4);
                index += 1;
            }
        }
        this.maze.output();

        this.determineLockAndKeyPositions();
    }

    /**
     * It spawns locks and keys in the maze, and stores the references to the locks and keys in the maze's adjacency list
     */
    determineLockAndKeyPositions(){
        // spawning locks and keys
        let noDeadEnds = this.deadEndPositions.length;
        let even = 0;
        if (noDeadEnds > maxLocks && maxLocks !== -1){
            noDeadEnds = maxLocks;
        }

        if ((noDeadEnds-1)%2 === 1){
            even = 1;
        }

        for (let n = noDeadEnds-1; n >= noDeadEnds%2; n--) {

            let nodePosition = this.deadEndPositions[n];

            if (n % 2 === even) {
                let key = new Item('key', n);
                let keyReference = this.itemGroup.push(key);
                key.entity.spawn(nodePosition.y, nodePosition.x);
                console.log(nodePosition)
                this.maze.nodes.getNode(nodePosition).contains = keyReference;
            } else if (n % 2 !== even) {
                let lock = new Lock(n);
                let lockReference = this.lockGroup.push(lock);
                lock.entity.spawn(nodePosition.y, nodePosition.x);

                this.maze.nodes.getNode(nodePosition).contains = lockReference;
            }
        }
    }

    /**
     * It sets the CSS properties of the root element to the width and height of the maze image
     */
    defineMazeProperties(){
        // setting css properties to correct values
        this.root = document.querySelector(':root');
        this.root.style.setProperty('--map-width', this.maze.width);
        this.root.style.setProperty('--map-height', this.maze.height);

        this.imgWidth = (this.maze.width * mazeScale) - 64;
        this.imgHeight = (this.maze.height * mazeScale) - 50;
    }

    /**
     * It displays a screen with a message and a button to restart or continue the game, the locations are different based
     * on whether the player lost or won, and whether they have finished the game or not
     * @param hasWon - boolean
     */
    gameEnd(hasWon){
        let continueLocation = "";
        if ((hasWon === true && game.maze.height*game.maze.width >= 625) || gameComplete === 1){
            continueLocation = "/gamecomplete";
        }

        this._gameOver = true;
        this.level.id = "hidden";
        this.endScreen.id = "shown";
        let score = Math.floor((this.maze.height + this.maze.width)/2 * (((2 ** -((this.timeElapsed/200) - 10)) + 50) + (this.player.enemiesKilled * 10) + (this.player.locksOpened * 15)));

        let popOut = this.endScreen.firstElementChild;
        let message = popOut.firstElementChild;

        let scoreDisplay = document.querySelector(".score");
        scoreDisplay.textContent = `Score: ${score}`;

        let restartButton = document.createElement('button');
        popOut.appendChild(restartButton);

        if (hasWon === true){
            let sizeIncrease = 2;
            if (this.maze.height % 5 === 0){
                sizeIncrease = 3;
            }
            if (continueLocation === ""){
            continueLocation = `/play?height=${this.maze.height + sizeIncrease}&width=${this.maze.width + sizeIncrease}`;
            }

            restartButton.textContent = "Try again?";
            restartButton.onclick = function(){
                window.location.href = window.location.href;
            }

            let continueButton = document.createElement('button');
            continueButton.textContent = "Continue?";
            continueButton.onclick = function() {
                window.location.href = continueLocation;
            }

            popOut.appendChild(continueButton)
            message.style.backgroundImage = "url(/static/img/levelcomplete.png)";

        } else {
            restartButton.textContent = "Restart?";
            restartButton.onclick = function(){
                window.location.href = "/";
            }
            message.style.backgroundImage = "url(/static/img/gameover.png)";
        }
    }


    /**
     * The gameLoop function is called every frame and it updates the items, and locks and allows the player
     * and enemies to move
     */
    gameLoop() {

        // need to get pixel size every frame as it varies depending on how large the browser window is
        pixelSize = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--pixel-size'));

        this.player.move();

        for (const enemy of this.enemyGroup.objectList){
            enemy.move();
            enemy.attack();
        }

        for (const item of this.itemGroup.objectList){
            item.update();
        }

        for (const lock of this.lockGroup.objectList){
            lock.update();
        }
        this._updateGameStatus();
    }
    
    /**
     * The step function calls the gameLoop function, which updates the game state, and then calls itself again
     */
    step() {
        if (this._gameOver === true){
            return;
        }
        this.gameLoop();
        window.requestAnimationFrame(function () {
            game.step();
        })
    }
}

game = new GameController();
game.defineMaze();
game.defineMazeProperties();
game.spawnPlayer();
game.spawnEnemies();
game.step();



/* Listening for key presses and then adding the key to the corresponding array. */
document.addEventListener('keydown', function (e) {
    let direction = directionKeys[e.key];
    let inventorySlot = inventoryKeys[e.key];
    let command = commands[e.key];
    // adds last key pressed to the start of the heldDirections array
    if (direction && game.heldDirections.indexOf(direction) === -1) {
        game.heldDirections.unshift(direction);
    } else if (inventorySlot && game.activeInventorySlot !== inventorySlot-1) {
        game.setActiveInventorySlot(inventorySlot-1);
    } else if (command){
        game.player.executeCommand(command);
    }
})

/* Removing the direction from the heldDirections array when the key is released. */
document.addEventListener('keyup', function (e) {
    let direction = directionKeys[e.key];
    let index = game.heldDirections.indexOf(direction);
    // removes key from helpDirections when it stops being pressed
    if (index > -1) {
        game.heldDirections.splice(index, 1);
    }
})