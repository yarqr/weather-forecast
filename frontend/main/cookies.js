let switchButton = document.querySelector(".nav--panel__theme-switcher");
let main = document.querySelector("body");

if (document.cookie !== '') {
  switchButton.innerHTML = ""
  main.classList.remove("main-night", "main-day")
  main.classList.add(document.cookie.slice(3))
  if (document.cookie === 'bg=main-night') {
    switchButton.insertAdjacentHTML(
      "afterbegin",
      `<img src = "/assets/icons/sun.png" class = "clicked-img">`
    );
  } else {
    switchButton.insertAdjacentHTML(
      "afterbegin",
      `<img src = "/assets/icons/moon.png">`
    );
  }
}

switchButton.addEventListener("click", () => {
  if (mainBody.classList.contains("main-day")) {
    document.cookie = 'bg=main-night'
  } else {
    document.cookie = 'bg=main-day'
  }
});




