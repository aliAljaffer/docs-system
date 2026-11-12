---
title: setting-routes
category: React Router
description: 'React note: setting-routes.'
tags:
- react
- routing
---

# setting-routes

`react` `routing`

In React Router, routes map URL paths to the elements that the app displays.

### To set routes

```js
import { BrowserRouter, Route, Routes } from "react-router-dom";
<BrowserRouter>
  <Routes>
    <Route path="/" element={elementToDisplayForThisRoute} /> // this means root
    route, /
    <Route path="added-to-url-after-/" />
    <Route path="countries/:id" /> // adds an (id) after the / which will be the
    name of the param
  </Routes>
</BrowserRouter>;
```

### Routes in 6.4+ (createBrowserRouter)

- For an AppLayout component, make it the parent of paths that it lays out and make it not have a path

```js
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Home from "./ui/Home";
import Menu from "./features/menu/Menu";
const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/menu",
    element: <Menu />,
  },
]);
function App() {
  return <RouterProvider router={router}></RouterProvider>;
}
```
