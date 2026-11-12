#!/usr/bin/env python3
"""Build the docs site with Zensical.

Project and course docs are fetched from the repos in sources.yaml. Home,
Contact, and Definitions live in content/en.
"""
from __future__ import annotations

import datetime
import fcntl
import hashlib
import json
import os
import posixpath
import re
import shutil
import subprocess
from pathlib import Path

import yaml

import brand
import fetch
import og
import postprocess
import provenance
from frontmatter import join_meta, split_meta

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content" / "en"
ASSETS = ROOT / "assets"
BUILD = ROOT / "build" / "en"
SITE = ROOT / "site"
TASKS = yaml.safe_load((ROOT / "episode-tasks.yaml").read_text())["episodes"]
ZENSICAL = os.environ.get("ZENSICAL") or shutil.which("zensical") or "zensical"

SITE_URL = "https://docs.alialjaffer.com"
PORTFOLIO_URL = "https://alialjaffer.com"
PORTFOLIO_LABEL = "alialjaffer.com"
OWNER = "Ali Aljaffer"
SITE_NAME = "Ali's Docs"
TAGLINE = "Documentation for the projects I build and the courses I teach."

ACTS = [
    (0, 1, "Introduction"),
    (2, 6, "Act 1: Software Engineer"),
    (7, 10, "Act 2: Cloud Engineer"),
    (11, 19, "Act 3: DevOps Engineer"),
    (20, 25, "Act 4: Cybersecurity Engineer"),
    (26, 26, "Wrap up"),
]

BASE_THEME = """\
site_name: {site_name}
site_description: {tagline}
site_url: {site_url}/
repo_url: https://github.com/{self_repo}
docs_dir: {docs_dir}
site_dir: site
theme:
  name: material
  custom_dir: overrides
  language: en
  font: false
  favicon: {favicon}
  logo: {logo}
  palette:
    - scheme: default
      primary: custom
      accent: custom
      media: "(prefers-color-scheme: light)"
      toggle: {{icon: material/weather-night, name: Night}}
    - scheme: slate
      primary: custom
      accent: custom
      media: "(prefers-color-scheme: dark)"
      toggle: {{icon: material/weather-sunny, name: Day}}
  features: [navigation.tabs, navigation.top, content.code.copy, content.code.annotate]
markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.tasklist:
      custom_checkbox: true
      clickable_checkbox: true
  - attr_list
  - md_in_html
  - tables
  - toc:
      permalink: true
extra_css:
{brand_styles}  - assets/brand.css?v={v}
  - assets/theme.css?v={v}
  - assets/hover.css?v={v}
  - assets/diagram-zoom.css?v={v}
  - assets/source-file.css?v={v}
extra_javascript:
  - assets/vendor/panzoom.min.js
  - assets/mathjax.js?v={v}
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js
  - assets/diagram-zoom.js?v={v}
  - assets/hover.js?v={v}
  - assets/analytics.js?v={v}
  - assets/checklist.js?v={v}
  - assets/course-nav.js?v={v}
"""


def asset_version() -> str:
    digest = hashlib.sha256()
    names = ("theme.css", "hover.css", "diagram-zoom.css", "source-file.css", "hover.js", "diagram-zoom.js", "analytics.js", "checklist.js", "course-nav.js", "mathjax.js")
    for path in [*(ASSETS / name for name in names), *brand.asset_inputs(brand.load())]:
        digest.update(path.read_bytes())
    return digest.hexdigest()[:10]


def title_of(path: Path) -> str:
    match = re.search(r"^# (.+)$", split_meta(path.read_text())[1], flags=re.M)
    return match.group(1).strip() if match else path.stem


def meta_of(path: Path) -> dict:
    return split_meta(path.read_text())[0]


def summary_of(path: Path) -> str:
    for block in re.split(r"\n\s*\n", split_meta(path.read_text())[1]):
        block = block.strip()
        if not block or block[0] in "#|-*>!<`[:" or block.startswith(("```", "**")) or re.match(r"\d+\.", block):
            continue
        plain = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", block)
        plain = re.sub(r"[*_`]", "", " ".join(plain.split()))
        if len(plain) < 30:
            continue
        return plain if len(plain) <= 200 else plain[:197].rsplit(" ", 1)[0] + "..."
    return ""


