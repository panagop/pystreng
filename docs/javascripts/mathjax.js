window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

// Wait for MathJax to load, then set up navigation handling
document.addEventListener('DOMContentLoaded', function() {
  // Handle Material for MkDocs instant navigation
  if (typeof app !== "undefined") {
    app.document$.subscribe(function() {
      MathJax.startup.promise.then(function() {
        return MathJax.typesetPromise();
      });
    });
  }
});