# Build, break, fix

**This week's question:** How do you know your program really works?

Today you build the game you designed last week. Then another pair tries to **break** it. Then you **fix** it.

## Warm-up: a loop with an if inside

Predict the output. Rate your confidence.

```python
secret = 7
for guess in range(5, 10):
    if guess == secret:
        print(guess, "Correct!")
    elif guess > secret:
        print(guess, "Too high")
    else:
        print(guess, "Too low")
```

<details>
<summary>Check your prediction</summary>

```text
5 Too low
6 Too low
7 Correct!
8 Too high
9 Too high
```

The loop does not stop at 7. Nothing tells it to stop! In your game, what **should** happen after a correct guess?

</details>

## How your game is graded

Your teacher will grade five things (1–7 scale):

| Criterion | To pass (5), your game must… |
|---|---|
| **Game logic** | Pick a random number and give the right feedback in normal play. |
| **Loop and ending** | Allow many guesses, and end on a win or after 10 attempts. |
| **Testing evidence** | Show at least 6 tests, with expected and actual results. |
| **Debugging and reflection** | Find a failure, try to fix it, and explain it. |
| **Readability** | Use clear names and readable code. |

The grade rewards **testing and debugging**, not only a game that works.

Crashes when someone types letters (like `abc`) are **not** penalised. We will solve that problem in week 20. Write those inputs down!

## 1. Build

Open **My Guess the Number game**. Code from your own pseudocode.

For every part of your code, you should be able to answer: *"Which line of my pseudocode does this come from?"*

Your code saves automatically, and your teacher can see it.

## 2. Break

Swap computers with another pair.

1. Run **their** test table.
2. Add **three attacks** of your own: inputs you think will break the game.
3. Write down every failure: the input, what should happen, what happened.

Ideas for attacks: the first guess is correct. Ten wrong guesses. 0, 101, -5. A very big number.

## 3. Fix

Go back to your own computer. Fix **at least one** failure. Update your test table:

| Input | Expected | Actual | Fixed? |
|---|---|---|---|
| | | | |

**Testing tip:** a random number makes testing hard. While you test, you can set `secret = 42`. Change it back to `random.randint(1, 100)` when you finish!

## Before you leave

Hand in your test table with this reflection:

*"The bug I'm proudest of finding was ___. I found it by ___."*