WIKI_ORDER = ["GCP", "AWS", "Cloud", "Networking", "Security", "AI", "React", "React Router", "Web", "Other"]
CATEGORY_NAMES = {"gcp": "GCP", "ai": "AI"}


def category_of(path: Path, folder: Path) -> str:
    meta = meta_of(path)
    if meta.get("category"):
        return meta["category"]
    if path.parent == folder:
        return "Other"
    return CATEGORY_NAMES.get(path.parent.name, path.parent.name.replace("-", " ").title())


def group_pages(folder: Path) -> dict[str, list[Path]]:
    groups: dict[str, list[Path]] = {}
    for path in folder.rglob("*.md"):
        if path.name != "index.md":
            groups.setdefault(category_of(path, folder), []).append(path)
    for pages in groups.values():
        pages.sort(key=title_of)
    return groups


def ordered_groups(groups: dict[str, list[Path]]) -> list[tuple[str, list[Path]]]:
    names = [n for n in WIKI_ORDER if n in groups] + sorted(n for n in groups if n not in WIKI_ORDER)
    return [(name, groups[name]) for name in names]


def definitions_index(root: Path) -> None:
    base = root / "definitions"
    groups = group_pages(base)
    lines = [
        "# Definitions",
        "",
        "Definitions and informational terms. Link to a definition once, and every page that mentions it appears under **Linked from**.",
        "",
    ]
    for category, pages in ordered_groups(groups):
        lines += [f"## {category}", ""]
        for page in pages:
            description = meta_of(page).get("description", "")
            lines.append(
                f"- [{title_of(page)}]({page.relative_to(base).as_posix()})"
                + (f": {description}" if description else "")
            )
        lines.append("")
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


WIKI = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


def process_wiki(root: Path) -> None:
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

    titles = {path: title_of(path) for path in files}
    backlinks: dict[str, list[dict[str, str]]] = {}
    for path in files:

        def replace(match: re.Match[str]) -> str:
            target = match.group(1).strip()
            label = (match.group(2) or target).strip()
            if target not in index:
                raise SystemExit(f"{path.name}: missing wikilink target: {target}")
            url = f"/{index[target].relative_to(root).with_suffix('').as_posix().removesuffix('index')}"
            source = f"/{path.relative_to(root).with_suffix('').as_posix().removesuffix('index')}"
            url, source = url.rstrip("/") + "/", source.rstrip("/") + "/"
            entry = {"title": titles[path], "url": source}
            bucket = backlinks.setdefault(url, [])
            if entry not in bucket:
                bucket.append(entry)
            return f"[{label}]({url})"

        path.write_text(WIKI.sub(replace, path.read_text()))

    for bucket in backlinks.values():
        bucket.sort(key=lambda item: item["title"])
    (root / "assets" / "backlinks.json").write_text(
        json.dumps(backlinks, indent=2, ensure_ascii=False) + "\n"
    )


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
    return "\n".join(out).replace("\n<details>\n", '\n<details markdown="1">\n')


