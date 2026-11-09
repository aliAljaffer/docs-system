/* Obsidian-style graph view with hover focus, type legend, and clustered layout. */
(() => {
  const container = document.getElementById("docs-graph");
  const status = document.getElementById("graph-status");
  if (!container || !window.ForceGraph) return;

  const layout = document.createElement("div");
  layout.className = "graph-layout";
  container.parentNode.insertBefore(layout, container);
  layout.appendChild(container);

  const base = location.pathname.startsWith("/ar/") ? "/ar" : "";
  const palette = {
    project: "#7aa2f7",
    course: "#9ece6a",
    episode: "#bb9af7",
    definition: "#e0af68",
    note: "#7dcfff",
    collection: "#2ac3de",
    page: "#a9b1d6",
  };
  const labels = {
    project: "Projects",
    course: "Courses",
    episode: "Episodes",
    definition: "Definitions",
    note: "Notes",
    collection: "Collections",
    page: "Pages",
  };
  const DIM = "rgba(130, 140, 170, 0.08)";
  const idOf = (value) => (value && typeof value === "object" ? value.id : value);
  const escape = (value) =>
    String(value).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

  fetch(`${base}/assets/graph.json`)
    .then((response) => response.json())
    .then((data) => {
      const adjacency = new Map();
      const degree = new Map();
      for (const node of data.nodes) adjacency.set(node.id, new Set());
      for (const link of data.links) {
        const source = idOf(link.source);
        const target = idOf(link.target);
        adjacency.get(source)?.add(target);
        adjacency.get(target)?.add(source);
        degree.set(source, (degree.get(source) || 0) + 1);
        degree.set(target, (degree.get(target) || 0) + 1);
      }

      const hidden = new Set();
      const typeOf = new Map(data.nodes.map((node) => [node.id, node.type]));
      let hovered = null;
      const isActive = (node) =>
        !hovered || node.id === hovered || adjacency.get(hovered)?.has(node.id);
      const isLiveLink = (link) => {
        if (!hovered) return true;
        return idOf(link.source) === hovered || idOf(link.target) === hovered;
      };
      const nodeColor = (node) => (isActive(node) ? palette[node.type] || palette.page : DIM);
      const nodeVal = (node) =>
        2 + Math.sqrt(degree.get(node.id) || 1) * 2 + (hovered && isActive(node) ? 2.5 : 0);
      const linkColor = (link) =>
        isLiveLink(link) ? "rgba(122, 162, 247, 0.9)" : "rgba(150, 160, 190, 0.04)";
      const linkWidth = (link) => (hovered && isLiveLink(link) ? 2.2 : 0.55);
      const linkParticles = (link) => (hovered && isLiveLink(link) ? 3 : 0);
      const applyFocus = () => {
        graph
          .nodeColor(nodeColor)
          .nodeVal(nodeVal)
          .linkColor(linkColor)
          .linkWidth(linkWidth)
          .linkDirectionalParticles(linkParticles);
      };

      const width = container.clientWidth || 800;
      const height = container.clientHeight || 600;
      const graph = ForceGraph()(container)
        .width(width)
        .height(height)
        .graphData(data)
        .nodeId("id")
        .nodeLabel(
          (node) =>
            `<div class="graph-tip"><strong>${escape(node.title)}</strong>` +
            `<span>${labels[node.type] || node.type} · ${adjacency.get(node.id).size} links</span></div>`,
        )
        .nodeColor(nodeColor)
        .nodeVal(nodeVal)
        .nodeVisibility((node) => !hidden.has(node.type))
        .linkColor(linkColor)
        .linkWidth(linkWidth)
        .linkDirectionalArrowLength(2.5)
        .linkDirectionalArrowRelPos(1)
        .linkDirectionalParticles(linkParticles)
        .linkDirectionalParticleWidth(1.4)
        .linkVisibility(
          (link) =>
            !hidden.has(typeOf.get(idOf(link.source))) &&
            !hidden.has(typeOf.get(idOf(link.target))),
        )
        .onNodeHover((node) => {
          hovered = node ? node.id : null;
          applyFocus();
          container.classList.toggle("has-hover", Boolean(hovered));
          clearTimeout(hideTimer);
          if (node) {
            renderInfo(node);
          } else {
            hideTimer = setTimeout(() => renderInfo(null), 250);
          }
        })
        .onNodeClick((node) => {
          window.location.href = node.id;
        })
        .cooldownTicks(360)
        .warmupTicks(60)
        .d3AlphaDecay(0.018)
        .d3VelocityDecay(0.24);

      graph.d3Force("charge").strength(-180).distanceMax(700);
      graph.d3Force("link").distance(72).strength(0.5);

      const groups = [...new Set(data.nodes.map((node) => node.group))].sort();
      const centers = new Map();
      groups.forEach((group, index) => {
        const angle = (2 * Math.PI * index) / groups.length;
        const radius = 180 + groups.length * 7;
        centers.set(group, { x: Math.cos(angle) * radius, y: Math.sin(angle) * radius });
      });
      graph.d3Force("cluster", (alpha) => {
        for (const node of graph.graphData().nodes) {
          const center = centers.get(node.group);
          if (!center) continue;
          node.vx += (center.x - node.x) * alpha * 0.035;
          node.vy += (center.y - node.y) * alpha * 0.035;
        }
      });

      const titles = new Map(data.nodes.map((node) => [node.id, node]));
      const outgoing = new Map();
      const incoming = new Map();
      for (const link of data.links) {
        const source = idOf(link.source);
        const target = idOf(link.target);
        if (!outgoing.has(source)) outgoing.set(source, new Set());
        if (!incoming.has(target)) incoming.set(target, new Set());
        outgoing.get(source).add(target);
        incoming.get(target).add(source);
      }

      const info = document.createElement("div");
      info.className = "graph-info";
      layout.appendChild(info);
      let hideTimer = null;

      const renderInfo = (node) => {
        if (!node) {
          info.innerHTML = "<p>Hover a node to see the pages linked to it.</p>";
          return;
        }
        const out = [...(outgoing.get(node.id) || [])];
        const inc = [...(incoming.get(node.id) || [])];
        const list = (ids) =>
          ids.length
            ? `<ul>${ids
                .map((id) => {
                  const target = titles.get(id);
                  return target
                    ? `<li><a href="${id}">${escape(target.title)}</a><small>${labels[target.type] || target.type}</small></li>`
                    : "";
                })
                .join("")}</ul>`
            : '<p class="graph-info__empty">No links.</p>';
        info.innerHTML =
          `<div class="graph-info__head"><strong>${escape(node.title)}</strong>` +
          `<span>${labels[node.type] || node.type} · <a href="${node.id}">Open page</a></span></div>` +
          `<div class="graph-info__cols"><section><h3>Links to (${out.length})</h3>${list(out)}</section>` +
          `<section><h3>Linked from (${inc.length})</h3>${list(inc)}</section></div>`;
      };

      info.addEventListener("mouseenter", () => clearTimeout(hideTimer));
      info.addEventListener("mouseleave", () => {
        if (!hovered) renderInfo(null);
      });
      renderInfo(null);

      const counts = new Map();
      for (const node of data.nodes) counts.set(node.type, (counts.get(node.type) || 0) + 1);
      const legend = document.createElement("div");
      legend.className = "graph-legend";
      for (const [type, count] of [...counts].sort((a, b) => b[1] - a[1])) {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "graph-legend__item";
        button.style.setProperty("--dot", palette[type] || palette.page);
        button.innerHTML = `<span class="graph-legend__dot"></span>${labels[type] || type}<small>${count}</small>`;
        button.addEventListener("click", () => {
          if (hidden.has(type)) hidden.delete(type);
          else hidden.add(type);
          button.classList.toggle("is-off", hidden.has(type));
          graph
            .nodeVisibility((node) => !hidden.has(node.type))
            .linkVisibility(
              (link) =>
                !hidden.has(typeOf.get(idOf(link.source))) &&
                !hidden.has(typeOf.get(idOf(link.target))),
            );
          applyFocus();
        });
        legend.appendChild(button);
      }
      container.appendChild(legend);

      const resize = () => {
        graph.width(container.clientWidth).height(container.clientHeight);
      };
      window.addEventListener("resize", resize);
      if (new URLSearchParams(location.search).has("debug")) {
        window.__graph = graph;
        window.__hovered = () => hovered;
        window.__active = isActive;
      }
      setTimeout(() => graph.zoomToFit(500, 50), 500);
      if (status) status.textContent = `${data.nodes.length} pages, ${data.links.length} links`;
    })
    .catch((error) => {
      if (status) {
        status.textContent = `Graph failed to load: ${error.message}`;
        status.classList.add("error");
      }
    });
})();
