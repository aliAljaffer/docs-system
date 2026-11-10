# Docs System

Site builder for `docs.alialjaffer.com`. Zensical is the locked builder.

The full plan, decisions, caveats, and gaps live in
`~/mk-project/hq-main/DOC_SYSTEM.md`. This file is only the operator quick start.

## Sources

| Content | Canonical location |
|---|---|
| English course pages | `~/mk-project/four-hats/docs/episodes/` |
| Verified apply steps | `~/mk-project/four-hats/docs/act*.md` |
| Project write-ups and blog posts | `~/portfolio/src/data/` |
| Study notes and definitions | `~/ObsidianVault/{studies,webdev}/` |
| Homelab docs | `~/src/homelab/docs/` |
| Grooszy docs | `~/grooszy/docs/` |
| Fai README and security policy | `~/fai/` |
| Operator docs | `~/openziti-operator/docs/` |
| English site-wide pages | `content/en/` |
| Arabic pages | `content/ar/` |
| Diagram sources | `~/mk-project/hq-main/scripts/diagrams/` |
| Slides and scripts | `~/mk-project/hq-main/` |

The vault import covers cloud and security definitions, GCP service references, certification notes, DevOps bootcamp notes, React notes, and web notes. Excalidraw drawings, trackers, and personal drafts are skipped.

## Build

```bash
cd ~/docs-system

# Import courses, portfolio pages, vault notes, and project docs
/Users/h/branding/.venv/bin/python sync.py

# Build English to site/, Arabic to site/ar/
/Users/h/branding/.venv/bin/python build.py

# English parity gate
/Users/h/branding/.venv/bin/python check_parity.py

# Preview both locales
python3 -m http.server -d site 8000
```

Open `http://localhost:8000/` and `http://localhost:8000/ar/`.

## CI sync

The publish workflow pulls the portfolio directly. No token and no portfolio workflow is needed.

1. Check out this repository.
2. Clone the portfolio repository.
3. Run `sync.py --portfolio`.
4. Validate, build, test, and publish the image.

It runs on a push to `main`, daily at 04:00 UTC, and manual dispatch. A portfolio commit appears on the next run.

Source paths can be overridden when the checkout moves:

| Variable | Default |
|---|---|
| `PORTFOLIO_DIR` | `~/portfolio/src/data` |
| `PORTFOLIO_PUBLIC_DIR` | `~/portfolio/public` |
| `OBSIDIAN_VAULT` | `~/ObsidianVault` |
| `FOUR_HATS_DIR` | `~/mk-project/four-hats` |
| `HQ_DIR` | `~/mk-project/hq-main` |
| `OPENZITI_DOCS_DIR` | `~/openziti-operator/docs` |
| `HOMELAB_DOCS_DIR` | `~/src/homelab/docs` |
| `GROOSZY_DOCS_DIR` | `~/grooszy/docs` |
| `FAI_DIR` | `~/fai` |

## Adding a New Entry

Decide what the entry is before you write it. Each section has one job.

| Section | Holds | Location | Frontmatter |
|---|---|---|---|
| Blogs | Published writing from the portfolio | `content/en/blogs/` | `title`, `date`, `description`, `tags` |
| Notes | Study notes and course summaries | `content/en/notes/<category>/` | `title`, `category`, `description`, `tags` |
| Definitions | Definitions and informational terms only | `content/en/definitions/<category>/` | optional |
| Projects | Systems you build | `catalog.yaml` plus `content/en/projects/` | catalog entry |

The directory decides the type. A file under `definitions/` is a definition. A file under `notes/` is a note. A file under `blogs/` is a blog. Portfolio files also carry `type: "project"` or `type: "blog"` in their frontmatter.

Guidelines:

