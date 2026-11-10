#!/usr/bin/env python3
"""Validate catalog courses and the frontmatter on projects, notes, definitions, and blogs."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
EN = ROOT / "content" / "en"
CATALOG = yaml.safe_load((ROOT / "catalog.yaml").read_text())
REQUIRED = {
    "notes": ("title", "description", "tags"),
    "blogs": ("title", "date", "description", "tags"),
    "projects": ("title", "date", "description", "tags"),
}
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
KEBAB = re.compile(r"[a-z0-9][a-z0-9-]*")


def frontmatter(path: Path) -> dict:
    text = path.read_text()
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    return yaml.safe_load(text[4:end]) or {}


def main() -> int:
    errors: list[str] = []

    for item in CATALOG.get("courses", []):
        for key in ("slug", "title", "status", "summary", "tags", "page"):
            if key not in item:
                errors.append(f"catalog courses: {item.get('slug', '?')} missing {key}")
        page = item.get("page") or ""
        if not page:
            if item.get("status") != "Planned":
                errors.append(f"catalog courses: {item['slug']} has no page")
        elif not (EN / page).exists():
            errors.append(f"catalog courses: {item['slug']} page missing: {page}")

    categories: dict[str, dict[str, list[str]]] = {}
    for path in sorted((EN / "projects").glob("*.md")) + sorted((EN / "projects").glob("*/index.md")):
        rel = path.relative_to(EN).as_posix()
        meta = frontmatter(path)
        for key in REQUIRED["projects"]:
            if not meta.get(key):
                errors.append(f"{rel}: missing {key}")
        if meta.get("date") and not DATE.fullmatch(str(meta["date"])):
            errors.append(f"{rel}: date must be YYYY-MM-DD")
        for tag in meta.get("tags") or []:
            if not KEBAB.fullmatch(str(tag)):
                errors.append(f"{rel}: tag is not lowercase kebab-case: {tag}")

    for folder in ("definitions", "notes", "blogs"):
        base = EN / folder
        for path in sorted(base.rglob("*.md")):
            if path.name == "index.md" or path.name.startswith("."):
                continue
            meta = frontmatter(path)
            rel = path.relative_to(EN).as_posix()
            text = path.read_text()
            heading = re.search(r"^# (.+)$", text, flags=re.M)
            if folder == "definitions":
                if not meta and not heading:
                    errors.append(f"{rel}: add an H1 title")
                    continue
                if not (meta.get("title") or heading):
                    errors.append(f"{rel}: missing title")
                categories.setdefault(folder, {}).setdefault(str(meta.get("category") or path.parent.name), []).append(rel)
                for tag in meta.get("tags") or []:
                    if not KEBAB.fullmatch(str(tag)):
                        errors.append(f"{rel}: tag is not lowercase kebab-case: {tag}")
                if "\u2014" in text:
                    errors.append(f"{rel}: contains an em dash")
                continue
            if not meta:
                errors.append(f"{rel}: missing frontmatter")
                continue
            for key in REQUIRED[folder]:
                if not meta.get(key):
                    errors.append(f"{rel}: missing {key}")
            tags = meta.get("tags") or []
            if not isinstance(tags, list) or not tags:
                errors.append(f"{rel}: tags must be a non-empty list")
            else:
                for tag in tags:
                    if not KEBAB.fullmatch(str(tag)):
                        errors.append(f"{rel}: tag is not lowercase kebab-case: {tag}")
            if folder == "notes":
                categories.setdefault(folder, {}).setdefault(str(meta.get("category") or path.parent.name), []).append(rel)
            if folder == "blogs":
                date = str(meta.get("date", ""))
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
                    errors.append(f"{rel}: date must be YYYY-MM-DD")
            if "\u2014" in text:
                errors.append(f"{rel}: contains an em dash")

    for folder, groups in categories.items():
        for name, pages in groups.items():
            if len(pages) == 1:
                print(f"WARN {pages[0]}: only page in {folder} category '{name}', check for a typo")

    if errors:
        print("\n".join(f"FAIL {item}" for item in errors))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
