---
title: useNavigate
category: React Router
description: 'React note: useNavigate.'
tags:
- react
- routing
---

# useNavigate

Navigator hook that returns a function to change the URL.

```js
import { Navigate } from "react-router-dom";
const navigate = useNavigate();
const options = { replace: True }; // Set to replace the URL without including it in the search history
navigate("/product", options); // Options are optional
navigate(-1); // Goes back in history one page.
```
