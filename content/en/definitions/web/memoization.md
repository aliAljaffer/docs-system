---
title: Memoization
category: Web
description: The act of storing previous function call results into a data structure,
  for faster retrieval on second attempts of the function call with the same parameters.
tags:
- web
- fundamentals
---

<!-- imported from ObsidianVault/webdev/general-concepts/memoization.md. Edit the source, then run sync.py. -->

# Memoization

`web` `fundamentals`

The act of storing previous function call results into a data structure, for faster retrieval on second attempts of the function call with the same parameters.

## React Memoization tools

`memo`: For components
```js
const memoizedComponent = memo(componentToMemoize)
```

`useMemo`: For objects
```js
    const memoizedComponent = useMemo(()=> {
        return objectIsMemoizedNow: true;
    }, [header])
```

`useCallback`: For functions
```js
const memoizedComponent = useCallback(functionToMemoize, [])
```
