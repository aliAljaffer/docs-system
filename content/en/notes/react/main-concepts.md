---
title: Main-concepts
category: React
description: '[[controlled-elements]]'
tags:
- react
- web
---

<!-- imported from ObsidianVault/webdev/react/main-concepts.md. Edit the source, then run sync.py. -->

# Main-concepts

`react` `web`

[[component]]

[[hook]]

[[controlled-elements]]

## One-way data flow

Always parent to child, never vice-versa.
## Re-Renders

UI Re-renders happen when any of these scenarios happen:
- State change
- Props change
- Parent re-renders
- Context changes

## Miscellaneous 

**Grab inputs**: `onChange={e => setState(e.target.value)}`

**onClick**: Almost always want to use `e.preventDefault()` in the click handlers.
