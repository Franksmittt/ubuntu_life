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

  function youtubeEmbedId(url) {
    if (!url) {
      return "";
    }

    var match = String(url).match(
      /(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|shorts\/))([A-Za-z0-9_-]{6,})/
    );
    return match ? match[1] : "";
  }

  function buildVideoEmbed(url) {
    var id = youtubeEmbedId(url);
    if (!id) {
      return null;
    }

    var wrapper = document.createElement("div");
    wrapper.className = "e-tab-content-video ulr-scisan-video-embed";
    wrapper.innerHTML =
      '<div class="elementor-wrapper elementor-fit-aspect-ratio elementor-aspect-ratio-169">' +
      '<iframe class="elementor-video-iframe" title="YouTube video" ' +
      'src="https://www.youtube.com/embed/' +
      id +
      '?rel=0&controls=1&modestbranding=1" ' +
      'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" ' +
      'allowfullscreen loading="lazy"></iframe></div>';
    return wrapper;
  }

  function activatePlaylistTab(playlist, tabIndex) {
    var titles = playlist.querySelectorAll(".e-tab-title");
    var panels = playlist.querySelectorAll(".e-tab-content");

    titles.forEach(function (title) {
      var selected = title.getAttribute("data-tab") === tabIndex;
      title.setAttribute("aria-selected", selected ? "true" : "false");
      title.setAttribute("tabindex", selected ? "0" : "-1");
    });

    panels.forEach(function (panel) {
      var selected = panel.getAttribute("data-tab") === tabIndex;
      if (selected) {
        panel.removeAttribute("hidden");
        var holder = panel.querySelector(":scope > div");
        var url = panel.getAttribute("data-video-url");
        if (holder && url && !panel.querySelector(".ulr-scisan-video-embed")) {
          holder.innerHTML = "";
          var embed = buildVideoEmbed(url);
          if (embed) {
            holder.appendChild(embed);
          }
        }
      } else {
        panel.setAttribute("hidden", "hidden");
      }
    });
  }

  function wireVideoPlaylist() {
    if (!scisanFrame || !scisanFrame.contentWindow) {
      return;
    }

    try {
      var doc = scisanFrame.contentWindow.document;
      doc.querySelectorAll(".elementor-widget-video-playlist .e-tabs").forEach(function (playlist) {
        if (playlist.dataset.ulrPlaylistWired === "true") {
          return;
        }

        playlist.dataset.ulrPlaylistWired = "true";
        var titles = playlist.querySelectorAll(".e-tab-title");
        titles.forEach(function (title) {
          var tabIndex = title.getAttribute("data-tab");
          var activate = function (event) {
            if (event) {
              event.preventDefault();
            }
            activatePlaylistTab(playlist, tabIndex);
            resizeScisanFrame();
          };

          title.addEventListener("click", activate);
          var button = title.querySelector("button");
          if (button) {
            button.addEventListener("click", activate);
          }
        });

        if (titles[0]) {
          activatePlaylistTab(playlist, titles[0].getAttribute("data-tab"));
        }
      });
    } catch (error) {
      // Keep rendered HTML/CSS fixes as fallback if access changes.
    }
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
      wireVideoPlaylist();
      wireScisanBrochureLinks();
      resizeScisanFrame();
      window.setTimeout(function () {
        fixScisanEmbedContent();
        wireVideoPlaylist();
        resizeScisanFrame();
      }, 500);
      window.setTimeout(function () {
        fixScisanEmbedContent();
        wireVideoPlaylist();
        wireScisanBrochureLinks();
        resizeScisanFrame();
      }, 1500);
    });
    window.addEventListener("resize", resizeScisanFrame);
  }
})();
