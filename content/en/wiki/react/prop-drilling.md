---
title: Prop-drilling
category: React
description: '...is the process of passing down data through [[props]] from a parent
  to a grandchild or greater. In this case, the child and several of its children
  do not use the passed data, and they only functio'
tags:
- react
- patterns
---

<!-- imported from ObsidianVault/webdev/react/design-patterns/prop-drilling.md. Edit the source, then run sync.py. -->

# Prop-drilling

`react` `patterns`

...is the process of passing down data through [[props]] from a parent to a grandchild or greater. In this case, the child and several of its children do not use the passed data, and they only function as "carriers" of the data to its final destination.
