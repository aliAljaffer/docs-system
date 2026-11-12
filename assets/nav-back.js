(() => {
  const top = ".md-nav--primary > .md-nav__list > .md-nav__item--section.md-nav__item--active";
  const section = document.querySelector(top);
  const overview = section && section.querySelector(":scope > .md-nav > .md-nav__list > .md-nav__item > a.md-nav__link[href]");
  const course = section && section.querySelector(":scope > .md-nav > .md-nav__list > .md-nav__item--nested.md-nav__item--active");
  if (!overview || !course) return;
  const label = section.querySelector(":scope > .md-nav > .md-nav__title, :scope > label.md-nav__link");
  const link = document.createElement("a");
  link.className = "md-nav__back";
  link.href = overview.getAttribute("href");
  link.setAttribute("aria-label", `Back to ${(label ? label.textContent : "overview").trim()}`);
  course.prepend(link);
})();
