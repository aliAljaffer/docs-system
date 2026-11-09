---
title: TailwindCSS Basics and Must-Knows
category: Web
description: TailwindCSS is a utility-first CSS framework that allows you to build
  custom designs directly in your HTML. It provides low-level utility classes that
  let you create complex designs without ever leavi
tags:
- web
---

<!-- imported from ObsidianVault/webdev/TailwindCSS.md. Edit the source, then run sync.py. -->

# TailwindCSS Basics and Must-Knows

`web`

## Introduction to TailwindCSS

TailwindCSS is a utility-first CSS framework that allows you to build custom designs directly in your HTML. It provides low-level utility classes that let you create complex designs without ever leaving your markup.

## Setting Up TailwindCSS

### Installation

You can install TailwindCSS using npm. First, ensure you have Node.js and npm installed, then run the following command:

```bash
npm install tailwindcss
```

### Initializing TailwindCSS

Create a configuration file to customize Tailwind's default settings:

```bash
npx tailwindcss init
```

This will generate a `tailwind.config.js` file in your project.

### Including TailwindCSS in Your CSS

Create a CSS file (e.g., `styles.css`) and include Tailwind's directives:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Then, build your CSS using the Tailwind CLI:

```bash
npx tailwindcss -i ./src/styles.css -o ./dist/output.css --watch
```

Replace `./src/styles.css` with the path to your input CSS file and `./dist/output.css` with the desired output path.

## Basic Usage

TailwindCSS is used by applying utility classes directly to HTML elements. These classes follow a convention that makes them easy to understand and apply.

### Container

The `container` class centers your content and applies automatic padding:

```html
<div class="container mx-auto">
  <!-- Your content -->
</div>
```

### Margin and Padding

Use margin (`m`) and padding (`p`) classes to control spacing:

```html
<div class="mt-4 mb-2 px-6 py-3">
  <!-- Your content -->
</div>
```

### Flexbox

TailwindCSS provides a set of classes for working with flexbox:

```html
<div class="flex justify-center items-center">
  <div class="flex-1">Item 1</div>
  <div class="flex-1">Item 2</div>
</div>
```

### Grid

TailwindCSS also includes grid utilities:

```html
<div class="grid grid-cols-3 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

### Typography

TailwindCSS includes a range of typography utilities:

```html
<h1 class="text-3xl font-bold">Hello, world!</h1>
<p class="text-gray-700">This is a paragraph.</p>
```

### Backgrounds

Apply background colors and images with ease:

```html
<div class="bg-blue-500 text-white p-4">This is a blue background.</div>
```

### Borders

Control borders with Tailwind's border utilities:

```html
<div class="border border-gray-300 rounded-lg p-4">This is a bordered box.</div>
```

### Responsive Design

TailwindCSS makes it easy to create responsive designs using breakpoints:

```html
<div class="p-4 md:p-8 lg:p-12">
  This padding changes at different screen sizes.
</div>
```

### Hover, Focus, and Other States

Apply styles based on different states like hover, focus, etc.:

```html
<button
  class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
>
  Hover me
</button>
```

### Customizing TailwindCSS

You can customize TailwindCSS by modifying the `tailwind.config.js` file. This allows you to add custom colors, spacing values, and more:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: "#ff6363",
        secondary: "#ffa600",
      },
      spacing: {
        72: "18rem",
        84: "21rem",
        96: "24rem",
      },
    },
  },
  variants: {},
  plugins: [],
};
```

### Plugins

TailwindCSS supports plugins to add additional utilities or components. For example, you can use the `@tailwindcss/forms` plugin to style form elements:

```bash
npm install @tailwindcss/forms
```

Add the plugin to your `tailwind.config.js`:

```javascript
module.exports = {
  // ...
  plugins: [require("@tailwindcss/forms")],
};
```

# TailwindCSS Cheatsheet

## Getting Started

### Installation

