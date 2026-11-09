---
title: TypeScript Basics and Must-Knows
category: Web
description: TypeScript is a statically typed superset of JavaScript that compiles
  to plain JavaScript. It adds optional static typing to the language, which can help
  catch errors early and make development more e
tags:
- web
---

<!-- imported from ObsidianVault/webdev/TypeScript.md. Edit the source, then run sync.py. -->

# TypeScript Basics and Must-Knows

`web`

## Introduction to TypeScript

TypeScript is a statically typed superset of JavaScript that compiles to plain JavaScript. It adds optional static typing to the language, which can help catch errors early and make development more efficient.

## Setting Up TypeScript

### Installation

To use TypeScript, you need to have Node.js installed. Then you can install TypeScript via npm:

```bash
npm install -g typescript
```

### Compiling TypeScript

To compile a TypeScript file, use the `tsc` command:

```bash
tsc filename.ts
```

This will generate a `filename.js` file that you can run with Node.js or include in your web application.

## Basic Types

TypeScript provides several basic types that are similar to those in JavaScript:

### Boolean

```typescript
let isDone: boolean = true;
```

### Number

```typescript
let decimal: number = 6;
let hex: number = 0xf00d;
let binary: number = 0b1010;
let octal: number = 0o744;
```

### String

```typescript
let color: string = "blue";
color = "red";
```

### Array

```typescript
let list: number[] = [1, 2, 3];
let list: Array<number> = [1, 2, 3];
```

### Tuple

```typescript
let x: [string, number];
x = ["hello", 10];
```

### Enum

```typescript
enum Color {
  Red,
  Green,
  Blue,
}
let c: Color = Color.Green;
```

### Any

```typescript
let notSure: any = 4;
notSure = "maybe a string instead";
notSure = false;
```

### Void

```typescript
function warnUser(): void {
  console.log("This is my warning message");
}
```

## Functions

### Function Types

Functions can be typed by defining the parameter and return types:

```typescript
function add(x: number, y: number): number {
  return x + y;
}

let myAdd: (x: number, y: number) => number = function (
  x: number,
  y: number
): number {
  return x + y;
};
```

### Optional and Default Parameters

Parameters can be optional or have default values:

```typescript
function buildName(firstName: string, lastName?: string): string {
  if (lastName) {
    return firstName + " " + lastName;
  } else {
    return firstName;
  }
}

let result1 = buildName("Bob"); // OK
let result2 = buildName("Bob", "Adams"); // OK
```

## Interfaces

Interfaces define the shape of objects:

```typescript
interface Person {
  firstName: string;
  lastName: string;
}

function greet(person: Person) {
  return "Hello, " + person.firstName + " " + person.lastName;
}

let user = { firstName: "John", lastName: "Doe" };

console.log(greet(user));
```

## Classes

Classes in TypeScript are similar to those in JavaScript but with added TypeScript features:

```typescript
class Greeter {
  greeting: string;
  constructor(message: string) {
    this.greeting = message;
  }
  greet() {
    return "Hello, " + this.greeting;
  }
}

let greeter = new Greeter("world");
console.log(greeter.greet());
```

### Inheritance

Classes can inherit from other classes:

```typescript
class Animal {
  name: string;
  constructor(theName: string) {
    this.name = theName;
  }
  move(distanceInMeters: number = 0) {
    console.log(`${this.name} moved ${distanceInMeters}m.`);
  }
}

class Dog extends Animal {
  bark() {
    console.log("Woof! Woof!");
  }
}

const dog = new Dog("Rex");
dog.bark();
dog.move(10);
```

## Generics

Generics allow for the creation of components that work with a variety of types:

```typescript
function identity<T>(arg: T): T {
  return arg;
}

let output1 = identity<string>("myString"); // type of output will be 'string'
let output2 = identity<number>(42); // type of output will be 'number'
```

## Modules

Modules in TypeScript allow for code organization and encapsulation. They can be imported and exported:

### Exporting

```typescript
export interface StringValidator {
  isAcceptable(s: string): boolean;
}

export class LettersOnlyValidator implements StringValidator {
  isAcceptable(s: string) {
    return /^[A-Za-z]+$/.test(s);
  }
}
```

### Importing

```typescript
import { StringValidator, LettersOnlyValidator } from "./validators";

let validator = new LettersOnlyValidator();
console.log(validator.isAcceptable("Hello")); // true
console.log(validator.isAcceptable("12345")); // false
```

## Type Inference

TypeScript can infer types when they are not explicitly provided:

```typescript
let x = 3; // inferred to be 'number'
let y = [0, 1, null]; // inferred to be '(number | null)[]
```
