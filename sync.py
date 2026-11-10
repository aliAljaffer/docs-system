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
        "slug": "s2t",
        "source": source("S2T_DIR", "/Users/h/s2t"),
        "files": ["README.md", "CHANGELOG.md", "CONTRIBUTING.md"],
        "titles": {"README.md": "README"},
        "renames": {"README.md": "project-readme.md"},
        "assets": [("images", "images")],
        "links": {
            ".github/workflows/release.yml": "https://github.com/aliAljaffer/s2t/blob/main/.github/workflows/release.yml",
            "Formula/s2t.rb": "https://github.com/aliAljaffer/s2t/blob/main/Formula/s2t.rb",
            "LICENSE": "https://github.com/aliAljaffer/s2t/blob/main/LICENSE",
        },
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
    "00-setup.md": "four-hats/setup.md",
    "cleanup-guide.md": "four-hats/cleanup-guide.md",
    "costs-and-free-options.md": "four-hats/costs-and-free-options.md",
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
    ("studies/networking/main.md", "Networking", ["networking", "devices"]),
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
SERVICE_DEFINITION_DIRS = [
    ("studies/cloud-architecht/gcp/networking", "GCP", ["gcp", "networking"]),
    ("studies/cloud-architecht/gcp/security", "GCP", ["gcp", "security"]),
    ("studies/cloud-architecht/gcp/compute", "GCP", ["gcp", "compute"]),
    ("studies/cloud-architecht/gcp/databases", "GCP", ["gcp", "databases"]),
    ("studies/cloud-architecht/gcp/storage", "GCP", ["gcp", "storage"]),
    ("studies/cloud-architecht/gcp/devops", "GCP", ["gcp", "devops"]),
    ("studies/cloud-architecht/gcp/data-analytics", "GCP", ["gcp", "data"]),
    ("studies/cloud-architecht/gcp/operations", "GCP", ["gcp", "operations"]),
    ("studies/cloud-architecht/gcp/management", "GCP", ["gcp", "management"]),
    ("studies/cloud-architecht/gcp/ai-ml", "GCP", ["gcp", "ai"]),
    ("studies/cloud-architecht/gcp/services", "GCP", ["gcp", "services"]),
    ("studies/cloud-architecht/services", "AWS", ["aws", "services"]),
]
CLOUD_DEFINITION_SLUGS = {
    "aws-compute", "aws-networking", "aws-security", "aws-services", "aws-storage",
    "ec2-user-data", "restful-apis", "cloud-concepts", "vms-and-containers",
    "free-services", "tagging", "allocation-tags", "partner-network",
    "application-integration", "operational-excellence-pillars",
    "cost-optimization-pillar", "performance-efficiency-pillar",
    "reliability-pillars", "security-pillars", "total-cost-of-ownership",
    "migration-strategies", "cloud-adoption-framework", "logging",
    "governance-and-compliance", "autoscaling-groups-and-load-balancers",
    "allocation-tags",
}
AWS_DEFINITION_SLUGS = {
    "aws-compute", "aws-networking", "aws-security", "aws-services", "aws-storage",
    "ec2-user-data", "free-services", "autoscaling-groups-and-load-balancers",
    "allocation-tags",
}
TITLE_OVERRIDES = {
    VAULT / "studies/networking/main.md": "Network devices",
    VAULT / "studies/cloud-architecht/gcp/readme.md": "GCP notes index",
}
EXTRA_NOTES = [
    ("studies/How to Get Into Tech.md", "Career", ["career"]),
]
NOTE_RULES = [
    ("studies/cloud-architecht/gcp", "GCP", "glob", ["gcp"]),
    ("studies/cloud-architecht/unsorted", "GCP", "rglob", ["gcp"]),
    ("studies/cloud-architecht/quizzes", "GCP", "rglob", ["gcp", "quiz"]),
    ("studies/cloud-architecht", "Certifications", "glob", ["certification"]),
    ("studies/DevOps Bootcamp", "DevOps", "rglob", ["devops"]),
    ("studies/PCSE", "GCP", "rglob", ["gcp", "security", "pcse"]),
    ("studies/cybersecurity", "Security", "rglob", ["security"]),
    ("studies/terraform", "Terraform", "rglob", ["terraform"]),
    ("webdev/react", "React", "rglob", ["react"]),
    ("webdev/interviews", "Interviews", "rglob", ["interview"]),
    ("webdev", "Web", "glob", ["web"]),
]
SKIP_NAME = re.compile(
    r"(?i)^(untitled|drawing|agenda|topic|resume|practice exam results|main thoughts|"
    r"certification journey|script-sbom|! main|progress|.*study tracker|.*review topics)"
)
SKIP_SOURCES = {
    VAULT / "studies/networking/OSI Model.md",
    *[VAULT / name for name, _category, _tags in WIKI_FILES],
}

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


