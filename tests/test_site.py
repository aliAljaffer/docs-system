#!/usr/bin/env python3
"""End-to-end checks for the built bilingual site."""
from __future__ import annotations

import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
EN = ROOT / "content" / "en"
AR = ROOT / "content" / "ar"
EPISODES = EN / "four-hats" / "episodes"


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.items: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key in {"href", "src"} and value:
                self.items.append((key, value))


def resolve(page: Path, value: str) -> Path | None:
    parsed = urlparse(value)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    path = unquote(parsed.path)
    target = SITE / path.lstrip("/") if path.startswith("/") else page.parent / path
    target = target.resolve()
    if target.is_dir() or path.endswith("/"):
        target = target / "index.html"
    elif target.suffix == "":
        target = target / "index.html"
    return target


class SiteTests(unittest.TestCase):
    def test_episode_count(self) -> None:
        pages = sorted(EPISODES.glob("ep*.md"))
        self.assertEqual(len(pages), 27, [p.name for p in pages])

    def test_episode_h1(self) -> None:
        pattern = re.compile(r"^# (ALL|SWE|CLD|DEV|CSC)-\d{2}: .+", re.M)
        for page in EPISODES.glob("ep*.md"):
            self.assertRegex(page.read_text(), pattern, page.name)

    def test_no_stub_text(self) -> None:
        for page in EPISODES.glob("ep*.md"):
            text = page.read_text()
            self.assertNotIn("Video coming", text, page.name)
            self.assertNotIn("Key idea", text, page.name)

    def test_no_em_dash(self) -> None:
        for page in list(EN.rglob("*.md")) + list(AR.rglob("*.md")):
            self.assertNotIn("\u2014", page.read_text(), page.name)

    def test_internal_links(self) -> None:
        broken: list[str] = []
        for page in SITE.rglob("*.html"):
            parser = Links()
            parser.feed(page.read_text())
            for _, value in parser.items:
                target = resolve(page, value)
                if target is None:
                    continue
                if not target.exists():
                    broken.append(f"{page.relative_to(SITE)} -> {value}")
        self.assertEqual(broken, [], "\n".join(broken[:20]))

    def test_pairs_have_switch(self) -> None:
        pairs = ["", "four-hats", "tools"]
        for rel in pairs:
            en = SITE / rel / "index.html" if rel else SITE / "index.html"
            ar = SITE / "ar" / rel / "index.html" if rel else SITE / "ar" / "index.html"
            if not en.exists() or not ar.exists():
                continue
            self.assertIn('class="lang-switch"', en.read_text(), f"en {rel}")
            self.assertIn('class="lang-switch"', ar.read_text(), f"ar {rel}")
            self.assertIn('hreflang="ar"', en.read_text(), f"en {rel}")
            self.assertIn('hreflang="en"', ar.read_text(), f"ar {rel}")

    def test_arabic_rtl(self) -> None:
        for source in AR.rglob("*.md"):
            rel = source.relative_to(AR).with_suffix("")
            page = SITE / "ar" / rel / "index.html" if rel.name != "index" else SITE / "ar" / rel.parent / "index.html"
            self.assertTrue(page.exists(), str(rel))
            self.assertIn('dir="rtl"', page.read_text(), str(rel))

    def test_apply_injected(self) -> None:
        for page in (SITE / "four-hats" / "episodes").rglob("index.html"):
            text = page.read_text()
            self.assertNotIn("<!-- APPLY -->", text, page.name)
        for number in (4, 8, 12, 19, 24):
            page = next((SITE / "four-hats" / "episodes").glob(f"ep{number:02d}-*/index.html"))
            self.assertIn("Verified steps", page.read_text(), page.name)

    def test_images_exist(self) -> None:
        missing: list[str] = []
        for page in SITE.rglob("*.html"):
            parser = Links()
            parser.feed(page.read_text())
            for key, value in parser.items:
                if key != "src" or not value.endswith((".webp", ".png", ".svg")):
                    continue
                target = resolve(page, value)
                if target and not target.exists():
                    missing.append(f"{page.relative_to(SITE)} -> {value}")
        self.assertEqual(missing, [], "\n".join(missing[:20]))

    def test_no_png_diagrams(self) -> None:
        for page in EN.rglob("*.md"):
            self.assertNotRegex(page.read_text(), r"assets/diagrams/[^)\s]+\.png", page.name)

    def test_episode_pages_built(self) -> None:
        for page in EPISODES.glob("ep*.md"):
            built = SITE / "four-hats" / "episodes" / page.stem / "index.html"
            self.assertTrue(built.exists(), page.stem)

    def test_wiki(self) -> None:
        for base in (SITE / "wiki", SITE / "ar" / "wiki"):
            self.assertTrue((base / "index.html").exists())
            self.assertTrue((base / "rest" / "index.html").exists())
        for page in SITE.rglob("*.html"):
            self.assertNotIn("[[", page.read_text(), page.name)
        en = (SITE / "assets" / "backlinks.json").read_text()
        ar = (SITE / "ar" / "assets" / "backlinks.json").read_text()
        self.assertIn("/wiki/rest/", en)
        self.assertIn("/ar/wiki/rest/", ar)

    def test_nav_sections_collapse(self) -> None:
        config = (ROOT / "mkdocs.en.yml").read_text()
        self.assertNotIn("navigation.sections", config)
        page = (SITE / "courses" / "index.html").read_text()
        self.assertIn("Four Hats", page)
        self.assertIn("md-nav__toggle", page)

    def test_assets_are_versioned(self) -> None:
        page = (SITE / "index.html").read_text()
        self.assertRegex(page, r"hover\.js\?v=[0-9a-f]{10}")
        self.assertRegex(page, r"analytics\.js\?v=[0-9a-f]{10}")
        js = (SITE / "assets" / "hover.js").read_text()
        self.assertIn("backlinks.json?v=", js)

    def test_hover_does_not_scroll(self) -> None:
        js = (SITE / "assets" / "hover.js").read_text()
        self.assertNotIn("scrollIntoView", js)
        self.assertIn('querySelectorAll(".headerlink")', js)

    def test_hover_and_font(self) -> None:
        self.assertTrue((SITE / "assets" / "hover.js").exists())
        self.assertTrue((SITE / "assets" / "hover.css").exists())
        self.assertTrue((SITE / "assets" / "fonts" / "noto-naskh-arabic.woff2").exists())
        page = (SITE / "wiki" / "rest" / "index.html").read_text()
        self.assertIn("hover.js", page)
        self.assertIn("hover.css", page)

    def test_callouts(self) -> None:
        page = (SITE / "wiki" / "index.html").read_text()
        self.assertIn('class="admonition tip"', page)
        self.assertNotIn("[!tip]", page)

    def test_analytics(self) -> None:
        js = (SITE / "assets" / "analytics.js").read_text()
        self.assertIn("3034df8d-b43a-4664-8a8a-6d89f86c32eb", js)
        self.assertIn("umami.alialjaffer.com", js)
        self.assertIn('data-tag", "docs"', js)
        self.assertIn("docs:preview", js)
        for page in (SITE / "index.html", SITE / "four-hats" / "episodes" / "ep04-add-a-feature-with-a-test" / "index.html"):
            self.assertIn("analytics.js", page.read_text())

    def test_slides(self) -> None:
        self.assertTrue((SITE / "slides" / "index.html").exists())
        decks = list((SITE / "slides").glob("ep*.html"))
        self.assertGreaterEqual(len(decks), 27)
        self.assertIn("analytics.js", decks[0].read_text())

    def test_redirects_configured(self) -> None:
        conf = (ROOT / "deploy" / "nginx.conf").read_text()
        self.assertIn("return 301 /four-hats/", conf)
        self.assertIn("rewrite ^/courses/four-hats/", conf)

    def test_sitemap_and_404(self) -> None:
        self.assertTrue((SITE / "sitemap.xml").exists())
        self.assertTrue((SITE / "404.html").exists())
        self.assertTrue((SITE / "ar" / "404.html").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
