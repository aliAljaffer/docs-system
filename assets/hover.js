/* Hover preview and backlinks for the docs system. */
(() => {
  const current = location.pathname.endsWith("/") ? location.pathname : location.pathname + "/";
  const cache = new Map();
  let card = null;
  let showTimer = null;
  let hideTimer = null;

  function ensureCard() {
    if (card) return card;
    card = document.createElement("div");
    card.className = "preview-card";
    document.body.appendChild(card);
    card.addEventListener("mouseenter", () => clearTimeout(hideTimer));
    card.addEventListener("mouseleave", hide);
    return card;
  }

  function hide() {
    if (!card) return;
    card.classList.remove("visible");
  }

  function cleanText(element) {
    if (!element) return "";
    const clone = element.cloneNode(true);
    clone.querySelectorAll(".headerlink").forEach((node) => node.remove());
    return clone.textContent.trim();
  }

  async function load(url) {
    if (cache.has(url)) return cache.get(url);
    const response = await fetch(url, { headers: { Accept: "text/html" } });
    const text = await response.text();
    const doc = new DOMParser().parseFromString(text, "text/html");
    const article = doc.querySelector(".md-content__inner") || doc.querySelector("article");
    const title = cleanText(article?.querySelector("h1")) || url;
    const first = article?.querySelector("p");
    const body = cleanText(first);
    const result = { title, body };
    cache.set(url, result);
    return result;
  }

  function position(link) {
    const rect = link.getBoundingClientRect();
    const width = Math.min(420, window.innerWidth - 32);
    let left = rect.left;
    if (left + width > window.innerWidth - 16) left = window.innerWidth - width - 16;
    let top = rect.bottom + 8;
    if (top + 240 > window.innerHeight) top = rect.top - 248;
    top = Math.min(Math.max(72, top), window.innerHeight - 240);
    card.style.left = Math.max(16, left) + "px";
    card.style.top = top + "px";
    card.style.width = width + "px";
  }

  function isDefinition(link) {
    return (
      link.closest(".md-content") !== null &&
      link.pathname.startsWith("/definitions/") &&
      link.pathname.replace(/\/$/, "") !== "/definitions"
    );
  }

  async function preview(link) {
    const url = new URL(link.href, location.href);
    if (url.origin !== location.origin) return;
    ensureCard();
    try {
      const { title, body } = await load(url.pathname);
      card.innerHTML = `<h3>${title}</h3><p>${body}</p><span class="preview-more">Click to open</span>`;
      position(link);
      card.classList.add("visible");
      document.dispatchEvent(
        new CustomEvent("docs:preview", { detail: { title, url: url.pathname } }),
      );
    } catch {
      hide();
    }
  }

  document.addEventListener("mouseover", (event) => {
    const link = event.target.closest("a[href]");
    if (!link || link.closest(".preview-card") || !isDefinition(link)) return;
    if (link.origin !== location.origin || link.pathname === current) return;
    if (link.hash && link.pathname === current) return;
    clearTimeout(showTimer);
    clearTimeout(hideTimer);
    showTimer = setTimeout(() => preview(link), 220);
  });

  document.addEventListener("mouseout", (event) => {
    const link = event.target.closest("a[href]");
    if (!link) return;
    clearTimeout(showTimer);
    hideTimer = setTimeout(hide, 180);
  });

  async function backlinks() {
    const target = document.querySelector(".md-content__inner");
    if (!target) return;
    let data;
    try {
      const response = await fetch(`/assets/backlinks.json?v=${encodeURIComponent(document.lastModified)}`);
      data = await response.json();
    } catch {
      return;
    }
    const entries = data[current] || [];
    if (!entries.length) return;
    const heading = document.createElement("h2");
    heading.id = "linked-from";
    heading.textContent = "Linked from";
    const list = document.createElement("ul");
    for (const entry of entries) {
      const item = document.createElement("li");
      const link = document.createElement("a");
      link.href = entry.url;
      link.textContent = entry.title;
      item.appendChild(link);
      list.appendChild(item);
    }
    const box = document.createElement("div");
    box.className = "backlinks";
    box.append(heading, list);
    target.appendChild(box);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", backlinks);
  } else {
    backlinks();
  }

  // Demo hook only: /four-hats/ep04/?preview=rest shows the card for a screenshot.
  const demo = new URLSearchParams(location.search).get("preview");
  if (demo) {
    setTimeout(() => {
      const link = [...document.querySelectorAll("a[href]")].find((a) => a.pathname.includes(demo));
      if (link) {
        preview(link);
      }
    }, 600);
  }
})();
