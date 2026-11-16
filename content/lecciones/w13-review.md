# Getting ready for the test

This week you take **written test #1**. It checks reading code, logic, and Python syntax: `if`, `elif`, `else`, `while` and `for`.

## Predict your score

Before the test, you will fill a **prediction slip**: the score you expect for each part, and your confidence (1–4). After the test, you will compare. Being honest here helps you learn how well you know what you know.

## Practice: predict, then check

Write your prediction and confidence for each one. Then open the answer.

**1.**

```python
x = 15
if x > 10:
    print("A")
elif x > 5:
    print("B")
else:
    print("C")
```

<details>
<summary>Check</summary>

`A`. The first True condition wins, and the chain stops.

</details>

**2.**

```python
n = 1
while n < 20:
    n = n * 3
print(n)
```

<details>
<summary>Check</summary>

`27`. n goes 1 → 3 → 9 → 27. When n is 27, `27 < 20` is False, so the loop stops. Only then does `print` run.

</details>

**3.**

```python
for i in range(2, 9, 3):
    print(i)
```

<details>
<summary>Check</summary>

```text
2
5
8
```

Start at 2, jump by 3, stop **before** 9.

</details>

**4.**

```python
total = 0
for i in range(4):
    total = total + i
print(total)
```

<details>
<summary>Check</summary>

`6`. `range(4)` is 0, 1, 2, 3, and 0 + 1 + 2 + 3 = 6.

</details>

**5.** How many times does this print `Hi`?

```python
count = 5
while count > 0:
    print("Hi")
    count = count - 2
```

<details>
<summary>Check</summary>

**3 times.** count goes 5 → 3 → 1 → -1. The condition is checked 4 times; the last check is False.

</details>

How many of your confidence-4 predictions were correct? Write it in your log.

## More practice

The exercises in this unit mix everything from weeks 7 to 12. They are a good way to review at home before the test.
