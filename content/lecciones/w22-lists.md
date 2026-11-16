# Remembering many things

**This week's question:** What changes when a program has to remember **many** things?

## Hook

Five test scores, five variables:

```python
score1 = 70
score2 = 85
score3 = 92
score4 = 60
score5 = 77
average = (score1 + score2 + score3 + score4 + score5) / 5
print(average)
```

Now do it for a class of 30 students. What's the problem? Write your ideas in your log.

## A list

A **list** keeps many values in one variable, in order:

```python
scores = [70, 85, 92, 60]
```

## Predict

Rate your confidence for each one. `scores = [70, 85, 92, 60]`.

```python
print(scores[0])
print(scores[3])
print(scores[4])
print(scores[-1])
print(len(scores))
```

<details>
<summary>Check your prediction</summary>

| Code | Result |
|---|---|
| `scores[0]` | `70`: positions (indexes) start at **0** |
| `scores[3]` | `60`: the 4th item |
| `scores[4]` | crash: `IndexError: list index out of range`. There is no 5th item! |
| `scores[-1]` | `60`: negative indexes count from the end |
| `len(scores)` | `4`: the number of items |

The index of the last item is always `len(scores) - 1`.

</details>

## Investigate

In the **Week 22 lab**, predict each one first, then try it:

1. `scores[1] = 90`, then `print(scores)`
2. `scores.append(77)`, then `print(scores)`
3. `print(85 in scores)` and `print(100 in scores)`
4. Loop through the list and add up the total:

```python
total = 0
for s in scores:
    total = total + s
print(total)
```

<details>
<summary>Check: what did you find?</summary>

1. `[70, 90, 92, 60]`: you can change an item.
2. `[70, 85, 92, 60, 77]`: `append` adds an item at the end.
3. `True`, then `False`: `in` checks whether a value is in the list.
4. `307`. In each round, `s` is the next item of the list.

</details>

## Make: score analyser

Enter scores until the user types `done`. Then print the count, the highest score and the average. Find the highest with a loop, not `max()`, so you can see the logic.

Your test plan must include an **empty list**: the user types `done` straight away. What happens to the average?

This is the exercise **Score analyser** in this unit.

## Before you leave

Complete these in your log:

1. A list is better than separate variables when ___.
2. The index of the last item is always ___.
