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
| `exclude` | no | Top-level folders to skip |

The build copies every Markdown file and image under `path`. `README.md` becomes the overview page. Without a README, the build creates the overview from the repo description. Links that leave the docs folder point to GitHub.

## Add a course

Same fields, under `courses:`. The URL is `/<slug>/`. `four-hats` also gets its episode navigation and the verified steps from the act guides (`episode-tasks.yaml`).

## Definitions, Home, Contact

These live in `content/en/`. Link a definition with `[[slug]]`. The build fails on an unresolved link.

## Updates

The site rebuilds on every push to `main`, on `repository_dispatch` (`docs-updated`), and daily at 03:00 UTC as a safety net. Overlapping runs queue; the newest pending run replaces older ones. Run the `Publish` workflow to rebuild now.

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
check_sources.py validates sources.yaml
content/en/      Home, Contact, Definitions, Four Hats overview
assets/          shared JS and CSS
episode-tasks.yaml  Four Hats episode to act-guide mapping
```

Do not edit `build/`, `site/`, or `mkdocs.en.yml`. They are generated.
