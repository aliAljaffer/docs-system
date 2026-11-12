#!/usr/bin/env python3
"""End-to-end checks for the built site."""
from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
SITE = ROOT / "site"

import brand  # noqa: E402
import fetch  # noqa: E402
import provenance  # noqa: E402
from build import convert_callouts  # noqa: E402


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.items: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.items += [(k, v) for k, v in attrs if k in {"href", "src"} and v]


def resolve(page: Path, value: str) -> Path | None:
    parsed = urlparse(value)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    path = unquote(parsed.path)
    target = (SITE / path.lstrip("/") if path.startswith("/") else page.parent / path).resolve()
    if target.is_dir() or path.endswith("/") or target.suffix == "":
        target = target / "index.html"
    return target


class SiteTests(unittest.TestCase):
    def test_nav_tabs(self) -> None:
        page = (SITE / "index.html").read_text()
        for name in ("Home", "Projects", "Courses", "Definitions", "Contact"):
            self.assertIn(name, page)
        for name in ("Blogs", "Notes", "Graph"):
            self.assertNotIn(f'md-tabs__link">\n        {name}', page)

    def test_every_source_built(self) -> None:
        config = fetch.load()
        for entry in config.get("projects", []):
            self.assertTrue((SITE / "projects" / entry["slug"] / "index.html").exists(), entry["slug"])
        for entry in config.get("courses", []):
            self.assertTrue((SITE / entry["slug"] / "index.html").exists(), entry["slug"])

    def test_internal_links(self) -> None:
        broken = []
        for page in SITE.rglob("*.html"):
            parser = Links()
            parser.feed(page.read_text())
            for _, value in parser.items:
                target = resolve(page, value)
                if target and not target.exists():
                    broken.append(f"{page.relative_to(SITE)} -> {value}")
        self.assertEqual(broken, [], "\n".join(broken[:20]))

    def test_apply_injected(self) -> None:
        for page in (SITE / "four-hats" / "episodes").rglob("index.html"):
            self.assertNotIn("<!-- APPLY -->", page.read_text(), page.name)
        page = next((SITE / "four-hats" / "episodes").glob("ep04-*/index.html"))
        self.assertIn("Verified steps", page.read_text())

    def test_slides_embedded(self) -> None:
        page = next((SITE / "four-hats" / "episodes").glob("ep04-*/index.html")).read_text()
        self.assertIn("<iframe", page)
        self.assertIn("requestFullscreen", page)
        self.assertIn("md-button", page)
        self.assertTrue(len(list((SITE / "four-hats" / "slides").glob("ep*.html"))) >= 27)

    def test_definitions_manifest(self) -> None:
        slugs = json.loads((SITE / "definitions.json").read_text())
        self.assertIn("aws/security-iam", slugs)
        self.assertNotIn("index", slugs)

    def test_page_titles_and_previews(self) -> None:
        cases = {
            "projects/s2t/index.html": "<title>s2t - Ali's Docs</title>",
            "definitions/aws/security-iam/index.html": "<title>IAM - Ali's Docs</title>",
        }
        for rel, title in cases.items():
            page = (SITE / rel).read_text().replace("&#x27;", "'")
            self.assertIn(title, page, rel)
            self.assertIn('property="og:title"', page, rel)
            self.assertIn('property="og:url"', page, rel)

    def test_every_page_has_its_own_preview_card(self) -> None:
        pages = [p for p in SITE.rglob("index.html") if p.relative_to(SITE).parts[0] != "assets"]
        self.assertGreater(len(pages), 100)
        for page in pages:
            match = re.search(r'property="og:image" content="https://docs\.alialjaffer\.com/([^"]*)og\.jpg"', page.read_text())
            self.assertIsNotNone(match, page)
            card = SITE / match.group(1) / "og.jpg"
            self.assertEqual(card.parent, page.parent, page)
            with Image.open(card) as im:
                self.assertEqual(im.size, (1200, 630), card)
        self.assertFalse((SITE / "assets" / "og.png").exists())
        self.assertFalse((SITE / "assets" / "brand" / "og").exists())

    def test_wiki(self) -> None:
        self.assertTrue((SITE / "definitions" / "rest" / "index.html").exists())
        self.assertIn("/definitions/", (SITE / "assets" / "backlinks.json").read_text())

    def test_callouts(self) -> None:
        result = convert_callouts("> [!tip] Hover a term\n> Move the pointer over a link.\n")
        self.assertIn('!!! tip "Hover a term"', result)
        self.assertIn("    Move the pointer", result)

    def test_shell_fences_are_highlighted(self) -> None:
        page = (SITE / "ckad" / "06-services" / "index.html").read_text()
        self.assertIn('<span class="nf">kubectl</span>', page)
        self.assertIn('<span class="k">expose</span>', page)
        self.assertIn("&lt;service-name&gt;.&lt;namespace&gt;", page)

    def test_removed_sections_absent(self) -> None:
        for name in ("blogs", "notes", "graph", "tags", "ar", "feed.xml", "posts.json"):
            self.assertFalse((SITE / name).exists(), name)

    def test_redirects_configured(self) -> None:
        conf = (ROOT / "deploy" / "nginx.conf").read_text()
        self.assertIn("return 301 /four-hats/", conf)
        self.assertIn("rewrite ^/courses/four-hats/", conf)

    def test_sitemap_and_404(self) -> None:
        self.assertTrue((SITE / "sitemap.xml").exists())
        self.assertTrue((SITE / "404.html").exists())

    def test_last_updated_and_edit_link(self) -> None:
        dated = re.compile(r'class="md-source-file">\s*Last updated <time datetime="\d{4}-\d{2}-\d{2}">')
        episode = next((SITE / "four-hats" / "episodes").glob("ep04-*/index.html"))
        pages = {
            SITE / "projects/homelab/api-endpoint/index.html": "aliAljaffer/homelab/edit/main/docs/",
            SITE / "definitions/rest/index.html": "aliAljaffer/docs-system/edit/main/content/en/",
            episode: "aliAljaffer/docs-system/edit/main/docs-src/four-hats/",
        }
        for page, origin in pages.items():
            html = page.read_text()
            self.assertRegex(html, dated, str(page))
            self.assertIn(f'<a href="https://github.com/{origin}', html, str(page))
        index = (SITE / "projects/index.html").read_text()
        self.assertNotIn('class="md-source-file"', index)
        self.assertNotIn("Edit this page", index)

    def test_commit_dates(self) -> None:
        dates = provenance.commit_dates(ROOT, "content/en")
        self.assertTrue(dates)
        for path, date in dates.items():
            self.assertRegex(date, r"^\d{4}-\d{2}-\d{2}$", path)

    def test_brand_css(self) -> None:
        css = (SITE / "assets" / "brand.css").read_text()
        raw = json.loads((ROOT / "brand" / "brand.json").read_text())
        light, night = css.split('[data-md-color-scheme="slate"]')
        for mode, block in (("light", light), ("night", night)):
            for key in brand.REQUIRED:
                value = raw[mode][key].lower()
                self.assertIn(f"--brand-{key.replace('_', '-')}: {value};", block, f"{mode}.{key}")
        for name, family in raw["fonts"].items():
            self.assertIn(f'--brand-font-{name}: "{family}"', light)

    def test_theme_has_no_brand_literals(self) -> None:
        theme = (ROOT / "assets" / "theme.css").read_text()
        self.assertNotRegex(theme, r"#[0-9a-fA-F]{3,8}\b")
        for family in json.loads((ROOT / "brand" / "brand.json").read_text())["fonts"].values():
            self.assertNotIn(family, theme)

    def test_page_uses_brand_head(self) -> None:
        page = (SITE / "projects" / "homelab" / "index.html").read_text()
        raw = json.loads((ROOT / "brand" / "brand.json").read_text())
        self.assertIn(f'rel="icon" href="../../assets/brand/{raw.get("favicon", raw["icon"])}?v=', page)
        self.assertIn(f'src="../../assets/brand/{raw["icon"]}?v=', page)
        for name in ("family=Inter", "JetBrains"):
            self.assertNotIn(name, page)
        self.assertNotIn('data-md-color-primary="indigo"', page)
        for sheet in json.loads((ROOT / "brand" / "brand.json").read_text()).get("stylesheets", []):
            self.assertIn(sheet if sheet.startswith("http") else f"assets/brand/{sheet}", page)

    def test_case_study_link(self) -> None:
        homelab = (SITE / "projects" / "homelab" / "index.html").read_text()
        self.assertIn('href="https://alialjaffer.com/case-study/homelab/"', homelab)
        ziti = (SITE / "projects" / "openziti-operator" / "index.html").read_text()
        self.assertNotIn("/case-study/", ziti)

    def test_portfolio_tab_and_footer(self) -> None:
        page = (SITE / "index.html").read_text()
        self.assertIn('<a href="https://alialjaffer.com" class="md-tabs__link">', page)
        self.assertIn("Ali Aljaffer", page)
        self.assertNotIn("Made with", page)

    def test_giscus_themes(self) -> None:
        reference = json.loads((ROOT / "tests" / "giscus_vars.json").read_text())
        for mode, names in reference.items():
            css = (SITE / "assets" / f"giscus-{mode}.css").read_text()
            missing = [n for n in names if f"{n}:" not in css]
            self.assertEqual(missing, [], mode)
            self.assertNotIn("$", css)
        comments = (SITE / "projects" / "homelab" / "index.html").read_text()
        for mode in ("light", "dark"):
            self.assertRegex(comments, rf"https://docs\.alialjaffer\.com/assets/giscus-{mode}\.css\?v=[0-9a-f]{{10}}")


