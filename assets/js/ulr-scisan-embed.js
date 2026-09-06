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

  var CREDENTIAL_FRAME_IDS = {
    "ulr-scisan-amanzi-frame": true,
    "ulr-scisan-hygiene-frame": true,
    "ulr-scisan-agri-frame": true,
  };

  var CREDENTIAL_STRIP_CSS =
    ".ulr-embed-creds{box-sizing:border-box;width:100%;margin:0;padding:1.15rem 1.25rem 1.35rem;background:linear-gradient(180deg,#f4f8fb 0%,#eef5eb 100%);border-top:1px solid rgba(11,46,79,.08);border-bottom:1px solid rgba(11,46,79,.08);font-family:Poppins,Montserrat,Arial,sans-serif;}" +
    ".ulr-embed-creds *,.ulr-embed-creds *::before,.ulr-embed-creds *::after{box-sizing:border-box;}" +
    ".ulr-embed-creds__inner{max-width:1280px;margin:0 auto;}" +
    ".ulr-embed-creds__kicker{margin:0 auto .85rem;max-width:48rem;text-align:center;font-size:.92rem;line-height:1.5;color:#0b2e4f;}" +
    ".ulr-embed-creds__kicker a{color:#256029;font-weight:600;text-decoration:none;}" +
    ".ulr-embed-creds__kicker a:hover{color:#0b5fa5;}" +
    ".ulr-embed-creds__list{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.75rem;margin:0;padding:0;}" +
    ".ulr-embed-creds__item{margin:0;padding:.9rem 1rem 1rem;border-radius:12px;background:#fff;border:1px solid #e2e6ea;box-shadow:0 6px 18px rgba(11,46,79,.05);}" +
    ".ulr-embed-creds__item dt{margin:0 0 .25rem;font-size:.68rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#2e7d32;}" +
    ".ulr-embed-creds__item dd{margin:0;font-size:.92rem;font-weight:600;line-height:1.4;color:#0b2e4f;}" +
    ".ulr-embed-creds__item dd span{display:block;margin-top:.15rem;font-size:.8rem;font-weight:400;color:#525a63;}" +
    "@media (max-width:991px){.ulr-embed-creds__list{grid-template-columns:repeat(2,minmax(0,1fr));}}" +
    "@media (max-width:575px){.ulr-embed-creds{padding:1rem .9rem 1.15rem;}.ulr-embed-creds__list{grid-template-columns:1fr;}}";

  function injectCredentialsStrip(frame) {
    if (!frame || !CREDENTIAL_FRAME_IDS[frame.id] || !frame.contentWindow) {
      return;
    }

    try {
      var doc = frame.contentWindow.document;
      if (!doc || !doc.body) {
        return;
      }

      if (doc.getElementById("ulr-embed-creds")) {
        return;
      }

      if (!doc.getElementById("ulr-embed-creds-style")) {
        var style = doc.createElement("style");
        style.id = "ulr-embed-creds-style";
        style.textContent = CREDENTIAL_STRIP_CSS;
        (doc.head || doc.documentElement).appendChild(style);
      }

      var strip = doc.createElement("section");
      strip.id = "ulr-embed-creds";
      strip.className = "ulr-embed-creds";
      strip.setAttribute("aria-label", "Ubuntu Life Resources registrations");
      strip.innerHTML =
        '<div class="ulr-embed-creds__inner">' +
        '<p class="ulr-embed-creds__kicker">Supplied by Ubuntu Life Resources — a registered <a href="about.html#registrations" target="_parent">UNGM and UNICEF vendor</a>, and corporate member of IWA and WISA.</p>' +
        '<dl class="ulr-embed-creds__list">' +
        '<div class="ulr-embed-creds__item"><dt>UNGM</dt><dd>5618342<span>United Nations Global Marketplace</span></dd></div>' +
        '<div class="ulr-embed-creds__item"><dt>UNICEF</dt><dd>Vendor UNGM 5618343<span>Registered vendor</span></dd></div>' +
        '<div class="ulr-embed-creds__item"><dt>IWA</dt><dd>16142154<span>International Water Association</span></dd></div>' +
        '<div class="ulr-embed-creds__item"><dt>WISA</dt><dd>10242<span>Water Institute of Southern Africa</span></dd></div>' +
        "</dl></div>";

      var hero =
        doc.querySelector('[data-id="76af5ff"]') ||
        doc.querySelector(".ulr-scisan-source-page .e-con.e-parent");
      var host = hero && hero.parentNode ? hero.parentNode : doc.querySelector(".ulr-scisan-source-page");

      if (hero && hero.parentNode) {
        if (hero.nextSibling) {
          hero.parentNode.insertBefore(strip, hero.nextSibling);
        } else {
          hero.parentNode.appendChild(strip);
        }
      } else if (host) {
        host.insertBefore(strip, host.firstChild);
      } else {
        doc.body.insertBefore(strip, doc.body.firstChild);
      }
    } catch (error) {
      // Same-origin iframe only.
    }
  }

  function refreshIframeMedia(frame) {
    if (!frame || !frame.contentWindow) {
      return;
    }

    try {
      if (typeof frame.contentWindow.ulrInitScisanMedia === "function") {
        frame.contentWindow.ulrInitScisanMedia();
      }
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
    var elementor = doc.querySelector(".elementor");

    return Math.ceil(
      Math.max(
        source ? source.scrollHeight : 0,
        source ? source.offsetHeight : 0,
        elementor ? elementor.scrollHeight : 0,
        elementor ? elementor.offsetHeight : 0,
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
      injectCredentialsStrip(frame);
      refreshIframeMedia(frame);
      resizeFrame();
      observeContent();
    }

    frame.addEventListener("load", function () {
      refreshEmbed();
      [100, 500, 1500, 3000, 5000, 8000].forEach(function (delay) {
        window.setTimeout(refreshEmbed, delay);
      });
    });

    try {
      var doc = frame.contentDocument || frame.contentWindow.document;
      if (doc && doc.readyState === "complete") {
        refreshEmbed();
        [100, 500, 1500, 3000, 5000, 8000].forEach(function (delay) {
          window.setTimeout(refreshEmbed, delay);
        });
      }
    } catch (error) {
      // Wait for load if the iframe is not accessible yet.
    }

    window.addEventListener("resize", scheduleResize);

    return {
      resize: resizeFrame,
      refresh: refreshEmbed,
    };
  };

  var dedicatedFrameIds = {
    "ulr-scisan-agri-frame": true,
    "ulr-scisan-hygiene-frame": true,
  };

  function initEmbedFrame(frameId, options) {
    if (!document.getElementById(frameId)) {
      return;
    }

    window.ulrInitScisanEmbed(frameId, options || {
      onRefresh: function (frame) {
        wireParentNavigation(frame);
        wireBrochureLinks(frame);
      },
    });
  }

  initEmbedFrame("ulr-scisan-agri-frame");
  initEmbedFrame("ulr-scisan-hygiene-frame");

  document.querySelectorAll(".ulr-scisan-exact-page__frame").forEach(function (frame) {
    if (!frame.id || dedicatedFrameIds[frame.id]) {
      return;
    }

    initEmbedFrame(frame.id);
  });
})();
