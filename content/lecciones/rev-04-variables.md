# Variables: boxes with names

## Remembering values

Programs need to **remember** things: a name, a score, a price. To remember a value, we put it in a **variable**.

Think of a variable as a **box with a label**. The label is the name of the variable. Inside the box is a value.

```python
name = "Valentina"
age = 14
```

After these two lines, there is a box called `name` with `"Valentina"` inside, and a box called `age` with `14` inside.

## = means "put in the box"

In maths, `=` means "is equal to". **In Python, `=` means: work out the right side, then put the result in the box on the left.**

```python
total = 3 + 4
```

Python works out `3 + 4`, which is 7, then puts `7` in the box `total`.

The box name always goes on the **left**. `3 + 4 = total` is an error.

## Using a variable

To use the value in the box, write the name **without quotes**:

```python
city = "Bogota"
print(city)
print("city")
```

Predict both lines, and rate your confidence.

<details>
<summary>Check your prediction</summary>

```text
Bogota
city
```

`city` without quotes means: *the value in the box called city*. `"city"` with quotes is just the text c-i-t-y.

</details>

Variables can be used in calculations:

```python
price = 3500
quantity = 4
total = price * quantity
print("Total:", total)
```

```text
Total: 14000
```

## Names for variables

Rules (if you break them, you get an error):

- Use letters, numbers and the underscore `_`.
- No spaces: use `final_grade`, not `final grade`.
- Don't start with a number: `grade2` works, `2grade` doesn't.
- Capital letters matter: `Score` and `score` are **two different** variables.

Good habits:

- Use names that say what is inside: `price` is better than `p` or `x`.
- Use small letters, and join words with `_`: `number_of_goals`.
- Avoid accents and ñ: `year`, not `año`. They work in Python 3, but they cause problems on some keyboards.

## Changing a variable

You can put a new value in a box. **The old value is gone.**

```python
score = 10
score = 25
print(score)
```

<details>
<summary>What does it show?</summary>

`25`. The second line **replaces** the 10.

</details>

Now a tricky one. Predict, and rate your confidence:

```python
a = 5
b = a
a = 10
print(b)
```

<details>
<summary>Check your prediction</summary>

`5`.

Line 2 copies the **value** of `a` (which is 5 at that moment) into `b`. When line 3 changes `a`, the box `b` doesn't change. Each box has its own value.

</details>

## Adding to a variable

This line looks impossible in maths class:

```python
score = score + 10
```

But remember: **first the right side, then the box on the left**. Step by step, if `score` is 5:

1. Python takes the value in the box: `5`.
2. It works out `5 + 10`, which is `15`.
3. It puts `15` in the box `score`.

So this line means: **"add 10 to the score"**.

There is a short way to write it, and you will see it a lot:

```python
score += 10     # the same as: score = score + 10
lives -= 1      # the same as: lives = lives - 1
```

## Tracing: following the values

To understand a program, **trace** it: follow the value of each variable, one line at a time. A table helps:

```python
coins = 3
coins = coins + 4
coins += 1
coins = coins * 2
print(coins)
```

| Line | coins |
|---|---|
| 1 | 3 |
| 2 | ? |
| 3 | ? |
| 4 | ? |

Fill in the table in your log before you check.

<details>
<summary>Check your trace</summary>

| Line | coins |
|---|---|
| 1 | 3 |
| 2 | 7 |
| 3 | 8 |
| 4 | 16 |

The program shows `16`.

</details>

## Using a variable before it exists

```python
print(points)
points = 50
```

<details>
<summary>What happens?</summary>

An error: `NameError: name 'points' is not defined`. Python runs from top to bottom. On line 1, the box `points` doesn't exist yet. **Create a variable before you use it.**

</details>

## Summary

- A variable is a box with a name and a value.
- `=` means: work out the right side, then put it in the box on the left.
- Use the name without quotes to get the value.
- A new value replaces the old one.
- `score = score + 10` (or `score += 10`) adds 10 to the score.
- Trace a program with a table: one row per line, one column per variable.
