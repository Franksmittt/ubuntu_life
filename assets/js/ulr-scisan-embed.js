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

  function isLocalPageLink(href) {
    if (!href || href.charAt(0) === "#") {
      return false;
    }
    if (/^(mailto:|tel:|javascript:)/i.test(href)) {
      return false;
    }
    if (/^https?:\/\//i.test(href)) {
      return /ubuntuliferesources\.co\.za/i.test(href);
    }
    return /\.html(?:[?#]|$)/i.test(href) || href.slice(-5) === ".html";
  }

  function wireParentNavigation(frame) {
    if (!frame || !frame.contentWindow) {
      return;
    }

    try {
      var doc = frame.contentWindow.document;
      doc.querySelectorAll("a[href]").forEach(function (anchor) {
        if (isBrochureAnchor(anchor) || anchor.dataset.ulrParentNavWired === "true") {
          return;
        }

        var href = anchor.getAttribute("href") || "";
        if (!isLocalPageLink(href)) {
          return;
        }

        anchor.dataset.ulrParentNavWired = "true";
        anchor.setAttribute("target", "_parent");
      });
    } catch (error) {
      // Same-origin iframe only.
    }
  }

  function wireBrochureLinks(frame) {
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
          requestBrochure(anchor.dataset.ulrBrochureName || anchor.textContent.trim());
        });
      });
    } catch (error) {
      // Same-origin iframe only; direct links remain as fallback.
    }
  }

  function lockIframeScroll(doc) {
    if (!doc || !doc.documentElement) {
      return;
    }

    var style = doc.getElementById("ulr-embed-scroll-lock");
    if (style) {
      return;
    }

    style = doc.createElement("style");
    style.id = "ulr-embed-scroll-lock";
    style.textContent =
      "html, body { overflow: hidden !important; height: auto !important; }";
    (doc.head || doc.documentElement).appendChild(style);
  }

  function getContentHeight(doc) {
    var body = doc.body;
    var html = doc.documentElement;
    var source = doc.querySelector(".ulr-scisan-source-page");

    return Math.ceil(
      Math.max(
        source ? source.scrollHeight : 0,
        source ? source.offsetHeight : 0,
        body ? body.scrollHeight : 0,
        body ? body.offsetHeight : 0,
        html ? html.scrollHeight : 0,
        html ? html.offsetHeight : 0
      )
    );
  }

  window.ulrInitScisanEmbed = function (frameId, options) {
    options = options || {};
    var frame = document.getElementById(frameId);

    if (!frame) {
      return null;
    }

    frame.setAttribute("scrolling", "no");

    var resizeTimer = null;
    var resizeObserver = null;

    function resizeFrame() {
      if (!frame.contentWindow) {
        return;
      }

      try {
        var doc = frame.contentWindow.document;
        lockIframeScroll(doc);
        var height = getContentHeight(doc);

        if (height > 0) {
          frame.style.height = height + "px";
          frame.style.minHeight = "0";
          window.dispatchEvent(new Event("resize"));
        }
      } catch (error) {
        // Keep the last known height if cross-origin access ever changes.
      }
    }

    function scheduleResize() {
      window.clearTimeout(resizeTimer);
      resizeTimer = window.setTimeout(resizeFrame, 50);
    }

    function observeContent() {
      if (resizeObserver || typeof ResizeObserver === "undefined") {
        return;
      }

      try {
        var doc = frame.contentWindow.document;
        var source = doc.querySelector(".ulr-scisan-source-page");

        resizeObserver = new ResizeObserver(scheduleResize);
        if (source) {
          resizeObserver.observe(source);
        }
        if (doc.body) {
          resizeObserver.observe(doc.body);
        }
      } catch (error) {
        // ResizeObserver is optional; timed resize calls still run.
      }
    }

    function refreshEmbed() {
      if (typeof options.onRefresh === "function") {
        options.onRefresh(frame);
      }
      resizeFrame();
      observeContent();
    }

    frame.addEventListener("load", function () {
      refreshEmbed();
      window.setTimeout(refreshEmbed, 100);
      window.setTimeout(refreshEmbed, 500);
      window.setTimeout(refreshEmbed, 1500);
    });

    window.addEventListener("resize", scheduleResize);

    return {
      resize: resizeFrame,
      refresh: refreshEmbed,
    };
  };

  var dedicatedFrames = {
    "ulr-scisan-agri-frame": true,
    "ulr-scisan-hygiene-frame": true,
  };

  document.querySelectorAll(".ulr-scisan-exact-page__frame").forEach(function (frame) {
    if (!frame.id || dedicatedFrames[frame.id]) {
      return;
    }

    window.ulrInitScisanEmbed(frame.id, {
      onRefresh: function (frame) {
        wireParentNavigation(frame);
        wireBrochureLinks(frame);
      },
    });
  });
})();
