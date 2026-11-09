/* Pan and zoom controls for Excalidraw SVG diagrams. */
(() => {
  const PZ = window.Panzoom || window.panzoom;
  if (!PZ) return;

  const diagrams = [...document.querySelectorAll('.md-typeset img[src$=".svg"]')];

  function track(action) {
    if (window.umami && typeof window.umami.track === "function") {
      window.umami.track("diagram-zoom", { action, path: location.pathname });
    }
  }

  for (const img of diagrams) {
    if (img.closest(".diagram-zoom")) continue;

    const shell = document.createElement("div");
    shell.className = "diagram-zoom";

    const viewport = document.createElement("div");
    viewport.className = "diagram-viewport";

    const canvas = document.createElement("div");
    canvas.className = "diagram-canvas";

    const tools = document.createElement("div");
    tools.className = "diagram-tools";
    tools.innerHTML =
      '<button type="button" data-action="in" aria-label="Zoom in" title="Zoom in">+</button>' +
      '<button type="button" data-action="out" aria-label="Zoom out" title="Zoom out">-</button>' +
      '<button type="button" data-action="reset" aria-label="Reset zoom" title="Reset zoom">Reset</button>' +
      '<button type="button" data-action="full" aria-label="Fullscreen" title="Fullscreen">Full</button>';

    const hint = document.createElement("span");
    hint.className = "diagram-hint";
    hint.textContent = "Drag to pan. Scroll or pinch to zoom.";

    img.parentNode.insertBefore(shell, img);
    viewport.appendChild(canvas);
    canvas.appendChild(img);
    shell.append(viewport, tools, hint);

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
