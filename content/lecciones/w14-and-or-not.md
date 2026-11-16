# and, or, not

**This week's question:** Two ways to say the same thing. Are they really the same?

## After the test: your exam wrapper

Look at your returned test. For each lost mark, write one of these labels:

- **Didn't know:** I didn't know the idea.
- **Misread:** I knew it, but I read the question or the code wrong.
- **Rushed:** I knew it, but I went too fast.

Write one plan for each label. Then compare your **predicted** score with your **actual** score. Were you over-confident, under-confident, or right?

## Predict

Rate your confidence for each line.

```python
print(True and False)
print(5 > 3 or 2 > 9)
print(not 4 == 4)
print(3 < 5 and 5 < 3)
```

<details>
<summary>Check your prediction</summary>

```text
False
True
False
False
```

</details>

## Investigate: build the rules yourself

In the **Week 14 lab**, test all four combinations for `and` and for `or`. Fill these tables in your log:

| A | B | A and B | A or B |
|---|---|---|---|
| True | True | | |
| True | False | | |
| False | True | | |
| False | False | | |

Then write each rule **in your own words**.

<details>
<summary>Check your tables</summary>

| A | B | A and B | A or B |
|---|---|---|---|
| True | True | True | True |
| True | False | False | True |
| False | True | False | True |
| False | False | False | False |

- `and` is True only when **both** sides are True.
- `or` is True when **at least one** side is True.
- `not` flips True and False.

</details>

## The lockout problem, solved

Remember week 9? *"Lock the account after 3 wrong tries."* Now you can say both conditions at once:

```python
secret = "python"
tries = 1
password = input("Password: ")
while password != secret and tries < 3:
    password = input("Wrong. Try again: ")
    tries = tries + 1
if password == secret:
    print("Welcome!")
else:
    print("Locked!")
```

Read the condition aloud: *"repeat while the password is wrong **and** I still have tries left"*.

## Predict card: a famous bug

What does this print when the answer is `banana`? Rate your confidence. Then test it in the lab.

```python
answer = input("Left or right? ")
if answer == "left" or "right":
    print("Good choice!")
else:
    print("Please type left or right.")
```

<details>
<summary>Check your prediction</summary>

It prints `Good choice!`, even for `banana`!

Python reads it as `(answer == "left") or ("right")`. The second part is just the text `"right"`, and a text that is not empty counts as True. So the whole condition is always True.

The correct way: **repeat the comparison** on both sides.

```python
if answer == "left" or answer == "right":
```

</details>

## Before you leave

Write two conditions that mean the same thing, for example `not (x > 5)` and `x <= 5`. Then write the test that proves they agree.
