#!/usr/bin/env python3
"""Resolve Obsidian-style wikilinks and compute backlinks for the demo.

This is the piece neither Zensical nor MkDocs provides natively. It runs before
either build and writes a normal Markdown tree plus assets/backlinks.json.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "content"
DST = ROOT / "site-src"
WIKI = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
TITLE = re.compile(r"^# (.+)$", flags=re.M)


def page_url(path: Path) -> str:
    rel = path.relative_to(DST).with_suffix("")
    return "/" + rel.as_posix() + "/"


def build_index(files: list[Path]) -> dict[str, Path]:
    index: dict[str, Path] = {}
    stems: dict[str, list[Path]] = {}
    for path in files:
        rel = path.relative_to(DST).with_suffix("").as_posix()
        index[rel] = path
        if rel.startswith("wiki/"):
            index[rel.removeprefix("wiki/")] = path
        if path.stem != "index":
            stems.setdefault(path.stem, []).append(path)
    for stem, paths in stems.items():
        if len(paths) == 1:
            index[stem] = paths[0]
    return index


def main() -> None:
    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST)

    files = sorted(DST.rglob("*.md"))
    index = build_index(files)
    titles = {
        path: (TITLE.search(path.read_text()).group(1).strip() if TITLE.search(path.read_text()) else path.stem)
        for path in files
    }
    backlinks: dict[str, list[dict[str, str]]] = {}

    for path in files:
        text = path.read_text()

        def replace(match: re.Match[str]) -> str:
            target = match.group(1).strip()
            label = (match.group(2) or target).strip()
            if target not in index:
                raise SystemExit(f"{path.name}: missing wikilink target: {target}")
            dest = index[target]
            url = page_url(dest)
            entry = {"title": titles[path], "url": page_url(path)}
            bucket = backlinks.setdefault(url, [])
            if entry not in bucket:
                bucket.append(entry)
            return f"[{label}]({url})"

        path.write_text(WIKI.sub(replace, text))

    for bucket in backlinks.values():
        bucket.sort(key=lambda item: item["title"])
    (DST / "assets" / "backlinks.json").write_text(
        json.dumps(backlinks, indent=2, ensure_ascii=False) + "\n"
    )
    print(f"resolved {len(files)} pages, {sum(len(v) for v in backlinks.values())} backlinks")


if __name__ == "__main__":
    main()
