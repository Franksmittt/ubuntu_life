(function () {
  function fileName(path) {
    const clean = (path || "").split("?")[0].split("#")[0];
    const parts = clean.split("/").filter(Boolean);
    return parts[parts.length - 1] || "index.html";
  }

  function activeHref(page) {
    if (page === "index.html" || page === "") {
      return "index.html";
    }
    if (page === "pillar-agri-biosecurity.html" || page === "product-sani-99-agri.html") {
      return "pillar-agri-biosecurity.html";
    }
    if (
      page === "pillar-water-purification.html" ||
      page === "product-sani-amanzi.html" ||
      page.indexOf("blog-sani-amanzi") === 0
    ) {
      return "pillar-water-purification.html";
    }
    if (
      page === "pillar-shelf-stable-nutrition.html" ||
      page.indexOf("product-pilchards") === 0 ||
      page.indexOf("product-sardines") === 0 ||
      page.indexOf("product-tuna") === 0 ||
      page === "product-tonno-bonno.html"
    ) {
      return "pillar-shelf-stable-nutrition.html";
    }
    if (page === "pillar-hygiene-sanitation.html") {
      return "pillar-hygiene-sanitation.html";
    }
    if (page === "pillar-preparedness.html") {
      return "pillar-preparedness.html";
    }
    if (page === "case-studies.html" || page.indexOf("case-study-") === 0) {
      return "case-studies.html";
    }
    return null;
  }

  function applyNavActive() {
    const target = activeHref(fileName(window.location.pathname));
    if (!target) {
      return;
    }

    document.querySelectorAll(".header-area .mainmenu").forEach(function (menu) {
      menu.querySelectorAll(":scope > ul > li").forEach(function (item) {
        item.classList.remove("current-menu-item");
        const link = item.querySelector(":scope > a");
        if (!link) {
          return;
        }
        if (fileName(link.getAttribute("href") || "") === target) {
          item.classList.add("current-menu-item");
        }
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applyNavActive);
  } else {
    applyNavActive();
  }
})();
