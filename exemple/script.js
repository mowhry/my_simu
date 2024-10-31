const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const speedInput = document.getElementById('speed');
 
const audioContext = new (window.AudioContext || window.webkitAudioContext)();
 
let ball = {
  x: canvas.width / 2,
  y: canvas.height / 2,
  radius: 20,
  dx: parseFloat(speedInput.value),
  dy: parseFloat(speedInput.value),
  gravity: 0.1,
  elasticity: 0.8,
  useGravity: true,
  useElasticity: true
};
 
function playSound(frequency = 440) {
  let oscillator = audioContext.createOscillator();
  oscillator.type = 'sine';
  oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);
  oscillator.connect(audioContext.destination);
  oscillator.start();
  oscillator.stop(audioContext.currentTime + 0.1);
}
 
function drawBall() {
  ctx.beginPath();
  ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI*2);
  ctx.fillStyle = '#0095DD';
  ctx.fill();
  ctx.closePath();
}
 
function updateBall() {
  if (ball.useGravity) {
    ball.dy += ball.gravity;
  }
  ball.x += ball.dx;
  ball.y += ball.dy;
 
  // Enhanced collision detection with the walls
  if (ball.x + ball.radius > canvas.width || ball.x - ball.radius < 0) {
    ball.dx = -ball.dx;
    ball.x = ball.x + ball.radius > canvas.width ? canvas.width - ball.radius : ball.radius;
    playSound(400 + Math.random() * 200);
  }
  if (ball.y + ball.radius > canvas.height || ball.y - ball.radius < 0) {
    ball.dy = -ball.dy * (ball.useElasticity ? ball.elasticity : 1);
    ball.y = ball.y + ball.radius > canvas.height ? canvas.height - ball.radius : ball.radius;
    playSound(400 + Math.random() * 200);
  }
}
 
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawBall();
  updateBall();
  requestAnimationFrame(draw);
}
 
function toggleGravity(checked) {
  ball.useGravity = checked;
  checkDisabled();
}
 
function toggleElasticity(checked) {
  ball.useElasticity = checked;
  checkDisabled();
}
 
function checkDisabled() {
  if (!ball.useGravity && !ball.useElasticity) {
    speedInput.disabled = false;
  } else {
    speedInput.disabled = true;
    speedInput.value = Math.sqrt(ball.dx * ball.dx + ball.dy * ball.dy).toFixed(1);
  }
}
 
function updateSpeed(value) {
  ball.dx = parseFloat(value);
  ball.dy = parseFloat(value);
}
 
function resizeCanvas() {
    canvas.width = window.innerWidth * 0.9;
    canvas.height = window.innerHeight * 0.7;
    if (ball.x + ball.radius > canvas.width) {
        ball.x = canvas.width - ball.radius;
    }
    if (ball.y + ball.radius > canvas.height) {
        ball.y = canvas.height - ball.radius;
    }
}
 
resizeCanvas();
window.addEventListener('resize', resizeCanvas);
draw();
