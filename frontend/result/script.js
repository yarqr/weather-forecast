let params = new URLSearchParams(document.location.search);
let body = document.querySelector(".res-page");
let returnButton = document.querySelector(".main__return-button");
let city = params.get("city");
let url = document.location.origin + `/api/get/weather/${city}`;
let resPage = document.querySelector(".res-page")
returnButton.addEventListener("click", () => {
  window.location.replace(window.location.origin);
});
async function req() {
  let txt = ``
  let response = await fetch(url);
  let result = await response.json();
  returnButton.removeAttribute("hidden");
  if (result !== null) {
    txt = `<section> ${city.toUpperCase()}</section> 
        <section class = "main__temp">  ${Math.round(
          result.temperature
        )} °C </section>`;
  } else {
    txt = `<section> city not found </section>`;
  }
  resPage.insertAdjacentHTML("afterbegin", txt);
}

req();