1. Put one idea on one page. A definition is a concept or service reference. A note is course material, a lab, a checklist, or a how-to. Do not put a course chapter in Definitions, and do not put a service reference in Notes.
2. Portfolio entries are drop-in. Add a `.md` file to `~/portfolio/src/data/`, then run `build.py`. It imports the page, adds frontmatter, and updates the home list, the Projects or Blogs index, and the nav. Do not edit `catalog.yaml` for a portfolio entry.
3. Copy `templates/definition.md`, `templates/note.md`, or `templates/blog.md` for authored pages.
4. A definition can be a bare file with an H1. Frontmatter is optional and adds a category, description, and tags.
5. Use an existing category. Definitions and notes use `Cloud`, `Networking`, `Security`, `React`, `Web`, `GCP`, or `Site`.
6. Tag every definition and note page. Use lowercase kebab-case tags and reuse existing tags before adding a new one.
7. Link a definition with `[[slug]]` from any note, blog, or project page. The build fails on an unresolved link.
8. A page with an `<!-- imported from ... -->` marker is generated. Edit the source, then run `sync.py`. Remove the marker to make the page yours and stop the import.
9. A project with repository documentation uses a hub at `content/en/projects/<slug>/index.md`. Copy the repository docs into the same directory and point the catalog at the hub. The nav, the Projects index, and the home page pick up the children from the directory.
10. Add a non-portfolio project to `catalog.yaml`. The home page list is generated from the catalog plus any project page with frontmatter.
11. Run the checks before you commit:

```bash
/Users/h/branding/.venv/bin/python check_entries.py
/Users/h/branding/.venv/bin/python build.py
/Users/h/branding/.venv/bin/python check_parity.py
/Users/h/branding/.venv/bin/python -m unittest discover -s tests -v
```

`.github/workflows/validate.yml` runs the same four commands on every pull request. The publish workflow runs them on `main` before it builds the image.

## Add a project

A portfolio project needs one file. Add `README.md` style content to `~/portfolio/src/data/<slug>.md` with `type: "project"`, then run `build.py`. The page, the home entry, the Projects index, and the nav update automatically. `sync.py` runs the portfolio import first when the source folder exists.

A project that does not live in the portfolio needs a catalog entry:

1. Add an entry to `catalog.yaml`: slug, title, status, summary, tags, page.
2. Copy `templates/project.md` to `content/en/projects/<slug>.md`, or to `content/en/projects/<slug>/index.md` when the project has imported docs.
3. Run `sync.py` if the project has source docs, then `build.py`.
4. The home page list is generated from the catalog plus any project page with frontmatter.

The curated page is the hub entry. Import deep documents from the project repository only when they are stable, and keep the curated page as the index.

Project pages under `content/en/projects/<slug>.md` and blogs under `content/en/blogs/` that start with an import marker are generated from `~/portfolio/src/data/`. Edit the source, then run `sync.py`. A generated page is never overwritten after you remove the marker.

The OpenZiti Operator, Homelab, Grooszy, and Fai keep their curated hub at `content/en/projects/<slug>/index.md`. The rest of each directory is copied from the project repository by `sync.py`. The project nav reads the directory, so an imported page appears without a catalog change.

## Add a course

1. Add an entry to the `courses` list in `catalog.yaml`: slug, title, status, summary, tags, page.
2. Copy `templates/course.md` to the course page and fill it.
3. Keep the course URL stable. Four Hats stays at `/four-hats/`; `/courses/` is the landing page.
4. Run `build.py`. The course appears on `/courses/` and in the Courses nav.

## Layout

```text
catalog.yaml            project registry: title, status, summary, tags, page
templates/              page templates for projects, definitions, notes, and blogs
content/en/             authored English pages plus synced sources
content/ar/             authored Arabic pages
assets/                 shared CSS, imported images, generated WebP diagrams
build/en, build/ar      assembled site trees, generated
site/                   final output, generated
sync.py                 imports sources, converts pages and diagrams
build.py                injects apply steps, writes nav and indexes, runs both builds
check_entries.py        validates catalog entries and page frontmatter
check_parity.py         gate for English episode pages
deck.py                 extracts a text digest from a slide deck
episode-tasks.yaml      episode to act-doc task mapping
```

Do not edit `content/en/four-hats/episodes/`, `build/`, `site/`, or `mkdocs.en.yml` and `mkdocs.ar.yml`. They are generated. Do not edit a page that carries an import marker. Edit the source, then run `sync.py`.

## Arabic rule

Pair by path: `content/en/foo.md` with `content/ar/foo.md`. Arabic pages carry Arabic theory and the English verified apply steps, injected unchanged at build time.
