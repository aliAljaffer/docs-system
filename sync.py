#!/usr/bin/env python3
"""Pull the course sources into the site content tree.

The four-hats repository owns the course text and the verified apply steps.
This script copies the English pages and converts the shared diagrams. It does
not write navigation or build the site.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FOUR_HATS = Path("/Users/h/mk-project/four-hats")
HQ = Path("/Users/h/mk-project/hq-main")
EN = ROOT / "content" / "en"
ASSETS = ROOT / "assets" / "diagrams"

PAGES = {
    "00-setup.md": "setup.md",
    "cleanup-guide.md": "cleanup-guide.md",
    "costs-and-free-options.md": "costs-and-free-options.md",
}


def main() -> None:
    eps_src = FOUR_HATS / "docs" / "episodes"
    eps_dst = EN / "four-hats" / "episodes"
    eps_dst.mkdir(parents=True, exist_ok=True)
    for old in eps_dst.glob("ep*.md"):
        old.unlink()
    count = 0
    for src in sorted(eps_src.glob("ep*.md")):
        shutil.copy2(src, eps_dst / src.name)
        count += 1

    for src_name, dst_name in PAGES.items():
        src = FOUR_HATS / "docs" / src_name
        if src.exists():
            shutil.copy2(src, EN / dst_name)

    sources = ROOT / "sources"
    sources.mkdir(parents=True, exist_ok=True)
    for act in FOUR_HATS.joinpath("docs").glob("act*.md"):
        shutil.copy2(act, sources / act.name)
    scripts = sources / "scripts"
    scripts.mkdir(exist_ok=True)
    for old in scripts.glob("ep*.md"):
        old.unlink()
    for script in (HQ / "scripts").glob("ep*.md"):
        shutil.copy2(script, scripts / script.name)

    slides = ROOT / "assets" / "slides"
    slides.mkdir(parents=True, exist_ok=True)
    for old in slides.glob("ep*.html"):
        old.unlink()
    for deck in (HQ / "slides").glob("ep*.html"):
        shutil.copy2(deck, slides / deck.name)
    for extra in (HQ / "slides").glob("*.css"):
        shutil.copy2(extra, slides / extra.name)
    fonts = HQ / "slides" / "fonts"
    if fonts.exists():
        shutil.copytree(fonts, slides / "fonts", dirs_exist_ok=True)

    ASSETS.mkdir(parents=True, exist_ok=True)
    for png in sorted((HQ / "scripts" / "diagrams").glob("ep*.png")):
        webp = ASSETS / f"{png.stem}.webp"
        if not webp.exists() or webp.stat().st_mtime < png.stat().st_mtime:
            subprocess.run(
                ["magick", str(png), "-resize", "1400x", "-strip",
                 "-quality", "82", str(webp)],
                check=True,
            )

    print(f"synced {count} episode pages")


if __name__ == "__main__":
    main()