MD_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)#\s]+\.md)(#[^)]*)?\)")


def scrub_secrets(text: str) -> str:
    text = re.sub(r"AKIA[0-9A-Z]{16}", "<redacted-access-key>", text)
    text = re.sub(
        r"(?i)((?:secret|access)_key\s*=\s*\")[^\"]+(\")",
        r"\1<redacted>\2",
        text,
    )
    text = re.sub(
        r"(?i)(aws_secret_access_key\s*=\s*\")[^\"]+(\")",
        r"\1<redacted>\2",
        text,
    )
    return text


def clean_vault(
    body: str,
    mapping: dict[str, str],
    images: dict[str, Path],
    src: Path,
    source_map: dict[Path, Path],
) -> str:
    body = COMMENT.sub("", body)
    body = body.replace("\u2014", " - ")
    body = TAG_LINE.sub("", body)
    VAULT_ASSETS.mkdir(parents=True, exist_ok=True)

    def asset(source: Path, raw_name: str) -> str:
        raw = re.sub(r"\s+", "-", raw_name.lower())
        if source.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            dest = VAULT_ASSETS / f"{Path(raw).stem}.webp"
            if not dest.exists() or dest.stat().st_mtime < source.stat().st_mtime:
                subprocess.run(
                    ["magick", str(source), "-resize", "1400x", "-strip",
                     "-quality", "82", str(dest)],
                    check=True,
                )
        else:
            dest = VAULT_ASSETS / raw
            if not dest.exists() or dest.stat().st_mtime < source.stat().st_mtime:
                shutil.copy2(source, dest)
        return dest.name

    def embed(match: re.Match[str]) -> str:
        name = match.group(1).strip()
        alt = (match.group(2) or "").strip()
        if name.lower().endswith(".md"):
            return ""
        source = images.get(name)
        if not source:
            return ""
        return f"![{alt}](/assets/vault/{asset(source, name)})"

    def md_image(match: re.Match[str]) -> str:
        alt, href = match.group(1), match.group(2).strip()
        if href.startswith(("/", "http://", "https://", "data:")):
            return match.group(0)
        name = href.split()[0]
        source = (src.parent / name).resolve()
        if not source.exists():
            source = (src.parent / "images" / Path(name).name).resolve()
        if not source.exists():
            source = images.get(Path(name).name, Path())
        if not source.exists():
            return ""
        return f"![{alt}](/assets/vault/{asset(source, source.name)})"

    def md_link(match: re.Match[str]) -> str:
        label, href, anchor = match.group(1), match.group(2), match.group(3) or ""
        target = (src.parent / href).resolve()
        dest = source_map.get(target)
        if not dest:
            return label
        rel = dest.relative_to(EN).with_suffix("").as_posix()
        return f"[{label}](/{rel}/{anchor})"

    body = EMBED.sub(embed, body)
    body = MD_IMAGE.sub(md_image, body)
    body = MD_LINK.sub(md_link, body)
    body = transform_links(body, mapping)
    body = re.sub(r"(?m)^====\s*$", "", body)
    body = re.sub(r"==([^=\n]+)==", r"**\1**", body)
    body = body.lstrip("\n")
    body = re.sub(r"\A# .+\n", "", body)
    body = scrub_secrets(body)
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
            if path.name == "index.md":
                continue
            if generated(path, "portfolio/") and path not in written:
                path.unlink()
    return projects, blogs


GENERIC_TITLES = {"overview", "readme", "main", "index", "notes"}


def note_title(src: Path, rel: Path, meta: dict, body: str) -> str:
    if src in TITLE_OVERRIDES:
        return TITLE_OVERRIDES[src]
    if meta.get("title"):
        return str(meta["title"])
    match = re.search(r"^# (.+)$", body, re.M)
    if match and match.start() == 0:
        return match.group(1).strip()
    stem = rel.stem
    if stem.lower() in GENERIC_TITLES or re.fullmatch(r"day\s*\d+", stem, re.I):
        parts = rel.with_suffix("").parts[-2:]
        return " ".join(part.replace("-", " ").replace("_", " ").title() for part in parts)
    return src.stem[:1].upper() + src.stem[1:]


