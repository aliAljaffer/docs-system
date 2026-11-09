#!/usr/bin/env python3
"""Build the bilingual site with Zensical.

English is built to /, Arabic to /ar/. Each language gets its own nav, search
index, UI strings, and direction. The Arabic pages carry Arabic theory and the
same English verified apply steps as the English page.
"""
from __future__ import annotations

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
SITE = ROOT / "site"
TASKS = yaml.safe_load((ROOT / "episode-tasks.yaml").read_text())["episodes"]
ZENSICAL = "/Users/h/branding/.venv/bin/zensical"

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
        "tools": "Tools",
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
        "tools": "الأدوات",
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
  features: [navigation.tabs, navigation.top, content.code.copy, content.code.annotate, navigation.sections]
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
  - assets/extra.css
"""


def title_of(path: Path) -> str:
    text = path.read_text()
    match = re.search(r"^# (.+)$", text, flags=re.M)
    return match.group(1).strip() if match else path.stem


def apply_content(ep: str) -> tuple[str, str]:
    spec = TASKS.get(ep, {})
    if spec.get("apply") == "none" or not spec.get("file"):
        return "", ""
    path = FOUR_HATS / "docs" / spec["file"]
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


def nav_for(root: Path, lang: str) -> list:
    labels = LABELS[lang]
    nav: list = [{"Home": "index.md"}]

    four = root / "four-hats"
    if (four / "index.md").exists():
        children: list = [{"Overview": "four-hats/index.md"}]
        if (four / "episodes.md").exists():
            children.append({labels["episodes"]: "four-hats/episodes.md"})
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
                rel = path.relative_to(root).as_posix()
                act.append({title_of(path): rel})
            children.append({label_en if lang == "en" else label_ar: act})
        nav.append({labels["four"]: children})

    for key, name in [
        ("setup", "setup.md"),
        ("cleanup", "cleanup-guide.md"),
        ("costs", "costs-and-free-options.md"),
    ]:
        if (root / name).exists():
            nav.append({labels[key]: name})

    if (root / "tools" / "index.md").exists():
        nav.append({labels["tools"]: "tools/index.md"})

    return nav


def assemble(lang: str) -> Path:
    root = BUILD / lang
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(CONTENT / lang, root)
    shutil.copytree(ASSETS, root / "assets", dirs_exist_ok=True)
    for page in root.rglob("*.md"):
        text = page.read_text()
        text = text.replace("](../assets/", "](../../assets/")
        text = text.replace("](../../assets/diagrams/", "](../../assets/diagrams/")
        page.write_text(text)
        inject_apply(page, lang)
    episode_index(root, lang)
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


def main() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    for lang in ("en", "ar"):
        root = assemble(lang)
        build(lang, root)
    postprocess(SITE, "en")
    postprocess(SITE / "ar", "ar")
    print("built site/ and site/ar/")


if __name__ == "__main__":
    main()
