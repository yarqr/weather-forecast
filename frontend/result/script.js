let params = new URLSearchParams(document.location.search);
let body = document.querySelector(".res-page");
let returnButton = document.querySelector(".main__return-button");
let city = params.get("city");
let url = document.location.origin + `/api/get/weather/${city}`;
let resPage = document.querySelector(".res-page")

returnButton.addEventListener("click", () => {
  window.location.replace(window.location.origin);
});

class Weather {
  constructor(temperature, description, feels_like, country, humidity, wind_speed) {
    this.temperature = temperature
    this.descriprtion = description
    this.feels_like = feels_like
    this.country = country
    this.humidity = humidity
    this.wind_speed = wind_speed
  }
  matchStatetoIcons() {
    switch (this.descriprtion) {
      case 'Rain':
        return "/assets/icons/thunderstorm.png"
      case 'Clouds':
        return "/assets/icons/clouds.png"
      case 'Thunderstorm':
        return "/assets/icons/thunderstorm.png"
      case 'Clear':
        return "/assets/icons/clear.png"
      case 'Mist':
        return "/assets/icons/fog.png"
      case 'Haze':
        return "/assets/icons/fog.png"
      case 'Drizzle':
        return "/assets/icons/drizzle.png"
    }
  }
  generImg() {
    if (this.country === "UA") {
      return `https://flagsapi.com/RU/flat/64.png`
    }
    return `https://flagsapi.com/${this.country}/flat/64.png`
  }
}
async function req() {
  let txt = ``
  let response = await fetch(url);
  let result = await response.json();
  returnButton.removeAttribute("hidden");
  if (result !== null) {
    let weather = new Weather(result.temperature, result.description, result.feels_like, result.country, result.humidity, result.wind_speed)
    txt = `<section class = "main__res"><article class="a1">${city.toUpperCase()}</article><img src=${weather.generImg()} class = "main__res__flag a2"/></section> 
        <section class = "main__temp">  ${Math.round(
          result.temperature
        )} °C   <img class = "main__temp__state-icon" src = ${weather.matchStatetoIcons()}/> </section>
        <section class = "main__wind">wind speed: ${weather.wind_speed} m/s</section>`
  } else {
    txt = `<section> city not found </section>`;
  }
  resPage.insertAdjacentHTML("afterbegin", txt);
}

req();
