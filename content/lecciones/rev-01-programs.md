# What is a program?

## Instructions, in order

A **program** is a list of instructions for a computer.

The computer follows the instructions **exactly**, **one at a time**, from the **top to the bottom**. It doesn't guess what you mean, and it doesn't skip lines or change their order.

Think of a recipe. If the recipe says "bake the cake", then "mix the eggs", you get a strange cake. The computer is like a cook who follows the recipe perfectly, even when the recipe is wrong.

**Python** is a programming language: a way to write instructions that a computer understands. We write the instructions as text, and Python runs them.

## Your first program

```python
print("Hello!")
```

This program has **one instruction**. `print` tells Python to show something on the screen. When you run it, the screen shows:

```text
Hello!
```

## Order matters

Predict what this program shows. Write your prediction, and rate your confidence from 1 (a guess) to 4 (completely sure).

```python
print("Get up")
print("Have breakfast")
print("Go to school")
```

<details>
<summary>Check your prediction</summary>

```text
Get up
Have breakfast
Go to school
```

Python runs the first line, then the second, then the third. Each `print` shows its text on a **new line**.

</details>

Now predict this one:

```python
print("Go to school")
print("Get up")
print("Have breakfast")
```

<details>
<summary>Check your prediction</summary>

```text
Go to school
Get up
Have breakfast
```

The computer does not know that this order is silly. It follows the instructions exactly as they are written. **If the order is wrong, the result is wrong.**

</details>

## Comments: notes for humans

Anything after a `#` is a **comment**. Python ignores it completely. Comments are notes for you and for other people who read your code.

```python
# This program greets the user
print("Hello!")   # this line shows a greeting
```

This shows only `Hello!`.

A comment is also useful for **switching off** a line without deleting it:

```python
print("Line one")
# print("Line two")
print("Line three")
```

<details>
<summary>What does it show?</summary>

```text
Line one
Line three
```

</details>

## How this platform works

Every exercise page has:

- **The editor**, on the right: where you write your code. The numbers on the left are **line numbers**.
- **Run**: runs your code and shows the result under the editor, in the **Output** area. Shortcut: **Ctrl + Enter**.
- **Check**: runs automatic **tests**. Each test runs your program and compares the result with the correct answer. You see which tests passed (✓) and which failed (✗), and why.
- **The Inputs box**: appears when your program asks the user questions. More about this in lesson 6.

Your code **saves automatically**, at school and at home. If you close the page and come back, your code is still there.

Some pages are **free workspaces** (✎). They have no tests: you can try anything you like.

## Predict before you run

In this course, we always **predict before we run**:

1. **Read** the code carefully.
2. **Predict:** write what you think it will do.
3. **Rate your confidence** from 1 to 4.
4. **Run** it and compare.

Why? Because running code without thinking teaches you very little. Predicting makes you **think like the computer**. And when you are sure but wrong, you have found exactly the thing you need to learn.

## Mistakes are normal

Every programmer makes mistakes all the time. When Python can't understand your code, it shows an **error message**. An error message is not a punishment: it's Python telling you where it got confused. Lesson 9 shows you how to read them.

## Summary

- A program is a list of instructions.
- Python runs them in order, from top to bottom, exactly as written.
- `print(...)` shows something on the screen.
- `#` starts a comment, which Python ignores.
- Predict, rate your confidence, then run.
