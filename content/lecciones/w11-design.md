# Design a program from its behaviour

**This week's question:** Can you describe *exactly* what a program does, just by watching it?

This week is about **thinking and planning**, not typing. You will design a game on paper. Next week you will build it.

## Watch the game

Your teacher will play a game called **Guess the Number** on the projector. You will **not** see the code.

Here is one game, from start to end:

```text
I'm thinking of a number from 1 to 100.
Your guess: 50
Too high
Your guess: 25
Too low
Your guess: 37
Too low
Your guess: 43
Too high
Your guess: 40
Correct! You got it in 5 guesses.
```

In your log, list **every behaviour** you notice. For example: what messages appear? When does the game end? How many guesses are allowed?

You can ask your teacher to replay the game with any input you choose. For example: *"What if I type 0?"* or *"What if I never guess it?"* Collect evidence!

<details>
<summary>Compare with the class list</summary>

Behaviours many students notice:

- The computer picks a secret number from 1 to 100.
- After each guess, it says `Too high`, `Too low` or `Correct!`.
- It counts the guesses.
- You have **10 attempts**. After 10 wrong guesses, the game ends and shows the number.
- It ends as soon as you guess correctly.

Did you notice anything else? What happens with a guess like 0 or 150?

</details>

## Write the pseudocode

With your partner, write the game in **pseudocode** on paper. Use these commands:

| Command | Meaning |
|---|---|
| `ASK` | Get something from the user. |
| `SAY` | Show a message. |
| `IF` / `ELSE` | Make a decision. |
| `WHILE` | Repeat while something is True. |

There is no template. Start from your list of behaviours.

## Swap and trace

Swap pseudocode with another pair. Trace their pseudocode with these three scenarios:

1. The player wins on the **first** guess.
2. The player makes **ten wrong guesses** in a row.
3. The player guesses a number **outside 1–100**.

Mark **exactly** where the pseudocode breaks. Then give it back.

## Fix and plan your tests

Fix your pseudocode. Then write a **test table** with at least 6 inputs:

| What I type | Why I chose it | What should happen |
|---|---|---|
| | | |

Keep it for next week!

## Tool card: random numbers

```python
import random
secret = random.randint(1, 100)
```

`random.randint(1, 100)` picks a whole number from 1 to 100. **Predict:** which values could `random.randint(1, 3)` give? Check it in the **Week 11 lab**.

<details>
<summary>Check your prediction</summary>

1, 2 or 3. Both ends are included. (This is different from `range()`, where the stop number is not included!)

</details>

**Stopping after 10 attempts** is tricky with what we know so far. One way: count the guesses, and use an `if` inside the loop. Another tool, if you need it: `break` stops a loop immediately.

## Before you leave

Complete these in your log:

1. The hardest behaviour to describe was ___.
2. I'm least sure my pseudocode handles ___.
