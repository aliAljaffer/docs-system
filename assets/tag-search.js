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
    const button = document.createElement("button");
    button.type = "button";
    button.className = tag.className;
    button.title = `Search pages tagged ${term}`;
    button.append(...tag.childNodes);
    button.addEventListener("click", () => search(term));
    tag.replaceWith(button);
  });
})();
