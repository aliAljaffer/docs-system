(() => {
  const key = "checklist:" + location.pathname;
  const boxes = [...document.querySelectorAll(".task-list-item input[type=checkbox]")];
  if (!boxes.length) return;

  const ownText = (node) => [...node.childNodes].map((c) =>
    c.nodeType === 3 ? c.textContent : /^[OU]L$/.test(c.tagName) ? "" : ownText(c)).join("");

  const hash = (s) => {
    let h = 2166136261;
    for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619);
    return (h >>> 0).toString(36);
  };

  const seen = {};
  const ids = boxes.map((box) => {
    const id = hash(ownText(box.closest(".task-list-item")).replace(/\s+/g, " ").trim());
    seen[id] = (seen[id] || 0) + 1;
    return seen[id] > 1 ? id + "~" + seen[id] : id;
  });

  const save = (list) => {
    try { localStorage.setItem(key, JSON.stringify(list)); } catch (e) {}
  };

  let saved = [];
  try { saved = JSON.parse(localStorage.getItem(key)); } catch (e) {}
  if (!Array.isArray(saved)) saved = [];
  if (saved.some((v) => typeof v === "number")) {
    saved = saved.map((v) => (typeof v === "number" ? ids[v] : v)).filter(Boolean);
    save(saved);
  }

  const ticked = new Set(saved);
  boxes.forEach((box, i) => {
    box.disabled = false;
    box.checked = ticked.has(ids[i]);
    box.addEventListener("change", () => save(ids.filter((_, j) => boxes[j].checked)));
  });
})();
