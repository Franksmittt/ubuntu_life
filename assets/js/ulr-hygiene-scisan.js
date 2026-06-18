(function () {
  "use strict";

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

  function normalizeBrochureCopy(anchor) {
    var textNode = anchor.querySelector(".elementor-button-text");
    if (!textNode) {
      return;
    }

    var text = textNode.textContent || "";
    if (/^download\b/i.test(text)) {
      textNode.textContent = text.replace(/^Download/i, "Request");
    } else if (text.trim().toUpperCase() === "BROCHURE") {
      textNode.textContent = "REQUEST BROCHURE";
    }
  }

  function wireScisanBrochureLinks(frame) {
    if (!frame || !frame.contentWindow) {
      return;
    }

    try {
      var doc = frame.contentWindow.document;
      doc.querySelectorAll("a").forEach(function (anchor) {
        if (!isBrochureAnchor(anchor) || anchor.dataset.ulrBrochureWired === "true") {
          return;
        }

        anchor.dataset.ulrBrochureWired = "true";
        anchor.removeAttribute("target");
        anchor.setAttribute("href", "#request-brochure");
        normalizeBrochureCopy(anchor);
        anchor.addEventListener("click", function (event) {
          event.preventDefault();
          requestBrochure(anchor.dataset.ulrBrochureName || "SANI-99 Brochure");
        });
      });
    } catch (error) {
      // The iframe is same-origin locally; keep the direct links as a fallback if access changes.
    }
  }

  function fixScisanEmbedContent(frame) {
    if (!frame || !frame.contentWindow) {
      return;
    }

    try {
      var doc = frame.contentWindow.document;

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

  if (typeof window.ulrInitScisanEmbed === "function") {
    window.ulrInitScisanEmbed("ulr-scisan-hygiene-frame", {
      onRefresh: function (frame) {
        fixScisanEmbedContent(frame);
        wireScisanBrochureLinks(frame);
      },
    });
  }
})();
