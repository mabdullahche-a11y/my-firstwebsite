if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
  const reveal = new IntersectionObserver((entries, observer) => {
    entries.forEach(({ target, isIntersecting }) => {
      if (!isIntersecting) return;
      target.classList.add("is-visible");
      observer.unobserve(target);
    });
  }, { threshold: 0.12 });

  document.querySelectorAll(".reveal").forEach((item) => reveal.observe(item));
}

const reviewCarousel = document.querySelector(".review-carousel");
if (reviewCarousel) initializeReviews(reviewCarousel);

function initializeReviews(carousel) {
  const track = carousel.querySelector(".review-track");
  const reviews = [...track.querySelectorAll(".review")];
  const controls = carousel.querySelector(".review-controls");
  const count = controls.querySelector("[data-review-count]");
  const toggle = controls.querySelector("[data-review-toggle]");
  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
  const narrowReviews = matchMedia("(max-width: 640px)");

  let current = 0;
  let playing = !reducedMotion.matches;
  let timer;
  let pointerInside = false;
  let focusInside = false;

  function showReview(index, direction = 0) {
    current = (index + reviews.length) % reviews.length;
    const visibleCount = narrowReviews.matches ? 2 : 3;
    reviews.forEach((review, position) => {
      const slot = (position - current + reviews.length) % reviews.length;
      review.hidden = slot >= visibleCount;
      review.style.order = slot;
      review.classList.toggle("is-featured", slot === (visibleCount === 3 ? 1 : 0));

      if (!review.hidden && direction && !reducedMotion.matches) {
        review.getAnimations().forEach((animation) => animation.cancel());
        review.animate([
          { transform: `translateX(${direction * 24}px)`, opacity: 0.65 },
          { transform: "translateX(0)", opacity: 1 },
        ], { duration: 380, easing: "cubic-bezier(.2,.7,.3,1)" });
      }
    });
    count.textContent = `${current + 1} / ${reviews.length}`;
  }

  function scheduleReview() {
    clearTimeout(timer);
    const rotating = playing && !pointerInside && !focusInside && !document.hidden;
    track.setAttribute("aria-live", rotating ? "off" : "polite");
    if (rotating) {
      timer = setTimeout(() => {
        showReview(current + 1, 1);
        scheduleReview();
      }, 8500);
    }
  }

  function setPlaying(value) {
    playing = value;
    toggle.textContent = playing ? "Pause slideshow" : "Play slideshow";
    scheduleReview();
  }

  controls.querySelectorAll("[data-review-step]").forEach((button) => {
    button.addEventListener("click", () => {
      const direction = Number(button.dataset.reviewStep);
      showReview(current + direction, direction);
      scheduleReview();
    });
  });
  toggle.addEventListener("click", () => setPlaying(!playing));
  carousel.addEventListener("pointerenter", (event) => {
    pointerInside = event.pointerType === "mouse";
    scheduleReview();
  });
  carousel.addEventListener("pointerleave", () => {
    pointerInside = false;
    scheduleReview();
  });
  carousel.addEventListener("focusin", () => {
    focusInside = true;
    scheduleReview();
  });
  carousel.addEventListener("focusout", (event) => {
    focusInside = carousel.contains(event.relatedTarget);
    scheduleReview();
  });
  document.addEventListener("visibilitychange", scheduleReview);
  narrowReviews.addEventListener("change", () => showReview(current));
  reducedMotion.addEventListener("change", (event) => {
    if (event.matches) setPlaying(false);
  });

  showReview(0);
  carousel.classList.add("is-ready");
  controls.hidden = false;
  setPlaying(playing);
}