```bash
npm install tailwindcss
npx tailwindcss init
```

### Including Tailwind in Your CSS

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Build Tailwind CSS

```bash
npx tailwindcss -i ./src/styles.css -o ./dist/output.css --watch
```

## Layout

### Container

```html
<div class="container mx-auto">
  <!-- Content -->
</div>
```

### Padding and Margin

```html
<div class="p-4 m-4">
  <!-- Content -->
</div>
```

### Flexbox

```html
<div class="flex justify-center items-center">
  <div class="flex-1">Item 1</div>
  <div class="flex-1">Item 2</div>
</div>
```

### Grid

```html
<div class="grid grid-cols-3 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

## Typography

### Text Size and Color

```html
<h1 class="text-3xl text-gray-700">Hello, world!</h1>
<p class="text-base text-gray-500">This is a paragraph.</p>
```

### Font Weight

```html
<p class="font-bold">Bold text</p>
<p class="font-light">Light text</p>
```

### Text Alignment

```html
<p class="text-left">Left aligned</p>
<p class="text-center">Center aligned</p>
<p class="text-right">Right aligned</p>
```

## Backgrounds

### Background Color

```html
<div class="bg-blue-500 text-white p-4">Blue background</div>
```

### Background Image

```html
<div
  class="bg-cover bg-center h-64"
  style="background-image: url('path/to/image.jpg');"
>
  <!-- Content -->
</div>
```

## Borders

### Border Width and Color

```html
<div class="border-4 border-red-500 p-4">Red border</div>
```

### Border Radius

```html
<div class="rounded-lg p-4">Rounded corners</div>
```

## Effects

### Shadow

```html
<div class="shadow-lg p-4">Large shadow</div>
```

### Opacity

```html
<div class="opacity-50">50% opacity</div>
```

## Sizing

### Width and Height

```html
<div class="w-1/2 h-64">Half width, fixed height</div>
```

### Max-Width and Max-Height

```html
<div class="max-w-sm max-h-screen">Maximum width and height</div>
```

## Responsive Design

### Breakpoints

```html
<div class="p-4 sm:p-8 md:p-12 lg:p-16 xl:p-20">Responsive padding</div>
```

### Hide and Show

```html
<div class="hidden md:block">Visible on medium and larger screens</div>
```

## Interactivity

### Hover, Focus, and Active

```html
<button
  class="bg-blue-500 hover:bg-blue-700 focus:bg-blue-900 active:bg-blue-600 text-white font-bold py-2 px-4 rounded"
>
  Interactive button
</button>
```

## Grid Template Columns

```html
<div class="grid grid-cols-3 gap-4">
  <div>1</div>
  <div>2</div>
  <div>3</div>
</div>
```

## Flexbox Utilities

### Flex Direction

```html
<div class="flex flex-row">
  <div>Row Item 1</div>
  <div>Row Item 2</div>
</div>

<div class="flex flex-col">
  <div>Column Item 1</div>
  <div>Column Item 2</div>
</div>
```

### Flex Wrap

```html
<div class="flex flex-wrap">
  <div class="w-1/3">Item 1</div>
  <div class="w-1/3">Item 2</div>
  <div class="w-1/3">Item 3</div>
</div>
```

### Justify Content

```html
<div class="flex justify-between">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

### Align Items

```html
<div class="flex items-center">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

## Customizing Tailwind

### Extending the Configuration

Modify the `tailwind.config.js` file:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: "#ff6363",
        secondary: "#ffa600",
      },
      spacing: {
        72: "18rem",
        84: "21rem",
        96: "24rem",
      },
    },
  },
  variants: {},
  plugins: [],
};
```

## Plugins

### Adding Plugins

Install and use plugins like `@tailwindcss/forms`:

```bash
npm install @tailwindcss/forms
```

```javascript
module.exports = {
  plugins: [require("@tailwindcss/forms")],
};
```
