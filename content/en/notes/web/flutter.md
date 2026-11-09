---
title: Flutter
category: Web
description: Models = Objects, Data models
tags:
- web
---

<!-- imported from ObsidianVault/webdev/Flutter.md. Edit the source, then run sync.py. -->

# Flutter

`web`

## Basics (Always keep in mind)

```dart
const // -> compile-time known value
final // -> run-time computed value
var // non-specific type. Will be inferred.
```

### Boilerplate

```dart
import `package:flutter/material.dart`
void main(){
  runApp(MyWidget()); // MyWidget is the root of the Widget tree
}
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext build){
    return const MaterialApp(
      home: someWidget; // TODO: Scaffold() ? Google it
    );
  }
}
```

- Use `const` when creating new objects in order to cache the object

- Comma (`,`) before closing parens to help see nesting.

- Adding Images: Add to `assets/images/` (optional) then edit `pub.yaml` to add the assets under `assets:`

## Common Widgets

- `Column()` and `Row()` for flex-directions. `children` property takes an array of Widgets. Inside, `mainAxisSize: MainAxisSize.min` to horizontally center.

- `SizedBox()` for margins/empty spaces. Must set `height`

- `Center()` for centering

- Buttons:

  - `TextButton()` (Pressable Text)
  - `ElevatedButton()` (BG and Shadow)
  - `OutlinedButton()` (No BG, but has Border).
  - For style, use `(___)Button().styleFrom(styleParamsHere)`.
  - Button with an icon is constructed using `OutlineButton.icon()` and has `label` property for inline text.

- Changing opacity: `Opacity()` but is resource-expensive.
  - Instead set `Image()` color to `Color.fromARGB()` and change the gamma.

## State Create/Set Structure for StatefulWidget

```dart
class MyState extends StatefulWidget{
    const MyState({super.key});s
    @override
    State<MyState> createState(){
        return _MyState();
    }
}

class _MyState extends State<MyState>{
    ...
    var state_value = 0;
    void onClick(){
        setState((){
            ...
            state_value = state_value + 1
        });
    }
    @override
    Widget build(BuildContext context){
        return Object(
            ...
            state_value
        )
    }
}
```

## Passing args to Widgets

```dart
class GradientContainer extends StatelessWidget {
  final List<Color> customColors; // The param to accept
  const GradientContainer({super.key, required this.customColors}); // Optionally make it required.

  @override
  void initState() {
    activeScreen = QuizHomepage(switchScreen);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: customColors,
        ),
      ),
    );
  }
}
```

## Stateful

- `initState()` is executed by Flutter when the widget State object is initialized

- `build()` executed when the Widget is built the first time and after every `setState()` call

- `dispose()` executed just before the Widget gets deleted.

- In the state class, you can use the `widget` class field to access Class fields

## Misc

Models = Objects, Data models

Spread `...` with map!

`Expanded` widget allows it's child to take space... basically wrap

## Fonts

- Google fonts plugin: `flutter pub add google_fonts` then import

````dart
Text(
  'This is Google Fonts',
  style: GoogleFonts.lato(
    textStyle: Theme.of(context).textTheme.displayLarge,
    fontSize: 48,
    fontWeight: FontWeight.w700,
    fontStyle: FontStyle.italic,
  ),
),
````
