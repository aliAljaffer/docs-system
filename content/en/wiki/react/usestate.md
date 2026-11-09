---
title: UseState
category: React
description: ''
tags:
- react
- hooks
---

<!-- imported from ObsidianVault/webdev/react/useState.md. Edit the source, then run sync.py. -->

# UseState

`react` `hooks`

- State creation:
  - **Simple**: `useState(20)`
  - **Function-based:** `useState(() => calculateSum());`
    - Function must be [[pure-functions|pure]] and has no arguments.
- **State update**:
  - **Simple**: `setState(30)`
  - **Current-state-based**: `useState((curr) => curr + 1);`
