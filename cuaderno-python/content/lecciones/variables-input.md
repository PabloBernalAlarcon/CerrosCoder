# Variables and questions with `input()`

A **variable** is like a labeled box where we keep a value so we can use it later.

```python
name = "Valentina"
age = 14
print(name, "is", age, "years old")
```

The `=` sign doesn't mean "equals" like in math class. It means **put this value in the box**.

## Rules for names

Variable names are written in lowercase, with no spaces, and they can't start with a number. If you need several words, join them with an underscore: `final_grade`, `number_of_goals`.

## Asking the user

`input()` asks a question and waits for the person to type something:

```python
city = input("Which city do you live in? ")
print("Nice!", city, "is a great city.")
```

On this platform, what the user "types" goes in the **Inputs for input()** box, one answer per line.

## Mixing text and variables with f-strings

If you put an `f` before the quotes, you can place variables inside curly braces `{ }`:

```python
name = "Samuel"
print(f"Hello, {name}. Welcome.")
```

## Careful! `input()` always gives you text

Even if you type a number, `input()` hands it to you as text. To do math, convert it with `int()` (whole numbers) or `float()` (numbers with decimals):

```python
goals = int(input("How many goals did your team score? "))
print(f"Double would be {goals * 2} goals")
```

> If you forget `int()`, `"3" + "4"` gives `"34"`: Python glues the texts together instead of adding them.
