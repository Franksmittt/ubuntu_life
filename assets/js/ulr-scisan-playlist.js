(function () {
  "use strict";

  function youtubeId(url) {
    if (!url) {
      return "";
    }

    var match = String(url).match(
      /(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|shorts\/))([A-Za-z0-9_-]{6,})/
    );
    return match ? match[1] : "";
  }

  function parseDataSettings(element) {
    if (!element) {
      return {};
    }

    var raw = element.getAttribute("data-settings");
    if (!raw) {
      return {};
    }

    try {
      return JSON.parse(
        raw
          .replace(/&quot;/g, '"')
          .replace(/&amp;/g, "&")
          .replace(/&#39;/g, "'")
          .replace(/\\\//g, "/")
      );
    } catch (error) {
      return {};
    }
  }

  function youtubeEmbedSrc(id, settings) {
    var params = ["rel=0", "controls=1", "modestbranding=1", "enablejsapi=1"];

    if (!settings || settings.autoplay === "yes" || settings.mute === "yes") {
      params.push("autoplay=1");
      params.push("mute=1");
    }

    if (settings && settings.loop === "yes") {
      params.push("loop=1");
      params.push("playlist=" + id);
    }

    return "https://www.youtube.com/embed/" + id + "?" + params.join("&");
  }

  function buildYoutubeEmbed(id, settings) {
    return (
      '<div class="ulr-scisan-video-embed">' +
      '<div class="elementor-wrapper elementor-fit-aspect-ratio elementor-aspect-ratio-169 elementor-open-inline">' +
      '<iframe class="elementor-video-iframe" title="YouTube video" src="' +
      youtubeEmbedSrc(id, settings) +
      '" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen loading="lazy"></iframe>' +
      "</div></div>"
    );
  }

  function panelHolder(panel) {
    var holder = panel.firstElementChild;
    if (!holder) {
      holder = document.createElement("div");
      panel.appendChild(holder);
    }
    return holder;
  }

  function ensureVideo(panel) {
    var url = panel.getAttribute("data-video-url");
    var id = youtubeId(url);
    if (!id) {
      return;
    }

    var holder = panelHolder(panel);
    var iframe = holder.querySelector("iframe");
    var src = youtubeEmbedSrc(id, { autoplay: "yes", mute: "yes" });

    if (!iframe) {
      holder.innerHTML =
        '<div class="e-tab-content-video ulr-scisan-video-embed">' +
        '<div class="elementor-wrapper elementor-fit-aspect-ratio elementor-aspect-ratio-169">' +
        '<iframe class="elementor-video-iframe" title="YouTube video" src="' +
        src +
        '" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen loading="lazy"></iframe>' +
        "</div></div>";
      return;
    }

    if ((iframe.getAttribute("src") || "") !== src) {
      iframe.setAttribute("src", src);
    }
  }

  function activateTab(playlist, tabIndex) {
    var key = String(tabIndex);

    playlist.querySelectorAll(".e-tab-title").forEach(function (title) {
      var selected = title.getAttribute("data-tab") === key;
      title.setAttribute("aria-selected", selected ? "true" : "false");
      title.setAttribute("tabindex", selected ? "0" : "-1");
      title.classList.toggle("e-active", selected);
    });

    playlist.querySelectorAll(".e-tabs-content-wrapper > .e-tab-content").forEach(function (panel) {
      var selected = panel.getAttribute("data-tab") === key;
      if (selected) {
        panel.removeAttribute("hidden");
        panel.classList.add("ulr-scisan-tab-active");
        panel.style.display = "block";
        ensureVideo(panel);
      } else {
        panel.setAttribute("hidden", "hidden");
        panel.classList.remove("ulr-scisan-tab-active");
        panel.style.display = "none";
      }
    });
  }

  function initPlaylist(playlist) {
    if (playlist.dataset.ulrPlaylistReady === "true") {
      return;
    }

    playlist.dataset.ulrPlaylistReady = "true";

    playlist.addEventListener("click", function (event) {
      var title = event.target.closest(".e-tab-title");
      if (!title || !playlist.contains(title)) {
        return;
      }

      event.preventDefault();
      var tabIndex = title.getAttribute("data-tab");
      if (tabIndex) {
        activateTab(playlist, tabIndex);
      }
    });

    var firstTitle = playlist.querySelector(".e-tab-title");
    if (firstTitle) {
      activateTab(playlist, firstTitle.getAttribute("data-tab"));
    }
  }

  function initYoutubeWidgets(root) {
    root.querySelectorAll(".elementor-widget-video").forEach(function (widget) {
      if (widget.closest(".elementor-widget-video-playlist")) {
        return;
      }

      var settings = parseDataSettings(widget);
      if (settings.video_type !== "youtube" || !settings.youtube_url) {
        return;
      }

      var id = youtubeId(settings.youtube_url);
      if (!id) {
        return;
      }

      var wrapper = widget.querySelector(".elementor-wrapper");
      var videoNode = widget.querySelector(".elementor-video");
      if (!wrapper || (videoNode && videoNode.querySelector("iframe"))) {
        return;
      }

      wrapper.innerHTML = buildYoutubeEmbed(id, settings);
    });
  }

  function initBackgroundVideos(root) {
    root.querySelectorAll("[data-settings]").forEach(function (element) {
      var settings = parseDataSettings(element);
      if (!settings.background_video_link) {
        return;
      }

      var video = element.querySelector("video.elementor-background-video-hosted");
      if (!video || video.getAttribute("src")) {
        return;
      }

      video.setAttribute("src", settings.background_video_link);
      video.muted = true;
      video.defaultMuted = true;
      video.playsInline = true;

      var playPromise = video.play();
      if (playPromise && typeof playPromise.catch === "function") {
        playPromise.catch(function () {
          // Autoplay may still be blocked until the user interacts.
        });
      }
    });
  }

  function initHostedVideos(root) {
    root.querySelectorAll("video.elementor-video[src]").forEach(function (video) {
      if (video.hasAttribute("autoplay")) {
        video.muted = true;
        video.defaultMuted = true;
        video.playsInline = true;
      }

      var playPromise = video.play();
      if (playPromise && typeof playPromise.catch === "function") {
        playPromise.catch(function () {
          // Leave controls available through native video UI if autoplay fails.
        });
      }
    });
  }

  function initAll() {
    var root = document.querySelector(".ulr-scisan-source-page") || document;
    initBackgroundVideos(root);
    initHostedVideos(root);
    initYoutubeWidgets(root);
    root.querySelectorAll(".elementor-widget-video-playlist .e-tabs").forEach(initPlaylist);
  }

  window.ulrInitScisanMedia = initAll;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll);
  } else {
    initAll();
  }
})();
