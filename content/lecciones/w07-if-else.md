# When does a line of code run?

**This week's question:** Python reads a program from top to bottom. But does it run *every* line?

## How we work this year

Every week, you will **predict before you run**:

1. **Predict.** Read the code. Write what you think it will print.
2. **Rate your confidence** from 1 to 4. (1 = a guess, 4 = completely sure.)
3. **Check.** Open the answer, or run the code.

Write your predictions and ratings in your log. Being sure and being right are different things. We will track both all year.

## Warm-up: True or False?

Predict what each line prints. Rate your confidence.

```python
print(7 > 3)
print("7" == 7)
print("AU" == "au")
```

<details>
<summary>Check your prediction</summary>

```text
True
False
False
```

- `7 > 3` is a question. Python answers it with `True` or `False`.
- `"7"` is text and `7` is a number. Text is never equal to a number.
- Python cares about capital letters. `"AU"` and `"au"` are different texts.

Were you a confident 4 and still wrong? That is useful information. Write it down.

</details>

## Read the trivia program

Do not run it yet. Read it carefully.

```python
score = 0
answer = input("What is the chemical symbol for gold? ")
if answer == "AU":
    print("Correct!")
    score += 1
else:
    print("Wrong. The answer is AU.")
print("Your score:", score)
```

Predict what it prints when the user types:

1. `AU`
2. `au`
3. `gold`
4. Nothing (they just press Enter)

<details>
<summary>Check your prediction</summary>

| The user types | The program prints |
|---|---|
| `AU` | `Correct!` then `Your score: 1` |
| `au` | `Wrong. The answer is AU.` then `Your score: 0` |
| `gold` | `Wrong. The answer is AU.` then `Your score: 0` |
| (Enter) | `Wrong. The answer is AU.` then `Your score: 0` |

The lines **inside** the `if` (moved to the right) run only when the condition is `True`. The lines inside the `else` run only when it is `False`. The last line is not inside either one, so it **always** runs.

</details>

## Investigate

Open **Week 7 lab** and work with your partner. For each card: predict first, then run.

1. **Which lines run only sometimes?** Prove it. Hint: add your own `print("here")` markers.
2. **Move `score += 1` to the left**, so it is not inside the `if` any more. Predict what happens. Then test it with `AU` and `gold`.
3. **Add `print(answer == "AU")`** just before the `if`. What does it show you?
4. **Change `==` to `!=`.** What else must change, so the program is still correct?

<details>
<summary>What did you find?</summary>

- Indentation (the spaces at the start of a line) decides which lines belong to the `if` or the `else`.
- If `score += 1` is not indented, it always runs. Then `gold` gets a point too!
- `print(answer == "AU")` shows the answer to the question before Python makes its decision.
- With `!=`, you must swap the two blocks: the "Wrong" message moves under the `if`.

</details>

## A problem for you

Add a question: *"What is 10 divided by 4?"* In Colombia we often write decimals with a comma, so `2.5` **and** `2,5` must both be correct.

Use only `if` and `else`. Test it with `2.5`, `2,5` and `3`. Does it work for all three? Keep your code: we will come back to it next week.

## Before you leave

Complete these in your log:

1. I'm confident I can ___ because I tested ___.
2. I'm still unsure about ___.
3. A question I have now is ___.
