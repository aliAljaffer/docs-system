---
title: UseFetcher
category: React
description: Use data from another route but without navigating there. Uses the loader()
  function in the route
tags:
- react
---

<!-- imported from ObsidianVault/webdev/react/react-router/useFetcher.md. Edit the source, then run sync.py. -->

# UseFetcher

`react`

Use data from another route but without navigating there. Uses the `loader()` function in the route

```js
const fetcher = useFetcher();
useEffect(
  function () {
    if (!fetcher.data && fetcher.state === "idle") fetcher.load("/menu");
  },
  [fetcher]
);
```
