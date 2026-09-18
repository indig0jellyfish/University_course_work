const display = document.getElementById("display");

function playSound(key) {
  const audio = document.getElementById(key);
  if (!audio) return;

  audio.currentTime = 0;
  audio.play();

  const pad = audio.parentElement;
  display.textContent = pad.id;
}

document.querySelectorAll(".drum-pad").forEach((pad) => {
  pad.addEventListener("click", function () {
    const key = this.querySelector("audio").id;
    playSound(key);
  });
});

document.addEventListener("keydown", function (e) {
  const key = e.key.toUpperCase();

  if (["Q","W","E","A","S","D","Z","X","C"].includes(key)) {
    playSound(key);
  }
});