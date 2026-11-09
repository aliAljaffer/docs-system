# Docs System

Site builder for `docs.alialjaffer.com`. Zensical is the locked builder.

The full plan, decisions, caveats, and gaps live in
`~/mk-project/hq-main/DOC_SYSTEM.md`. This file is only the operator quick start.

## Sources

| Content | Canonical location |
|---|---|
| English course pages | `~/mk-project/four-hats/docs/episodes/` |
| Verified apply steps | `~/mk-project/four-hats/docs/act*.md` |
| English site-wide pages | `content/en/` |
| Arabic pages | `content/ar/` |
| Diagram sources | `~/mk-project/hq-main/scripts/diagrams/` |
| Slides and scripts | `~/mk-project/hq-main/` |

## Build

```bash
cd ~/docs-system

# Copy course pages and convert diagrams
/Users/h/branding/.venv/bin/python sync.py

# Build English to site/, Arabic to site/ar/
/Users/h/branding/.venv/bin/python build.py

# English parity gate
/Users/h/branding/.venv/bin/python check_parity.py

# Preview both locales
python3 -m http.server -d site 8000
```

Open `http://localhost:8000/` and `http://localhost:8000/ar/`.

## Layout

```text
content/en/             authored English pages plus synced course pages
content/ar/             authored Arabic pages
assets/                 shared CSS and generated WebP diagrams
build/en, build/ar      assembled site trees, generated
site/                   final output, generated
sync.py                 copies sources and converts diagrams
build.py                injects apply steps, writes nav, runs both builds
check_parity.py         gate for English episode pages
deck.py                 extracts a text digest from a slide deck
episode-tasks.yaml      episode to act-doc task mapping
```

Do not edit `content/en/four-hats/episodes/`, `build/`, `site/`, or `mkdocs.en.yml` and `mkdocs.ar.yml`. They are generated.

## Arabic rule

Pair by path: `content/en/foo.md` with `content/ar/foo.md`. Arabic pages carry Arabic theory and the English verified apply steps, injected unchanged at build time.
