# Docs System

Site builder for `docs.alialjaffer.com`. Zensical builds the site. Each project and course page is fetched from its own repository at build time.

## Commands

```bash
make setup   # create .venv, install requirements.txt
make check   # validate sources.yaml
make build   # fetch the repos, build site/, run the tests
make serve   # preview at http://localhost:8000/
```

## Add a project

Add three fields to `sources.yaml`, then push to `main`.

```yaml
projects:
  - slug: my-project
    repo: owner/name
    branch: main
    path: docs
```

| Field | Required | Meaning |
|---|---|---|
| `slug` | yes | URL segment, `/projects/<slug>/` |
| `repo` | yes | Public GitHub repo, `owner/name` |
| `branch` | yes | Branch to read |
| `path` | yes | Docs folder in the repo. Use `.` for the repo root |
| `title` | no | Default: the slug in title case |
| `description` | no | Default: the GitHub repo description |
| `case_study` | no | Case study id on alialjaffer.com. Adds a `Case study` link next to `Repository`. Letters, digits, and hyphens |
| `exclude` | no | Top-level folders to skip |
| `src` | no | Local folder to copy instead of cloning the repo. `repo`, `branch`, and `path` still build the GitHub links. `four-hats` uses `docs-src/four-hats` |

The build copies every Markdown file and image under `path`. `README.md` becomes the overview page. Without a README, the build creates the overview from the repo description. Links that leave the docs folder point to GitHub.

## Add a course

Same fields, under `courses:`. The URL is `/<slug>/`. `four-hats` keeps its docs in `docs-src/four-hats` (this repo is the source). It also gets its episode navigation and the verified steps from the act guides (`episode-tasks.yaml`).

## Last updated and edit link

Each page shows the date of the last commit to its source file. The build reads it from git history. Pages the build generates, such as listings and the episode index, show no date.

Each dated page also links to its source file on GitHub. Generated pages have no edit link.

CI checkouts need full history. Set `fetch-depth: 0` on `actions/checkout`. The build stops on a shallow clone.

## Brand

The brand lives in `brand/`. It is a vendored copy of a branch of the private `branding` repo. Nothing else hard-codes a colour or font.

- `brand/brand.json` and `brand/icon.svg` hold the colours, fonts, font stylesheets, and icon.
- `brand.py` compiles the brand into `brand.css` and the Giscus themes.
- `assets/theme.css` maps `--brand-*` onto the theme variables. It holds no colours or font names.
- `templates/giscus.css.tmpl` maps the brand onto the Giscus variables.

Only `paper`, `ink`, and `accent` are required per mode. The compiler derives the rest.

### Change the brand

1. Run `make brand BRAND_REF=<branch>`. It copies that branch of the `branding` repo into `brand/`. The default branch is `terminal`.
2. Run `make build`.
3. Check the pages in light and night mode.
4. Deploy. The asset version changes, so caches refresh.

## Definitions, Home, Contact

These live in `content/en/`. Link a definition with `[[slug]]`. The build fails on an unresolved link.

## Updates

The site rebuilds on every push to `main`, on `repository_dispatch` (`docs-updated`), and daily at 03:00 UTC. The daily run deploys only when this repo or a source repo has a new commit since the last deploy. Other triggers always deploy. Overlapping runs queue; the newest pending run replaces older ones. Run the `Publish` workflow to rebuild now.

### Rebuild on source repo push

1. Install the `update-manifests-homelab` GitHub App on the source repo.
2. Add the App private key as the secret `HOMELAB_APP_KEY` in the source repo.
3. Add `.github/workflows/notify-docs.yml` to the source repo:

```yaml
name: Notify docs
on:
  push:
    branches: [main]
    paths: ["docs/**", "README.md"]
jobs:
  notify:
    uses: aliAljaffer/docs-system/.github/workflows/notify.yml@main
    secrets: inherit
```

Match `branches` and `paths` to the `branch` and `path` in `sources.yaml`.

## Layout

```text
sources.yaml     projects and courses: repo, branch, path
fetch.py         clones the repos and copies the docs
build.py         assembles the tree, rewrites links, writes nav and indexes
brand.py         compiles brand/ into brand.css and the Giscus themes
brand/           brand.json and icon (vendored from the branding repo)
check_sources.py validates sources.yaml
content/en/      Home, Contact, Definitions, Four Hats overview
assets/          shared JS and CSS (theme.css maps the brand onto the theme)
templates/       definition template and the Giscus theme template
episode-tasks.yaml  Four Hats episode to act-guide mapping
```

Do not edit `build/`, `site/`, or `mkdocs.en.yml`. They are generated.