def sync_vault() -> tuple[int, int]:
    jobs: list[tuple[Path, Path, str, list[str], Path]] = []
    seen: set[Path] = set()
    for folder, category, tags in WIKI_DIRS:
        for src in sorted((VAULT / folder).glob("*.md")):
            tags_all = list(dict.fromkeys(tags + EXTRA_TAGS.get(src.stem.lower(), [])))
            dest = WIKI / slugify(category) / f"{slugify(src.stem)}.md"
            jobs.append((src, dest, category, tags_all, src.relative_to(VAULT / folder)))
            seen.add(src)
    for name, category, tags in WIKI_FILES:
        src = VAULT / name
        if src.exists():
            dest = WIKI / slugify(category) / f"{slugify(src.stem)}.md"
            jobs.append((src, dest, category, tags, Path(src.name)))
            seen.add(src)

    for folder, category, tags in SERVICE_DEFINITION_DIRS:
        base = VAULT / folder
        if not base.exists():
            continue
        for src in sorted(base.rglob("*.md")):
            if src in seen:
                continue
            rel = src.relative_to(base)
            stem = "-".join(slugify(part) for part in rel.with_suffix("").parts)
            if not stem:
                continue
            dest = WIKI / slugify(category) / f"{stem}.md"
            jobs.append((src, dest, category, tags, rel))
            seen.add(src)

    for folder, category, mode, tags in NOTE_RULES:
        base = VAULT / folder
        if not base.exists():
            continue
        sources = base.rglob("*.md") if mode == "rglob" else base.glob("*.md")
        for src in sorted(sources):
            if src in seen or src in SKIP_SOURCES:
                continue
            if SKIP_NAME.search(src.stem) or "excalidraw" in src.stem.lower():
                continue
            if src.stat().st_size < 40:
                continue
            rel = src.relative_to(base)
            stem = "-".join(slugify(part) for part in rel.with_suffix("").parts)
            if not stem:
                continue
            if slugify(src.stem) in CLOUD_DEFINITION_SLUGS:
                kind = "AWS" if slugify(src.stem) in AWS_DEFINITION_SLUGS else "Cloud"
                dest = WIKI / slugify(kind) / f"{stem}.md"
                jobs.append((src, dest, kind, tags, rel))
            else:
                dest = NOTES / slugify(category) / f"{stem}.md"
                jobs.append((src, dest, category, tags, rel))
            seen.add(src)

    for name, category, tags in EXTRA_NOTES:
        src = VAULT / name
        if not src.exists() or src in seen:
            continue
        dest = NOTES / slugify(category) / f"{slugify(src.stem)}.md"
        jobs.append((src, dest, category, tags, Path(src.name)))
        seen.add(src)

    dest_stems = [dest.stem for _src, dest, _cat, _tags, _rel in jobs]
    duplicate = [stem for stem, count in Counter(dest_stems).items() if count > 1]
    if duplicate:
        raise SystemExit(f"duplicate vault page names: {duplicate}")

    existing = [path for path in EN.rglob("*.md")]
    counts = Counter(path.stem for path in existing)
    mapping = {stem: stem for stem, count in counts.items() if count == 1}
    source_counts = Counter(src.stem for src, *_rest in jobs)
    for src, dest, _cat, _tags, _rel in jobs:
        if source_counts[src.stem] == 1:
            mapping[src.stem] = dest.stem
            mapping[src.stem.lower()] = dest.stem
        mapping[dest.stem] = dest.stem

    images = vault_images()
    source_map = {src.resolve(): dest for src, dest, *_rest in jobs}
    written: set[Path] = set()
    wiki = notes = 0
    for src, dest, category, tags, rel in jobs:
        meta, raw = split_frontmatter(src.read_text())
        title = note_title(src, rel, meta, raw)
        body = clean_vault(raw, mapping, images, src, source_map)
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
            text = text.replace("\u2014", " - ")
            for old, new in (spec.get("links") or {}).items():
                text = text.replace(f"]({old})", f"]({new})")
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
