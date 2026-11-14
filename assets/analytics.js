/* Rich analytics for docs.alialjaffer.com, powered by the homelab Umami. */
(() => {
  const UMAMI_HOST = "https://umami.alialjaffer.com";
  const WEBSITE_ID = "3034df8d-b43a-4664-8a8a-6d89f86c32eb";
  const SITE_HOST = "docs.alialjaffer.com";
  const FORCE = new URLSearchParams(location.search).has("analytics");

  if (!FORCE && location.hostname !== SITE_HOST) return;
  if (navigator.doNotTrack === "1" || window.doNotTrack === "1") return;

  // Umami and the track() calls must not run while a speculation-rules prerender is hidden.
  function start() {
    const pending = [];
    function flush() {
      if (!window.umami || typeof window.umami.track !== "function") return;
      while (pending.length) {
        const [name, data] = pending.shift();
        window.umami.track(name, data);
      }
    }

    // page-type fires at DOMContentLoaded, often before the async tracker has
    // defined window.umami. Queue until it exists instead of dropping the event.
    function track(name, data) {
      pending.push([name, data]);
      flush();
    }

    const script = document.createElement("script");
    script.fetchPriority = "low";
    script.src = `${UMAMI_HOST}/script.js`;
    script.setAttribute("data-website-id", WEBSITE_ID);
    script.setAttribute("data-host-url", UMAMI_HOST);
    script.setAttribute("data-domains", FORCE ? `${SITE_HOST},${location.hostname}` : SITE_HOST);
    script.setAttribute("data-tag", "docs");
    script.setAttribute("data-performance", "true");
    script.setAttribute("data-do-not-track", "true");
    script.addEventListener("load", flush);
    document.head.appendChild(script);

    const path = () => location.pathname;
    const lang = () => document.documentElement.lang || "en";
    const pageTitle = () => document.title.replace(/\s+-\s+Ali's Docs$/, "");

    function pageType() {
      const heading = document.querySelector("h1")?.textContent?.trim() || "";
      const episode = heading.match(/^([A-Z]{3}-\d{2}):/);
      if (episode) return { type: "episode", code: episode[1] };
      // Cloudflare serves the custom 404 at the requested URL, so the path is no guide.
      if (heading.startsWith("404")) return { type: "404" };
      if (path().startsWith("/four-hats/slides/")) return { type: "slide" };
      if (path().startsWith("/four-hats/")) return { type: "course" };
      return { type: "page" };
    }

    function ready() {
      const info = pageType();
      track("page-type", {
        ...info,
        section: path().split("/")[1] || "home",
        lang: lang(),
        title: pageTitle(),
      });

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

      let url;
      try {
        url = new URL(link.href, location.href);
      } catch {
        return;
      }

      if (url.origin === location.origin && url.pathname.startsWith("/four-hats/slides/")) {
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
        return;
      }

      if (url.hash && url.pathname === location.pathname) {
        track("toc-jump", { target: url.hash.slice(1), path: path() });
      }
    });

    document.addEventListener("click", (event) => {
      const tag = event.target.closest("button.md-tag");
      if (tag) track("tag-filter", { term: tag.textContent.trim(), path: path() });
    });

    document.addEventListener("click", (event) => {
      if (!event.target.closest("[data-md-component=search] button")) return;
      track("search-open", { lang: lang(), path: path() });
    });

    document.addEventListener("click", (event) => {
      const button = event.target.closest("[data-fullscreen]");
      if (!button) return;
      const frame = button.closest("div")?.querySelector("iframe");
      track("slide-fullscreen", {
        deck: frame?.getAttribute("src") || "",
        path: path(),
      });
    });

    document.addEventListener("click", (event) => {
      const button = event.target.closest(".md-clipboard");
      if (!button) return;
      const code = button.closest("pre")?.querySelector("code");
      const match = code?.className.match(/language-([a-z0-9+-]+)/i);
      track("code-copy", { language: match ? match[1] : "unknown", path: path() });
    });

    // zensical renders the search input inside a shadow root that is not a
    // descendant of the search component, so find it by role on the event path.
    document.addEventListener(
      "keydown",
      (event) => {
        if (event.key !== "Enter") return;
        const input = event
          .composedPath()
          .find((node) => node instanceof HTMLInputElement && node.getAttribute("role") === "combobox");
        const term = (input?.value || "").trim();
        if (!term) return;
        track("search", { term: term.slice(0, 80), length: term.length, lang: lang(), path: path() });
      },
      true,
    );

    document.addEventListener("docs:preview", (event) => {
      const detail = event.detail || {};
      track("wiki-preview", {
        term: detail.title || "",
        target: detail.url || "",
        path: path(),
      });
    });

    const boxes = [...document.querySelectorAll(".task-list-item input[type=checkbox]")];
    let complete = false;
    boxes.forEach((box, index) => {
      box.addEventListener("change", () => {
        track("task-toggle", { checked: box.checked, index, path: path() });
        if (!complete && boxes.every((b) => b.checked)) {
          complete = true;
          track("checklist-complete", { total: boxes.length, path: path() });
        }
      });
    });

    document.querySelectorAll('input[name="__palette"]').forEach((input) => {
      input.addEventListener("change", () => {
        track("theme-change", {
          scheme: input.dataset.mdColorScheme === "slate" ? "dark" : "light",
          path: path(),
        });
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
    if ("onscrollend" in window) {
      window.addEventListener("scrollend", depth, { passive: true });
    } else {
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
    }
  }

  if (document.prerendering) {
    document.addEventListener("prerenderingchange", start, { once: true });
  } else {
    start();
  }
})();