class BrandCompilerTests(unittest.TestCase):
    def write(self, data: dict) -> Path:
        folder = Path(tempfile.mkdtemp())
        (folder / "icon.svg").write_text("<svg/>")
        (folder / "brand.json").write_text(json.dumps({"fonts": {"text": "X"}, "icon": "icon.svg", **data}))
        return folder / "brand.json"

    def test_missing_required_key(self) -> None:
        modes = {"light": {"ink": "#111", "accent": "#00f"}, "night": {"paper": "#000", "ink": "#fff", "accent": "#0ff"}}
        with self.assertRaises(SystemExit):
            brand.load(self.write(modes))

    def test_bad_hex(self) -> None:
        good = {"paper": "#fff", "ink": "#000", "accent": "#00f"}
        with self.assertRaises(SystemExit):
            brand.load(self.write({"light": {**good, "accent": "blue"}, "night": good}))

    def test_shape_and_syntax(self) -> None:
        good = {"paper": "#ffffff", "ink": "#000000", "accent": "#0000ff"}
        loaded = brand.load(self.write({"light": good, "night": good}))
        self.assertEqual(loaded.shape["radius"], "0")
        self.assertEqual(loaded.syntax["light"]["keyword"], "#0000ff")
        loaded = brand.load(self.write({"light": good, "night": good, "shape": {"radius": "12px", "shadow": True},
                                        "syntax": {"light": {"keyword": "#123456"}}}))
        self.assertIn("--brand-radius: 12px;", brand.css(loaded))
        self.assertIn("--brand-syntax-keyword: #123456;", brand.css(loaded))
        self.assertNotIn("--brand-shadow: none;", brand.css(loaded))
        with self.assertRaises(SystemExit):
            brand.load(self.write({"light": good, "night": good, "shape": {"radius": "1rem"}}))
        with self.assertRaises(SystemExit):
            brand.load(self.write({"light": good, "night": good, "syntax": {"light": {"tag": "#123456"}}}))

    def test_minimal_brand_gets_defaults(self) -> None:
        light = {"paper": "#ffffff", "ink": "#000000", "accent": "#0000ff"}
        night = {"paper": "#000000", "ink": "#ffffff", "accent": "#00ffff"}
        loaded = brand.load(self.write({"light": light, "night": night}))
        self.assertEqual(loaded.modes["light"]["paper_2"], "#ffffff")
        self.assertEqual(loaded.modes["night"]["accent_ink"], "#00ffff")
        self.assertIn("color-mix", loaded.modes["light"]["ink_soft"])
        self.assertIn("--brand-rule:", brand.css(loaded))

    def test_type_and_surfaces(self) -> None:
        good = {"paper": "#ffffff", "ink": "#000000", "accent": "#0000ff"}
        plain = brand.css(brand.load(self.write({"light": good, "night": good})))
        for line in ("--brand-body-size: 0.8rem;", "--brand-heading-rule: 1px;", "--brand-wash-a-strength: 0%;",
                     "--brand-grain-opacity: 0;", "--brand-nav-active-bg: transparent;"):
            self.assertIn(line, plain)
        painted = brand.css(brand.load(self.write({
            "light": {**good, "wash_a": "#ff00ff"}, "night": good,
            "shape": {"surfaces": "filled", "washes": True, "grain": True},
            "type": {"body_size": "17px", "heading_rule": False, "label_font": "code"},
        })))
        for line in ("--brand-body-size: 17px;", "--brand-heading-rule: 0;", "--brand-wash-a: #ff00ff;",
                     "--brand-wash-a-strength: 30%;", "--brand-grain-opacity: 0.5;", "--brand-font-label: var(--brand-font-code);"):
            self.assertIn(line, painted)
        for bad in ({"type": {"body_size": "big"}}, {"type": {"leading": "2"}}, {"shape": {"surfaces": "glossy"}}):
            with self.assertRaises(SystemExit):
                brand.load(self.write({"light": good, "night": good, **bad}))

    def test_night_shadow_is_soft_and_logo_swaps(self) -> None:
        good = {"paper": "#ffffff", "ink": "#000000", "accent": "#0000ff"}
        path = self.write({"light": good, "night": good, "shape": {"shadow": True}})
        css = brand.css(brand.load(path))
        self.assertEqual(css.count("rgba(0, 0, 0, 0.06)"), 2)
        self.assertEqual(css.count("rgba(0, 0, 0, 0.08)"), 2)
        self.assertIn("--brand-logo-reversed: none;", css)
        (path.parent / "icon-reversed.svg").write_text("<svg/>")
        self.assertIn('--brand-logo-reversed: url("brand/icon-reversed.svg");', brand.css(brand.load(path)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
