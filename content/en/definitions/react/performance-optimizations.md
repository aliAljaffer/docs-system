---
title: Performance optimizations
category: React
description: 'React note: Performance optimizations.'
tags:
- react
---

# Performance optimizations

`react`

React performance optimization reduces wasted renders, improves responsiveness, and shrinks the bundle size.

Do NOT prematurely optimize. Run and test for bottlenecks first. Some bottlenecks are not worth optimizing for (Not a lot of gains)

We optimize performance in order to achieve three objectives:
1. Prevent wasted renders 
   - [[memoization]]
   - Passing elements as `children` or regular `prop`

2. Improve Responsiveness
   -  [[memoization]]
   - `useTransition`

3. Reduce Bundle Size
   - Use less 3rd party packages
   - Code splitting and [[lazy-loading]]
