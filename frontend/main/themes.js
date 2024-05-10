let buttonToSwitchTheme = document.querySelector(".nav--panel__theme-switcher");
let mainBody = document.querySelector("body");
buttonToSwitchTheme.addEventListener("click", () => {
  if (mainBody.classList.contains("main-day")) {
    mainBody.classList.remove("main-day");
    mainBody.classList.add("main-night");
    buttonToSwitchTheme.innerHTML = "";
    buttonToSwitchTheme.insertAdjacentHTML(
      "afterbegin",
      `<img src = "../../assets/icons/sun.png" class = "clicked-img">`
    );
  } else {
    mainBody.classList.remove("main-night");
    mainBody.classList.add("main-day");
    buttonToSwitchTheme.innerHTML = "";
    buttonToSwitchTheme.insertAdjacentHTML(
      "afterbegin",
      `<img src = "../../assets/icons/moon.png">`
    );
  }
});
