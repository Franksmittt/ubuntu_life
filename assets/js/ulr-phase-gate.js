/**
 * Ubuntu Life Resources — phased rollout gate.
 * Bump APPROVED_PHASE when the client signs off each tranche of pages.
 */
(function () {
  "use strict";

  /** Highest phase the client has approved (1 = home + food supply only). */
  var APPROVED_PHASE = 1;

  /** Pages open for review before their phase is fully approved. */
  var EARLY_ACCESS = {
    "pillar-water-purification.html": true,
  };

  /** Minimum phase required to view each page. */
  var PAGE_PHASE = {
    "index.html": 1,
    "": 1,
    "pillar-shelf-stable-nutrition.html": 1,

    "pillar-agri-biosecurity.html": 2,
    "pillar-water-purification.html": 2,
    "pillar-institutional-supply.html": 2,
    "pillars.html": 2,
    "products.html": 2,

    "about.html": 3,
    "contact.html": 3,
    "product-tonno-bonno.html": 3,
    "product-sani-amanzi.html": 3,
    "product-sani-99-agri.html": 3,
    "product-pilchards-tomato-sauce.html": 3,
    "product-pilchards-chilli-sauce.html": 3,
    "product-pilchards-vegetable-oil.html": 3,
    "product-sardines-tomato-sauce.html": 3,
    "product-sardines-chilli-sauce.html": 3,
    "product-sardines-vegetable-oil.html": 3,
    "product-tuna-chunks-in-brine.html": 3,
    "product-tuna-chunks-in-vegetable-oil.html": 3,
    "product-tuna-shredded-light-brine.html": 3,
    "product-tuna-shredded-light-vegetable-oil.html": 3,
    "product-tuna-shredded-light-olive-oil.html": 3,
  };

  var PHASE_LABELS = {
    1: "Phase 1 — Home & Strategic Food Supply",
    2: "Phase 2 — Core pillars & product catalogue",
    3: "Phase 3 — Product detail pages, about & contact",
  };

  function pageFile() {
    var path = window.location.pathname || "";
    var file = path.split("/").pop();
    if (!file || file.indexOf(".html") === -1) {
      return "index.html";
    }
    return file;
  }

  function requiredPhase(file) {
    if (Object.prototype.hasOwnProperty.call(PAGE_PHASE, file)) {
      return PAGE_PHASE[file];
    }
    if (file.indexOf("product-") === 0) {
      return 3;
    }
    return 2;
  }

  function isUnlocked(file) {
    if (EARLY_ACCESS[file]) {
      return true;
    }
    return requiredPhase(file) <= APPROVED_PHASE;
  }

  function gateMessage(required) {
    var prev = required - 1;
    return {
      title: "Complete Phase " + prev,
      lead:
        "This page is locked until Phase " +
        prev +
        " is reviewed and approved. We are publishing the site in stages so each section can be signed off before the next goes live.",
      phaseLabel: PHASE_LABELS[required] || "Next release",
    };
  }

  function buildGate(msg) {
    var root = document.createElement("div");
    root.className = "ulr-phase-gate";
    root.setAttribute("role", "dialog");
    root.setAttribute("aria-modal", "true");
    root.setAttribute("aria-labelledby", "ulr-phase-gate-title");

    root.innerHTML =
      '<div class="ulr-phase-gate__card">' +
      '<p class="ulr-phase-gate__eyebrow">Review in progress</p>' +
      "<h1 id=\"ulr-phase-gate-title\" class=\"ulr-phase-gate__title\">" +
      msg.title +
      "</h1>" +
      '<p class="ulr-phase-gate__lead">' +
      msg.lead +
      "</p>" +
      '<p class="ulr-phase-gate__next"><strong>Next unlock:</strong> ' +
      msg.phaseLabel +
      "</p>" +
      '<p class="ulr-phase-gate__open"><strong>Currently available:</strong> Home · Strategic Food Supply · Water Purification Solutions</p>' +
      '<div class="ulr-phase-gate__actions">' +
      '<a class="tj-primary-btn" href="index.html"><span class="btn-text"><span>Back to Home</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>' +
      '<a class="tj-primary-btn ulr-phase-gate__btn-secondary" href="pillar-shelf-stable-nutrition.html"><span class="btn-text"><span>Strategic Food Supply</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>' +
      "</div>" +
      "</div>";

    return root;
  }

  function applyGate() {
    var file = pageFile();
    if (isUnlocked(file)) {
      document.documentElement.classList.add("ulr-phase-open");
      return;
    }

    var msg = gateMessage(requiredPhase(file));
    document.documentElement.classList.add("ulr-phase-locked");

    var hide = document.getElementById("smooth-wrapper");
    if (!hide) {
      hide = document.querySelector("main");
    }
    if (hide) {
      hide.setAttribute("aria-hidden", "true");
    }

    var pre = document.querySelector(".tj-preloader");
    if (pre) {
      pre.classList.remove("is-loading");
      pre.style.display = "none";
    }

    document.body.appendChild(buildGate(msg));
    document.body.style.overflow = "hidden";
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applyGate);
  } else {
    applyGate();
  }

  window.ULR_PHASE_GATE = {
    approved: APPROVED_PHASE,
    pageFile: pageFile,
    requiredPhase: requiredPhase,
    isUnlocked: isUnlocked,
  };
})();
