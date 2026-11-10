---
title: UseState
category: React
description: 'React note: UseState.'
tags:
- react
- hooks
---


# UseState

`react` `hooks`

- State creation:
  - **Simple**: `useState(20)`
  - **Function-based:** `useState(() => calculateSum());`
    - Function must be [[pure-functions|pure]] and has no arguments.
- **State update**:
  - **Simple**: `setState(30)`
  - **Current-state-based**: `useState((curr) => curr + 1);`
