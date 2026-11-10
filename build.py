#!/usr/bin/env python3
"""Build the bilingual site with Zensical.

English is built to /, Arabic to /ar/. Each language gets its own nav, search
index, UI strings, and direction. The Arabic pages carry Arabic theory and the
same English verified apply steps as the English page.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import shutil
import subprocess
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

import yaml

import sync

ROOT = Path(__file__).resolve().parent
FOUR_HATS = Path("/Users/h/mk-project/four-hats")
CONTENT = ROOT / "content"
ASSETS = ROOT / "assets"
BUILD = ROOT / "build"
SOURCES = ROOT / "sources"
ACT_ROOT = SOURCES if any(SOURCES.glob("act*.md")) else FOUR_HATS / "docs"
SITE = ROOT / "site"
TASKS = yaml.safe_load((ROOT / "episode-tasks.yaml").read_text())["episodes"]
CATALOG = yaml.safe_load((ROOT / "catalog.yaml").read_text())
ZENSICAL = os.environ.get("ZENSICAL") or shutil.which("zensical") or "/Users/h/branding/.venv/bin/zensical"

SITE_URL = "https://docs.alialjaffer.com"

ACTS = [
    (0, 1, "Introduction", "المقدمة"),
    (2, 6, "Act 1: Software Engineer", "المسار 1: مهندس البرمجيات"),
    (7, 10, "Act 2: Cloud Engineer", "المسار 2: مهندس السحابة"),
    (11, 19, "Act 3: DevOps Engineer", "المسار 3: مهندس DevOps"),
    (20, 25, "Act 4: Cybersecurity Engineer", "المسار 4: مهندس الأمن السيبراني"),
    (26, 26, "Wrap up", "الختام"),
]

LABELS = {
    "en": {
        "home": "Home",
        "four": "Four Hats",
        "overview": "Overview",
        "episodes": "Episodes",
        "setup": "Setup",
        "cleanup": "Cleanup",
        "costs": "Costs and free options",
        "projects": "Projects",
        "courses": "Courses",
        "blogs": "Blogs",
        "notes": "Notes",
        "graph": "Graph",
        "definitions": "Definitions",
        "contact": "Contact",
        "site": "Docs",
        "switch": "العربية",
        "apply_note": "Copied from `{file}`. Edit the act guide, not this page.",
    },
    "ar": {
        "home": "الرئيسية",
        "four": "أربع قبعات",
        "overview": "نظرة عامة",
        "episodes": "الحلقات",
        "setup": "الإعداد",
        "cleanup": "التنظيف",
        "costs": "التكلفة والخيارات المجانية",
        "projects": "المشاريع",
        "courses": "الدورات",
        "blogs": "المدونات",
        "notes": "الملاحظات",
        "graph": "الخريطة",
        "definitions": "التعريفات",
        "contact": "اتصل",
        "site": "الوثائق",
        "switch": "English",
        "apply_note": "الخطوات التالية منقولة من `{file}`. عدّل دليل المسار، لا هذه الصفحة.",
    },
}

BASE_THEME = """\
site_name: {site_name}
site_url: {site_url}
docs_dir: {docs_dir}
site_dir: {site_dir}
theme:
  name: material
  language: {language}
  palette:
    - scheme: default
      media: "(prefers-color-scheme: light)"
      toggle: {{icon: material/weather-night, name: Night}}
    - scheme: slate
      media: "(prefers-color-scheme: dark)"
      toggle: {{icon: material/weather-sunny, name: Day}}
  features: [navigation.tabs, navigation.top, content.code.copy, content.code.annotate]
markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.tasklist:
      custom_checkbox: true
  - attr_list
  - tables
  - toc:
      permalink: true
extra_css:
  - assets/extra.css?v={asset_version}
  - assets/hover.css?v={asset_version}
  - assets/graph.css?v={asset_version}
  - assets/diagram-zoom.css?v={asset_version}
extra_javascript:
  - assets/vendor/panzoom.min.js
  - assets/diagram-zoom.js?v={asset_version}
  - assets/graph.js?v={asset_version}
  - assets/hover.js?v={asset_version}
  - assets/analytics.js?v={asset_version}
