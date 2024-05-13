let params = new URLSearchParams(document.location.search);
let body = document.querySelector(".res-page");
let returnButton = document.querySelector(".main__return-button");
let city = params.get("city");
let url = document.location.origin + `/api/get/weather/${city}`;

returnButton.addEventListener("click", () => {
  window.location.replace(window.location.origin);
});
async function req() {
  let response = await fetch(url);
  let result = await response.json();
  returnButton.removeAttribute("hidden");
  if (result !== null) {
    body.insertAdjacentHTML(
      "afterbegin",
      `<section> ${city.toUpperCase()}</section> 
        <section class = "main__temp">  ${Math.round(
          result.temperature
        )} °C </section>`
    );
  } else {
    body.insertAdjacentHTML(
      "afterbegin",
      `<section> city not found </section>`
    );
  }
}

await req();
