# Talking to the computer: `print()`

A **program** is a list of instructions that the computer follows in order, from top to bottom. The first instruction we'll learn is `print()`, which shows something on the screen.

```python
print("Hello, world!")
print("I'm learning Python")
```

Text goes between **quotes**. For Python, anything between quotes is *text* (programmers call it a *string*).

## Numbers and math

Numbers go **without** quotes, and Python can do math:

```python
print(7 + 5)      # addition: 12
print(10 - 3)     # subtraction: 7
print(4 * 6)      # multiplication: 24
print(15 / 2)     # division: 7.5
```

Notice the difference: `print("7 + 5")` shows the text `7 + 5`, but `print(7 + 5)` shows `12`.

## Several things at once

If you separate things with commas, `print()` shows them on the same line with a space in between:

```python
print("I am", 14, "years old")
```

## Comments

Anything you write after `#` is a **comment**: Python ignores it. Comments are notes for you or for other people reading your code.

> **Common mistakes:** forgetting to close the quotes or the parenthesis, and writing `Print` with a capital P. Python cares about capital and lowercase letters.
