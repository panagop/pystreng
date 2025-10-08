// Handle MathJax re-rendering on navigation
document.addEventListener('DOMContentLoaded', function() {
  // Render math on initial load
  if (window.MathJax && MathJax.typesetPromise) {
    MathJax.typesetPromise();
  }
});

// Handle instant navigation - multiple approaches for reliability
if (typeof document$ !== "undefined") {
  document$.subscribe(function() {
    // Add a small delay to ensure content is loaded
    setTimeout(function() {
      if (window.MathJax && MathJax.typesetPromise) {
        MathJax.typesetPromise();
      }
    }, 100);
  });
}

// Fallback: listen for location changes
(function() {
  let currentLocation = location.href;
  const observer = new MutationObserver(function() {
    if (location.href !== currentLocation) {
      currentLocation = location.href;
      setTimeout(function() {
        if (window.MathJax && MathJax.typesetPromise) {
          MathJax.typesetPromise();
        }
      }, 150);
    }
  });
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
})();

// Additional fallback: trigger on any content change
document.addEventListener('DOMSubtreeModified', function() {
  if (window.MathJax && MathJax.typesetPromise) {
    MathJax.typesetPromise();
  }
});