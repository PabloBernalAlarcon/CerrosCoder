# Which data should be allowed to change?

**This week's question:** Some data changes all the time. Some data should **never** change. Can Python help us protect it?

## Warm-up

`names = ["Ana", "Luis", "Sara", "Tomás"]`. Predict each one. Rate your confidence.

```python
print(names[1])
print(names[-2])
print(len(names) - 1)
```

<details>
<summary>Check your prediction</summary>

`Luis`, then `Sara`, then `3` (the index of the last item).

</details>

## A tuple

```python
days = ("Mon", "Tue", "Wed", "Thu", "Fri")
```

This looks like a list, but it uses **round brackets**. It is a **tuple**. Should a program be allowed to change the days of the week?

**Predict:** what happens if you run `days[0] = "Sun"`? Then try it in the **Week 23 lab**.

<details>
<summary>Check your prediction</summary>

```text
TypeError: 'tuple' object does not support item assignment
```

A tuple can't change after you create it. You can read it (`days[0]`, `len(days)`, a `for` loop), but you can't change, add or remove items.

**Rule of thumb:** a **list** for data that changes, a **tuple** for data that should stay fixed.

</details>

## Sort the cards

List or tuple? Write one reason for each:

1. A shopping cart
2. An RGB colour, like `(255, 128, 0)`
3. The months of the year
4. A high-score table

<details>
<summary>Check your thinking</summary>

1. **List:** you add and remove items.
2. **Tuple:** a colour is always exactly three numbers.
3. **Tuple:** the months never change.
4. **List:** new scores come in and the order changes.

Some answers can be argued both ways. Your reason matters more than the label.

</details>

## A list of tuples

Each question in a quiz is a **pair**: the question and its answer. A tuple is perfect for a pair, and a list holds all the pairs:

```python
questions = [
    ("Chemical symbol for gold? ", "AU"),
    ("The planet closest to the Sun? ", "mercury"),
]

for q in questions:
    print(q[0], "->", q[1])
```

You can also unpack the pair directly: `for question, answer in questions:`.

## Make: the quiz engine

Upgrade the week 7 trivia program: questions and answers live in a list, and a loop asks every question and keeps score.

**Rule:** adding a new question must mean adding **one line of data** only. And test it: what happens with zero questions?

This is the exercise **Quiz engine** in this unit.

## Before you leave

Rate your "I can" statements for lists from 1 to 4, each with a line of code as evidence. Also write one idea for a project you might want to build: the project starts next week!
