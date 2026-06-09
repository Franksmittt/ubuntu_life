(function () {
  "use strict";

  document.querySelectorAll(".ulr-amanzi-scisan-flip").forEach(function (btn) {
    btn.addEventListener("click", function () {
      btn.classList.toggle("is-flipped");
    });
  });
})();
