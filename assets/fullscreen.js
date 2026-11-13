document.addEventListener("click", (event) => {
  const button = event.target.closest("[data-fullscreen]");
  if (!button) return;
  button.closest("div")?.querySelector("iframe")?.requestFullscreen();
});
