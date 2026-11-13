(function () {
  const host = document.currentScript;
  const themes = JSON.parse(host.dataset.themes);
  const theme = () => themes[document.body.getAttribute("data-md-color-scheme") === "slate" ? "dark" : "light"];
  const giscus = document.createElement("script");
  giscus.src = "https://giscus.app/client.js";
  giscus.async = true;
  giscus.crossOrigin = "anonymous";
  giscus.referrerPolicy = "no-referrer";
  giscus.fetchPriority = "low";
  Object.entries({
    repo: "aliAljaffer/aliAljaffer.github.io", repoId: "R_kgDOIZBWHA",
    category: "Announcements", categoryId: "DIC_kwDOIZBWHM4DBcZ5",
    mapping: "pathname", strict: "0", reactionsEnabled: "1",
    inputPosition: "top", loading: "lazy",
    lang: host.dataset.lang, theme: theme(),
  }).forEach(([k, v]) => giscus.dataset[k] = v);
  host.after(giscus);
  new MutationObserver(() => document.querySelector("iframe.giscus-frame")?.contentWindow
    ?.postMessage({ giscus: { setConfig: { theme: theme() } } }, "https://giscus.app"))
    .observe(document.body, { attributeFilter: ["data-md-color-scheme"] });
})();
