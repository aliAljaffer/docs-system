---
title: Installation
category: React
description: 'React note: Installation.'
tags:
- react
---

# Installation

`react`

This page shows how to create a React project with Create React App or Vite, and how to set up ESLint.

Create React App: `npx create-react-app@5 [directory]`

- Start: `npm start`

Vite.js + React: `npm create vite@latest` then `npm i` to install packages. USE `.jsx` FOR VITE!

1. Install essentials: `npm i eslint@8 vite-plugin-eslint eslint-config-react-app --save`

2. Create the ESLint config file for your eslint version:

   - If eslint < 9.0: create `.eslintrc.json` with content:

     ```json
     {
       "extends": "react-app"
     }
     ```

   - Else create `.eslint.config.cjs`:

     ```js
     module.exports = {
       extends: "react-app",
     };
     ```

3. In `vite.config.js` import `eslint`:

   ```js
   import { defineConfig } from "vite";
   import react from "@vitejs/plugin-react";
   import eslint from "vite-plugin-eslint";
   // https://vitejs.dev/config/
   export default defineConfig({
     plugins: [react(), eslint()],
   });
   ```

4. Start: `npm run dev`

JSON-Server start: `here`
