#!/usr/bin/env python3
"""Pull external sources into the site content tree.

The four-hats repository owns the course text and the verified apply steps.
The portfolio repository owns the project write-ups and blog posts. The
openziti-operator repository owns its reference documentation. The Obsidian
vault owns the study notes and the definition pages.

This script converts and copies those sources. It does not write navigation
or build the site.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path

import yaml


def source(name: str, default: str) -> Path:
    return Path(os.environ.get(name) or default)


ROOT = Path(__file__).resolve().parent
FOUR_HATS = source("FOUR_HATS_DIR", "/Users/h/mk-project/four-hats")
HQ = source("HQ_DIR", "/Users/h/mk-project/hq-main")
PORTFOLIO = source("PORTFOLIO_DIR", "/Users/h/portfolio/src/data")
PORTFOLIO_PUBLIC = source("PORTFOLIO_PUBLIC_DIR", "/Users/h/portfolio/public")
OPENZITI = source("OPENZITI_DOCS_DIR", "/Users/h/openziti-operator/docs")
VAULT = source(
    "OBSIDIAN_VAULT",
    str(
        next(
            (
                path
                for path in (Path.home() / "ObsidianVault", Path.home() / "Desktop" / "ObsidianVault")
                if path.exists()
            ),
            Path.home() / "Desktop" / "ObsidianVault",
        )
    ),
)
PROJECT_DOCS = [
    {"slug": "openziti-operator", "source": OPENZITI, "files": None},
    {"slug": "homelab", "source": source("HOMELAB_DOCS_DIR", "/Users/h/src/homelab/docs"), "files": None},
    {
        "slug": "grooszy",
        "source": source("GROOSZY_DOCS_DIR", "/Users/h/grooszy/docs"),
        "files": None,
        "renames": {"README.md": "documents.md"},
    },
    {
        "slug": "fai",
        "source": source("FAI_DIR", "/Users/h/fai"),
        "files": ["README.md", "SECURITY.md"],
        "titles": {"README.md": "README"},
        "renames": {"README.md": "project-readme.md"},
        "assets": [
            ("screenshots", "screenshots"),
            ("brand/renders/readme-header.png", "brand/renders/readme-header.png"),
        ],
    },
]
VAULT = next(
    (
        path
        for path in (Path.home() / "ObsidianVault", Path.home() / "Desktop" / "ObsidianVault")
        if path.exists()
    ),
    Path.home() / "Desktop" / "ObsidianVault",
)
EN = ROOT / "content" / "en"
WIKI = EN / "definitions"
NOTES = EN / "notes"
BLOGS = EN / "blogs"
ASSETS = ROOT / "assets" / "diagrams"
PORTFOLIO_ASSETS = ROOT / "assets" / "portfolio"
VAULT_ASSETS = ROOT / "assets" / "vault"

PAGES = {
    "00-setup.md": "setup.md",
    "cleanup-guide.md": "cleanup-guide.md",
    "costs-and-free-options.md": "costs-and-free-options.md",
}

MARKER = "<!-- imported from {source}. Edit the source, then run sync.py. -->"
IMAGE = re.compile(r"\]\(/([^)/]+\.(?:png|jpg|jpeg|gif|svg|webp))\)")
EMBED = re.compile(r"!\[\[([^\]|]+?)(?:\\?\|([^\]]+))?\]\]")
WIKI_LINK = re.compile(r"\[\[([^\]|\\]+?)(?:\\?\|([^\]]+))?\]\]")
TAG_LINE = re.compile(r"(?m)^(#[A-Za-z0-9/_-]+(?:\s+#[A-Za-z0-9/_-]+)*)\s*$")
COMMENT = re.compile(r"%%.*?%%", re.S)
FENCE = re.compile(r"^\s*(```|~~~)")

WIKI_DIRS = [
    ("studies/definitions", "Cloud", ["cloud", "fundamentals"]),
    ("webdev/general-concepts", "Web", ["web", "fundamentals"]),
]
WIKI_FILES = [
    ("studies/networking/OSI Model.md", "Networking", ["networking", "osi"]),
    ("studies/cybersecurity/cryptography.md", "Security", ["security", "cryptography"]),
    ("webdev/react/useState.md", "React", ["react", "hooks"]),
    ("webdev/react/useEffect.md", "React", ["react", "hooks"]),
    ("webdev/react/useRef.md", "React", ["react", "hooks"]),
    ("webdev/react/useReducer.md", "React", ["react", "hooks"]),
    ("webdev/react/suspense.md", "React", ["react", "components"]),
    ("webdev/react/react-lazy.md", "React", ["react", "performance"]),
    ("webdev/react/context-api/main-context-concepts.md", "React", ["react", "context"]),
    ("webdev/react/context-api/provider.md", "React", ["react", "context"]),
    ("webdev/react/design-patterns/controlled-elements.md", "React", ["react", "forms"]),
    ("webdev/react/design-patterns/prop-drilling.md", "React", ["react", "patterns"]),
]
NOTE_FILES = [
    ("studies/networking/main.md", "Networking", ["networking", "devices"], ""),
    ("studies/cybersecurity/Attack detection.md", "Security", ["security", "incident-response"], ""),
    ("studies/cybersecurity/Attack prevention strategies.md", "Security", ["security"], ""),
    ("studies/cybersecurity/Respond to attacks.md", "Security", ["security", "incident-response"], ""),
    ("studies/cybersecurity/threat intelligence.md", "Security", ["security", "threat-intelligence"], ""),
    ("studies/PCSE/PCSE Home.md", "GCP", ["gcp", "security", "pcse"], "pcse-home"),
    ("studies/PCSE/1 - Configuring Access.md", "GCP", ["gcp", "security", "pcse"], "pcse-1-configuring-access"),
    ("studies/PCSE/2 - Network Security.md", "GCP", ["gcp", "security", "pcse"], "pcse-2-network-security"),
    ("studies/PCSE/3 - Data Protection.md", "GCP", ["gcp", "security", "pcse"], "pcse-3-data-protection"),
    ("studies/PCSE/4 - Managing Operations.md", "GCP", ["gcp", "security", "pcse"], "pcse-4-managing-operations"),
    ("studies/PCSE/5 - Compliance.md", "GCP", ["gcp", "security", "pcse"], "pcse-5-compliance"),
    ("studies/PCSE/Cheat Sheets.md", "GCP", ["gcp", "security", "pcse"], "pcse-cheat-sheets"),
    ("studies/PCSE/gcloud Commands.md", "GCP", ["gcp", "security", "pcse"], "pcse-gcloud-commands"),
    ("webdev/TypeScript.md", "Web", ["web", "typescript"], ""),
    ("webdev/TailwindCSS.md", "Web", ["web", "css", "tailwind"], ""),
    ("webdev/SASS.md", "Web", ["web", "css", "sass"], ""),
    ("webdev/react/main-concepts.md", "React", ["react", "web"], ""),
    ("webdev/react/performance-optimizations.md", "React", ["react", "performance"], ""),
    ("webdev/react/react-router/setting-routes.md", "React", ["react", "react-router"], ""),
    ("webdev/react/react-router/loaders.md", "React", ["react", "react-router"], ""),
    ("webdev/react/react-router/forms.md", "React", ["react", "react-router"], ""),
]

EXTRA_TAGS = {
    "cidr": ["networking"],
    "containers": ["containers", "kubernetes"],
    "multi factor authentication": ["security"],
    "principle of least privilege": ["security"],
    "totp": ["security"],
    "traffic analysis": ["security"],
    "generative ai": ["ai"],
    "traditional ai": ["ai"],
    "infrastructure as code": ["iac"],
    "serverless": ["serverless"],
    "availability zones": ["geography"],
    "edge location": ["geography"],
    "region": ["geography"],
    "business continuity": ["reliability"],
    "disaster recovery": ["reliability"],
    "fault tolerance": ["reliability"],
    "high availability": ["reliability"],
    "high durability": ["reliability"],
    "rto": ["reliability"],
    "sla": ["reliability"],
}


def slugify(name: str) -> str:
    name = name.lower().replace("&", " and ")
    name = re.sub(r"[^a-z0-9]+", "-", name)
    return name.strip("-")


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    return yaml.safe_load(text[4:end]) or {}, text[end + 5:].lstrip("\n")


def clean_portfolio(body: str) -> str:
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


def vault_images() -> dict[str, Path]:
    found: dict[str, Path] = {}
    for path in VAULT.rglob("*"):
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}:
            found.setdefault(path.name, path)
    return found


def resolve_link(raw: str, mapping: dict[str, str]) -> tuple[str | None, str, str]:
    target = raw.strip()
    anchor = ""
    if "#" in target:
        target, anchor = target.split("#", 1)
    label = target.strip()
    if not target:
        return None, label, anchor
    for key in (target, target.lower(), slugify(target)):
        if key in mapping:
            return mapping[key], label, anchor
    return None, label, anchor


def transform_links(text: str, mapping: dict[str, str]) -> str:
    out: list[str] = []
    fenced = False
    for line in text.splitlines():
        if FENCE.match(line):
            fenced = not fenced
            out.append(line)
            continue
        if fenced:
            line = WIKI_LINK.sub(lambda m: m.group(2) or m.group(1), line)
            out.append(line)
            continue

        def replace(match: re.Match[str]) -> str:
            dest, label, _anchor = resolve_link(match.group(1), mapping)
            name = match.group(2) or label
            if not dest:
                return name
            if match.group(2):
                return f"[[{dest}|{name}]]"
            if dest == label:
                return f"[[{dest}]]"
            return f"[[{dest}|{label}]]"

        out.append(WIKI_LINK.sub(replace, line))
    return "\n".join(out)


def clean_vault(body: str, mapping: dict[str, str], images: dict[str, Path]) -> str:
    body = COMMENT.sub("", body)
    body = body.replace("\u2014", " - ")
    body = TAG_LINE.sub("", body)
    VAULT_ASSETS.mkdir(parents=True, exist_ok=True)

    def embed(match: re.Match[str]) -> str:
        name = match.group(1).strip()
        alt = (match.group(2) or "").strip()
        if name.lower().endswith(".md"):
            return ""
        source = images.get(name)
        if not source:
            return ""
        dest = VAULT_ASSETS / re.sub(r"\s+", "-", name.lower())
        if not dest.exists() or dest.stat().st_mtime < source.stat().st_mtime:
            shutil.copy2(source, dest)
        return f"![{alt}](/assets/vault/{dest.name})"

    body = EMBED.sub(embed, body)
    body = transform_links(body, mapping)
    body = re.sub(r"(?m)^====\s*$", "", body)
    body = re.sub(r"==([^=\n]+)==", r"**\1**", body)
    body = body.lstrip("\n")
    body = re.sub(r"\A# .+\n", "", body)
    return re.sub(r"\n{3,}", "\n\n", body).strip()


def describe(body: str) -> str:
    text = re.sub(r"```.*?```", "", body, flags=re.S)
    for block in re.split(r"\n\s*\n", text):
        block = block.strip().splitlines()[0] if block.strip() else ""
        if not block or block.startswith(("#", "|", "-", "*", "!", ">", "`")):
            continue
        line = WIKI_LINK.sub(lambda m: m.group(2) or m.group(1), block)
        line = EMBED.sub("", line)
        line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
        line = re.sub(r"[*_`>#]", "", line)
        line = " ".join(line.split())
        if len(line) > 20:
            return line[:200].rstrip()
    return ""


def frontmatter(meta: dict) -> str:
    data = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True).strip()
    return f"---\n{data}\n---\n"


def tag_line(tags: list[str]) -> list[str]:
    if not tags:
        return []
    return [" ".join(f"`{tag}`" for tag in tags), ""]


def project_page(stem: str, meta: dict, body: str) -> str:
    title = meta.get("name") or stem
    tags = meta.get("tags") or []
    page_meta = {
        "title": title,
        "date": meta.get("date", ""),
        "description": str(meta.get("description") or "").strip(),
        "tags": tags,
    }
    lines = [
        frontmatter(page_meta),
        MARKER.format(source=f"portfolio/src/data/{stem}.md"),
        "",
        f"# {title}",
        "",
        "**Status:** Active",
        "",
    ]
    if meta.get("description"):
        lines += [str(meta["description"]).strip(), ""]
    lines += tag_line(tags)
    lines += link_block(meta)
    lines += [body, ""]
    return "\n".join(lines)


def blog_page(stem: str, meta: dict, body: str) -> str:
    title = meta.get("name") or stem
    tags = meta.get("tags") or []
    page_meta = {
        "title": title,
        "date": meta.get("date", ""),
        "description": str(meta.get("description") or "").strip(),
        "tags": tags,
    }
    lines = [
        frontmatter(page_meta),
        MARKER.format(source=f"portfolio/src/data/{stem}.md"),
        "",
        f"# {title}",
        "",
        f"**Published:** {meta.get('date', '')}",
        "",
    ]
    if meta.get("description"):
        lines += [str(meta["description"]).strip(), ""]
    lines += tag_line(tags)
    lines += link_block(meta)
    lines += [body, ""]
    return "\n".join(lines)


def vault_page(source: Path, title: str, category: str, tags: list[str], body: str) -> str:
    rel = source.relative_to(VAULT).as_posix()
    description = describe(body)
    if not description:
        kind = "definition" if source.is_relative_to(VAULT / "studies" / "definitions") else "note"
        description = f"{category} {kind}: {title}."
    page_meta = {
        "title": title,
        "category": category,
        "description": description,
        "tags": tags,
    }
    lines = [
        frontmatter(page_meta),
        MARKER.format(source=f"ObsidianVault/{rel}"),
        "",
        f"# {title}",
        "",
    ]
    lines += tag_line(tags)
    lines += [body, ""]
    return "\n".join(lines)


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


def generated(path: Path, source: str) -> bool:
    text = path.read_text()
    return "<!-- imported from " in text and source in text


def title_from(source: Path, body: str) -> str:
    match = re.search(r"^# (.+)$", body, re.M)
    if match and match.start() == 0:
        return match.group(1).strip()
    stem = source.stem
    return stem[:1].upper() + stem[1:]


def sync_portfolio() -> tuple[int, int]:
    written: set[Path] = set()
    projects = blogs = 0
    for src in sorted(PORTFOLIO.glob("*.md")):
        stem = src.stem
        if stem == "template":
            continue
        data, body = split_frontmatter(src.read_text())
        meta = data.get(stem) or next(iter(data.values()), {})
        if not meta or not meta.get("show", True):
            continue
        body = clean_portfolio(body)
        if meta.get("type") == "blog":
            dest = BLOGS / f"{stem}.md"
            text = blog_page(stem, meta, body)
        else:
            if (EN / "projects" / stem / "index.md").exists():
                continue
            dest = EN / "projects" / f"{stem}.md"
            text = project_page(stem, meta, body)
        if dest.exists() and not generated(dest, "portfolio/"):
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text)
        written.add(dest)
        if meta.get("type") == "blog":
            blogs += 1
        else:
            projects += 1
    for folder in (EN / "projects", WIKI, BLOGS):
        for path in folder.rglob("*.md"):
            if generated(path, "portfolio/") and path not in written:
                path.unlink()
    return projects, blogs


def sync_vault() -> tuple[int, int]:
    jobs: list[tuple[Path, Path, str, list[str]]] = []
    for folder, category, tags in WIKI_DIRS:
        for src in sorted((VAULT / folder).glob("*.md")):
            tags_all = list(dict.fromkeys(tags + EXTRA_TAGS.get(src.stem.lower(), [])))
            dest = WIKI / slugify(category) / f"{slugify(src.stem)}.md"
            jobs.append((src, dest, category, tags_all))
    for name, category, tags in WIKI_FILES:
        src = VAULT / name
        if src.exists():
            dest = WIKI / slugify(category) / f"{slugify(src.stem)}.md"
            jobs.append((src, dest, category, tags))
    for name, category, tags, override in NOTE_FILES:
        src = VAULT / name
        if not src.exists() or src.stat().st_size < 80:
            continue
        dest = NOTES / slugify(category) / f"{override or slugify(src.stem)}.md"
        jobs.append((src, dest, category, tags))

    dest_stems = [dest.stem for _src, dest, _cat, _tags in jobs]
    duplicate = [stem for stem, count in Counter(dest_stems).items() if count > 1]
    if duplicate:
        raise SystemExit(f"duplicate vault page names: {duplicate}")

    existing = [path for path in EN.rglob("*.md")]
    counts = Counter(path.stem for path in existing)
    mapping = {stem: stem for stem, count in counts.items() if count == 1}
    for src, dest, _cat, _tags in jobs:
        mapping[src.stem] = dest.stem
        mapping[src.stem.lower()] = dest.stem
        mapping[dest.stem] = dest.stem

    images = vault_images()
    written: set[Path] = set()
    wiki = notes = 0
    for src, dest, category, tags in jobs:
        _meta, raw = split_frontmatter(src.read_text())
        title = title_from(src, raw)
        body = clean_vault(raw, mapping, images)
        if len(body) < 10:
            continue
        text = vault_page(src, title, category, tags, body)
        if dest.exists() and not generated(dest, "ObsidianVault/"):
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text)
        written.add(dest)
        if dest.is_relative_to(WIKI):
            wiki += 1
        else:
            notes += 1
    for folder in (WIKI, NOTES):
        for path in folder.rglob("*.md"):
            if path.name != "index.md" and generated(path, "ObsidianVault/") and path not in written:
                path.unlink()
    return wiki, notes


def sync_project_docs() -> int:
    count = 0
    for spec in PROJECT_DOCS:
        source: Path = spec["source"]
        dest = EN / "projects" / spec["slug"]
        dest.mkdir(parents=True, exist_ok=True)
        for old in dest.rglob("*.md"):
            if old.name == "index.md" and old.parent == dest:
                continue
            old.unlink()

        if spec["files"]:
            sources = [source / name for name in spec["files"]]
        else:
            sources = sorted(source.rglob("*.md"))
        for src in sources:
            if not src.exists():
                continue
            if src.name == "index.md" and src.parent == source:
                continue
            rel = src.relative_to(source)
            target = dest / (spec.get("renames") or {}).get(rel.as_posix(), rel.as_posix())
            target.parent.mkdir(parents=True, exist_ok=True)
            text = src.read_text()
            title = (spec.get("titles") or {}).get(rel.as_posix())
            if title:
                text = re.sub(r"^# .+$", f"# {title}", text, count=1, flags=re.M)
            text = re.sub(r"\[\[([^\]]+)\]\]", r"\\[\\[\1\\]\\]", text)
            target.write_text(text)
            count += 1

        for src_name, dst_name in spec.get("assets", []):
            src_path = source / src_name
            if src_path.is_dir():
                shutil.copytree(src_path, dest / dst_name, dirs_exist_ok=True)
            elif src_path.exists():
                target = dest / dst_name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, target)
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--portfolio",
        action="store_true",
        help="import only the portfolio project pages and blog posts",
    )
    args = parser.parse_args()
    if args.portfolio:
        projects, blogs = sync_portfolio()
        print(f"synced {projects} projects and {blogs} blogs from the portfolio")
        return

    episodes = sync_four_hats()
    projects, blogs = sync_portfolio()
    wiki, notes = sync_vault()
    docs = sync_project_docs()
    print(
        f"synced {episodes} episodes, {projects} projects, {blogs} blogs, "
        f"{wiki} definitions, {notes} notes, {docs} project docs"
    )


if __name__ == "__main__":
    main()
