// Game Variables
const canvas = document.getElementById('pongCanvas');
const ctx = canvas.getContext('2d');

// Game Objects
const paddle = {
    x: 10,
    y: canvas.height / 2 - 50,
    width: 10,
    height: 100,
    dy: 0,
    maxSpeed: 6,
    color: '#00ff41'
};

const aiPaddle = {
    x: canvas.width - 20,
    y: canvas.height / 2 - 50,
    width: 10,
    height: 100,
    dy: 0,
    maxSpeed: 5,
    difficulty: 'NORMAL',
    color: '#ff006e'
};

const ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    radius: 8,
    dx: 5,
    dy: 5,
    speed: 5,
    maxSpeed: 8,
    color: '#00d4ff'
};

let playerScore = 0;
let aiScore = 0;
let gameRunning = true;
let ballWallCollision = false;

// Keyboard Controls
const keys = {};
window.addEventListener('keydown', (e) => {
    keys[e.key] = true;
    e.preventDefault();
});

window.addEventListener('keyup', (e) => {
    keys[e.key] = false;
});

// Mouse Controls
canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    const mouseY = e.clientY - rect.top;
    paddle.y = Math.max(0, Math.min(mouseY - paddle.height / 2, canvas.height - paddle.height));
});

// Update Player Paddle
function updatePlayerPaddle() {
    if (keys['ArrowUp'] || keys['w'] || keys['W']) {
        paddle.dy = -paddle.maxSpeed;
    } else if (keys['ArrowDown'] || keys['s'] || keys['S']) {
        paddle.dy = paddle.maxSpeed;
    } else {
        paddle.dy = 0;
    }

    paddle.y += paddle.dy;

    // Boundary collision
    if (paddle.y < 0) paddle.y = 0;
    if (paddle.y + paddle.height > canvas.height) paddle.y = canvas.height - paddle.height;
}

// Update AI Paddle with Dynamic Difficulty
function updateAIPaddle() {
    const aiCenter = aiPaddle.y + aiPaddle.height / 2;
    const ballCenter = ball.y;
    let speed = aiPaddle.maxSpeed;

    // AI Difficulty Levels
    if (aiPaddle.difficulty === 'EASY') {
        speed = 3;
        // AI misses sometimes (30% miss rate)
        if (Math.random() < 0.3) {
            return;
        }
    } else if (aiPaddle.difficulty === 'HARD') {
        speed = 6;
    } else if (aiPaddle.difficulty === 'IMPOSSIBLE') {
        speed = 7;
    }

    // AI tracks the ball
    if (aiCenter < ballCenter - 35) {
        aiPaddle.dy = speed;
    } else if (aiCenter > ballCenter + 35) {
        aiPaddle.dy = -speed;
    } else {
        aiPaddle.dy = 0;
    }

    aiPaddle.y += aiPaddle.dy;

    // Boundary collision
    if (aiPaddle.y < 0) aiPaddle.y = 0;
    if (aiPaddle.y + aiPaddle.height > canvas.height) aiPaddle.y = canvas.height - aiPaddle.height;
}

// Update Ball
function updateBall() {
    ball.x += ball.dx;
    ball.y += ball.dy;

    // Top and bottom wall collision
    if (ball.y - ball.radius < 0 || ball.y + ball.radius > canvas.height) {
        ball.dy = -ball.dy;
        ball.y = Math.max(ball.radius, Math.min(ball.y, canvas.height - ball.radius));
        ballWallCollision = true;
    } else {
        ballWallCollision = false;
    }
}

