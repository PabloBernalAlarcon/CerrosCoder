# How does a program know when to stop?

**This week's question:** How can a program repeat something, and how does it know when to stop?

| Key word | Meaning |
|---|---|
| **loop** | Code that repeats. |
| **condition** | A question. The answer is True or False. |
| **trace** | Follow the code one step at a time. |

## Do Now

Here is the correct grade classifier from last week. Predict the output for `score = 70` and for `score = 89`. Rate your confidence.

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

<details>
<summary>Check your prediction</summary>

Both print `Good`. 89 is not `>= 90`, so the chain stops at `>= 70`.

</details>

## The problem

A program must ask for a password **until it is correct**. Use only `if` and `else`.

Try it on paper for 2 minutes. How many `if`s do you need?

<details>
<summary>What did you find?</summary>

You can't know! The user might need 2 tries, or 50. We need a way to **repeat**.

`while` means: **repeat while the condition is True.**

Think of it like this: **while = an if that repeats.**

</details>

## Trace a loop

Read this loop. Do **not** run it yet.

```python
count = 1
while count <= 3:
    print("Round", count)
    count = count + 1
print("Done")
```

Make a trace table in your log. Write one row **each time Python checks the condition**:

| count | count <= 3 ? | What prints? |
|---|---|---|
| 1 | | |
| … | | |

Last question: **how many times does Python check the condition?** Rate your confidence.

<details>
<summary>Check your trace</summary>

| count | count <= 3 ? | What prints? |
|---|---|---|
| 1 | True | `Round 1` |
| 2 | True | `Round 2` |
| 3 | True | `Round 3` |
| 4 | False | `Done` (after the loop) |

Python checks the condition **4 times**. The code inside the loop runs **3 times**. The last check is False: that is what stops the loop.

</details>

## Investigate

Open **Week 9 lab**. Write each prediction as a comment, then run.

1. **Change `<=` to `<`.** What prints now?
2. **Count down:** write a loop that prints 10, 9, 8 … 1, then `Go!`.
3. **Delete `count = count + 1`.** Predict first! (The platform stops the program after 5 seconds.)

<details>
<summary>Check: exercise 1</summary>

It prints `Round 1`, `Round 2`, `Done`. When count is 3, `3 < 3` is False.

</details>

<details>
<summary>Check: exercise 2</summary>

```python
count = 10
while count >= 1:
    print(count)
    count = count - 1
print("Go!")
```

Is `print("Go!")` moved to the right? Then it is **inside** the loop and prints 10 times. Indentation is not just style!

</details>

<details>
<summary>Check: exercise 3</summary>

It prints `Round 1` forever. Nothing changes `count`, so `count <= 3` is always True. This is an **infinite loop**.

Every loop needs something inside it that can make the condition False.

</details>

## Make: the password checker

Before you write any code, plan your tests in your log:

| What I type | Why I chose it | What should happen |
|---|---|---|
| | | |

Include at least one input that you think will break the program. For example: what about `PYTHON` in capitals?

Then write the loop:

```python
secret = "python"
password = input("Password: ")
while password != secret:
    password = input("Wrong. Try again: ")
print("Welcome!")
```

Read the condition aloud: *"repeat while the password is NOT the secret"*.

## Before you leave

Complete these in your log:

1. A while loop stops when ___.
2. In my trace table, Python checked the condition ___ times. I know because ___.
3. Today I made ___ predictions with confidence 3 or 4. ___ were correct.
