let params = new URLSearchParams(document.location.search);
let body = document.querySelector("body");
let returnButton = document.querySelector(".main__return-button");
let city = params.get("city");
let url =
  `https://6363-176-59-107-12.ngrok-free.app` + `/api/get/weather/${city}`;

returnButton.addEventListener("click", () => {
  window.location.replace(window.location.origin);
});

let response = fetch(url, {
  headers: {
    "ngrok-skip-browser-warning": 1,
  },
})
  .then((response) => response.json())
  .then((data) => {
    if (data !== null) {
      returnButton.removeAttribute("hidden");
      body.insertAdjacentHTML(
        "afterbegin",
        `<section> ${city} </section> 
        <section>  ${Math.round(data.temperature)} °C </section>`
      );
    } else {
      returnButton.removeAttribute("hidden");
      body.insertAdjacentHTML(
        "afterbegin",
        `<section> city not found </section>`
      );
    }
  });