LINK = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)((?:\s+\"[^\"]*\")?)\)")


def rewrite_links(page: Path, base: Path, entry: dict) -> None:
    """Keep links that resolve inside the fetched docs. Point the rest at GitHub."""
    page_dir = page.parent.relative_to(base).as_posix()
    repo, branch = entry["repo"], entry["branch"]

    def fix(match: re.Match[str]) -> str:
        bang, label, target, title = match.groups()
        if re.match(r"([a-z][a-z0-9+.-]*:|#|/)", target, flags=re.I):
            return match.group(0)
        path, _, anchor = target.partition("#")
        rel = posixpath.normpath(posixpath.join(page_dir, path))
        if not rel.startswith("..") and (base / rel).exists():
            if posixpath.basename(path) == "README.md" and (base / rel).with_name("index.md").exists():
                target = path[: -len("README.md")] + "index.md" + (f"#{anchor}" if anchor else "")
            return f"{bang}[{label}]({target}{title})"
        repo_rel = posixpath.normpath(posixpath.join(entry["path"], rel))
        if bang:
            url = f"https://raw.githubusercontent.com/{repo}/{branch}/{repo_rel}"
        else:
            kind = "tree" if path.endswith("/") or not posixpath.splitext(path)[1] else "blob"
            url = f"https://github.com/{repo}/{kind}/{branch}/{repo_rel}" + (f"#{anchor}" if anchor else "")
        return f"{bang}[{label}]({url}{title})"

    out: list[str] = []
    fenced = False
    for line in page.read_text().splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        out.append(line if fenced else LINK.sub(fix, line))
    page.write_text("\n".join(out) + "\n")


def insert_after_h1(text: str, block: str) -> str:
    match = re.search(r"^# .+\n", text, flags=re.M)
    at = match.end() if match else len(text) - len(split_meta(text)[1])
    return text[:at] + block + text[at:]


def case_study_link(entry: dict) -> str:
    if "case_study" not in entry:
        return ""
    return f" · [Case study]({PORTFOLIO_URL}/case-study/{entry['case_study']}/)"


def normalize(base: Path, entry: dict, kind: str) -> None:
    if kind == "projects":
        readme = next((p for p in base.glob("*") if p.name.lower() == "readme.md"), None)
        if readme and not (base / "index.md").exists():
            readme.rename(base / "index.md")
        if not (base / "index.md").exists():
            title = entry.get("title", entry["slug"].replace("-", " ").title())
            (base / "index.md").write_text(f"# {title}\n\n{entry.get('description', '')}\n")
        index = base / "index.md"
        text = index.read_text()
        link = f"\n[Repository](https://github.com/{entry['repo']}) on `{entry['branch']}`{case_study_link(entry)}\n"
        index.write_text(insert_after_h1(text, link))


def mask_fences(text: str) -> str:
    """Blank fenced lines, same length, so headings inside code blocks do not end a section."""
    out: list[str] = []
    fenced = False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            out.append(line)
        else:
            out.append(re.sub(r"[^\n]", " ", line) if fenced else line)
    return "".join(out)


def apply_content(acts: Path, ep: str) -> tuple[str, str]:
    spec = TASKS.get(ep, {})
    if spec.get("apply") == "none" or not spec.get("file"):
        return "", ""
    path = acts / spec["file"]
    text = path.read_text()
    masked = mask_fences(text)
    if "section" in spec:
        heading = spec["section"]
        match = re.search(
            rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", masked, flags=re.M | re.S
        )
        if not match:
            raise SystemExit(f"{path.name}: section not found: {heading}")
        return text[match.start(1):match.end(1)].strip(), spec["file"]
    blocks = []
    for number in spec.get("tasks", []):
        match = re.search(
            rf"^#### Task {number}: .+?(?=^#### Task |^### |^## |\Z)",
            masked,
            flags=re.M | re.S,
        )
        if not match:
            raise SystemExit(f"{path.name}: Task {number} not found")
        blocks.append(text[match.start():match.end()].strip())
    return "\n\n".join(blocks), spec["file"]


SHELL_FENCES = {"bash", "sh", "shell", "console", "zsh"}


def use_shell_lexer(text: str) -> str:
    """Point tagged shell fences at the docs-shell lexer, which colours commands and flags."""
    out: list[str] = []
    fenced = False
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("```"):
            if not fenced and stripped[3:].strip() in SHELL_FENCES:
                line = line[: len(line) - len(stripped)] + "```docs-shell\n"
            fenced = not fenced
        out.append(line)
    return "".join(out)


def rebase_links(body: str) -> str:
    """Act-guide links are relative to docs/; the body lands in docs/episodes/."""

    def fix(match: re.Match[str]) -> str:
        bang, label, target, title = match.groups()
        if re.match(r"([a-z][a-z0-9+.-]*:|#|/)", target, flags=re.I):
            return match.group(0)
        if target.startswith("00-setup.md"):
            target = "setup.md" + target[len("00-setup.md"):]
        return f"{bang}[{label}](../{target}{title})"

    out: list[str] = []
    fenced = False
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        out.append(line if fenced else LINK.sub(fix, line))
    return "\n".join(out)


def embed_slides(base: Path) -> None:
    script = f'<script src="/assets/analytics.js?v={asset_version()}"></script></body>'
    for deck in (base / "slides").glob("ep*.html"):
        html = deck.read_text()
        if "/assets/analytics.js" not in html:
            deck.write_text(html.replace("</body>", script))
        page = base / "episodes" / f"{deck.stem}.md"
        if not page.exists():
            continue
        url = f"/four-hats/slides/{deck.name}"
        block = (
            '<div markdown="0">\n'
            f'<iframe src="{url}" title="Slides" loading="lazy" allowfullscreen '
            'style="width:100%;aspect-ratio:16/9;border:0"></iframe>\n'
            '<p><button type="button" class="md-button" onclick="this.closest(\'div\').querySelector(\'iframe\').requestFullscreen()">Fullscreen</button> '
            f'<a href="{url}" target="_blank" rel="noopener">Open in new tab</a></p>\n</div>\n'
        )
        page.write_text(insert_after_h1(page.read_text(), "\n" + block))


def four_hats(base: Path) -> None:
    """Course-specific steps: inject act-guide steps, then drop unlisted pages."""
    marker = "<!-- APPLY -->"
    for page in sorted((base / "episodes").glob("ep*.md")):
        text = page.read_text()
        if marker not in text:
            continue
        body, source = apply_content(base, page.name[:4])
        body = rebase_links(body)
        if body:
            note = f"Copied from `{source}`. Edit the act guide, not this page."
            text = text.replace(marker, f"### Verified steps\n\n{note}\n\n{body}\n")
        else:
            text = text.replace(marker, "").rstrip() + "\n"
        page.write_text(text)
    embed_slides(base)
    setup = base / "00-setup.md"
    if setup.exists():
        setup.rename(base / "setup.md")
    for page in base.glob("act*.md"):
        page.unlink()
    plan = base / "infrastructure-plan.md"
    if plan.exists():
        plan.unlink()
    lines = ["# Episodes", ""]
    by_number = {int(p.name[2:4]): p for p in (base / "episodes").glob("ep*.md")}
    for start, end, label in ACTS:
        group = [by_number[n] for n in range(start, end + 1) if n in by_number]
        if group:
            lines += [f"## {label}", "", "| Episode |", "|---|"]
            lines += [f"| [{title_of(p)}](episodes/{p.name}) |" for p in group]
            lines.append("")
    (base / "episodes.md").write_text("\n".join(lines))


def label_pages(root: Path, config: dict) -> list[og.Card]:
    """Give every page a tab title and description that name that page, and return its preview card."""
    cards = []
    owners = {}
    for kind in ("projects", "courses"):
        for entry in config.get(kind, []):
            owners[fetch.dest_of(kind, entry)] = entry
    for page in sorted(root.rglob("*.md")):
        rel = page.relative_to(root)
        if rel.parts[0] == "assets":
            continue
        meta, body = split_meta(page.read_text())
        heading = title_of(page) if re.search(r"^# ", body, flags=re.M) else page.stem
        section = ""
        owner = next((e for d, e in owners.items() if rel.as_posix().startswith(d + "/")), None)
        if rel.as_posix() == "index.md":
            heading = SITE_NAME
        elif owner and rel.name == "index.md" and len(rel.parts) == len(Path(fetch.dest_of("projects" if rel.parts[0] == "projects" else "courses", owner)).parts) + 1:
            heading = owner["title"]
        elif owner:
            section = owner["title"]
            card_title = heading
            heading = f"{heading} - {owner['title']}"
        if "updated" in meta:
            meta["updated"] = str(meta["updated"])
        meta.setdefault("title", "Home" if heading == SITE_NAME else heading)
        if owner and "repo" in owner:
            meta.setdefault("repo_url", f"https://github.com/{owner['repo']}")
        if "description" not in meta:
            summary = owner["description"] if owner and rel.name == "index.md" else summary_of(page)
            if summary:
                meta["description"] = summary
        page.write_text(join_meta(meta, body))
        url = rel.parent if rel.name == "index.md" else rel.with_suffix("")
        cards.append(og.Card(
            path="" if url == Path(".") else url.as_posix(),
            title=card_title if section else heading,
            section=section,
            description=str(meta.get("description") or TAGLINE),
        ))
    return cards


def prepare(root: Path, config: dict) -> None:
    for kind in ("projects", "courses"):
        for entry in config.get(kind, []):
            base = root / fetch.dest_of(kind, entry)
            if entry.get("local"):
                entry.setdefault("description", summary_of(base / "index.md"))
                continue
            if entry["slug"] == "four-hats":
                four_hats(base)
            normalize(base, entry, kind)
            for page in base.rglob("*.md"):
                page.write_text(convert_callouts(page.read_text()))
                rewrite_links(page, base, entry)
            if kind == "courses" and not (base / "index.md").exists():
                title = entry.get("title", entry["slug"].replace("-", " ").title())
                (base / "index.md").write_text(f"# {title}\n\n{entry.get('description', '')}\n")
            if entry.get("description") is None:
                entry["description"] = summary_of(base / "index.md")
            entry.setdefault("title", entry["slug"].replace("-", " ").title())


def listing(config: dict, kind: str) -> list[str]:
    prefix = "projects/" if kind == "projects" else ""
    return [
        f"- [{e['title']}]({prefix}{e['slug']}/index.md)" + (f": {e['description']}" if e["description"] else "")
        for e in config.get(kind, [])
    ]


def write_index(root: Path, config: dict, kind: str, title: str, intro: str) -> None:
    lines = [f"# {title}", "", intro, ""]
    for entry in config.get(kind, []):
        lines += [f"## {entry['title']}", "", entry["description"], ""]
        target = f"{entry['slug']}/" if kind == "projects" else f"../{entry['slug']}/"
        repo = f" · [Repository](https://github.com/{entry['repo']})" if "repo" in entry else ""
        lines += [f"[Read the docs]({target}){repo}{case_study_link(entry)}", ""]
    dest = root / kind if kind == "projects" else root / "courses"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "index.md").write_text("\n".join(lines))


