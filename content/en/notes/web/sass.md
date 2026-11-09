---
title: SASS and SCSS Basics and Must-Knows
category: Web
description: SASS (Syntactically Awesome Style Sheets) is a CSS preprocessor that
  adds powerful features such as variables, nested rules, mixins, and more, making
  CSS more maintainable and easier to write. SCSS (S
tags:
- web
---

<!-- imported from ObsidianVault/webdev/SASS.md. Edit the source, then run sync.py. -->

# SASS and SCSS Basics and Must-Knows

`web`

## Introduction to SASS and SCSS

SASS (Syntactically Awesome Style Sheets) is a CSS preprocessor that adds powerful features such as variables, nested rules, mixins, and more, making CSS more maintainable and easier to write. SCSS (Sassy CSS) is a syntax of SASS that's fully compatible with CSS, making it easier to integrate into existing projects.

## Setting Up SASS/SCSS

### Installation

To use SASS/SCSS, you need to have Node.js installed. Then you can install SASS via npm:

```bash
npm install -g sass
```

### Compiling SASS/SCSS

To compile a SASS/SCSS file, use the `sass` command:

```bash
sass input.scss output.css
```

This will generate a `output.css` file that you can include in your project.

## Basic Syntax

### SCSS vs. SASS

SCSS uses a syntax similar to CSS:

```scss
// SCSS Syntax
$primary-color: #333;

body {
  color: $primary-color;
}
```

SASS uses an indented syntax, without semicolons and curly braces:

```sass
// SASS Syntax
$primary-color: #333

body
  color: $primary-color
```

For simplicity, this guide will use SCSS syntax.

## Variables

Variables store values that can be reused throughout your stylesheet:

```scss
$primary-color: #333;
$font-stack: Helvetica, sans-serif;

body {
  font: 100% $font-stack;
  color: $primary-color;
}
```

## Nesting

Nesting allows you to nest your CSS selectors in a way that follows the same visual hierarchy of your HTML:

```scss
nav {
  ul {
    margin: 0;
    padding: 0;
    list-style: none;
  }

  li {
    display: inline-block;
  }

  a {
    text-decoration: none;
  }
}
```

## Partials and Imports

Partials help you modularize your CSS. A partial is a SCSS file named with a leading underscore (e.g., `_partial.scss`). You can then import it into other SCSS files:

```scss
// _partial.scss
$primary-color: #333;

body {
  color: $primary-color;
}

// styles.scss
@import "partial";
```

## Mixins

Mixins allow you to create reusable chunks of code:

```scss
@mixin border-radius($radius) {
  -webkit-border-radius: $radius;
  -moz-border-radius: $radius;
  -ms-border-radius: $radius;
  border-radius: $radius;
}

.box {
  @include border-radius(10px);
}
```

## Extend/Inheritance

The `@extend` directive lets you share a set of CSS properties from one selector to another:

```scss
%message-shared {
  border: 1px solid #ccc;
  padding: 10px;
  color: #333;
}

.message {
  @extend %message-shared;
}

.success {
  @extend %message-shared;
  border-color: green;
}

.error {
  @extend %message-shared;
  border-color: red;
}
```

## Functions

SASS allows you to define your own functions, which can then be used to compute values:

```scss
@function calculate-em($size, $base) {
  @return $size / $base * 1em;
}

body {
  font-size: calculate-em(14px, 16px);
}
```

## Control Directives

SASS supports control directives like `@if`, `@for`, `@each`, and `@while` for logic and loops:

### If

```scss
$theme: dark;

body {
  @if $theme == dark {
    background-color: #333;
    color: white;
  } @else {
    background-color: white;
    color: #333;
  }
}
```

### For

```scss
@for $i from 1 through 3 {
  .item-#{$i} {
    width: 2em * $i;
  }
}
```

### Each

```scss
@each $animal in puma, sea-slug, egret, salamander {
  .#{$animal}-icon {
    background-image: url("/images/#{$animal}.png");
  }
}
```

### While

```scss
$i: 6;

@while $i > 0 {
  .item-#{$i} {
    width: 2em * $i;
  }
  $i: $i - 1;
}
```

# SASS Cheatsheet

## Getting Started

### Installation

To install SASS via npm:

```bash
npm install -g sass
```

### Compiling SASS/SCSS

To compile a SASS/SCSS file to CSS:

```bash
sass input.scss output.css
```

## Syntax

### SCSS vs. SASS

#### SCSS Syntax (uses braces and semicolons):

```scss
$primary-color: #333;

body {
  color: $primary-color;
}
```

#### SASS Syntax (uses indentation):

```sass
$primary-color: #333

body
  color: $primary-color
```

## Variables

```scss
$primary-color: #333;
$font-stack: Helvetica, sans-serif;

body {
  font: 100% $font-stack;
  color: $primary-color;
}
```

## Nesting

```scss
nav {
  ul {
    margin: 0;
    padding: 0;
    list-style: none;
  }

  li {
    display: inline-block;
  }

  a {
    text-decoration: none;
  }
}
```

## Partials and Imports

### Partial (e.g., `_partial.scss`):

```scss
$primary-color: #333;

body {
  color: $primary-color;
}
```

### Importing a partial:

```scss
@import "partial";
```

## Mixins

```scss
@mixin border-radius($radius) {
  -webkit-border-radius: $radius;
  -moz-border-radius: $radius;
  -ms-border-radius: $radius;
  border-radius: $radius;
}

.box {
  @include border-radius(10px);
}
```

## Extend/Inheritance

```scss
%message-shared {
  border: 1px solid #ccc;
  padding: 10px;
  color: #333;
}

.message {
  @extend %message-shared;
}

.success {
  @extend %message-shared;
  border-color: green;
}

.error {
  @extend %message-shared;
  border-color: red;
}
```

## Functions

```scss
@function calculate-em($size, $base) {
  @return $size / $base * 1em;
}

body {
  font-size: calculate-em(14px, 16px);
}
```

## Control Directives

### If

```scss
$theme: dark;

body {
  @if $theme == dark {
    background-color: #333;
    color: white;
  } @else {
    background-color: white;
    color: #333;
  }
}
```

### For

```scss
@for $i from 1 through 3 {
  .item-#{$i} {
    width: 2em * $i;
  }
}
```

### Each

```scss
@each $animal in puma, sea-slug, egret, salamander {
  .#{$animal}-icon {
    background-image: url("/images/#{$animal}.png");
  }
}
```

### While

```scss
$i: 6;

@while $i > 0 {
  .item-#{$i} {
    width: 2em * $i;
  }
  $i: $i - 1;
}
```

## Placeholder Selectors

```scss
%button-style {
  padding: 10px 20px;
  border-radius: 5px;
  background-color: blue;
  color: white;
}

.button {
  @extend %button-style;
  font-size: 16px;
}

.small-button {
  @extend %button-style;
  font-size: 12px;
}
```

## Nested Properties

```scss
nav {
  border: {
    style: solid;
    width: 1px;
    color: #ccc;
  }
}
```
