---
title: Grooszy
date: '2026-10-29'
description: Private, self-hosted analysis of Saudi bank statements. Go for parsing, Next.js for the interface, PostgreSQL for storage.
tags:
- go
- nextjs
- postgresql
- privacy
status: Active
---

# Grooszy

**Status:** Active

Grooszy is a private, self-hosted tool for analysing Saudi bank statements. It imports Alinma XLSX and Al Rajhi PDF exports, checks every statement against its own header, blocks duplicate imports, and explains spending in plain language.

No statement data leaves the deployment.

## Stack

| Part | Choice |
|---|---|
| Parsing and storage | Go |
| Interface | Next.js |
| Database | PostgreSQL |
| Identity | Keycloak |
| Deployment | Kubernetes on the homelab |

## What it does

- Imports Alinma XLSX exports.
- Imports Al Rajhi PDF exports.
- Refuses a statement that does not reconcile against its own header.
- Blocks duplicate imports.
- Groups spending and explains it in plain language.

## Documentation

The repository documents are imported into this site. The index is the entry point.

- [Repository](https://github.com/aliAljaffer/grooszy)
- [Documents index](documents.md)
- [API](API.md)
- [Chat](CHAT.md)
- [Backups](BACKUPS.md)
- [Data model](DATA-MODEL.md)
- [Explainers](EXPLAINERS.md)
- [Features](FEATURES.md)
- [Image](IMAGE.md)
- [Keycloak client](KEYCLOAK-CLIENT.md)
- [Operations](OPERATIONS.md)
- [Parsing notes](PARSING-NOTES.md)
- [Parsing parity](PARSING-PARITY.md)
- [Privacy](PRIVACY.md)
- [Reminders](REMINDERS.md)

## Import status

These pages are copied from `docs/` in the repository by `sync.py`. Edit the repository, then run `sync.py`, not these pages.
