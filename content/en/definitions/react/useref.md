---
title: useRef
category: React
description: 'React note: UseRef.'
tags:
- react
- hooks
---


# useRef

- the Ref is persisted across renders

- Should not be read/written `.current` in render logic like state [[usestate|useState]]

- For DOM elements: Make `const myRef = useRef()` and add it as property to the element to reference: `<p ref={myRef}>I love Hooks</p>`

- Element will be stored in `myRef.current`
