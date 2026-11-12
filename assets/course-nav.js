(() => {
  const section = document.querySelector(".md-nav--primary > .md-nav__list > .md-nav__item--section.md-nav__item--active");
  const list = section && section.querySelector(":scope > .md-nav > .md-nav__list");
  const overview = list && list.querySelector(":scope > .md-nav__item > a.md-nav__link[href]");
  const course = list && list.querySelector(":scope > .md-nav__item--nested.md-nav__item--active");
  if (!document.documentElement.hasAttribute("data-course") || !overview || !course) return;
  const label = section.querySelector(":scope > .md-nav > .md-nav__title");
  const link = document.createElement("a");
  link.className = "md-nav__back";
  link.href = overview.getAttribute("href");
  link.textContent = `Back to ${(label ? label.textContent : "courses").trim()}`;
  course.prepend(link);
})();
