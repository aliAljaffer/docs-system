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


| Action | Simple | Function-based |
|---|---|---|
| State creation | `useState(20)` | `useState(() => calculateSum());` |
| State update | `setState(30)` | **Current-state-based**: `useState((curr) => curr + 1);` |

For function-based state creation, the function must be [[pure-functions|pure]] and has no arguments.
