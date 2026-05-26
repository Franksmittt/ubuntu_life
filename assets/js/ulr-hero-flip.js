/**
 * Hero headline — cycles pillars with a vertical flip.
 */
(function () {
  "use strict";

  var flip = document.querySelector("[data-ulr-hero-flip]");
  if (!flip) return;

  var live = flip.querySelector("[data-ulr-hero-flip-live]");
  var store = flip.querySelectorAll(".ulr-hero-glass__flip-store [data-label]");
  if (!live || !store.length) return;

  var labels = Array.prototype.map.call(store, function (el) {
    return {
      text: el.textContent.trim(),
      shimmer: el.classList.contains("ulr-hero-glass__shimmer"),
    };
  });

  var index = 0;
  var holdMs = 3200;
  var animMs = 450;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function render(i) {
    var item = labels[i];
    if (item.shimmer) {
      live.innerHTML =
        '<span class="ulr-hero-glass__shimmer">' + item.text + "</span>";
    } else {
      live.textContent = item.text;
    }
  }

  if (reduced) {
    live.textContent = labels
      .map(function (item) {
        return item.text;
      })
      .join(", ");
    return;
  }

  function next() {
    flip.classList.add("is-exit");
    window.setTimeout(function () {
      index = (index + 1) % labels.length;
      render(index);
      flip.classList.remove("is-exit");
      flip.classList.add("is-pre-enter");
      void flip.offsetWidth;
      flip.classList.remove("is-pre-enter");
    }, animMs);
  }

  render(0);
  window.setInterval(next, holdMs);
})();
