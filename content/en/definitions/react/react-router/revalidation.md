---
title: revalidation
category: React Router
description: 'React note: revalidation.'
tags:
- react
- routing
---

# revalidation

`react` `routing`

In React Router, revalidation re-fetches the data of the current page after an action runs, so the page shows the latest data.

```js
function UpdateOrder({ order }) {
  const fetcher = useFetcher();

  return (
    <fetcher.Form method="PATCH" className="text-right">
      <Button type="primary">Make priority</Button>
    </fetcher.Form>
  );
}

export async function action({ request, params }) {
  const data = { priority: true };

  await updateOrder(params.orderId, data);
  return null;
}
```

After the button submits the patch request, the page is revalidated to reflect the new possible changes in data.
