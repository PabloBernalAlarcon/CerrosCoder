# Asking questions with input()

## Programs that listen

So far, our programs always do the same thing. With `input()`, a program can **ask the user a question** and use the answer.

```python
name = input("What is your name? ")
print("Hello", name)
```

1. `input(...)` shows the question and **waits** until the user types something and presses Enter.
2. What the user typed is **put in the box** `name`.
3. The next line uses it.

If the user types `Ana`, the program shows:

```text
What is your name? Ana
Hello Ana
```

**Tip:** leave a space at the end of the question, `"What is your name? "`, so the answer doesn't touch the question mark.

## On this platform: the Inputs box

On this platform, nobody types while the program runs. Instead, you write the answers **before** you run, in the **Inputs** box: **one answer per line**, in order. The first `input()` gets the first line, the second `input()` gets the second line, and so on.

When you press **Run**, the Output shows each question followed by the answer it used.

When you press **Check**, each test gives its own answers to your program. The tests only compare what your **print** lines show; the question text inside `input()` doesn't matter. So you can word your questions however you like.

If your program asks more questions than there are answers, you get an `EOFError`: the program asked for an answer, but there were none left.

## input() always gives text

This is the most important rule of this lesson. Predict what happens when the user types `14`:

```python
age = input("How old are you? ")
print(age + 1)
```

<details>
<summary>Check your prediction</summary>

An error: `TypeError: can only concatenate str (not "int") to str`.

Even when the user types a number, **`input()` always gives text**. So `age` is `"14"`, and Python can't add the text `"14"` and the number 1.

</details>

To do maths, **convert** the answer:

```python
age = int(input("How old are you? "))
print("Next year you will be", age + 1)
```

Read the first line from the **inside out**:

1. `input(...)` asks the question and gives the text `"14"`.
2. `int(...)` turns `"14"` into the number `14`.
3. `=` puts `14` in the box `age`.

Use `int(input(...))` for whole numbers and `float(input(...))` for decimals.

## Which one should I use?

| The answer is… | Use | Example |
|---|---|---|
| a name, a word, a sentence | `input(...)` | a name, a city |
| a whole number | `int(input(...))` | an age, a quantity |
| a number that can have decimals | `float(input(...))` | a grade, a price, a height |

Predict: the user types `4.5` for this program. What happens?

```python
grade = int(input("Your grade: "))
print(grade)
```

<details>
<summary>Check your prediction</summary>

`ValueError: invalid literal for int() with base 10: '4.5'`. The text `"4.5"` is not a whole number. A grade can have decimals, so use `float(input(...))`.

</details>

And if the user types letters, like `abc`, into `int(input(...))`? Also a `ValueError`. In week 20, you will learn how to protect a program from that.

## Several questions

```python
width = float(input("Width: "))
height = float(input("Height: "))
area = width * height
print("Area:", area)
```

With the inputs `3` and `4`, the program shows `Area: 12.0`.

## Summary

- `input("question")` asks a question and gives back what the user typed.
- Put the answer in a variable: `answer = input("...")`.
- `input()` **always gives text**. Convert with `int(...)` or `float(...)`.
- On this platform, write the answers in the **Inputs** box, one per line.
