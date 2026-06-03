/**
 * SANI AMANZI doc page — reading progress + smooth in-page nav
 */
(function () {
  "use strict";

  if (!document.body.classList.contains("ulr-amanzi-doc-flow")) {
    return;
  }

  var main = document.querySelector(".ulr-amanzi-doc__inner");
  if (!main) {
    return;
  }

  var progress = document.createElement("div");
  progress.className = "ulr-amanzi-doc-progress";
  progress.setAttribute("aria-hidden", "true");
  progress.innerHTML = '<span class="ulr-amanzi-doc-progress__bar"></span>';
  document.body.appendChild(progress);
  var bar = progress.querySelector(".ulr-amanzi-doc-progress__bar");

  function updateProgress() {
    var docH = document.documentElement.scrollHeight - window.innerHeight;
    var pct = docH > 0 ? (window.scrollY / docH) * 100 : 0;
    bar.style.width = Math.min(100, Math.max(0, pct)) + "%";
  }

  window.addEventListener("scroll", updateProgress, { passive: true });
  updateProgress();

  main.querySelectorAll('.ulr-amanzi-doc-nav a[href^="#"]').forEach(function (link) {
    link.addEventListener("click", function (e) {
      var id = link.getAttribute("href");
      if (!id || id.length < 2) {
        return;
      }
      var target = document.querySelector(id);
      if (!target) {
        return;
      }
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
      if (history.replaceState) {
        history.replaceState(null, "", id);
      }
    });
  });
})();
