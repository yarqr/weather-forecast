let cityForm = document.querySelector("form");
let serializeForm = (formNode) => {
  const { elements } = formNode;
  return elements[0].value;
};

cityForm.addEventListener("submit", (event) => {
  event.preventDefault();
  let city = serializeForm(cityForm);
  window.location.replace(`${window.location}` + `/city=${city}`);
});
// let btn = document.querySelector(".btn")
// btn.addEventListener("click", () => {
//     window.location.replace(`${window.location}` + `/city=Киров`)
// });

// event.preventDefault();
//   let city = serializeForm(cityForm);
//   let request = fetch("#", {
//     method: "POST",
//     body: JSON.stringify({
//       cityName: city,
//     }),
//   });
