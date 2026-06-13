(function () {
  "use strict";

  var scisanFrame = document.getElementById("ulr-scisan-agri-frame");

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

  if (scisanFrame) {
    scisanFrame.addEventListener("load", function () {
      resizeScisanFrame();
      window.setTimeout(resizeScisanFrame, 500);
      window.setTimeout(resizeScisanFrame, 1500);
    });
    window.addEventListener("resize", resizeScisanFrame);
  }

  document.querySelectorAll(".ulr-amanzi-scisan-flip").forEach(function (btn) {
    btn.addEventListener("click", function () {
      btn.classList.toggle("is-flipped");
    });
  });
})();
