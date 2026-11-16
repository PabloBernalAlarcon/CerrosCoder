# What does range() actually produce?

**This week's question:** `range()` makes a sequence of numbers. Can you predict it **before** you print it?

## Warm-up: trace a countdown

Predict the output. Rate your confidence.

```python
n = 3
while n > 0:
    print(n)
    n = n - 1
print("Liftoff!")
```

<details>
<summary>Check your prediction</summary>

```text
3
2
1
Liftoff!
```

</details>

## Two loops, side by side

Read both. Is the output the same? What does the `for` loop **not** need?

```python
# while loop (week 9)
count = 1
while count <= 3:
    print("Round", count)
    count = count + 1
```

```python
# for loop
for i in range(1, 4):
    print("Round", i)
```

<details>
<summary>Check your thinking</summary>

Both print `Round 1`, `Round 2`, `Round 3`.

The `for` loop does not need `count = 1` before the loop, and it does not need `count = count + 1` inside it. `range(1, 4)` gives `i` the values 1, 2, 3, one at a time.

</details>

## Predict the ranges

For each one, write the numbers you expect. Rate your confidence. Then check in the **Week 10 lab** with:

```python
for i in range(5):
    print(i)
```

1. `range(5)`
2. `range(1, 5)`
3. `range(0, 10, 2)`
4. `range(10, 0, -1)`
5. `range(5, 5)`

<details>
<summary>Check your predictions</summary>

| Range | Numbers |
|---|---|
| `range(5)` | 0, 1, 2, 3, 4 |
| `range(1, 5)` | 1, 2, 3, 4 |
| `range(0, 10, 2)` | 0, 2, 4, 6, 8 |
| `range(10, 0, -1)` | 10, 9, 8, 7, 6, 5, 4, 3, 2, 1 |
| `range(5, 5)` | nothing at all |

</details>

## Investigate: find the rule

Work with your partner in the lab.

1. Write the rule for **start**, **stop** and **step** in your own words. Why does `range(1, 5)` **not** include 5?
2. Find a range that produces 3, 6, 9 … 30.
3. Find a range that produces 5, 4, 3, 2, 1, 0.
4. Which ranges produce **nothing**? Can you predict that before running?

<details>
<summary>Check: the rule</summary>

`range(start, stop, step)` starts at **start**, jumps by **step**, and stops **before** it reaches **stop**. The stop number is never included.

- If you leave out start, it is 0.
- If you leave out step, it is 1.
- 3, 6, 9 … 30 is `range(3, 31, 3)`.
- 5, 4 … 0 is `range(5, -1, -1)`.
- A range is empty when you can't move from start toward stop: `range(5, 5)`, or `range(1, 10, -1)`.

</details>

## for or while?

Sort these tasks. For each one, write `for` or `while` and **one reason**.

1. Repeat until the password is right.
2. Print 10 lines.
3. Print the times table from 1 to 10.
4. Keep playing until the player says "stop".

<details>
<summary>Check your thinking</summary>

Use **for** when you know how many times to repeat (2 and 3). Use **while** when you repeat **until** something happens, and you don't know when (1 and 4).

</details>

## Before you leave

Complete these in your log:

1. `range(a, b)` stops at ___ because ___.
2. I would choose `while` instead of `for` when ___.
3. Which range prediction was I most confident about? Was I right?
