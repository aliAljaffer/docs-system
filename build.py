#!/usr/bin/env python3
"""Build the bilingual site with Zensical.

English is built to /, Arabic to /ar/. Each language gets its own nav, search
index, UI strings, and direction. The Arabic pages carry Arabic theory and the
same English verified apply steps as the English page.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import yaml

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
        "notes": "Notes",
        "tools": "Tools",
        "wiki": "Wiki",
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
        "notes": "الملاحظات",
        "tools": "الأدوات",
        "wiki": "الويكي",
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
extra_javascript:
  - assets/hover.js?v={asset_version}
  - assets/analytics.js?v={asset_version}
"""


def asset_version() -> str:
    digest = hashlib.sha256()
    for name in ("extra.css", "hover.css", "hover.js", "analytics.js"):
        digest.update((ASSETS / name).read_bytes())
    return digest.hexdigest()[:10]


def title_of(path: Path) -> str:
    text = path.read_text()
    match = re.search(r"^# (.+)$", text, flags=re.M)
    return match.group(1).strip() if match else path.stem


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


def projects_index(root: Path, lang: str) -> None:
    if lang != "en":
        return
    projects = CATALOG.get("projects", [])
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


def nav_for(root: Path, lang: str) -> list:
    labels = LABELS[lang]
    nav: list = [{"Home": "index.md"}]

    if (root / "projects" / "index.md").exists():
        children = [{"Overview": "projects/index.md"}]
        for item in CATALOG.get("projects", []):
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
            ("setup", "setup.md"),
            ("cleanup", "cleanup-guide.md"),
            ("costs", "costs-and-free-options.md"),
        ]:
            if (root / name).exists():
                four_children.append({labels[key]: name})
        children[-1] = {"Four Hats": four_children}
        for course in CATALOG.get("courses", []):
            page = course.get("page", "")
            if page and course["slug"] != "four-hats" and (root / page).exists():
                children.append({course["title"]: page})
        nav.append({labels["courses"]: children})

    if (root / "notes" / "index.md").exists():
        children = [{"Overview": "notes/index.md"}]
        for page in sorted((root / "notes").glob("*.md")):
            if page.name == "index.md":
                continue
            children.append({title_of(page): page.relative_to(root).as_posix()})
        nav.append({labels["notes"]: children})

    if (root / "tools" / "index.md").exists():
        nav.append({labels["tools"]: "tools/index.md"})

    if (root / "wiki" / "index.md").exists():
        children = [{"Overview": "wiki/index.md"}]
        for page in sorted((root / "wiki").glob("*.md")):
            if page.name == "index.md":
                continue
            children.append({title_of(page): page.relative_to(root).as_posix()})
        nav.append({labels["wiki"]: children})

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
        if rel.startswith("wiki/"):
            index[rel.removeprefix("wiki/")] = path
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
            r"\]\(\.\./(?:act[1-4]-[a-z-]+\.md|00-setup\.md|cleanup-guide\.md|costs-and-free-options\.md)(#[^)]*)?\)",
            lambda m: "](https://github.com/aliAljaffer/four-hats/blob/main/docs/"
            + m.group(0).split("../", 1)[1],
            text,
        )
        page.write_text(text)
        inject_apply(page, lang)
        text = page.read_text()
        for name in ("00-setup.md", "cleanup-guide.md", "costs-and-free-options.md"):
            text = text.replace(
                f"]({name})",
                f"](https://github.com/aliAljaffer/four-hats/blob/main/docs/{name})",
            )
        text = text.replace(
            "](../cv/skills-ledger.md)",
            "](https://github.com/aliAljaffer/four-hats/blob/main/cv/skills-ledger.md)",
        )
        page.write_text(text)
    episode_index(root, lang)
    projects_index(root, lang)
    courses_index(root, lang)
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


def main() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    for lang in ("en", "ar"):
        root = assemble(lang)
        build(lang, root)
    postprocess(SITE, "en")
    postprocess(SITE / "ar", "ar")
    publish_slides()
    print("built site/ and site/ar/")


if __name__ == "__main__":
    main()
