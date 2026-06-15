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

  function embedSrc(id) {
    return (
      "https://www.youtube.com/embed/" +
      id +
      "?rel=0&controls=1&modestbranding=1&enablejsapi=1"
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
    var src = embedSrc(id);

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

  function initAll() {
    document.querySelectorAll(".elementor-widget-video-playlist .e-tabs").forEach(initPlaylist);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll);
  } else {
    initAll();
  }
})();
