(function () {
  "use strict";

  function requestBrochure(brochureName) {
    var trigger = document.createElement("button");
    trigger.type = "button";
    trigger.className = "js-request-brochure";
    trigger.setAttribute("data-brochure-name", brochureName || "Product brochure");
    trigger.hidden = true;
    document.body.appendChild(trigger);
    trigger.click();
    trigger.remove();
  }

  function isBrochureAnchor(anchor) {
    var href = anchor.getAttribute("href") || "";
    var text = (anchor.textContent || "").trim().toLowerCase();

    return (
      anchor.hasAttribute("data-ulr-brochure-name") ||
      (href.indexOf("brochure") !== -1 && /\.pdf|SANI|CuGROW/i.test(href)) ||
      text === "brochure" ||
      text.indexOf("download our brochure") !== -1
    );
  }

  function wireBrochureLinks(doc) {
    doc.querySelectorAll("a").forEach(function (anchor) {
      if (!isBrochureAnchor(anchor) || anchor.dataset.ulrBrochureWired === "true") {
        return;
      }

      anchor.dataset.ulrBrochureWired = "true";
      anchor.removeAttribute("target");
      anchor.setAttribute("href", "#request-brochure");
      anchor.addEventListener("click", function (event) {
        event.preventDefault();
        requestBrochure(anchor.dataset.ulrBrochureName || anchor.textContent.trim());
      });
    });
  }

  function resizeFrame(frame) {
    if (!frame || !frame.contentWindow) {
      return;
    }

    try {
      var doc = frame.contentWindow.document;
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
        frame.style.height = height + "px";
      }
    } catch (error) {
      frame.style.minHeight = "12000px";
    }
  }

  function wireFrame(frame) {
    if (!frame || frame.dataset.ulrScisanWired === "true") {
      return;
    }

    frame.dataset.ulrScisanWired = "true";
    frame.addEventListener("load", function () {
      try {
        wireBrochureLinks(frame.contentWindow.document);
      } catch (error) {
        /* same-origin only */
      }
      resizeFrame(frame);
      window.setTimeout(function () {
        resizeFrame(frame);
      }, 500);
      window.setTimeout(function () {
        resizeFrame(frame);
        try {
          wireBrochureLinks(frame.contentWindow.document);
        } catch (error) {
          /* noop */
        }
      }, 1500);
    });
  }

  document.querySelectorAll(".ulr-scisan-exact-page__frame").forEach(wireFrame);
  window.addEventListener("resize", function () {
    document.querySelectorAll(".ulr-scisan-exact-page__frame").forEach(resizeFrame);
  });
})();
