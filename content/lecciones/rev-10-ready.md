# Ready for week 7?

This lesson mixes everything from the review. Use it to check what you know, and what you need to practise.

## Mixed predictions

For each program, write your prediction **and** your confidence from 1 to 4 in your log. Then check.

**1.**

```python
x = 4
y = x * 2
x = 10
print(x, y)
```

<details>
<summary>Check</summary>

`10 8`. `y` was calculated when `x` was 4. Changing `x` later doesn't change `y`.

</details>

**2.**

```python
a = "5"
b = "6"
print(a + b)
print(int(a) + int(b))
```

<details>
<summary>Check</summary>

```text
56
11
```

</details>

**3.** The user types `Ana`.

```python
name = input("Name: ")
print(f"{name} has {len(name)} letters")
```

<details>
<summary>Check</summary>

`Ana has 3 letters`

</details>

**4.**

```python
score = 7
score += 3
score = score * 2
print(score >= 20)
```

<details>
<summary>Check</summary>

`True`. score goes 7 → 10 → 20, and `20 >= 20` is `True`.

</details>

**5.** The user types `AU`.

```python
answer = input("Symbol for gold? ")
print(answer == "AU", answer == "au")
```

<details>
<summary>Check</summary>

`True False`

</details>

**6.**

```python
print(10 / 4)
print((2 + 3) * 2)
print("2" + "3" == "5")
```

<details>
<summary>Check</summary>

```text
2.5
10
False
```

`"2" + "3"` is the text `"23"`, which is not `"5"`.

</details>

How many of your **confidence 3 and 4** predictions were correct? If one surprised you, go back to that lesson.

## I can…

Rate each statement from 1 to 4 in your log. Next to each one, write a line of code that proves it.

- I can predict what `print` shows, including spaces.
- I can explain the difference between `"7"` and `7`.
- I can store, use and change values in variables.
- I can trace a program with a table.
- I can ask a question with `input()` and convert the answer.
- I can build an exact message with an f-string.
- I can predict whether a comparison is `True` or `False`.
- I can read an error message and find the line and the cause.

## A look ahead

Week 7 starts with this question: **does Python run every line of a program?** So far, the answer has always been yes. Next week, you will see programs that **decide**.