// Collision Detection - Paddles
function checkPaddleCollision() {
    // Player Paddle Collision
    if (ball.x - ball.radius < paddle.x + paddle.width &&
        ball.y > paddle.y &&
        ball.y < paddle.y + paddle.height) {
        ball.dx = -ball.dx;
        ball.x = paddle.x + paddle.width + ball.radius;

        // Add spin based on paddle velocity
        const deltaY = ball.y - (paddle.y + paddle.height / 2);
        ball.dy = deltaY * 0.1 + paddle.dy * 0.2;

        // Increase ball speed gradually
        ball.speed = Math.min(ball.speed + 0.1, ball.maxSpeed);
        updateBallVelocity();
    }

    // AI Paddle Collision
    if (ball.x + ball.radius > aiPaddle.x &&
        ball.y > aiPaddle.y &&
        ball.y < aiPaddle.y + aiPaddle.height) {
        ball.dx = -ball.dx;
        ball.x = aiPaddle.x - ball.radius;

        // Add spin based on paddle velocity
        const deltaY = ball.y - (aiPaddle.y + aiPaddle.height / 2);
        ball.dy = deltaY * 0.1 + aiPaddle.dy * 0.2;

        // Increase ball speed gradually
        ball.speed = Math.min(ball.speed + 0.1, ball.maxSpeed);
        updateBallVelocity();
    }
}

// Update Ball Velocity
function updateBallVelocity() {
    const speed = Math.sqrt(ball.dx ** 2 + ball.dy ** 2);
    if (speed > ball.maxSpeed) {
        ball.dx = (ball.dx / speed) * ball.maxSpeed;
        ball.dy = (ball.dy / speed) * ball.maxSpeed;
    }
}

// Check Scoring
function checkScore() {
    if (ball.x < 0) {
        aiScore++;
        resetBall();
        updateUI();
    } else if (ball.x > canvas.width) {
        playerScore++;
        resetBall();
        updateUI();
    }
}

// Reset Ball
function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.speed = 5;
    ball.dx = (Math.random() > 0.5 ? 1 : -1) * ball.speed;
    ball.dy = (Math.random() > 0.5 ? 1 : -1) * (Math.random() * 3 + 2);
}

// Draw Functions
function drawPaddle(p) {
    ctx.fillStyle = p.color;
    ctx.fillRect(p.x, p.y, p.width, p.height);
    ctx.strokeStyle = p.color;
    ctx.lineWidth = 2;
    ctx.strokeRect(p.x, p.y, p.width, p.height);
}

function drawBall() {
    ctx.fillStyle = ball.color;
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#00ff88';
    ctx.lineWidth = 2;
    ctx.stroke();
}

function drawNet() {
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
    ctx.setLineDash([10, 10]);
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(canvas.width / 2, 0);
    ctx.lineTo(canvas.width / 2, canvas.height);
    ctx.stroke();
    ctx.setLineDash([]);
}

// Update UI
function updateUI() {
    document.getElementById('playerScore').textContent = playerScore;
    document.getElementById('aiScore').textContent = aiScore;
    document.getElementById('difficulty').textContent = aiPaddle.difficulty;
    document.getElementById('ballSpeed').textContent = ball.speed.toFixed(1);
}

// Adjust Difficulty Based on Score Difference
function adjustDifficulty() {
    const diff = playerScore - aiScore;

    if (diff > 5) {
        aiPaddle.difficulty = 'HARD';
        aiPaddle.maxSpeed = 6;
    } else if (diff > 2) {
        aiPaddle.difficulty = 'NORMAL';
        aiPaddle.maxSpeed = 5;
    } else if (diff < -5) {
        aiPaddle.difficulty = 'EASY';
        aiPaddle.maxSpeed = 3;
    } else if (diff < -2) {
        aiPaddle.difficulty = 'NORMAL';
        aiPaddle.maxSpeed = 5;
    }
}

// Main Game Loop
function gameLoop() {
    // Clear canvas
    ctx.fillStyle = '#1a1a2e';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw game elements
    drawNet();
    drawPaddle(paddle);
    drawPaddle(aiPaddle);
    drawBall();

    if (gameRunning) {
        // Update game objects
        updatePlayerPaddle();
        updateAIPaddle();
        updateBall();
        checkPaddleCollision();
        checkScore();
        adjustDifficulty();
    }

    requestAnimationFrame(gameLoop);
}

// Reset Game
document.getElementById('resetBtn').addEventListener('click', () => {
    playerScore = 0;
    aiScore = 0;
    ball.speed = 5;
    aiPaddle.difficulty = 'NORMAL';
    aiPaddle.maxSpeed = 5;
    resetBall();
    updateUI();
});

// Initialize Game
function init() {
    updateUI();
    gameLoop();
}

init();