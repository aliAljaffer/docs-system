#!/usr/bin/env python3
"""Check translation pairs and the built language switch.

Default mode reports gaps. Strict mode exits non-zero when a pair is missing or
a paired page lost its switch or hreflang tags.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EN = ROOT / "content" / "en"
AR = ROOT / "content" / "ar"
SITE = ROOT / "site"


def rels(root: Path) -> set[str]:
    return {
        p.relative_to(root).with_suffix("").as_posix()
        for p in root.rglob("*.md")
    }


def built(base: Path, rel: str) -> Path:
    path = base / rel / "index.html"
    return path if path.exists() else base / f"{rel}.html"


def main() -> None:
    strict = "--strict" in sys.argv
    en, ar = rels(EN), rels(AR)
    missing_ar = sorted(en - ar)
    missing_en = sorted(ar - en)

    print(f"English pages: {len(en)}")
    print(f"Arabic pages: {len(ar)}")
    if missing_en:
        print("Arabic without English:")
        for rel in missing_en:
            print(f"  {rel}")
    if missing_ar:
        print(f"English without Arabic ({len(missing_ar)}):")
        for rel in missing_ar[:20]:
            print(f"  {rel}")
        if len(missing_ar) > 20:
            print(f"  ... {len(missing_ar) - 20} more")

    broken: list[str] = []
    for rel in sorted(en & ar):
        page = built(SITE, rel)
        if not page.exists():
            broken.append(f"missing English build: {rel}")
            continue
        text = page.read_text()
        if 'class="lang-switch"' not in text:
            broken.append(f"no switch: {rel}")
        if 'hreflang="ar"' not in text:
            broken.append(f"no ar hreflang: {rel}")
        arabic = built(SITE / "ar", rel)
        if not arabic.exists():
            broken.append(f"missing Arabic build: {rel}")
            continue
        text = arabic.read_text()
        if 'class="lang-switch"' not in text:
            broken.append(f"no switch in Arabic: {rel}")
        if 'hreflang="en"' not in text:
            broken.append(f"no en hreflang in Arabic: {rel}")

    if broken:
        print("Built-page problems:")
        for item in broken:
            print(f"  {item}")

    failed = strict and (missing_ar or missing_en or broken)
    print("FAIL" if failed else "OK")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
