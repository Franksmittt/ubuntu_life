(function () {
  "use strict";

  var scisanFrame = document.getElementById("ulr-scisan-hygiene-frame");

  function requestBrochure(brochureName) {
    var trigger = document.createElement("button");
    trigger.type = "button";
    trigger.className = "js-request-brochure";
    trigger.setAttribute("data-brochure-name", brochureName || "SANI-99 Brochure");
    trigger.hidden = true;
    document.body.appendChild(trigger);
    trigger.click();
    trigger.remove();
  }

  function isBrochureAnchor(anchor) {
    var href = anchor.getAttribute("href") || "";
    var text = anchor.textContent || "";

    return (
      anchor.hasAttribute("data-ulr-brochure-name") ||
      (href.indexOf("SANI-99") !== -1 && href.toLowerCase().indexOf("brochure") !== -1) ||
      text.trim().toLowerCase() === "brochure" ||
      text.toLowerCase().indexOf("brochure") !== -1
    );
  }

  function wireScisanBrochureLinks() {
    if (!scisanFrame || !scisanFrame.contentWindow) {
      return;
    }

    try {
      var doc = scisanFrame.contentWindow.document;
      doc.querySelectorAll("a").forEach(function (anchor) {
        if (!isBrochureAnchor(anchor) || anchor.dataset.ulrBrochureWired === "true") {
          return;
        }

        anchor.dataset.ulrBrochureWired = "true";
        anchor.removeAttribute("target");
        anchor.setAttribute("href", "#request-brochure");
        anchor.addEventListener("click", function (event) {
          event.preventDefault();
          requestBrochure(anchor.dataset.ulrBrochureName || "SANI-99 Brochure");
        });
      });
    } catch (error) {
      // The iframe is same-origin locally; keep the direct links as a fallback if access changes.
    }
  }

  function resizeScisanFrame() {
    if (!scisanFrame || !scisanFrame.contentWindow) {
      return;
    }

    try {
      var doc = scisanFrame.contentWindow.document;
      var body = doc.body;
      var html = doc.documentElement;
      var height = Math.max(
        body ? body.scrollHeight : 0,
        body ? body.offsetHeight : 0,
        html ? html.clientHeight : 0,
        html ? html.scrollHeight : 0,
        html ? html.offsetHeight : 0
      );

      if (height) {
        scisanFrame.style.height = height + "px";
      }
    } catch (error) {
      scisanFrame.style.minHeight = "12000px";
    }
  }

  function fixScisanEmbedContent() {
    if (!scisanFrame || !scisanFrame.contentWindow) {
      return;
    }

    try {
      var doc = scisanFrame.contentWindow.document;

      doc.querySelectorAll(".elementor-invisible").forEach(function (node) {
        node.classList.remove("elementor-invisible");
      });

      doc.querySelectorAll(".eael-animate-zoom-in, .eael-animate-flip").forEach(function (node) {
        node.classList.remove("eael-animate-zoom-in", "eael-animate-flip");
      });
    } catch (error) {
      // Keep rendered HTML/CSS fixes as fallback.
    }
  }

  if (scisanFrame) {
    scisanFrame.addEventListener("load", function () {
      fixScisanEmbedContent();
      wireScisanBrochureLinks();
      resizeScisanFrame();
      window.setTimeout(function () {
        fixScisanEmbedContent();
        resizeScisanFrame();
      }, 500);
      window.setTimeout(function () {
        fixScisanEmbedContent();
        wireScisanBrochureLinks();
        resizeScisanFrame();
      }, 1500);
    });
    window.addEventListener("resize", resizeScisanFrame);
  }
})();
