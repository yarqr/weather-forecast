let params = new URLSearchParams(document.location.search);
let body = document.querySelector("body");
let returnButton = document.querySelector(".main__return-button");
let city = params.get("city");
let url = document.location.origin + `/api/get/weather/${city}`;

returnButton.addEventListener("click", () => {
  window.location.replace(window.location.origin);
});

let response = fetch(url)
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
