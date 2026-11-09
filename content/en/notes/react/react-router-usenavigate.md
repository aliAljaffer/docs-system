---
title: UseNavigate
category: React
description: Navigator hook that returns a function to change the URL.
tags:
- react
---

<!-- imported from ObsidianVault/webdev/react/react-router/useNavigate.md. Edit the source, then run sync.py. -->

# UseNavigate

`react`

Navigator hook that returns a function to change the URL.

```js
import { Navigate } from "react-router-dom";
const navigate = useNavigate();
const options = { replace: True }; // Set to replace the URL without including it in the search history
navigate("/product", options); // Options are optional
navigate(-1); // Goes back in history one page.
```
