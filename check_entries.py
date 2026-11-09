#!/usr/bin/env python3
"""Validate catalog entries and the frontmatter on notes, definitions, and blogs."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
EN = ROOT / "content" / "en"
CATALOG = yaml.safe_load((ROOT / "catalog.yaml").read_text())
CATEGORIES = {
    "definitions": {"Cloud", "Networking", "Security", "AI", "React", "Web"},
    "notes": {"GCP", "Cloud", "Networking", "Security", "AI", "React", "Web", "Site"},
}
REQUIRED = {
    "notes": ("title", "category", "description", "tags"),
    "blogs": ("title", "date", "description", "tags"),
}


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

    for kind in ("projects", "courses"):
        for item in CATALOG.get(kind, []):
            for key in ("slug", "title", "status", "summary", "tags", "page"):
                if key not in item:
                    errors.append(f"catalog {kind}: {item.get('slug', '?')} missing {key}")
            page = item.get("page") or ""
            if not page:
                if item.get("status") != "Planned":
                    errors.append(f"catalog {kind}: {item['slug']} has no page")
                continue
            if not (EN / page).exists():
                errors.append(f"catalog {kind}: {item['slug']} page missing: {page}")
            if kind == "projects" and not Path(page).name == "index.md":
                hub = EN / Path(page).with_suffix("")
                if hub.is_dir() and (hub / "index.md").exists():
                    errors.append(
                        f"catalog projects: {item['slug']} points at {page}, use {hub.name}/index.md"
                    )

    catalog_pages = {item.get("page") for item in CATALOG.get("projects", [])}
    paths = list((EN / "projects").glob("*.md")) + list((EN / "projects").glob("*/index.md"))
    for path in sorted(paths):
        rel = path.relative_to(EN).as_posix()
        if rel in catalog_pages:
            continue
        meta = frontmatter(path)
        if not meta:
            errors.append(f"{rel}: add a catalog entry or frontmatter title, description, tags")
            continue
        for key in ("title", "status", "description", "tags"):
            if not meta.get(key):
                errors.append(f"{rel}: missing {key}")

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
                category = meta.get("category")
                if category and category not in CATEGORIES["definitions"]:
                    errors.append(f"{rel}: unknown category: {category}")
                for tag in meta.get("tags") or []:
                    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", str(tag)):
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
            elif folder != "blogs":
                for tag in tags:
                    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", str(tag)):
                        errors.append(f"{rel}: tag is not lowercase kebab-case: {tag}")
            category = meta.get("category")
            if category and category not in CATEGORIES.get(folder, {category}):
                errors.append(f"{rel}: unknown category: {category}")
            if folder == "blogs":
                date = str(meta.get("date", ""))
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
                    errors.append(f"{rel}: date must be YYYY-MM-DD")
            if "\u2014" in text:
                errors.append(f"{rel}: contains an em dash")

    if errors:
        print("\n".join(f"FAIL {item}" for item in errors))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
