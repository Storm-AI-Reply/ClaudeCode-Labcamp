/**
 * Open external links (e.g., Anthropic docs, python.org) in a new tab so the
 * labcamp page stays open. Re-runs on Material instant navigation.
 */
(function () {
  function markExternalLinks() {
    var root = document.querySelector(".md-content");
    if (!root) return;

    root.querySelectorAll('a[href^="http"]').forEach(function (a) {
      if (a.getAttribute("target")) return;
      try {
        var url = new URL(a.href);
        if (url.origin !== window.location.origin) {
          a.setAttribute("target", "_blank");
          a.setAttribute("rel", "noopener noreferrer");
        }
      } catch (e) {
        /* ignore */
      }
    });
  }

  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(markExternalLinks);
  } else {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", markExternalLinks);
    } else {
      markExternalLinks();
    }
  }
})();
