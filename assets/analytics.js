/* Rich analytics for docs.alialjaffer.com, powered by the homelab Umami. */
(() => {
  const UMAMI_HOST = "https://umami.alialjaffer.com";
  const WEBSITE_ID = "ea36b581-4b7d-4c81-9691-3182bfd8dfc8";
  const SITE_HOST = "docs.alialjaffer.com";
  const FORCE = new URLSearchParams(location.search).has("analytics");

  if (!FORCE && location.hostname !== SITE_HOST) return;
  if (navigator.doNotTrack === "1" || window.doNotTrack === "1") return;

  const script = document.createElement("script");
  script.defer = true;
  script.src = `${UMAMI_HOST}/script.js`;
  script.setAttribute("data-website-id", WEBSITE_ID);
  script.setAttribute("data-host-url", UMAMI_HOST);
  script.setAttribute("data-domains", SITE_HOST);
  script.setAttribute("data-tag", "docs");
  script.setAttribute("data-performance", "true");
  script.setAttribute("data-do-not-track", "true");
  document.head.appendChild(script);

  const path = () => location.pathname;
  const lang = () => document.documentElement.lang || "en";
  const pageTitle = () => document.title.replace(/\s+-\s+Docs$/, "");

  function track(name, data) {
    if (window.umami && typeof window.umami.track === "function") {
      window.umami.track(name, data);
    }
  }

  function pageType() {
    const heading = document.querySelector("h1")?.textContent?.trim() || "";
    const episode = heading.match(/^([A-Z]{3}-\d{2}):/);
    if (episode) return { type: "episode", code: episode[1] };
    if (path().startsWith("/wiki/")) return { type: "wiki" };
    if (path().startsWith("/four-hats/")) return { type: "course" };
    if (path().startsWith("/slides/")) return { type: "slide" };
    if (path().endsWith("/404.html")) return { type: "404" };
    return { type: "page" };
  }

  function ready() {
    const info = pageType();
    track("page-type", { ...info, lang: lang(), title: pageTitle() });

    if (info.type === "404") {
      track("page-404", { path: path(), referrer: document.referrer || "direct" });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", ready);
  } else {
    ready();
  }

  document.addEventListener("click", (event) => {
    const link = event.target.closest("a[href]");
    if (!link) return;

    if (link.classList.contains("lang-switch")) {
      track("language-switch", {
        from: lang(),
        to: link.getAttribute("lang") || "",
        target: link.getAttribute("href") || "",
        path: path(),
      });
      return;
    }

    let url;
    try {
      url = new URL(link.href, location.href);
    } catch {
      return;
    }

    if (url.origin === location.origin && url.pathname.startsWith("/slides/")) {
      track("slide-open", { deck: url.pathname, path: path() });
      return;
    }

    if (/\.(pdf|zip|tar\.gz|tgz|dmg|pkg)$/i.test(url.pathname)) {
      track("file-download", { file: url.pathname, path: path() });
      return;
    }

    if (url.origin !== location.origin && /^https?:$/.test(url.protocol)) {
      track("outbound-link", {
        domain: url.hostname,
        target: url.pathname,
        path: path(),
      });
    }
  });

  document.addEventListener("click", (event) => {
    const button = event.target.closest(".md-clipboard");
    if (!button) return;
    const code = button.closest("pre")?.querySelector("code");
    const match = code?.className.match(/language-([a-z0-9+-]+)/i);
    track("code-copy", { language: match ? match[1] : "unknown", path: path() });
  });

  document.querySelectorAll("input.md-search__input").forEach((input) => {
    input.addEventListener("keydown", (event) => {
      if (event.key !== "Enter") return;
      const query = input.value.trim().slice(0, 120);
      if (query) track("search", { query, lang: lang(), path: path() });
    });
  });

  document.addEventListener("docs:preview", (event) => {
    const detail = event.detail || {};
    track("wiki-preview", {
      term: detail.title || "",
      target: detail.url || "",
      path: path(),
    });
  });

  document.querySelectorAll(".task-list-item input[type=checkbox]").forEach((box, index) => {
    box.addEventListener("change", () => {
      track("task-toggle", { checked: box.checked, index, path: path() });
    });
  });

  document.querySelectorAll('input[name="__palette"]').forEach((input) => {
    input.addEventListener("change", () => {
      track("theme-change", { scheme: input.id, path: path() });
    });
  });

  document.querySelectorAll(".md-footer__link").forEach((link) => {
    link.addEventListener("click", () => {
      const direction = link.classList.contains("md-footer__link--prev") ? "previous" : "next";
      track("episode-nav", { direction, target: link.getAttribute("href") || "", path: path() });
    });
  });

  const marks = [25, 50, 75, 100];
  const seen = new Set();
  let timer = null;
  function depth() {
    const root = document.documentElement;
    const total = root.scrollHeight - root.clientHeight;
    if (total <= 0) return;
    const percent = Math.min(100, Math.round((root.scrollTop / total) * 100));
    for (const mark of marks) {
      if (percent >= mark && !seen.has(mark)) {
        seen.add(mark);
        track("scroll-depth", { depth: mark, path: path() });
      }
    }
  }
  window.addEventListener(
    "scroll",
    () => {
      if (timer) return;
      timer = setTimeout(() => {
        timer = null;
        depth();
      }, 200);
    },
    { passive: true },
  );
})();
