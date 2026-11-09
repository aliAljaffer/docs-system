---
title: UseReducer
category: React
description: Used a lot by Redux Toolkit
tags:
- react
- hooks
---

<!-- imported from ObsidianVault/webdev/react/useReducer.md. Edit the source, then run sync.py. -->

# UseReducer

`react` `hooks`

Used a lot by Redux Toolkit

- `const [state, dispatch] = useReducer(reducerFunction, initialState)`

- Takes in two arguments: `reducer()` function, and `initialState` containing the initial state.

- Returns two values: `state` the current state, and `dispatch` a function to dispatch actions that usually update `state`.

[Learn useReducer In 20 Minutes](https://www.youtube.com/watch?v=kK_Wqx3RnHk)

```js
function reducer(state, action){
	switch(action.type){
		case 'increment':
			return {count: state.count + action.payload}
		case 'decrement':
			return {count: state.count - action.payload}
		default:
			return state
	}
}

export default function App(){
	const [state, dispatch] = useReducer(reducer, { count: 0 });
	function inc(){
		dispatch({type: 'increment', payload: 1})
	}
	function dec(){
		dispatch({type: 'increment', payload: 1})
	}

	return (
		<>
			<button onClick={inc}>+</button>
			<span>{state.count}</span>
			<button onClick={dec}>-</button>
		</>
		)
}
```
