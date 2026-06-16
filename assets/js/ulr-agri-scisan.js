(function () {
  "use strict";

  function requestBrochure(brochureName) {
    var trigger = document.createElement("button");
    trigger.type = "button";
    trigger.className = "js-request-brochure";
    trigger.setAttribute("data-brochure-name", brochureName || "SANI-99 for AGRI Brochure");
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
      text.trim().toLowerCase() === "brochure"
    );
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
        anchor.addEventListener("click", function (event) {
          event.preventDefault();
          requestBrochure(anchor.dataset.ulrBrochureName || "SANI-99 for AGRI Brochure");
        });
      });
    } catch (error) {
      // The iframe is same-origin locally; keep the direct links as a fallback if access changes.
    }
  }

  if (typeof window.ulrInitScisanEmbed === "function") {
    window.ulrInitScisanEmbed("ulr-scisan-agri-frame", {
      onRefresh: function (frame) {
        wireScisanBrochureLinks(frame);
      },
    });
  }

  document.querySelectorAll(".ulr-amanzi-scisan-flip").forEach(function (btn) {
    btn.addEventListener("click", function () {
      btn.classList.toggle("is-flipped");
    });
  });
})();