def inject_home(root: Path, config: dict) -> None:
    page = root / "index.md"
    text = page.read_text()
    for marker, kind in (("<!-- PROJECTS -->", "projects"), ("<!-- COURSES -->", "courses")):
        text = text.replace(marker, "\n".join(listing(config, kind)))
    page.write_text(text)


SUBDIR_LABELS = {"adr": "Decisions", "reference": "API reference"}


def tree_nav(root: Path, base: Path, title: str) -> dict:
    rel = lambda p: p.relative_to(root).as_posix()
    children: list = [{"Overview": rel(base / "index.md")}]
    for path in sorted(base.glob("*.md")):
        if path.name != "index.md":
            children.append({title_of(path): rel(path)})
    for folder in sorted(p for p in base.iterdir() if p.is_dir()):
        pages = sorted(folder.rglob("*.md"))
        if pages:
            children.append(
                {SUBDIR_LABELS.get(folder.name, folder.name.title()): [{title_of(p): rel(p)} for p in pages]}
            )
    return {title: children}


def four_hats_nav(root: Path, base: Path, title: str) -> dict:
    rel = lambda p: p.relative_to(root).as_posix()
    children: list = [{"Overview": rel(base / "index.md")}]
    for name, label in (("setup.md", "Setup"), ("episodes.md", "Episodes")):
        if (base / name).exists():
            children.append({label: rel(base / name)})
    by_number = {int(p.name[2:4]): p for p in (base / "episodes").glob("ep*.md")}
    for start, end, label in ACTS:
        group = [by_number[n] for n in range(start, end + 1) if n in by_number]
        if group:
            children.append({label: [{title_of(p): rel(p)} for p in group]})
    for name, label in (("cleanup-guide.md", "Cleanup"), ("costs-and-free-options.md", "Costs and free options")):
        if (base / name).exists():
            children.append({label: rel(base / name)})
    return {title: children}


