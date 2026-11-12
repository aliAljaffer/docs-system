/* Pan and zoom controls for Excalidraw SVG diagrams. */
(() => {
  const PZ = window.Panzoom || window.panzoom;
  if (!PZ) return;

  const shells = [...document.querySelectorAll(".diagram-zoom")];

  function track(action) {
    if (window.umami && typeof window.umami.track === "function") {
      window.umami.track("diagram-zoom", { action, path: location.pathname });
    }
  }

  for (const shell of shells) {
    const viewport = shell.querySelector(".diagram-viewport");
    const canvas = shell.querySelector(".diagram-canvas");
    const tools = shell.querySelector(".diagram-tools");

    const pz = PZ(canvas, {
      maxZoom: 10,
      minZoom: 0.5,
      contain: false,
      cursor: "grab",
      smooth: true,
    });

    viewport.addEventListener(
      "wheel",
      (event) => {
        event.preventDefault();
        pz.zoomWithWheel(event);
      },
      { passive: false },
    );

    tools.addEventListener("click", (event) => {
      const button = event.target.closest("button[data-action]");
      if (!button) return;
      const action = button.dataset.action;
      if (action === "in" || action === "out") {
        const current = pz.getTransform().scale;
        const next = Math.min(
          Math.max(action === "in" ? current * 1.5 : current / 1.5, pz.getMinZoom()),
          pz.getMaxZoom(),
        );
        const rect = viewport.getBoundingClientRect();
        pz.zoomAbs(rect.width / 2, rect.height / 2, next);
      }
      if (action === "reset") {
        pz.zoomAbs(0, 0, 1);
        pz.moveTo(0, 0);
      }
      if (action === "full") {
        if (document.fullscreenElement === shell) {
          document.exitFullscreen();
        } else {
          shell.requestFullscreen();
        }
      }
      track(action);
    });

    viewport.addEventListener("dblclick", () => {
      pz.zoomAbs(0, 0, 1);
      pz.moveTo(0, 0);
      track("reset");
    });

    document.addEventListener("fullscreenchange", () => {
      if (document.fullscreenElement === shell) {
        shell.classList.add("is-fullscreen");
      } else {
        shell.classList.remove("is-fullscreen");
        pz.zoomAbs(0, 0, 1);
        pz.moveTo(0, 0);
      }
    });
  }
})();
