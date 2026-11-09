#!/usr/bin/env python3
"""Pull external sources into the site content tree.

The four-hats repository owns the course text and the verified apply steps.
The portfolio repository owns the project write-ups and notes. The
openziti-operator repository owns its reference documentation. This script
converts and copies those sources. It does not write navigation or build the
site.
"""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
FOUR_HATS = Path("/Users/h/mk-project/four-hats")
HQ = Path("/Users/h/mk-project/hq-main")
PORTFOLIO = Path("/Users/h/portfolio/src/data")
PORTFOLIO_PUBLIC = Path("/Users/h/portfolio/public")
OPENZITI = Path("/Users/h/openziti-operator/docs")
EN = ROOT / "content" / "en"
ASSETS = ROOT / "assets" / "diagrams"
PORTFOLIO_ASSETS = ROOT / "assets" / "portfolio"
OPENZITI_PAGES = EN / "projects" / "openziti-operator"

PAGES = {
    "00-setup.md": "setup.md",
    "cleanup-guide.md": "cleanup-guide.md",
    "costs-and-free-options.md": "costs-and-free-options.md",
}

MARKER = "<!-- imported from portfolio/src/data/{name}. Edit the source, then run sync.py. -->"
IMAGE = re.compile(r"\]\(/([^)/]+\.(?:png|jpg|jpeg|gif|svg|webp))\)")


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    return yaml.safe_load(text[4:end]) or {}, text[end + 5:].lstrip("\n")


def clean_body(body: str) -> str:
    body = body.replace("](/case-study/", "](https://alialjaffer.com/case-study/")
    body = re.sub(
        r"<excalidraw src=\"(/[^\"]+)\"></excalidraw>",
        r"[Open the Excalidraw drawing](https://alialjaffer.com\1)",
        body,
    )
    body = re.sub(r"\]\((?!mailto:)([^)\s]+@[^)\s]+)\)", r"](mailto:\1)", body)
    body = re.sub(r'<iframe className="[^"]*"\s*', "<iframe ", body)
    PORTFOLIO_ASSETS.mkdir(parents=True, exist_ok=True)
    for name in sorted(set(IMAGE.findall(body))):
        source = PORTFOLIO_PUBLIC / name
        if source.exists():
            shutil.copy2(source, PORTFOLIO_ASSETS / name)
        body = body.replace(f"](/{name})", f"](/assets/portfolio/{name})")
    return re.sub(r"\n{3,}", "\n\n", body).strip()


def link_block(meta: dict) -> list[str]:
    repo = str(meta.get("repo") or "")
    url = str(meta.get("url") or "")
    lines = []
    if repo and "example" not in repo and "no-repo" not in repo:
        lines.append(f"- [Repository]({repo})")
    if url and "example.com" not in url and "no-url" not in url:
        lines.append(f"- [Live]({url})")
    if not lines:
        return []
    return ["## Links", "", *lines, ""]


def tag_line(meta: dict) -> list[str]:
    tags = meta.get("tags") or []
    if not tags:
        return []
    return [" ".join(f"`{tag}`" for tag in tags), ""]


def project_page(stem: str, meta: dict, body: str) -> str:
    title = meta.get("name") or stem
    lines = [
        MARKER.format(name=f"{stem}.md"),
        "",
        f"# {title}",
        "",
        "**Status:** Active",
        "",
    ]
    if meta.get("description"):
        lines += [str(meta["description"]).strip(), ""]
    lines += tag_line(meta)
    lines += link_block(meta)
    lines += [body, ""]
    return "\n".join(lines)


def note_page(stem: str, meta: dict, body: str) -> str:
    title = meta.get("name") or stem
    lines = [
        MARKER.format(name=f"{stem}.md"),
        "",
        f"# {title}",
        "",
        f"**Published:** {meta.get('date', '')}",
        "",
    ]
    if meta.get("description"):
        lines += [str(meta["description"]).strip(), ""]
    lines += tag_line(meta)
    lines += link_block(meta)
    lines += [body, ""]
    return "\n".join(lines)


def generated(path: Path) -> bool:
    return path.read_text().startswith("<!-- imported from portfolio/")


def sync_portfolio() -> tuple[int, int]:
    written: set[Path] = set()
    projects = notes = 0
    for src in sorted(PORTFOLIO.glob("*.md")):
        stem = src.stem
        if stem == "template":
            continue
        data, body = split_frontmatter(src.read_text())
        meta = data.get(stem) or next(iter(data.values()), {})
        if not meta or not meta.get("show", True):
            continue
        body = clean_body(body)
        if meta.get("type") == "blog":
            dest = EN / "wiki" / f"{stem}.md"
            text = note_page(stem, meta, body)
        else:
            dest = EN / "projects" / f"{stem}.md"
            text = project_page(stem, meta, body)
        if dest.exists() and not generated(dest):
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text)
        written.add(dest)
        if meta.get("type") == "blog":
            notes += 1
        else:
            projects += 1
    for folder in (EN / "projects", EN / "wiki"):
        for path in folder.glob("*.md"):
            if generated(path) and path not in written:
                path.unlink()
    return projects, notes


def sync_openziti() -> int:
    OPENZITI_PAGES.mkdir(parents=True, exist_ok=True)
    for old in OPENZITI_PAGES.rglob("*.md"):
        if old == OPENZITI_PAGES / "index.md":
            continue
        old.unlink()
    count = 0
    for src in sorted(OPENZITI.rglob("*.md")):
        rel = src.relative_to(OPENZITI)
        if rel.name == "index.md":
            continue
        dst = OPENZITI_PAGES / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        count += 1
    return count


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
    episodes = sync_four_hats()
    projects, notes = sync_portfolio()
    docs = sync_openziti()
    print(
        f"synced {episodes} episodes, {projects} projects, "
        f"{notes} notes, {docs} operator docs"
    )


if __name__ == "__main__":
    main()
