(function () {
  "use strict";

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
})();
