const button = document.getElementById("theme-switcher-button");
const dropdown = document.getElementById("theme-dropdown");
const messageElement = document.getElementById("theme-message");
const themeItems = dropdown.querySelectorAll("li");

const themes = [
  {
    name: "light",
    message: "Light theme activated! Clean and bright."
  },
  {
    name: "dark",
    message: "Dark theme activated! Easy on the eyes."
  },
  {
    name: "ocean",
    message: "Ocean theme activated! Calm and refreshing."
  },
  {
    name: "rose",
    message: "Rose theme activated! Romantic and pretty."
  }
];

button.addEventListener("click", () => {
  const isExpanded = button.getAttribute("aria-expanded") === "true";

  if (isExpanded) {
    dropdown.setAttribute("hidden", "");
    button.setAttribute("aria-expanded", "false");
  } else {
    dropdown.removeAttribute("hidden");
    button.setAttribute("aria-expanded", "true");
  }
});

themeItems.forEach(item => {
  item.addEventListener("click", () => {
    const selectedTheme = item.id.replace("theme-", "");

    document.body.className = "";
    document.body.classList.add(`theme-${selectedTheme}`);

    const themeData = themes.find(theme => theme.name === selectedTheme);
    if (themeData) {
      messageElement.textContent = themeData.message;
    }

    dropdown.setAttribute("hidden", "");
    button.setAttribute("aria-expanded", "false");
  });
});
