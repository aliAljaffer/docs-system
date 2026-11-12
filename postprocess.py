"""Build-time HTML passes: markup that used to be added by scripts after page load."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ARTICLE = re.compile(r'(<article class="md-content__inner md-typeset">)(.*?)(</article>)', re.S)
SVG_IMG = re.compile(r'<img\b[^>]*\bsrc="[^"]*\.svg"[^>]*>')

DIAGRAM_TOOLS = (
    '<button type="button" data-action="in" aria-label="Zoom in" title="Zoom in">+</button>'
    '<button type="button" data-action="out" aria-label="Zoom out" title="Zoom out">-</button>'
    '<button type="button" data-action="reset" aria-label="Reset zoom" title="Reset zoom">Reset</button>'
    '<button type="button" data-action="full" aria-label="Fullscreen" title="Fullscreen">Full</button>'
)


def diagram_shell(img: re.Match[str]) -> str:
    return (
        '<div class="diagram-zoom"><div class="diagram-viewport"><div class="diagram-canvas">'
        f"{img.group(0)}"
        f'</div></div><div class="diagram-tools">{DIAGRAM_TOOLS}</div>'
        '<span class="diagram-hint">Drag to pan. Scroll or pinch to zoom.</span></div>'
    )


def backlinks_box(entries: list[dict[str, str]]) -> str:
    items = "".join(f'<li><a href="{html.escape(e["url"])}">{html.escape(e["title"])}</a></li>' for e in entries)
    return f'<div class="backlinks"><h2 id="linked-from">Linked from</h2><ul>{items}</ul></div>'


def enhance(page_html: str, url: str, backlinks: dict[str, list[dict[str, str]]]) -> str:
    def article(match: re.Match[str]) -> str:
        body = SVG_IMG.sub(diagram_shell, match.group(2))
        if backlinks.get(url):
            body += backlinks_box(backlinks[url])
        return match.group(1) + body + match.group(3)

    return ARTICLE.sub(article, page_html, count=1)


def run(site: Path, backlinks_file: Path) -> int:
    backlinks = json.loads(backlinks_file.read_text())
    changed = 0
    for page in site.rglob("index.html"):
        url = "/" + page.parent.relative_to(site).as_posix() + "/" if page.parent != site else "/"
        text = page.read_text()
        result = enhance(text, url, backlinks)
        if result != text:
            page.write_text(result)
            changed += 1
    return changed
