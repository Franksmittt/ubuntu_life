/**
 * Ubuntu Life Resources — phased rollout gate.
 * Bump APPROVED_PHASE when the client signs off each tranche of pages.
 */
(function () {
  "use strict";

  /** Highest phase the client has approved (3 = all pages unlocked). */
  var APPROVED_PHASE = 3;

  /** Pages open for review before their phase is fully approved. */
  var EARLY_ACCESS = {
    "pillar-water-purification.html": true,
    "pillar-agri-biosecurity.html": true,
    "pillar-hygiene-sanitation.html": true,
    "blog.html": true,
    "blog-sani-amanzi-point-of-use-water.html": true,
  };

  /** Pages temporarily held back while content changes are in progress. */
  var SOFT_LOCKED_PAGES = {};

  /** Soft password preview — unlock persists for the browser session only. */
  var PASSWORD_LOCKED_PAGES = {
    "pillar-preparedness.html": {
      password: "85879",
      storageKey: "ulr-preparedness-unlock",
      title: "Preparedness preview",
      lead:
        "This preparedness page is in preview. Enter the password to view it while updates are in progress.",
    },
  };

  /** Hash routes temporarily held back while content changes are in progress. */
  var SOFT_LOCKED_ROUTES = {};

  /** Minimum phase required to view each page. */
  var PAGE_PHASE = {
    "index.html": 1,
    "": 1,
    "pillar-shelf-stable-nutrition.html": 1,
    "pillar-agri-biosecurity.html": 1,
    "pillar-hygiene-sanitation.html": 1,

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

  function routeKey(file) {
    var hash = (window.location.hash || "").replace(/^#/, "");
    return hash ? file + "#" + hash : file;
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

  function isPasswordUnlocked(file) {
    var config = PASSWORD_LOCKED_PAGES[file];
    if (!config) {
      return true;
    }

    try {
      return sessionStorage.getItem(config.storageKey) === "1";
    } catch (error) {
      return false;
    }
  }

  function setPasswordUnlocked(file) {
    var config = PASSWORD_LOCKED_PAGES[file];
    if (!config) {
      return;
    }

    try {
      sessionStorage.setItem(config.storageKey, "1");
    } catch (error) {
      // Ignore storage failures; gate will prompt again on reload.
    }
  }

  function isUnlocked(file) {
    if (PASSWORD_LOCKED_PAGES[file] && !isPasswordUnlocked(file)) {
      return false;
    }
    if (SOFT_LOCKED_ROUTES[routeKey(file)]) {
      return false;
    }
    if (SOFT_LOCKED_PAGES[file]) {
      return false;
    }
    if (EARLY_ACCESS[file]) {
      return true;
    }
    return requiredPhase(file) <= APPROVED_PHASE;
  }

  function gateMessage(file, required) {
    var key = routeKey(file);
    if (SOFT_LOCKED_ROUTES[key]) {
      return SOFT_LOCKED_ROUTES[key];
    }
    if (SOFT_LOCKED_PAGES[file]) {
      return SOFT_LOCKED_PAGES[file];
    }

    var prev = required - 1;
    return {
      title: "Complete Phase " + prev,
      lead:
        "This page is locked until Phase " +
        prev +
        " is reviewed and approved. We are publishing the site in stages so each section can be signed off before the next goes live.",
      phaseLabel: PHASE_LABELS[required] || "Next release",
      currentlyAvailable:
        "Home · Strategic Food Supply · Water Purification Solutions · Agricultural Biosecurity · Insights (blog)",
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
      '<p class="ulr-phase-gate__open"><strong>Currently available:</strong> ' +
      msg.currentlyAvailable +
      "</p>" +
      '<div class="ulr-phase-gate__actions">' +
      '<a class="tj-primary-btn" href="index.html"><span class="btn-text"><span>Back to Home</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>' +
      '<a class="tj-primary-btn ulr-phase-gate__btn-secondary" href="pillar-shelf-stable-nutrition.html"><span class="btn-text"><span>Strategic Food Supply</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>' +
      "</div>" +
      "</div>";

    return root;
  }

  function buildPasswordGate(config) {
    var root = document.createElement("div");
    root.className = "ulr-phase-gate ulr-phase-gate--password";
    root.setAttribute("role", "dialog");
    root.setAttribute("aria-modal", "true");
    root.setAttribute("aria-labelledby", "ulr-phase-gate-title");

    root.innerHTML =
      '<div class="ulr-phase-gate__card">' +
      '<p class="ulr-phase-gate__eyebrow">Preview access</p>' +
      "<h1 id=\"ulr-phase-gate-title\" class=\"ulr-phase-gate__title\">" +
      config.title +
      "</h1>" +
      '<p class="ulr-phase-gate__lead">' +
      config.lead +
      "</p>" +
      '<form class="ulr-phase-gate__password-form" autocomplete="off">' +
      '<label class="ulr-phase-gate__password-label" for="ulr-phase-gate-password">Password</label>' +
      '<input id="ulr-phase-gate-password" class="ulr-phase-gate__password-input" type="password" inputmode="numeric" autocomplete="off" required />' +
      '<p class="ulr-phase-gate__error" role="alert" hidden>Incorrect password. Please try again.</p>' +
      '<div class="ulr-phase-gate__actions">' +
      '<button type="submit" class="tj-primary-btn"><span class="btn-text"><span>View page</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></button>' +
      '<a class="tj-primary-btn ulr-phase-gate__btn-secondary" href="index.html"><span class="btn-text"><span>Back to Home</span></span><span class="btn-icon"><i class="tji-arrow-right-long"></i></span></a>' +
      "</div>" +
      "</form>" +
      "</div>";

    var form = root.querySelector(".ulr-phase-gate__password-form");
    var input = root.querySelector("#ulr-phase-gate-password");
    var error = root.querySelector(".ulr-phase-gate__error");

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (input.value === config.password) {
        setPasswordUnlocked(pageFile());
        applyGate();
        return;
      }

      error.hidden = false;
      error.textContent = "Incorrect password. Please try again.";
      input.focus();
      input.select();
    });

    window.setTimeout(function () {
      if (input) {
        input.focus();
      }
    }, 0);

    return root;
  }

  function applyGate() {
    var file = pageFile();
    if (isUnlocked(file)) {
      document.documentElement.classList.remove("ulr-phase-locked");
      document.documentElement.classList.add("ulr-phase-open");
      var existing = document.querySelector(".ulr-phase-gate");
      if (existing) {
        existing.remove();
      }
      var visible = document.getElementById("smooth-wrapper");
      if (!visible) {
        visible = document.querySelector("main");
      }
      if (visible) {
        visible.removeAttribute("aria-hidden");
      }
      document.body.style.overflow = "";
      return;
    }

    var msg = gateMessage(file, requiredPhase(file));
    document.documentElement.classList.remove("ulr-phase-open");
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

    var currentGate = document.querySelector(".ulr-phase-gate");
    if (currentGate) {
      currentGate.remove();
    }

    var passwordConfig = PASSWORD_LOCKED_PAGES[file];
    if (passwordConfig && !isPasswordUnlocked(file)) {
      document.body.appendChild(buildPasswordGate(passwordConfig));
    } else {
      document.body.appendChild(buildGate(msg));
    }
    document.body.style.overflow = "hidden";
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applyGate);
  } else {
    applyGate();
  }
  window.addEventListener("hashchange", applyGate);

  window.ULR_PHASE_GATE = {
    approved: APPROVED_PHASE,
    pageFile: pageFile,
    routeKey: routeKey,
    requiredPhase: requiredPhase,
    isUnlocked: isUnlocked,
  };
})();
