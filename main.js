/* swapping the game functionality to js to make it playable */

let pyodide;
let timer = null;

const screenEl = document.getElementById("screen");
const startBtn = document.getElementById("start");
const pauseBtn = document.getElementById("pause");
const restartBtn = document.getElementById("restart");

function draw() {
  screenEl.textContent = pyodide.runPython("game.render()");
}

function stopTimer() {
  if (timer !== null) {
    clearInterval(timer);
    timer = null;
  }
}

function startTimer() {
  if (timer !== null) return;
  timer = setInterval(() => {
    const status = pyodide.runPython("game.tick()");
    draw();
    if (status === "dead") {
      stopTimer();
      screenEl.textContent += "\n\nGame over. Press Restart.";
    }
  }, 400);
}

async function init() {
  pyodide = await loadPyodide();
  const gamePy = await (await fetch("./game.py")).text();
  pyodide.runPython(gamePy);
  pyodide.runPython("game = Game(size=10)");
  draw();

  document.addEventListener("keydown", (e) => {
    const keyMap = {
      ArrowUp: "UP",
      ArrowDown: "DOWN",
      ArrowLeft: "LEFT",
      ArrowRight: "RIGHT",
    };
    if (keyMap[e.key]) {
      e.preventDefault();
      pyodide.runPython(`game.set_direction("${keyMap[e.key]}")`);
    }
  });

  startBtn.onclick = () => startTimer();
  pauseBtn.onclick = () => stopTimer();
  restartBtn.onclick = () => {
    stopTimer();
    pyodide.runPython("game = Game(size=10)");
    draw();
  };
}

init().catch((err) => {
  screenEl.textContent =
    "Startup error:\n\n" +
    (err?.stack || err?.message || String(err));
});
