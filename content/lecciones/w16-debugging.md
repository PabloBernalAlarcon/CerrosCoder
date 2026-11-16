# Can you find the bug from the output alone?

**This week's question:** When a program is wrong, how do you find the problem without guessing?

## Warm-up: which program?

A countdown printed this. It should end at 1, but it doesn't:

```text
10
9
8
7
6
5
4
3
2
```

Which program produced it? Choose one and rate your confidence.

**A**
```python
for i in range(10, 1, -1):
    print(i)
```

**B**
```python
for i in range(10, 0, -1):
    print(i)
```

**C**
```python
for i in range(9, 0, -1):
    print(i + 1)
```

<details>
<summary>Check your choice</summary>

**A.** `range(10, 1, -1)` stops **before** 1, so the last number is 2.

B prints 10 down to 1, which is correct. C also prints 10 down to 1: `i` goes from 9 to 1, and the program prints `i + 1`.

Two different programs can give the same output. The output is **evidence**, and you still need to check the code.

</details>

## Bug-hunt stations

The exercises in this unit are **bug-hunt stations**. Each program has **exactly one bug**.

At each station, write in your log:

| Station | Symptom (what goes wrong) | My predicted cause | Actual cause | Match? |
|---|---|---|---|---|
| | | | | |

1. **Run** the program and describe the symptom.
2. **Predict** the cause **before** you change anything.
3. **Confirm** it: use a trace table, or add `print()` lines to see the values.
4. **Fix** it, and run the tests.

Some stations have an error message. Read the **last line** of the error and the **line number**. What does Python say it didn't understand?

## Our debugging steps

After the stations, the class builds a list of debugging steps. Here is a start. Change it to match what worked for you:

1. **Reproduce:** make the bug happen again.
2. **Read** the error message or the output carefully.
3. **Predict** the cause.
4. **Change one thing** only.
5. **Retest**, with the same input and with a boundary input.

Write your own version in your log.

## Before you leave

Complete these in your log:

1. My first move when code fails is now ___. Before today it was ___.
2. How often did my predicted cause match the real one?
