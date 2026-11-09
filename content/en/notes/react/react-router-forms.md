---
title: Forms
category: React
description: Use <Form method="POST" from react router. Kinda like PHP. Hidden input
  enables us to submit the cart with the order, without needing an input field displayed.
tags:
- react
---

<!-- imported from ObsidianVault/webdev/react/react-router/forms.md. Edit the source, then run sync.py. -->

# Forms

`react`

Use `<Form method="POST">` from react router. Kinda like PHP. Hidden input enables us to submit the cart with the order, without needing an input field displayed.

```js
const hiddenInput = (
  <input type="hidden" name="cart" value={JSON.stringify(cart)} />
);
export async function action({ request }) {
  const formData = request.formData();
  const data = Object.fromEntries(formData);
  return null;
}
```

- A form knows its own action because of RRouter:

```js
import CreateOrder, {
  action as createOrderAction,
} from "./features/order/CreateOrder";

{
  path: "/order/new",
  element: <CreateOrder />,
  action: createOrderAction, // Here
}
```

- Use `redirect()` instead of [[react-router-usenavigate|useNavigate]] when not in a hook or component.

- Error handling in Forms is done with the `useFormData()` hook. In the `action()`, return an errors object if there are any errors,
  then in the original component, use the hook to get the data returned by the action and render errors conditionally

```js
// Form example
<Form>
  <div>
    <label>Phone number</label>
    <div>
      <input type="tel" name="phone" required />
    </div>
    {
      formErrors?.phone && (
        <p>{formErrors.phone}</p>
      ) /*Error is displayed if action returned any errors about phone number*/
    }
  </div>
</Form>;
export async function action({ request }) {
  const formData = await request.formData();
  const data = Object.fromEntries(formData);
  const order = {
    ...data,
    cart: JSON.parse(data.cart),
    priority: data.priority === "on",
    phone: data.phone.replaceAll(" ", ""),
  };
  // Errors object
  const errors = {};
  if (!isValidSaudiPhone(order.phone))
    errors.phone =
      "Please give us a valid Saudi phone number. You can use either the +966, 00966, or 05 format.";
  // If no errors, move on.
  if (Object.keys(errors).length !== 0) return errors;

  const newOrder = await createOrder(order);

  return redirect(`/order/${newOrder.id}`);
}
```
