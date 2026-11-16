# How can a program tell a number from text?

**This week's question:** In week 12, some games crashed when a player typed `abc`. How can a program protect itself from unexpected input?

## After the assessment: your exam wrapper

Look at your returned assessment. Label each lost mark **didn't know**, **misread** or **rushed**, and write one plan for each label. Compare your week 14 and week 19 "I can" ratings: what changed, and what is your evidence?

## Predict: which ones crash?

These are real inputs that crashed games in week 12. Predict which lines crash. Rate your confidence.

```python
int("42")
int(" 42")
int("7.5")
int("")
int("abc")
```

<details>
<summary>Check your prediction</summary>

| Code | Result |
|---|---|
| `int("42")` | `42` |
| `int(" 42")` | `42` (spaces around the number are allowed) |
| `int("7.5")` | crash: `ValueError` |
| `int("")` | crash: `ValueError` |
| `int("abc")` | crash: `ValueError` |

</details>

## Tool card 1: isdigit()

`text.isdigit()` returns `True` if **every** character in the text is a digit (0–9).

In the **Week 20 lab**, build a table. Predict first!

| Text | `.isdigit()` |
|---|---|
| `"42"` | |
| `"abc"` | |
| `"-3"` | |
| `""` | |
| `"7.5"` | |
| `" 42"` | |

<details>
<summary>Check your table</summary>

| Text | `.isdigit()` |
|---|---|
| `"42"` | `True` |
| `"abc"` | `False` |
| `"-3"` | `False`, because `-` is not a digit! |
| `""` | `False` |
| `"7.5"` | `False` |
| `" 42"` | `False`, because a space is not a digit |

So `isdigit()` says no to negative numbers, even though `int("-3")` works.

</details>

## Tool card 2: try / except

```python
text = input("A whole number: ")
try:
    n = int(text)
    print("Thanks:", n)
except ValueError:
    print("Not a whole number")
```

Python **tries** the code. If `int()` fails with a `ValueError`, it jumps to `except` instead of crashing.

**Investigate:** which inputs does each approach accept? Find an input where `isdigit()` and `try`/`except` **disagree**.

<details>
<summary>Check: where do they disagree?</summary>

- `"-3"`: `isdigit()` says no, but `int()` works.
- `" 42"`: `isdigit()` says no, but `int()` works.

Use `isdigit()` when only positive whole numbers make sense (like an age or a guess from 1 to 100). Use `try`/`except` when negative numbers are fine, or when you want Python itself to decide.

</details>

## Make: an "unbreakable" input

Keep asking until the user types a whole number from 1 to 100. Plan **at least 5 attack inputs** first. This is the exercise **Unbreakable input** in this unit.

Extension: add the validation to your own Guess the Number game.

## Before you leave

Complete these in your log:

1. `isdigit` is enough when ___.
2. `try`/`except` is better when ___.
