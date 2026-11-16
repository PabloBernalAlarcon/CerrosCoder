# Questions with True or False

## Programs that ask questions

Programs often need to ask yes/no questions: *Is the password correct? Is the grade 4.5 or more?*

In Python, these questions are **comparisons**, and the answer is always `True` or `False`.

```python
print(7 > 3)
```

```text
True
```

## The comparison operators

| Symbol | Question | Example | Result |
|---|---|---|---|
| `==` | Are they equal? | `5 == 5` | `True` |
| `!=` | Are they different? | `5 != 5` | `False` |
| `>` | Is it bigger? | `7 > 3` | `True` |
| `<` | Is it smaller? | `7 < 3` | `False` |
| `>=` | Is it bigger or equal? | `4.5 >= 4.5` | `True` |
| `<=` | Is it smaller or equal? | `3 <= 2` | `False` |

## = and == are different!

This is the most common mistake in this topic:

- `=` **puts a value in a box**: `age = 14`.
- `==` **asks a question**: `age == 14` means "is age equal to 14?"

```python
age = 14
print(age == 14)
print(age == 15)
```

<details>
<summary>What does it show?</summary>

```text
True
False
```

</details>

## The answer can go in a variable

A comparison gives a value, `True` or `False`, so you can store it:

```python
grade = 5.2
passed = grade >= 4.5
print("Passed:", passed)
```

```text
Passed: True
```

## Boundaries

Predict each line, and rate your confidence:

```python
print(18 > 18)
print(18 >= 18)
print(4.4 >= 4.5)
```

<details>
<summary>Check your prediction</summary>

```text
False
True
False
```

`>` does **not** include the number itself; `>=` does. "18 or older" is `age >= 18`. Many bugs hide exactly on the boundary, so always test the boundary numbers.

</details>

## Comparing text

Text comparisons are **exact**: every character must match, including **capital letters** and **spaces**.

Predict each line:

```python
print("AU" == "AU")
print("AU" == "au")
print("AU" == "AU ")
print("Bogota" != "Medellin")
```

<details>
<summary>Check your prediction</summary>

```text
True
False
False
True
```

`"AU"` and `"au"` are different (capital letters). `"AU"` and `"AU "` are different too: the second one has a space at the end.

</details>

## Text and numbers are never equal

Predict:

```python
print("7" == 7)
```

<details>
<summary>Check your prediction</summary>

`False`. Text is never equal to a number, even when it looks the same.

This matters with `input()`, which always gives text:

```python
answer = input("What is 3 + 4? ")
print(answer == 7)
```

Even if the user types `7`, this shows `False`! Two ways to fix it:

- Compare text with text: `answer == "7"`.
- Or convert first: `int(answer) == 7`.

</details>

## Why this matters for week 7

In week 7, programs use these True/False questions to **decide** which lines to run:

```python
if answer == "AU":
    print("Correct!")
```

The line `print("Correct!")` runs **only** when the question `answer == "AU"` is `True`. If you can predict `True` or `False` for any comparison, you are ready for week 7.

## Summary

- Comparisons ask questions: `==`, `!=`, `>`, `<`, `>=`, `<=`.
- The answer is always `True` or `False`.
- `=` stores a value; `==` compares.
- `>=` includes the boundary; `>` doesn't.
- Text comparisons are exact: capital letters and spaces matter.
- Text and numbers are never equal: `"7" == 7` is `False`.
