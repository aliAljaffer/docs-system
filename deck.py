#!/usr/bin/env python3
"""Extract a text digest from an episode slide deck for authoring.

The decks hold the definitions, decisions, and trap lists that the video shows.
They are a better source for theory than the presenter script alone.
"""
from __future__ import annotations

import re
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SLIDES = ROOT / "assets" / "slides"


def clean(fragment: str) -> str:
    fragment = re.sub(r"<br\s*/?>", "\n", fragment)
    fragment = re.sub(r"</(p|li|div|h[1-6]|tr)>", "\n", fragment)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    text = unescape(fragment)
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def digest(path: Path) -> str:
    html = path.read_text()
    out = [f"# Deck: {path.stem}", ""]
    for match in re.finditer(r'<section class="slide">(.*?)</section>', html, flags=re.S):
        slide = match.group(1)
        time = re.search(r'<span class="time">(.*?)</span>', slide)
        badge = re.search(r'<span class="badge">(.*?)</span>', slide)
        title = re.search(r'<h1 class="slide-title">(.*?)</h1>', slide, flags=re.S)
        heading = re.search(r'<h2 class="slide-heading">(.*?)</h2>', slide, flags=re.S)
        body = re.search(r'<div class="slide-content">(.*)</div>', slide, flags=re.S)
        label = " · ".join(
            part for part in [
                clean(time.group(1)) if time else "",
                clean(badge.group(1)) if badge else "",
            ] if part
        )
        out.append(f"## {label or 'slide'}")
        if title:
            out.append(clean(title.group(1)))
        if heading:
            out.append(f"### {clean(heading.group(1))}")
        if body:
            text = clean(body.group(1))
            text = re.sub(r"^Speaker cue:.*$", "", text, flags=re.M)
            if text.strip():
                out.append(text)
        out.append("")
    return "\n".join(out)


def main() -> None:
    names = sys.argv[1:] or [p.stem for p in sorted(SLIDES.glob("ep*.html"))]
    out_dir = ROOT / ".cache" / "digests"
    out_dir.mkdir(parents=True, exist_ok=True)
    for name in names:
        path = SLIDES / (name if name.endswith(".html") else f"{name}.html")
        if not path.exists():
            raise SystemExit(f"No deck: {path}")
        dest = out_dir / f"{path.stem}.md"
        dest.write_text(digest(path))
        print(dest)


if __name__ == "__main__":
    main()
