(() => {
  const key = "checklist:" + location.pathname;
  const boxes = [...document.querySelectorAll(".task-list-item input[type=checkbox]")];
  if (!boxes.length) return;
  let saved = [];
  try { saved = JSON.parse(localStorage.getItem(key)) || []; } catch (e) {}
  boxes.forEach((box, i) => {
    box.disabled = false;
    box.checked = saved.includes(i);
    box.addEventListener("change", () => {
      const checked = boxes.flatMap((b, j) => (b.checked ? [j] : []));
      localStorage.setItem(key, JSON.stringify(checked));
    });
  });
})();
