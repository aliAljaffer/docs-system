---
title: UseEffect
category: React
description: Used for side-effects.
tags:
- react
- hooks
---

<!-- imported from ObsidianVault/webdev/react/useEffect.md. Edit the source, then run sync.py. -->

# UseEffect

`react` `hooks`

Used for side-effects.

```javascript
useEffect(
  function () {
    // something...

    return () => {
      // This is a cleanup function
      // return it to tell React to use it for clean up
      // such as removing timers or event handlers that aren't necessary later
    };
  },
  [
    /* This is a dependacy array. If a value in the dependancy array changes,
    the effect is triggered. Empty array means the effect runs only on first mount*/
  ]
);
```

#### Best Practices for useEffect()

- Dep array: Every state variable, prop, and context value used inside the effect MUST be included in the array. **Dont use objects or arrays as deps.**

- Additionally, reactive values also need to be included.

- To remove function deps: Move it to the effect, if it's needed outside then  [[memoization|memoize]] it.

- Effects should be as a last resort!
