# Numbers and maths

## Two kinds of numbers

Python has two kinds of numbers:

| Kind | Python name | Examples |
|---|---|---|
| Whole numbers | `int` (integer) | `7`, `0`, `-15`, `2026` |
| Decimal numbers | `float` | `2.5`, `-0.75`, `3.0` |

**Important for Colombia:** in Python, decimals always use a **point**, never a comma: `2.5`, not `2,5`.

And big numbers are written **without** separators: `1000000`, not `1.000.000` or `1,000,000`. To Python, a comma separates **different values**, so `print(1,000)` shows `1 0`!

## The operators

| Operation | Symbol | Example | Result |
|---|---|---|---|
| Addition | `+` | `7 + 5` | `12` |
| Subtraction | `-` | `7 - 10` | `-3` |
| Multiplication | `*` | `4 * 6` | `24` |
| Division | `/` | `15 / 2` | `7.5` |

Multiplication uses `*` (a star), not `x`.

## Division always gives a decimal

Predict, and rate your confidence:

```python
print(10 / 2)
```

<details>
<summary>Check your prediction</summary>

```text
5.0
```

Division with `/` **always** gives a `float`, even when the answer is a whole number. `5.0` and `5` have the same value, but Python shows them differently.

</details>

## Order of operations

Python follows the same rules as maths class: **multiplication and division first**, then addition and subtraction. **Brackets** change the order.

Predict both lines:

```python
print(2 + 3 * 4)
print((2 + 3) * 4)
```

<details>
<summary>Check your prediction</summary>

```text
14
20
```

In the first line, Python does `3 * 4 = 12` first, then `2 + 12 = 14`. In the second line, the brackets go first: `2 + 3 = 5`, then `5 * 4 = 20`.

</details>

A classic mistake: the average of 8, 6 and 7.

```python
print(8 + 6 + 7 / 3)
print((8 + 6 + 7) / 3)
```

<details>
<summary>Which one is the average?</summary>

The second one: `7.0`. The first one divides **only** the 7 by 3, then adds 8 and 6, which gives `16.333333333333332`.

When you are not sure about the order, **use brackets**. They make your intention clear.

</details>

## Strange decimals

Predict:

```python
print(0.1 + 0.2)
```

<details>
<summary>Check your prediction</summary>

```text
0.30000000000000004
```

This is not a mistake in your code. Computers store decimals in a way that is sometimes a tiny bit inexact. For our programs, this almost never matters. But now you won't be surprised when you see it.

</details>

## Negative numbers

A minus sign before a number makes it negative: `-5`. You can do maths with negative numbers too:

```python
print(-3 + 10)     # 7
print(-2 * -4)     # 8
```

## Summary

- `int` is a whole number, `float` is a decimal number.
- Decimals use a point: `2.5`. Big numbers have no separators: `1000000`.
- The operators are `+`, `-`, `*` and `/`.
- `/` always gives a decimal.
- Multiplication and division go first. Use brackets to change the order.
