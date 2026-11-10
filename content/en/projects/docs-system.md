---
title: Docs system
date: '2026-11-09'
description: This site. Zensical, bilingual, source-controlled, deployed by ArgoCD, with Umami analytics and a wiki.
tags:
- documentation
- zensical
- analytics
status: Active
---

# Docs system

**Status:** Active

This site is a project too. It is a static documentation hub for projects, courses, blogs, notes, and definitions.

## How it works

| Part | Choice |
|---|---|
| Builder | Zensical |
| Languages | English at `/`, Arabic at `/ar/` |
| Source | GitHub repository `docs-system` |
| Pipeline | GitHub Actions builds the image, ArgoCD deploys it |
| Analytics | Umami, dedicated Docs property |
| Definitions | Term pages with backlinks and hover previews |

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
- Shared definitions live under `definitions/`.

Adding a project means one entry in `catalog.yaml`, one page, and a build.
