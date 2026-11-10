---
title: loaders
category: React Router
description: 'React note: loaders.'
tags:
- react
- routing
---

# loaders

`react` `routing`

React Router 
- Loaders load data before component renders

1. Create a `loader()` function inside the component that needs the data

2. Provide the function to the route in a `loader` prop

3. use `useLoaderData()` in the component to get the loaded data

```js
// getMenu() - helpers.js

export async function getMenu() {
  const res = await fetch(`${API_URL}/menu`);

  // fetch won't throw error on 400 errors (e.g. when URL is wrong), so we need to do it manually. This will then go into the catch block, where the message is set
  if (!res.ok) throw Error("Failed getting menu");

  const { data } = await res.json();
  return data;
}

export async function getOrder(id) {
  const res = await fetch(`${API_URL}/order/${id}`);
  if (!res.ok) throw Error(`Couldn't find order #${id}`);

  const { data } = await res.json();
  return data;
}

// Menu.jsx
import { useLoaderData } from "react-router-dom";
import { getMenu } from "../../utils/helpers";
function Menu() {
  const menu = useLoaderData();
  return <h1>Menu</h1>;
}

export async function loader() {
  const menu = await getMenu();
  return menu;
}

// -----------------------------------------------

// App.jsx
const router = createBrowserRouter([
  {
    element: <AppLayout />,
    children: [
      {
        path: "/",
        element: <Home />,
      },
      {
        path: "/menu",
        element: <Menu />,
        loader: menuLoader,
      },
    ],
  },
]);
```

Loaders also receive params, which you can extract. the name `orderId` is because we defined it as such in the routes

```js
// Order.jsx
export async function loader({ params }) {
const order = await getOrder(params.orderId);
return order;
}

// App.jsx
import Order, { loader as orderLoader } from "./features/order/Order";
...
{
{ path: "/order/:orderID", element: <Order />, loader: orderLoader }
}
...

```