def nav_for(root: Path, config: dict) -> list:
    nav: list = [{"Home": "index.md"}]
    projects = [{"Overview": "projects/index.md"}]
    projects += [tree_nav(root, root / "projects" / e["slug"], e["title"]) for e in config.get("projects", [])]
    nav.append({"Projects": projects})
    courses = [{"Overview": "courses/index.md"}]
    for e in config.get("courses", []):
        build = four_hats_nav if e["slug"] == "four-hats" else tree_nav
        courses.append(build(root, root / e["slug"], e["title"]))
    nav.append({"Courses": courses})
    children = [{"Overview": "definitions/index.md"}]
    for category, pages in ordered_groups(group_pages(root / "definitions")):
        children.append({category: [{title_of(p): p.relative_to(root).as_posix()} for p in pages]})
    nav.append({"Definitions": children})
    nav.append({"Contact": "contact.md"})
    nav.append({PORTFOLIO_LABEL: PORTFOLIO_URL})
    return nav


def assemble() -> tuple[Path, list[og.Card]]:
    config = fetch.load()
    if BUILD.parent.exists():
        shutil.rmtree(BUILD.parent)
    shutil.copytree(CONTENT, BUILD)
    provenance.stamp(BUILD, provenance.commit_dates(ROOT, "content/en"), provenance.local_origin("content/en"))
    shutil.copytree(ASSETS, BUILD / "assets")
    identity = brand.load()
    version = asset_version()
    brand.compile(identity, BUILD / "assets", SITE_URL, version)
    definitions_index(BUILD)
    process_wiki(BUILD)
    fetch.fetch_all(BUILD, config)
    prepare(BUILD, config)
    for page in BUILD.rglob("*.md"):
        page.write_text(use_shell_lexer(page.read_text()))
    inject_home(BUILD, config)
    write_index(BUILD, config, "projects", "Projects", TAGLINE)
    write_index(BUILD, config, "courses", "Courses", "Long-form courses built around one project or one skill path.")
    cards = label_pages(BUILD, config)
    brand_styles = "".join(f"  - {s if s.startswith('http') else f'assets/brand/{s}?v={version}'}\n" for s in identity.stylesheets)
    site = {
        "copyright": f'&copy; {datetime.date.today().year} {OWNER} &middot; <a href="{PORTFOLIO_URL}">{PORTFOLIO_LABEL}</a>',
        "extra": {
            "generator": False,
            "giscus": {mode: f"{SITE_URL}/assets/giscus-{mode}.css?v={version}" for mode in ("light", "dark")},
        },
    }
    (ROOT / "mkdocs.en.yml").write_text(
        BASE_THEME.format(
            site_name=SITE_NAME, tagline=TAGLINE, site_url=SITE_URL, docs_dir=BUILD.relative_to(ROOT).as_posix(),
            v=version, self_repo=provenance.SELF_REPO, favicon=f"assets/brand/{identity.favicon}?v={version}", logo=f"assets/brand/{identity.logo}?v={version}", brand_styles=brand_styles,
        )
        + yaml.safe_dump(site, sort_keys=False)
        + "\nnav:\n"
        + yaml.safe_dump(nav_for(BUILD, config), sort_keys=False, allow_unicode=True)
    )
    return ROOT / "mkdocs.en.yml", cards


def run() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    config, cards = assemble()
    result = subprocess.run([ZENSICAL, "build", "-f", str(config)], capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(result.stdout + result.stderr)
    print(result.stdout.strip().splitlines()[-1])
    print(f"{postprocess.run(SITE, SITE / 'assets' / 'backlinks.json')} pages enhanced")
    eyebrow = SITE_URL.split("://", 1)[1].upper()
    count = og.write_all(brand.BRAND_DIR / "og", brand.load().modes["light"], eyebrow, cards, SITE)
    print(f"{count} preview cards")
    slugs = sorted(
        p.relative_to(BUILD / "definitions").with_suffix("").as_posix()
        for p in (BUILD / "definitions").rglob("*.md")
        if p.name != "index.md"
    )
    (SITE / "definitions.json").write_text(json.dumps(slugs) + "\n")


if __name__ == "__main__":
    with open(ROOT / ".build.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        run()
