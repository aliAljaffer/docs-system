---
title: Provider
category: React
description: A Provider is a component that provides a global value to its children.
  Providers are used in Context API to share a piece of data across the entire app,
  such as theme or maybe chosen language.
tags:
- react
- context
---

<!-- imported from ObsidianVault/webdev/react/context-api/provider.md. Edit the source, then run sync.py. -->

# Provider

`react` `context`

A Provider is a component that provides a global value to its children. Providers are used in Context API to share a piece of data across the entire app, such as theme or maybe chosen language.

```js
const ThemeContext = createContext();

const ThemeContextProvider = (children) => {
	const [theme, setTheme] = useState<"dark" | "light">("dark");
	return (<ThemeContext.Provider value={{theme}}> {children} </ThemeContext.Provider>)
}

const useTheme = () => {
	const context = useContext(ThemeContext);
	if (!context) return new Error("Theme context used outside of provider.")
	return context;
}}
```
