document.querySelectorAll("[data-filters]").forEach((filters) => {
  const cards = filters.parentElement.querySelectorAll("[data-filter-grid] [data-category]");
  const buttons = filters.querySelectorAll("[data-filter]");
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      buttons.forEach((item) => item.setAttribute("aria-pressed", String(item === button)));
      cards.forEach((card) => {
        card.hidden = button.dataset.filter !== "All" && card.dataset.category !== button.dataset.filter;
      });
    });
  });
});

document.querySelectorAll("[data-comparison] input").forEach((input) => {
  input.addEventListener("input", () => {
    input.closest("[data-comparison]").style.setProperty("--split", `${input.value}%`);
  });
});

const booking = document.querySelector("[data-booking]");
if (booking) {
  const treatment = booking.querySelector("select");
  const link = booking.querySelector("[data-booking-link]");
  const initialLink = link.href;
  treatment.addEventListener("change", () => {
    const url = new URL(initialLink);
    if (treatment.value) {
      url.searchParams.set("text", `Hello, I’d like to ask about an appointment for ${treatment.value.toLowerCase()}.`);
    }
    link.href = url.href;
  });
}
