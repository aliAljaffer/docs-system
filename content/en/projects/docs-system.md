# Docs system

**Status:** Active

This site is a project too. It is a static documentation hub for projects, courses, tools, and notes.

## How it works

| Part | Choice |
|---|---|
| Builder | Zensical |
| Languages | English at `/`, Arabic at `/ar/` |
| Source | GitHub repository `docs-system` |
| Pipeline | GitHub Actions builds the image, ArgoCD deploys it |
| Analytics | Umami, dedicated Docs property |
| Wiki | Term pages with backlinks and hover previews |

## Design and operations

The full plan, decisions, caveats, and gaps live in the HQ repository.

- [Plan](https://github.com/aliAljaffer/minikube-project/blob/main/DOC_SYSTEM.md)
- [Repository](https://github.com/aliAljaffer/docs-system)
- [Live site](https://docs.alialjaffer.com)
- [Umami](https://umami.alialjaffer.com)

## Content model

- Projects live under `projects/`.
- Courses keep their own URL. Four Hats is at `/four-hats/`.
- Notes live under `notes/`.
- Tool references live under `tools/`.
- Shared definitions live under `wiki/`.

Adding a project means one entry in `catalog.yaml`, one page, and a build.
