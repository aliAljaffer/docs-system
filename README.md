# Docs System

Site builder for `docs.alialjaffer.com`. Zensical is the locked builder. Every page lives in this repo.

## Commands

```bash
make setup   # create .venv, install requirements.txt
make check   # validate frontmatter
make build   # build site/, run the parity gate and the tests
make serve   # preview at http://localhost:8000/ and /ar/
```

`python sync.py four-hats` imports the Four Hats course from its own repo. Set `FOUR_HATS_DIR` and `HQ_DIR` first. CI never runs it.

## Adding a New Entry

Create one Markdown file, then push to `main`. The directory sets the type. The frontmatter sets everything else.

| Field | Blogs | Projects | Notes | Definitions | Meaning |
|---|---|---|---|---|---|
| `title` | required | required | required | optional (H1 fallback) | Page and nav title |
| `description` | required | required | required | optional | Index and home summary |
| `date` | required | required | | | Sort order, `YYYY-MM-DD` |
| `tags` | required | required | required | optional | Lowercase kebab-case |
| `status` | | optional, default `Active` | | | Project status |
| `repo`, `url` | | optional | | | Links block |
| `category` | | | optional, folder fallback | optional, folder fallback | Index group |
| `draft` | optional | optional | optional | optional | `true` excludes the page from the build |
| `comments` | optional | optional | | | `false` turns comments off |

Locations:

| Type | Path |
|---|---|
| Blog | `content/en/blogs/<slug>.md` |
| Project | `content/en/projects/<slug>.md`, or `content/en/projects/<slug>/index.md` with child pages beside it |
| Note | `content/en/notes/<category>/<slug>.md` |
| Definition | `content/en/definitions/<category>/<slug>.md` |

The build adds the status or date line, the tag chips, and the links block under the H1 of every blog and project. Do not write them by hand.

Guidelines:

1. Put one idea on one page.
2. Copy a file from `templates/` to start.
3. Link a definition with `[[slug]]`. The build fails on an unresolved link.
4. Reuse existing tags before you add a new one.
5. Run `make check build` before you commit.

Blogs and projects get Giscus comments from `overrides/partials/comments.html`.

## Add a course

1. Add an entry to the `courses` list in `catalog.yaml`: slug, title, status, summary, tags, page.
2. Copy `templates/course.md` to the course page and fill it.
3. Keep the course URL stable. Four Hats stays at `/four-hats/`.

## Layout

```text
catalog.yaml            site tagline and course registry
templates/              page templates
content/en/             English pages
content/ar/             Arabic pages
overrides/              theme partials (comments)
assets/                 shared CSS, JS, images, diagrams
sources/                Four Hats act docs and video scripts
build/en, build/ar      assembled trees, generated
site/                   final output and posts.json, generated
sync.py                 manual Four Hats import
build.py                injects headers and apply steps, writes nav, indexes, and posts.json
check_entries.py        validates frontmatter
check_parity.py         gate for English episode pages
deck.py                 text digest from a slide deck: python deck.py [name ...]
episode-tasks.yaml      episode to act-doc task mapping
```

Do not edit `build/`, `site/`, `mkdocs.en.yml`, or `mkdocs.ar.yml`. They are generated.

## Arabic rule

Pair by path: `content/en/foo.md` with `content/ar/foo.md`. Arabic pages carry Arabic theory and the English verified apply steps, injected unchanged at build time.