"""


def asset_version() -> str:
    digest = hashlib.sha256()
    for name in ("extra.css", "hover.css", "graph.css", "diagram-zoom.css", "hover.js", "graph.js", "diagram-zoom.js", "analytics.js"):
        digest.update((ASSETS / name).read_bytes())
    return digest.hexdigest()[:10]


def title_of(path: Path) -> str:
    text = path.read_text()
    match = re.search(r"^# (.+)$", text, flags=re.M)
    return match.group(1).strip() if match else path.stem


def meta_of(path: Path) -> dict:
    text = path.read_text()
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    return yaml.safe_load(text[4:end]) or {}


WIKI_ORDER = [
    "GCP", "AWS", "Cloud", "Networking", "Security", "AI", "React", "Web",
    "Other",
]
NOTES_ORDER = [
    "GCP", "GCP Networking", "GCP Security", "GCP Compute", "GCP Databases",
    "GCP Storage", "GCP DevOps", "GCP Data analytics", "GCP Operations",
    "GCP Management", "GCP AI", "GCP Services", "Cloud", "Security", "AI",
    "Networking", "DevOps", "Terraform", "Certifications", "Projects",
    "React", "Web", "Interviews", "Career", "Site", "Other",
]


CATEGORY_NAMES = {"gcp": "GCP", "ai": "AI"}


def category_of(path: Path, folder: Path) -> str:
    meta = meta_of(path)
    if meta.get("category"):
        return meta["category"]
    name = path.parent.name
    if path.parent == folder:
        return "Other"
    return CATEGORY_NAMES.get(name, name.replace("-", " ").title())


def group_pages(folder: Path) -> dict[str, list[Path]]:
    groups: dict[str, list[Path]] = {}
    for path in folder.rglob("*.md"):
        if path.name == "index.md":
            continue
        category = category_of(path, folder)
        groups.setdefault(category, []).append(path)
    for pages in groups.values():
        pages.sort(key=title_of)
    return groups


def ordered_groups(
    groups: dict[str, list[Path]], preferred: list[str]
) -> list[tuple[str, list[Path]]]:
    names = [name for name in preferred if name in groups]
    names += sorted(name for name in groups if name not in preferred)
    return [(name, groups[name]) for name in names]


def section_index(
    root: Path, folder: str, title: str, intro: str, order: list[str]
) -> None:
    base = root / folder
    if not base.exists():
        return
    groups = group_pages(base)
    if not groups:
        return
    lines = [f"# {title}", "", intro, ""]
    for category, pages in ordered_groups(groups, order):
        lines += [f"## {category}", ""]
        for page in pages:
            link = page.relative_to(base).as_posix()
            description = meta_of(page).get("description", "")
            entry = f"- [{title_of(page)}]({link})"
            lines += [entry + (f": {description}" if description else "")]
        lines.append("")
    if folder == "definitions":
        lines += [
            "## How mentions work",
            "",
            "Write a double-bracket link such as &#91;&#91;rest&#93;&#93; in any page. The build resolves it to the definition and records the backlink.",
            "",
            '!!! tip "Hover a term"',
            "    Move the pointer over a link to preview the definition without leaving the page.",
            "",
        ]
    (base / "index.md").write_text("\n".join(lines))


def blogs_index(root: Path, lang: str) -> None:
    if lang != "en":
        return
    folder = root / "blogs"
    if not folder.exists():
        return
    pages = [p for p in folder.glob("*.md") if p.name != "index.md"]
    if not pages:
        return
    pages.sort(key=lambda p: str(meta_of(p).get("date", "")), reverse=True)
    lines = [
        "# Blogs",
        "",
        "Writing from the portfolio: field notes, project stories, and lessons learned.",
        "",
        "| Date | Post |",
        "|---|---|",
    ]
    for page in pages:
        date = str(meta_of(page).get("date", ""))
        lines.append(f"| {date} | [{title_of(page)}]({page.name}) |")
    lines += [
        "",
        "The wiki holds the definitions these posts use. The notes hold the study material.",
        "",
    ]
    (folder / "index.md").write_text("\n".join(lines))



def apply_content(ep: str) -> tuple[str, str]:
    spec = TASKS.get(ep, {})
    if spec.get("apply") == "none" or not spec.get("file"):
        return "", ""
    path = ACT_ROOT / spec["file"]
    text = path.read_text()
    if "section" in spec:
        heading = spec["section"]
        match = re.search(
            rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, flags=re.M | re.S
        )
        if not match:
            raise SystemExit(f"{path.name}: section not found: {heading}")
        return match.group(1).strip(), spec["file"]
    blocks = []
    for number in spec.get("tasks", []):
        match = re.search(
            rf"^#### Task {number}: .+?(?=^#### Task |^### |^## |\Z)",
            text,
            flags=re.M | re.S,
        )
        if not match:
            raise SystemExit(f"{path.name}: Task {number} not found")
        blocks.append(match.group(0).strip())
    return "\n\n".join(blocks), spec["file"]


def inject_apply(page: Path, lang: str) -> None:
    marker = "<!-- APPLY -->"
    text = page.read_text()
    if marker not in text:
        return
    ep = page.name[:4]
    body, source = apply_content(ep)
    if not body:
        page.write_text(text.replace(marker, "").rstrip() + "\n")
        return
    note = LABELS[lang]["apply_note"].format(file=source)
    block = f"### {LABELS[lang]['apply_note'].split('`')[0].strip() or 'Apply'}\n\n{note}\n\n{body}\n"
    if lang == "en":
        block = f"### Verified steps\n\n{note}\n\n{body}\n"
    else:
        heading = "الخطوات الموثقة"
        block = f"### {heading}\n\n{note}\n\n{body}\n"
    page.write_text(text.replace(marker, block))


def episode_index(root: Path, lang: str) -> Path | None:
    eps = sorted((root / "four-hats" / "episodes").glob("ep*.md"))
    if not eps:
        return None
    lines = [f"# {LABELS[lang]['episodes']}", ""]
    by_number = {int(p.name[2:4]): p for p in eps}
    for start, end, label_en, label_ar in ACTS:
        group = [by_number[n] for n in range(start, end + 1) if n in by_number]
        if not group:
            continue
        lines += [f"## {label_en if lang == 'en' else label_ar}", "", "| Episode |", "|---|"]
        for path in group:
            title = title_of(path)
            lines.append(f"| [{title}](episodes/{path.name}) |")
        lines.append("")
    dest = root / "four-hats" / "episodes.md"
    dest.write_text("\n".join(lines))
    return dest


def project_entries(root: Path) -> list[dict]:
    entries = []
    for item in CATALOG.get("projects", []):
        entry = dict(item)
        if not entry.get("date"):
            page = root / item["page"]
            if page.exists():
                entry["date"] = str(meta_of(page).get("date", ""))
        entries.append(entry)
    seen = {item["page"] for item in entries}
    extra: list[dict] = []
    paths = list((root / "projects").glob("*.md")) + list((root / "projects").glob("*/index.md"))
    for path in paths:
        rel = path.relative_to(root).as_posix()
        if rel in seen:
            continue
        meta = meta_of(path)
        if not meta.get("title"):
            continue
        extra.append(
            {
                "slug": path.parent.name if path.name == "index.md" else path.stem,
                "title": meta.get("title"),
                "status": meta.get("status", "Active"),
                "summary": meta.get("description", ""),
                "tags": meta.get("tags", []),
                "page": rel,
                "date": str(meta.get("date", "")),
            }
        )
    extra.sort(key=lambda item: item["date"], reverse=True)
    entries.extend(extra)
    entries.sort(key=lambda item: str(item.get("date", "")), reverse=True)
    return entries


def inject_projects(root: Path) -> None:
    page = root / "index.md"
    marker = "<!-- PROJECTS -->"
    if not page.exists() or marker not in page.read_text():
        return
    lines = []
    for item in project_entries(root):
        summary = item.get("summary", "")
        lines.append(f"- [{item['title']}]({item['page']})" + (f": {summary}" if summary else ""))
    page.write_text(page.read_text().replace(marker, "\n".join(lines)))


def projects_index(root: Path, lang: str) -> None:
    if lang != "en":
        return
    projects = project_entries(root)
    if not projects:
        return
    lines = [
        "# Projects",
        "",
        CATALOG.get("site", {}).get("tagline", ""),
        "",
    ]
    for item in projects:
        page = Path(item["page"])
        target = f"{page.parent.name}/" if page.name == "index.md" else page.name
        lines += [
            f"## {item['title']}",
            "",
            f"**Status:** {item.get('status', 'Active')}",
            "",
            item.get("summary", ""),
            "",
            " ".join(f"`{tag}`" for tag in item.get("tags", [])),
            "",
            f"[Read the docs]({target})",
            "",
        ]
    dest = root / "projects"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "index.md").write_text("\n".join(lines))


def courses_index(root: Path, lang: str) -> None:
    if lang != "en":
        return
    courses = CATALOG.get("courses", [])
    if not courses:
        return
    lines = [
        "# Courses",
        "",
        "Long-form courses built around one project or one skill path.",
        "",
    ]
    for course in courses:
        lines += [
            f"## {course['title']}",
            "",
            f"**Status:** {course.get('status', 'Planned')}",
            "",
            course.get("summary", ""),
            "",
            " ".join(f"`{tag}`" for tag in course.get("tags", [])),
            "",
        ]
        page = course.get("page", "")
        if page:
            lines += [f"[Start the course](../{page})", ""]
    dest = root / "courses"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "index.md").write_text("\n".join(lines))


SUBDIR_LABELS = {"adr": "Decisions", "reference": "API reference"}


def project_nav(root: Path, item: dict) -> dict | None:
    page = root / item["page"]
    if not page.exists():
        return None
    if page.name != "index.md":
        return {item["title"]: item["page"]}
    parent = page.parent
    children: list = [{"Overview": item["page"]}]
    for path in sorted(parent.glob("*.md")):
        if path.name == "index.md":
            continue
        children.append({title_of(path): path.relative_to(root).as_posix()})
    for folder in sorted(p for p in parent.iterdir() if p.is_dir()):
        pages = sorted(folder.glob("*.md"))
        if not pages:
            continue
        children.append(
            {
                SUBDIR_LABELS.get(folder.name, folder.name.title()): [
                    {title_of(path): path.relative_to(root).as_posix()}
                    for path in pages
                ]
            }
        )
    return {item["title"]: children}


def section_nav(root: Path, folder: str, order: list[str]) -> list:
    base = root / folder
    pages = [p for p in base.rglob("*.md") if p.name != "index.md"]
    if not pages:
        return []
    if not any(category_of(page, base) != "Other" for page in pages):
        return [
            {title_of(page): page.relative_to(root).as_posix()}
            for page in sorted(pages, key=title_of)
        ]
    groups = group_pages(base)
    return [
        {
            category: [
                {title_of(page): page.relative_to(root).as_posix()}
                for page in group
            ]
        }
        for category, group in ordered_groups(groups, order)
    ]


def nav_for(root: Path, lang: str) -> list:
    labels = LABELS[lang]
    nav: list = [{"Home": "index.md"}]

    if (root / "projects" / "index.md").exists():
        children = [{"Overview": "projects/index.md"}]
        for item in project_entries(root):
            entry = project_nav(root, item)
            if entry:
                children.append(entry)
        nav.append({labels["projects"]: children})

    four = root / "four-hats"
    if (four / "index.md").exists():
        children = []
        if (root / "courses" / "index.md").exists():
            children.append({"Overview": "courses/index.md"})
        children.append({"Four Hats": []})
        four_children = [{"Overview": "four-hats/index.md"}]
        if (four / "setup.md").exists():
            four_children.append({labels["setup"]: "four-hats/setup.md"})
        if (four / "episodes.md").exists():
            four_children.append({labels["episodes"]: "four-hats/episodes.md"})
        by_number = {
            int(p.name[2:4]): p
            for p in (four / "episodes").glob("ep*.md")
        }
        for start, end, label_en, label_ar in ACTS:
            group = [by_number[n] for n in range(start, end + 1) if n in by_number]
            if not group:
                continue
            act: list = []
            for path in group:
                act.append({title_of(path): path.relative_to(root).as_posix()})
            four_children.append({label_en if lang == "en" else label_ar: act})
        for key, name in [
            ("cleanup", "four-hats/cleanup-guide.md"),
            ("costs", "four-hats/costs-and-free-options.md"),
        ]:
            if (root / name).exists():
                four_children.append({labels[key]: name})
        children[-1] = {"Four Hats": four_children}
        for course in CATALOG.get("courses", []):
            page = course.get("page", "")
            if page and course["slug"] != "four-hats" and (root / page).exists():
                children.append({course["title"]: page})
        nav.append({labels["courses"]: children})

    if (root / "blogs" / "index.md").exists():
        posts = [p for p in (root / "blogs").glob("*.md") if p.name != "index.md"]
        posts.sort(key=lambda p: str(meta_of(p).get("date", "")), reverse=True)
        children = [{"Overview": "blogs/index.md"}]
        for page in posts:
            children.append({title_of(page): page.relative_to(root).as_posix()})
        nav.append({labels["blogs"]: children})

    if (root / "notes" / "index.md").exists():
        children = [{"Overview": "notes/index.md"}]
        children += section_nav(root, "notes", NOTES_ORDER)
        nav.append({labels["notes"]: children})

    if (root / "graph.md").exists():
        nav.append({labels["graph"]: "graph.md"})

    if (root / "definitions" / "index.md").exists():
        children = [{"Overview": "definitions/index.md"}]
        children += section_nav(root, "definitions", WIKI_ORDER)
        nav.append({labels["definitions"]: children})

    if (root / "contact.md").exists():
        nav.append({labels["contact"]: "contact.md"})

    return nav


CALLOUT = re.compile(r"^> \[!(\w+)\][+-]?\s*(.*)$")


def convert_callouts(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        match = CALLOUT.match(lines[i])
        if not match:
            out.append(lines[i])
            i += 1
            continue
        kind, title = match.group(1).lower(), match.group(2).strip()
        out.append(f'!!! {kind} "{title}"' if title else f"!!! {kind}")
        i += 1
        while i < len(lines) and lines[i].startswith(">"):
            body = lines[i][1:].lstrip()
            out.append(f"    {body}" if body else "")
            i += 1
    return "\n".join(out)


WIKI = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


def page_url(rel: str, lang: str) -> str:
    prefix = "/ar" if lang == "ar" else ""
    return f"{prefix}/{rel}/" if rel else f"{prefix}/"


def process_wiki(root: Path, lang: str) -> None:
    files = sorted(root.rglob("*.md"))
    index: dict[str, Path] = {}
    stems: dict[str, list[Path]] = {}
    for path in files:
        rel = path.relative_to(root).with_suffix("").as_posix()
        index[rel] = path
        if rel.startswith("definitions/"):
            index[rel.removeprefix("definitions/")] = path
        if path.stem != "index":
            stems.setdefault(path.stem, []).append(path)
    for stem, paths in stems.items():
        if len(paths) == 1:
            index[stem] = paths[0]

    titles = {}
    for path in files:
        match = re.search(r"^# (.+)$", path.read_text(), flags=re.M)
        titles[path] = match.group(1).strip() if match else path.stem

    backlinks: dict[str, list[dict[str, str]]] = {}
    for path in files:
        text = path.read_text()

        def replace(match: re.Match[str]) -> str:
            target = match.group(1).strip()
            label = (match.group(2) or target).strip()
            if target not in index:
                raise SystemExit(f"{path.name}: missing wikilink target: {target}")
            dest = index[target]
            url = page_url(dest.relative_to(root).with_suffix("").as_posix(), lang)
            source = page_url(path.relative_to(root).with_suffix("").as_posix(), lang)
            entry = {"title": titles[path], "url": source}
            bucket = backlinks.setdefault(url, [])
            if entry not in bucket:
                bucket.append(entry)
            return f"[{label}]({url})"

        path.write_text(WIKI.sub(replace, text))

    for bucket in backlinks.values():
        bucket.sort(key=lambda item: item["title"])
    out = root / "assets" / "backlinks.json"
    out.write_text(json.dumps(backlinks, indent=2, ensure_ascii=False) + "\n")


def assemble(lang: str) -> Path:
    root = BUILD / lang
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(CONTENT / lang, root)
    shutil.copytree(
        ASSETS,
        root / "assets",
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("slides"),
    )
    for page in root.rglob("*.md"):
        text = page.read_text()
        text = convert_callouts(text)
        text = text.replace("](../assets/", "](../../assets/")
        text = text.replace("](../../assets/diagrams/", "](../../assets/diagrams/")
        text = re.sub(
            r"\]\(\.\./(?:act[1-4]-[a-z-]+\.md)(#[^)]*)?\)",
            lambda m: "](https://github.com/aliAljaffer/four-hats/blob/main/docs/"
            + m.group(0).split("../", 1)[1],
            text,
        )
        text = text.replace("](../00-setup.md", "](../setup.md")
        page.write_text(text)
        inject_apply(page, lang)
        text = page.read_text()
        text = re.sub(
            r"\]\((?:\.\./)*(?:four-hats/)?(costs-and-free-options|cleanup-guide)\.md\)",
            r"](/four-hats/\1/)",
            text,
        )
        text = text.replace(
            "](../cv/skills-ledger.md)",
            "](https://github.com/aliAljaffer/four-hats/blob/main/cv/skills-ledger.md)",
        )
        page.write_text(text)
    episode_index(root, lang)
    inject_projects(root)
    projects_index(root, lang)
    courses_index(root, lang)
    blogs_index(root, lang)
    section_index(
        root,
        "notes",
        "Notes",
        "Study notes, course summaries, and working reference material.",
        NOTES_ORDER,
    )
    section_index(
        root,
        "definitions",
        "Definitions",
        "Definitions and informational terms. Link to a definition once, and every page that mentions it appears under **Linked from**.",
        WIKI_ORDER,
    )
    process_wiki(root, lang)
    return root


def write_config(lang: str, docs_dir: Path) -> Path:
    labels = LABELS[lang]
    if lang == "en":
        site_dir, site_url, language = SITE, f"{SITE_URL}/", "en"
    else:
        site_dir, site_url, language = SITE / "ar", f"{SITE_URL}/ar/", "ar"
    config = BASE_THEME.format(
        site_name=labels["site"],
        site_url=site_url,
        docs_dir=docs_dir.relative_to(ROOT).as_posix(),
        site_dir=site_dir.relative_to(ROOT).as_posix(),
        language=language,
        asset_version=asset_version(),
    )
    config += "\nnav:\n" + yaml.safe_dump(
        nav_for(docs_dir, lang), sort_keys=False, allow_unicode=True
    )
    path = ROOT / f"mkdocs.{lang}.yml"
    path.write_text(config)
    return path


def build(lang: str, docs_dir: Path) -> None:
    config = write_config(lang, docs_dir)
    result = subprocess.run(
        [ZENSICAL, "build", "-f", str(config)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise SystemExit(result.stdout + result.stderr)
    print(result.stdout.strip().splitlines()[-1])


def rel_path(html: Path, base: Path) -> str:
    rel = html.relative_to(base)
    if rel.name == "index.html":
        return rel.parent.as_posix().removeprefix(".")
    return rel.with_suffix("").as_posix()


def pair_exists(lang: str, rel: str) -> bool:
    other = "ar" if lang == "en" else "en"
    return (CONTENT / other / (rel or ".") / "index.md").exists() or (
        CONTENT / other / f"{rel}.md"
    ).exists()


def localised_url(rel: str, lang: str) -> str:
    prefix = "" if lang == "en" else "/ar"
    suffix = f"/{rel}/" if rel else "/"
    return f"{SITE_URL}{prefix}{suffix}"


def postprocess(base: Path, lang: str) -> None:
    labels = LABELS[lang]
    for html in base.rglob("*.html"):
        if lang == "en" and (SITE / "ar") in html.parents:
            continue
        rel = rel_path(html, base)
        text = html.read_text()
        if pair_exists(lang, rel):
            other = "ar" if lang == "en" else "en"
            links = (
                f'<link rel="alternate" hreflang="en" href="{localised_url(rel, "en")}">'
                f'<link rel="alternate" hreflang="ar" href="{localised_url(rel, "ar")}">'
                f'<link rel="alternate" hreflang="x-default" href="{localised_url(rel, "en")}">'
            )
            text = text.replace("</head>", links + "</head>", 1)
            target = f"/ar/{rel}/" if lang == "en" and rel else (
                "/ar/" if lang == "en" else (f"/{rel}/" if rel else "/")
            )
            switch = (
                f'<a class="lang-switch" href="{target}" '
                f'hreflang="{other}" lang="{other}">{labels["switch"]}</a>'
            )
            text = text.replace('<div class="md-search"', switch + '<div class="md-search"', 1)
        html.write_text(text)


def publish_slides() -> None:
    source = ASSETS / "slides"
    decks = sorted(source.glob("ep*.html"))
    if not decks:
        return
    dest = SITE / "slides"
    dest.mkdir(parents=True, exist_ok=True)
    for deck in decks:
        html = deck.read_text()
        if "/assets/analytics.js" not in html:
            html = html.replace(
                "</body>",
                f'<script src="/assets/analytics.js?v={asset_version()}"></script></body>',
            )
        (dest / deck.name).write_text(html)
    for extra in source.glob("*.css"):
        shutil.copy2(extra, dest / extra.name)
    fonts = source / "fonts"
    if fonts.exists():
        shutil.copytree(fonts, dest / "fonts", dirs_exist_ok=True)
    rows = "\n".join(
        f'<li><a href="{deck.name}">{deck.stem.replace("-", " ")}</a></li>'
        for deck in decks
    )
    (dest / "index.html").write_text(
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"robots\" content=\"noindex\"><title>Slides</title>"
        "<style>body{font-family:system-ui;max-width:60rem;margin:3rem auto;"
        "padding:0 1rem;line-height:1.6}li{margin:.4rem 0}</style></head>"
        f"<body><h1>Slides</h1><p>Raw 16:9 decks. These are visual aids, not lessons.</p><ul>{rows}</ul></body></html>"
    )


class ContentLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.inside = 0
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "article" and "md-content__inner" in (values.get("class") or ""):
            self.inside += 1
        if self.inside and tag == "a" and values.get("href"):
            self.hrefs.append(values["href"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "article" and self.inside:
            self.inside -= 1


def graph_url(path: Path, base: Path, lang: str) -> str:
    rel = path.relative_to(base)
    if rel.name == "index.html":
        rel = rel.parent
    else:
        rel = rel.with_suffix("")
    prefix = "/ar" if lang == "ar" else ""
    part = rel.as_posix().strip("/")
    if part == ".":
        part = ""
    return f"{prefix}/{part}/" if part else f"{prefix}/"


def page_title(text: str) -> str:
    match = re.search(r"<h1[^>]*>(.*?)</h1>", text, flags=re.S)
    raw = match.group(1) if match else ""
    return unescape(re.sub(r"<[^>]+>", "", raw)).replace("¶", "").strip()


def page_type(rel: str) -> str:
    parts = Path(rel).parts
    if not parts:
        return "page"
    if parts[0] == "projects":
        return "project"
    if parts[0] == "four-hats":
        return "episode" if "episodes" in parts else "course"
    if parts[0] == "courses":
        return "collection"
    if parts[0] == "definitions":
        return "definition"
    if parts[0] == "notes":
        return "note"
    return "page"


def page_group(rel: str) -> str:
    parts = Path(rel).parts
    if not parts:
        return "root"
    if parts[0] == "four-hats":
        return "four-hats/episodes" if "episodes" in parts else "four-hats"
    if parts[0] in {"projects", "definitions", "notes"} and len(parts) > 2:
        return f"{parts[0]}/{parts[1]}"
    return parts[0]


def build_graph(base: Path, lang: str) -> None:
    pages: dict[str, Path] = {}
    for html in base.rglob("*.html"):
        parts = html.relative_to(base).parts
        if "404" in html.name or "assets" in parts or "slides" in parts:
            continue
        pages[graph_url(html, base, lang)] = html

    nodes = []
    for url, path in sorted(pages.items()):
        text = path.read_text()
        rel = path.relative_to(base).as_posix()
        nodes.append(
            {
                "id": url,
                "title": page_title(text) or Path(rel).stem,
                "type": page_type(rel),
                "group": page_group(rel),
            }
        )

    links: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for url, path in pages.items():
        parser = ContentLinks()
        parser.feed(path.read_text())
        for href in parser.hrefs:
            parsed = urlparse(href)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            if parsed.path.startswith("/"):
                if lang == "ar" and parsed.path.startswith("/ar/"):
                    target = SITE / parsed.path.lstrip("/")
                else:
                    target = base / parsed.path.lstrip("/")
            else:
                target = (path.parent / parsed.path).resolve()
            if target.is_dir() or parsed.path.endswith("/"):
                target = target / "index.html"
            elif target.suffix == "":
                target = target / "index.html"
            try:
                target.relative_to(base)
            except ValueError:
                continue
            if not target.exists() or target.suffix != ".html":
                continue
            dest = graph_url(target, base, lang)
            if dest == url or dest not in pages:
                continue
            edge = (url, dest)
            if edge not in seen:
                seen.add(edge)
                links.append({"source": url, "target": dest})

    payload = {"nodes": nodes, "links": links}
    (base / "assets" / "graph.json").write_text(
        json.dumps(payload, ensure_ascii=False) + "\n"
    )


def run() -> None:
    if sync.PORTFOLIO.exists():
        sync.sync_portfolio()
    if SITE.exists():
        shutil.rmtree(SITE)
    for lang in ("en", "ar"):
        root = assemble(lang)
        build(lang, root)
    postprocess(SITE, "en")
    postprocess(SITE / "ar", "ar")
    build_graph(SITE, "en")
    build_graph(SITE / "ar", "ar")
    publish_slides()
    print("built site/ and site/ar/")


def main() -> None:
    with open(ROOT / ".build.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        run()


if __name__ == "__main__":
    main()
