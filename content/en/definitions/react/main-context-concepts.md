---
title: main-context-concepts
category: React
description: The React Context API provides a way to pass data through the component
  tree without having to pass props down manually at every level. It is useful for
  sharing data that can be considered “global” fo
tags:
- react
- context
---


# main-context-concepts

The **React Context API** provides a way to pass data through the component tree without having to pass [[props]] down manually at every level. It is useful for sharing data that can be considered “global” for a tree of React components.

- [[usereducer|useReducer]] preferred for state management in Contexts

1. Start with `const MyContext = createContext();` (Note the case of the variable name)
2. Create a [[provider]] that returns a `<MyContext.Provider></MyContext.Provider>` with `value` prop set to the values you want to be global in the context.
3. Remember to pass `children` inbetween [[provider|Provider]]
4. Custom Hook creation:
   1. Create a `useMyContext` hook that starts with `const context = useContext(MyContext);`
   2. Check if `context` is defined. If not, throw an error for when context is used outside [[provider|Provider]].
   3. Return the `context` object
5. Export both `useMyContext` and [[provider|Provider]]
