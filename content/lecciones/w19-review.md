# Getting ready: read, predict, fix

This week's assessment has three parts:

1. **Predict** the output of short programs, with a confidence rating. (The confidence is never graded.)
2. **Find and fix** a bug in short programs. Each one has one bug.
3. **Write** a small function from a description.

It covers conditions, `and`/`or`/`not`, loops and functions.

## Your "I can" statements

Before the assessment, rate these again from 1 to 4, as you did in week 14. For each rating, write **evidence**: a line of code that proves it.

- I can predict which branch of an `if`/`elif`/`else` chain runs.
- I can combine conditions with `and`, `or` and `not`.
- I can trace a loop and say how many times it runs.
- I can find a bug using the output and a trace table.
- I can write a function with parameters that returns a value.

## Practice: predict

**1.**

```python
def mystery(n):
    if n > 10 and n < 20:
        return "teen number"
    elif n > 10:
        return "big"
    return "small"

print(mystery(12))
print(mystery(25))
print(mystery(4))
```

<details>
<summary>Check</summary>

```text
teen number
big
small
```

The last `return "small"` is reached only when neither condition returned first.

</details>

**2.**

```python
def show(x):
    print(x + 1)

y = show(4)
print(y)
```

<details>
<summary>Check</summary>

```text
5
None
```

`show` prints, but returns nothing.

</details>

**3.** How many stars?

```python
count = 0
for i in range(3):
    for j in range(2):
        count = count + 1
print("*" * count)
```

<details>
<summary>Check</summary>

`******` (6 stars). The inner loop runs 2 times for each of the 3 outer rounds.

</details>

## Practice: find and fix

The exercises in this unit are practice for the "find and fix" and "write" parts.
