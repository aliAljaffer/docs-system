---
title: useFetcher
category: React Router
description: 'React note: useFetcher.'
tags:
- react
- routing
---

# useFetcher

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
