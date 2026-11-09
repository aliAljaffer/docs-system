---
title: Main-context-concepts
category: React
description: The React Context API provides a way to pass data through the component
  tree without having to pass props down manually at every level. It is useful for
  sharing data that can be considered “global” fo
tags:
- react
- context
---

<!-- imported from ObsidianVault/webdev/react/context-api/main-context-concepts.md. Edit the source, then run sync.py. -->

# Main-context-concepts

`react` `context`

The **React Context API** provides a way to pass data through the component tree without having to pass [[props]] down manually at every level. It is useful for sharing data that can be considered “global” for a tree of React components.

- [[usereducer|useReducer]] preferred for state management in Contexts

- Start with `const MyContext = createContext();` (Note the case of the variable name)

- Create a [[provider]] that returns a `<MyContext.Provider></MyContext.Provider>` with `value` prop set to the values you want to be global in the context.

- Remember to pass `children` inbetween [[provider|Provider]]

- Custom Hook creation:

  - Create a `useMyContext` hook that starts with `const context = useContext(MyContext);`

  - Check if `context` is defined. If not, throw an error for when context is used outside [[provider|Provider]].

  - Return the `context` object

- Export both `useMyContext` and [[provider|Provider]]
