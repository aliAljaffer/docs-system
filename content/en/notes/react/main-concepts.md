---
title: Main-concepts
category: React
description: Always parent to child, never vice-versa.
tags:
- react
---


# Main-concepts

`react`

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
