const canvas = document.getElementById('tetris');
const ctx = canvas.getContext('2d');

// 方塊的大小
const ROWS = 20;
const COLUMNS = 10;
const BLOCK_SIZE = 30;
const COLORS = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF', '#FF7F00'];

// 定義方塊形狀
const SHAPES = [
    [[1, 1, 1, 1]], // I
    [[1, 1], [1, 1]], // O
    [[0, 1, 0], [1, 1, 1]], // T
    [[1, 0, 0], [1, 1, 1]], // L
    [[0, 0, 1], [1, 1, 1]], // J
    [[1, 1, 0], [0, 1, 1]], // S
    [[0, 1, 1], [1, 1, 0]]  // Z
];

let board = Array.from({ length: ROWS }, () => Array(COLUMNS).fill(null));
let currentShape, currentX, currentY, gameInterval;

function startGame() {
    newShape();
    if (gameInterval) clearInterval(gameInterval);
    gameInterval = setInterval(updateGame, 500);
}

function newShape() {
    const shapeIndex = Math.floor(Math.random() * SHAPES.length);
    currentShape = SHAPES[shapeIndex];
    currentX = Math.floor(COLUMNS / 2) - Math.floor(currentShape[0].length / 2);
    currentY = 0;
}

function drawBoard() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLUMNS; c++) {
            if (board[r][c]) {
                ctx.fillStyle = board[r][c];
                ctx.fillRect(c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
                ctx.strokeStyle = 'white';
                ctx.strokeRect(c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            }
        }
    }
}

function drawShape() {
    for (let r = 0; r < currentShape.length; r++) {
        for (let c = 0; c < currentShape[r].length; c++) {
            if (currentShape[r][c]) {
                ctx.fillStyle = COLORS[SHAPES.indexOf(currentShape)];
                ctx.fillRect((currentX + c) * BLOCK_SIZE, (currentY + r) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
                ctx.strokeStyle = 'white';
                ctx.strokeRect((currentX + c) * BLOCK_SIZE, (currentY + r) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            }
        }
    }
}

function collide() {
    for (let r = 0; r < currentShape.length; r++) {
        for (let c = 0; c < currentShape[r].length; c++) {
            if (currentShape[r][c]) {
                if (currentY + r >= ROWS || currentX + c < 0 || currentX + c >= COLUMNS || board[currentY + r][currentX + c]) {
                    return true;
                }
            }
        }
    }
    return false;
}

function mergeShape() {
    for (let r = 0; r < currentShape.length; r++) {
        for (let c = 0; c < currentShape[r].length; c++) {
            if (currentShape[r][c]) {
                board[currentY + r][currentX + c] = COLORS[SHAPES.indexOf(currentShape)];
            }
        }
    }
}

function clearFullRows() {
    for (let r = ROWS - 1; r >= 0; r--) {
        if (board[r].every(cell => cell !== null)) {
            board.splice(r, 1);
            board.unshift(Array(COLUMNS).fill(null));
        }
    }
}

function updateGame() {
    if (collide()) {
        mergeShape();
        clearFullRows();
        newShape();
        if (collide()) {
            clearInterval(gameInterval);
            alert("遊戲結束!");
            return;
        }
    } else {
        currentY++;
    }

    drawBoard();
    drawShape();
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') {
        currentX--;
        if (collide()) currentX++;
    } else if (e.key === 'ArrowRight') {
        currentX++;
        if (collide()) currentX--;
    } else if (e.key === 'ArrowDown') {
        currentY++;
        if (collide()) currentY--;
    } else if (e.key === 'ArrowUp') {
        const rotatedShape = currentShape[0].map((_, index) => currentShape.map(row => row[index]));
        currentShape = rotatedShape;
        if (collide()) {
            currentShape = SHAPES[SHAPES.indexOf(currentShape)]; // 撤銷旋轉
        }
    }
});

startGame();

