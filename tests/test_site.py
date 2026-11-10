#!/usr/bin/env python3
"""End-to-end checks for the built site."""
from __future__ import annotations

import json
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
SITE = ROOT / "site"

import fetch  # noqa: E402
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
            self.assertIn("assets/og.png", page, rel)
        self.assertTrue((SITE / "assets" / "og.png").exists())

    def test_wiki(self) -> None:
        self.assertTrue((SITE / "definitions" / "rest" / "index.html").exists())
        self.assertIn("/definitions/", (SITE / "assets" / "backlinks.json").read_text())

    def test_callouts(self) -> None:
        result = convert_callouts("> [!tip] Hover a term\n> Move the pointer over a link.\n")
        self.assertIn('!!! tip "Hover a term"', result)
        self.assertIn("    Move the pointer", result)

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
