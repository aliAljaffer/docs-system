---
title: React-lazy
category: React
description: In React, we use [[lazy-loading]] on components that might be too complex
  or big to save on loading time. React provides a lazy() function to do that. Traditionally,
  we'll use [[suspense]] on lazy-loa
tags:
- react
- performance
---

<!-- imported from ObsidianVault/webdev/react/react-lazy.md. Edit the source, then run sync.py. -->

# React-lazy

`react` `performance`

In React, we use [[lazy-loading]] on components that might be too complex or big to save on loading time. React provides a `lazy()` function to do that. Traditionally, we'll use [[suspense]] on lazy-loaded components.

```js
const Button = lazy(() => import("./features/Button.js"));
```
