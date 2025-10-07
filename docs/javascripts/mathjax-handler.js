// Handle MathJax re-rendering on navigation
document.addEventListener('DOMContentLoaded', function() {
  // Render math on initial load
  if (window.MathJax && MathJax.typesetPromise) {
    MathJax.typesetPromise();
  }
});

// Handle instant navigation
if (typeof document$ !== "undefined") {
  document$.subscribe(function() {
    if (window.MathJax && MathJax.typesetPromise) {
      MathJax.typesetPromise();
    }
  });
}