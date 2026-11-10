---
title: React-installation
category: React
description: 'Create React App: npx create-react-app@5 [directory]'
tags:
- react
---


# React-installation

`react`

Create React App: `npx create-react-app@5 [directory]`

- Start: `npm start`

Vite.js + React: `npm create vite@latest` then `npm i` to install packages. USE `.jsx` FOR VITE!

- Install essentials: `npm i eslint@8 vite-plugin-eslint eslint-config-react-app --save`

- if eslint < 9.0: create `.eslintrc.json` with content:

  ```json
  {
    "extends": "react-app"
  }
  ```

- else create `.eslint.config.cjs`:

  ```js
  module.exports = {
    extends: "react-app",
  };
  ```

- in `vite.config.js` import `eslint`:

  ```js
  import { defineConfig } from "vite";
  import react from "@vitejs/plugin-react";
  import eslint from "vite-plugin-eslint";
  // https://vitejs.dev/config/
  export default defineConfig({
    plugins: [react(), eslint()],
  });
  ```

- Start: `npm run dev`

JSON-Server start: `here`
