# Why give a chunk of code a name?

**This week's question:** When the same lines appear again and again, how can we write them only once?

## What's annoying here?

```python
print("*" * 20)
print("Welcome")
print("*" * 20)
print("*" * 20)
print("Level 2")
print("*" * 20)
print("*" * 20)
print("Game over")
print("*" * 20)
```

If you want the stars to become `=` signs, how many lines must you change? Write a better idea in your log.

## Predict: a function

Read this program. Predict the output. Then **number the lines in the order Python runs them**. Rate your confidence.

```python
def banner(msg):
    print("*" * 20)
    print(msg)
    print("*" * 20)

print("Start")
banner("Welcome")
banner("Game over")
```

<details>
<summary>Check your prediction</summary>

```text
Start
********************
Welcome
********************
********************
Game over
********************
```

`def` only **defines** the function: Python remembers it, but doesn't run it. The first line that runs is `print("Start")`. Then each **call**, `banner(...)`, jumps into the function, runs its lines, and comes back.

When `banner("Welcome")` runs, `msg` is `"Welcome"`. `msg` is a **parameter**: a name for the value the function receives.

</details>

## Investigate

Use the **Week 17 lab**. Predict, then test each card.

1. When does the code inside `def` actually run?
2. Delete **both** calls. Predict what prints.
3. Call `banner()` with nothing inside the brackets. Predict the error.
4. Move the `def` **below** the calls. Predict, then test.
5. Add a second parameter, `symbol`, so you can call `banner("Hi", "=")`.

<details>
<summary>Check: what did you find?</summary>

1. Only when the function is **called**.
2. Only `Start`. Without calls, the function never runs.
3. `TypeError: banner() missing 1 required positional argument: 'msg'`. The function needs a value for `msg`.
4. `NameError`: Python reads from top to bottom, so the function must be defined **before** it is called.
5. For example:

```python
def banner(msg, symbol):
    print(symbol * 20)
    print(msg)
    print(symbol * 20)
```

</details>

## Make: refactor the trivia program

Refactor (rewrite) the week 7 trivia program with a function `ask_question(question, answer)`. It asks one question and prints if it was correct. The program must **behave exactly as before**. This is the exercise **Trivia with a function** in this unit.

## Before you leave

Complete these in your log:

1. The code inside a function runs when ___.
2. In my own words, a parameter is ___.
