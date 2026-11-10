---
title: Component
category: Web
description: Component contains the logic (hook) and the view of an element. By convention,
  components start with a capital letter.
tags:
- web
- fundamentals
---


# Component

`web` `fundamentals`

## React components

```js
export default function ComponentA() {
	return <div>Hello, </div>
}

export const ComponentB = () => {
	return <div>World!</div>
}

function ComponentC() {
	return (<>
		<ComponentA />
		<ComponentB />
	</>)
}
```

Component contains the logic ([[hook]]) and the view of an element. By convention, components start with a capital letter.

## Angular components

```js
@Component({
  selector: 'app-component-overview',
  template: '<h1>Hello World!</h1>',
  styles: ['h1 { font-weight: normal; }'],
  standalone: true
})
```

Components are the main building blocks for Angular applications. Each component consists of:

- An **HTML** template that declares what renders on the page
- A **TypeScript** class that defines behavior
- A **CSS** selector that defines how the component is used in a template
- Optionally, CSS styles applied to the template

[source](https://v17.angular.io/guide/component-overview)

`ng generate component <component-name>`

By default, this command creates the following:

- A directory named after the component
- A component file, `<component-name>.component.ts`
- A template file, `<component-name>.component.html`
- A CSS file, `<component-name>.component.css`
- A testing specification file, `<component-name>.component.spec.ts`

Files created separately can be linked to the component using `urls` and a relative path:

```js
@Component({
  selector: 'app-component-overview',
  templateUrl: './component-overview.component.html',
  styleUrls: ['./component-overview.component.css']
})
```
