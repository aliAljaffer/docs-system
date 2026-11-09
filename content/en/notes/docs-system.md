# Documentation system notes

A public note about how this site is built. The full plan lives in the HQ repository.

## Why one site

One origin for every project, course, and note. A new project is a directory and a catalog entry, not a new site.

## Why Zensical

Zensical is the maintained successor to MkDocs Material. It builds both languages, and the output is static.

## What is custom

- The Arabic two-pass build.
- The wiki link resolver and backlink index.
- The hover preview.
- The language switcher and hreflang post-processing.

All of it is plain Python and JavaScript around a static build. See [[rest]] for a wiki link example.

## Links

- [Docs system project](../projects/docs-system.md)
- [Plan](https://github.com/aliAljaffer/minikube-project/blob/main/DOC_SYSTEM.md)
