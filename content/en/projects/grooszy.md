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

The repository holds the detailed documents. Start with the README, then use the topic pages.

- [Repository](https://github.com/aliAljaffer/grooszy)
- [README](https://github.com/aliAljaffer/grooszy/blob/main/README.md)
- [API](https://github.com/aliAljaffer/grooszy/blob/main/docs/API.md)
- [Data model](https://github.com/aliAljaffer/grooszy/blob/main/docs/DATA-MODEL.md)
- [Operations](https://github.com/aliAljaffer/grooszy/blob/main/docs/OPERATIONS.md)
- [Privacy](https://github.com/aliAljaffer/grooszy/blob/main/docs/PRIVACY.md)
- [Backups](https://github.com/aliAljaffer/grooszy/blob/main/docs/BACKUPS.md)
- [Parsing notes](https://github.com/aliAljaffer/grooszy/blob/main/docs/PARSING-NOTES.md)

## Import status

The repository documents are linked, not copied. Importing them into this site is planned.
