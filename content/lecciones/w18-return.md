# Printing or returning?

**This week's question:** A function can **show** a result, or **give it back**. What's the difference, and why does it matter?

## Predict

Predict the output. Rate your confidence.

```python
def double_print(x):
    print(x * 2)

def double_return(x):
    return x * 2

result = double_print(5)
print(result)
```

<details>
<summary>Check your prediction</summary>

```text
10
None
```

`double_print(5)` **shows** 10 on the screen. But it gives nothing back, so `result` is `None`. `None` is Python's way to say "nothing".

</details>

## Investigate

In the **Week 18 lab**, predict each one first, then try it:

1. `print(double_return(5) + 1)`
2. `print(double_print(5) + 1)`
3. `total = double_return(3) + double_return(4)`, then `print(total)`

<details>
<summary>Check: what did you find?</summary>

1. `11`. `double_return(5)` **is** 10, so you can use it in a calculation.
2. It prints `10`, then crashes: `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'`. You can't add 1 to "nothing".
3. `14`.

Write the difference in your own words in your log. For example:

- `print` **shows** a value to the person using the program.
- `return` **gives** the value back to the code that called the function, so the program can keep using it.

When a function reaches `return`, it stops immediately.

</details>

## Make: refactor your game

Open **My game, refactored**. Copy your week 12 game into it (open **My Guess the Number game** in week 12 to find your code). Then refactor it into functions, for example:

- `get_guess()`: asks for a guess and **returns** it as a number.
- `check_guess(guess, secret)`: **returns** `True` when the guess is correct.

**Rule:** the game must behave **exactly** as before. Run your week 12 test table again to prove it.

If your game is lost or broken, ask your teacher for the reference version. Today's skill is refactoring, not rebuilding.

## Before you leave

Complete in your log:

*"Refactoring means ___. My test table shows the game still works because ___."*
