/* Obsidian-style graph view built from the page link index. */
(() => {
  const container = document.getElementById("docs-graph");
  const status = document.getElementById("graph-status");
  if (!container || !window.ForceGraph) return;

  const base = location.pathname.startsWith("/ar/") ? "/ar" : "";
  const palette = {
    project: "#7aa2f7",
    course: "#9ece6a",
    episode: "#bb9af7",
    wiki: "#e0af68",
    note: "#7dcfff",
    tool: "#f7768e",
    collection: "#2ac3de",
    page: "#a9b1d6",
  };

  fetch(`${base}/assets/graph.json`)
    .then((response) => response.json())
    .then((data) => {
      const degree = new Map();
      for (const link of data.links) {
        degree.set(link.source, (degree.get(link.source) || 0) + 1);
        degree.set(link.target, (degree.get(link.target) || 0) + 1);
      }

      const width = container.clientWidth || 800;
      const height = container.clientHeight || 600;

      const graph = ForceGraph()(container)
        .width(width)
        .height(height)
        .graphData(data)
        .nodeId("id")
        .nodeLabel((node) => node.title)
        .nodeColor((node) => palette[node.type] || palette.page)
        .nodeVal((node) => 2 + Math.sqrt(degree.get(node.id) || 1) * 2)
        .linkColor(() => "rgba(150, 160, 190, 0.35)")
        .linkDirectionalArrowLength(2.5)
        .linkDirectionalArrowRelPos(1)
        .onNodeClick((node) => {
          window.location.href = node.id;
        })
        .cooldownTicks(150)
        .warmupTicks(30);

      const resize = () => {
        graph.width(container.clientWidth).height(container.clientHeight);
      };
      window.addEventListener("resize", resize);
      setTimeout(() => graph.zoomToFit(400, 40), 400);
      if (status) status.textContent = `${data.nodes.length} pages, ${data.links.length} links`;
    })
    .catch((error) => {
      if (status) {
        status.textContent = `Graph failed to load: ${error.message}`;
        status.classList.add("error");
      }
    });
})();
