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
