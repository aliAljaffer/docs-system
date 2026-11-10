#!/usr/bin/env python3
"""Manual import of the Four Hats course. Run: python sync.py four-hats

The course repo stays canonical for students. CI never runs this.
Set FOUR_HATS_DIR and HQ_DIR to the source checkouts.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EN = ROOT / "content" / "en"
ASSETS = ROOT / "assets" / "diagrams"
FOUR_HATS = Path(os.environ.get("FOUR_HATS_DIR", Path.home() / "mk-project/four-hats"))
HQ = Path(os.environ.get("HQ_DIR", Path.home() / "mk-project/hq-main"))

PAGES = {
    "00-setup.md": "four-hats/setup.md",
    "cleanup-guide.md": "four-hats/cleanup-guide.md",
    "costs-and-free-options.md": "four-hats/costs-and-free-options.md",
}


def sync_four_hats() -> int:
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
    for act in (FOUR_HATS / "docs").glob("act*.md"):
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
    for svg in sorted((HQ / "scripts" / "diagrams").glob("ep*.svg")):
        shutil.copy2(svg, ASSETS / svg.name)
    for png in sorted((HQ / "scripts" / "diagrams").glob("ep*.png")):
        webp = ASSETS / f"{png.stem}.webp"
        if not webp.exists() or webp.stat().st_mtime < png.stat().st_mtime:
            subprocess.run(
                ["magick", str(png), "-resize", "1400x", "-strip",
                 "-quality", "82", str(webp)],
                check=True,
            )
    return count


def main() -> None:
    if sys.argv[1:] != ["four-hats"]:
        raise SystemExit("usage: python sync.py four-hats")
    print(f"synced {sync_four_hats()} episodes")


if __name__ == "__main__":
    main()
