---
title: Controlled-elements
category: React
description: Controlled elements in React are elements that have a state that gets
  updated concurrently as user enters data. The state and user input are tied together.
  Example
tags:
- react
- forms
---

<!-- imported from ObsidianVault/webdev/react/design-patterns/controlled-elements.md. Edit the source, then run sync.py. -->

# Controlled-elements

`react` `forms`

Controlled elements in React are elements that have a state that gets updated concurrently as user enters data. The state and user input are tied together. 
## Example

`<input>`: set `value` prop to `state` value. Set the `onChange` function to the state setter with the value `e.target.value`. Now each keystroke updates the state.
