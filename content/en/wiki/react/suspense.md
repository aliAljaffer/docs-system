---
title: Suspense
category: React
description: Suspense API is a way for us to show a loading indicator or any type
  of fallback component while the child components are loading. To accompany [[lazy-loading]],
  you can use Suspense around the object
tags:
- react
- components
---

<!-- imported from ObsidianVault/webdev/react/suspense.md. Edit the source, then run sync.py. -->

# Suspense

`react` `components`

Suspense API is a way for us to show a loading indicator or any type of fallback component while the child components are loading.
To accompany [[lazy-loading]], you can use Suspense around the object/component to load to provide a fallback component while the lazy-loaded component loads in.

```js
import { Suspence, lazy } from 'react';
import LoadingSpinner from './LoadingSpinner';

const Button = lazy(() => import("./features/Button.js"));
...
<Suspense fallback={<LoadingSpinner />}>
  <Button />
</Suspence>
...
```
