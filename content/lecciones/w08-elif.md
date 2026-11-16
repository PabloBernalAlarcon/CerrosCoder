# Does the order of my conditions matter?

**This week's question:** When a program has several conditions, which one wins?

## Do Now: last week's code

Many of you solved the 2.5 / 2,5 problem like this:

```python
answer = input("What is 10 divided by 4? ")
if answer == "2.5":
    print("Correct!")
if answer == "2,5":
    print("Correct!")
else:
    print("Wrong")
```

Predict the output for each input. Rate your confidence (1–4).

1. `2.5`
2. `2,5`
3. `3`

<details>
<summary>Check your prediction</summary>

| Input | Output | Why |
|---|---|---|
| `2.5` | `Correct!` **and** `Wrong` | The first `if` is True. Then Python asks the second `if`: False. So its `else` runs. |
| `2,5` | `Correct!` | The second `if` is True, so its `else` is skipped. |
| `3` | `Wrong` | Both are False. The `else` runs. |

**Key idea:** each `if` is a separate question. The `else` belongs **only** to the `if` directly above it.

</details>

## Draw it

Think of each `if` as a diamond in a flowchart.

- **What this code does:** two separate diamonds. Python visits **both**.
- **What we wanted:** a chain. Each "no" leads to the next question. The first "yes" ends the chain.

## Name it: elif

`elif` means **"else, if"**. It is a question Python asks **only if every question before it was "no"**.

```python
answer = input("What is 10 divided by 4? ")
if answer == "2.5":
    print("Correct!")
elif answer == "2,5":
    print("Correct!")
else:
    print("Wrong")
```

Now `2.5` prints only `Correct!`.

In your log, write: *"Last week I thought ___. Now I think ___."*

## Read the grade classifier

Predict alone first. Then compare with your partner. If you disagree, don't decide yet: the code will decide.

```python
score = 95
if score >= 50:
    print("Pass")
elif score >= 70:
    print("Good")
elif score >= 90:
    print("Excellent")
else:
    print("Not yet")
```

What does it print for `score = 95`? And for `75`, `50` and `30`?

<details>
<summary>Check your prediction</summary>

| score | Output |
|---|---|
| 95 | `Pass` |
| 75 | `Pass` |
| 50 | `Pass` |
| 30 | `Not yet` |

Most people predict `Excellent` for 95. But Python checks `score >= 50` first. It is True, so Python prints `Pass` and **stops**. It never checks `>= 70` or `>= 90`.

**Python does not look for the best match. It takes the first True condition.**

</details>

## Investigate

Open **Week 8 lab**. For each exercise, write your prediction as a comment (`# I predict ...`) before you run.

1. **Trace it.** With score = 95, which conditions does Python check? Add `print("checking >= 70")` lines to find out.
2. **if, if, if.** Change every `elif` to `if`. Predict, then test with 95 and 75.
3. **Fix the order.** Make the classifier correct. Then find a **second**, different correct version.
4. **Convince me.** Write a list of 6–8 test scores. Next to each one, write *why* you chose it.

<details>
<summary>Check: exercise 2</summary>

- **95** prints `Pass`, `Good`, `Excellent`. Three separate `if`s, all True.
- **75** prints `Pass`, `Good`, `Not yet`. The `else` belongs only to the last `if` (`>= 90`), which is False.

</details>

<details>
<summary>Check: exercise 3 (two correct orders)</summary>

Start from the top, with `>=`:

```python
if score >= 90:
    print("Excellent")
elif score >= 70:
    print("Good")
elif score >= 50:
    print("Pass")
else:
    print("Not yet")
```

Or start from the bottom, with `<`:

```python
if score < 50:
    print("Not yet")
elif score < 70:
    print("Pass")
elif score < 90:
    print("Good")
else:
    print("Excellent")
```

</details>

<details>
<summary>Check: exercise 4 (good test scores)</summary>

- **49 and 50, 69 and 70, 89 and 90.** Bugs hide on the boundaries.
- **0 and 100:** the smallest and biggest scores.
- **One score inside each band**, such as 30, 60, 80, 95.

Why test 69 and 70, and not 65? Because 65 and 66 behave the same. 69 and 70 should get **different** labels.

</details>

## When does order matter?

In the classifier, the conditions **overlap**: 95 is `>= 50` **and** `>= 90`. So the first True one wins, and order matters.

In this adventure, an answer can't be `"left"` and `"right"` at the same time. So the order does **not** matter:

```python
choice = input("Left or Right? ")
if choice == "left":
    print("You found gold!")
elif choice == "right":
    print("You fell in a pit!")
else:
    print("You stand still, confused. Try left or right.")
```

**Tool:** `.lower()` changes text to small letters. `input("Left or Right? ").lower()` makes `LEFT`, `Left` and `left` all the same.

## Before you leave

Complete these in your log:

1. Order matters in an elif chain when ___. The test that showed me was ___.
2. I'm still unsure about ___.
3. Count today's predictions where your confidence was 3 or 4. How many were correct?
