const footballTeam = {
  team: "Argentina",
  year: 1986,
  headCoach: "Carlos Bilardo",
  players: [
    { name: "Diego Maradona", position: "midfielder", isCaptain: true },
    { name: "Jorge Valdano", position: "forward", isCaptain: false },
    { name: "Oscar Ruggeri", position: "defender", isCaptain: false },
    { name: "Nery Pumpido", position: "goalkeeper", isCaptain: false }
  ]
};

// Display team info
document.getElementById("team").textContent = footballTeam.team;
document.getElementById("year").textContent = footballTeam.year;
document.getElementById("head-coach").textContent = footballTeam.headCoach;

const playerCards = document.getElementById("player-cards");
const select = document.getElementById("players");

// Function to display players
function displayPlayers(position) {
  playerCards.innerHTML = "";

  let filteredPlayers = footballTeam.players;

  if (position !== "all") {
    filteredPlayers = footballTeam.players.filter(
      player => player.position === position
    );
  }

  filteredPlayers.forEach(player => {
    const card = document.createElement("div");
    card.classList.add("player-card");

    const name = document.createElement("h2");
    name.textContent = player.isCaptain
      ? `(Captain) ${player.name}`
      : player.name;

    const pos = document.createElement("p");
    pos.textContent = `Position: ${player.position}`;

    card.appendChild(name);
    card.appendChild(pos);
    playerCards.appendChild(card);
  });
}

// Initial display (All Players)
displayPlayers("all");

// Filter when dropdown changes
select.addEventListener("change", function () {
  displayPlayers(this.value);
});
