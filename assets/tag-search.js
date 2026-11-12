/* Make page tags open the search dialog with the tag as the query. */
(() => {
  function searchInput() {
    for (const host of document.querySelectorAll("body > div")) {
      const input = host.shadowRoot && host.shadowRoot.querySelector("input[type=text]");
      if (input) return input;
    }
    return null;
  }

  function search(term) {
    const button = document.querySelector("[data-md-component=search] button");
    if (!button) return;
    button.click();
    let tries = 0;
    const timer = setInterval(() => {
      const input = searchInput();
      if (!input && ++tries < 40) return;
      clearInterval(timer);
      if (!input) return;
      const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
      setter.call(input, term);
      input.dispatchEvent(new Event("input", { bubbles: true }));
      input.focus();
    }, 25);
  }

  document.querySelectorAll(".md-tag").forEach((tag) => {
    const term = tag.textContent.trim();
    tag.setAttribute("role", "button");
    tag.setAttribute("tabindex", "0");
    tag.setAttribute("title", `Search pages tagged ${term}`);
    tag.addEventListener("click", () => search(term));
    tag.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        search(term);
      }
    });
  });
})();
