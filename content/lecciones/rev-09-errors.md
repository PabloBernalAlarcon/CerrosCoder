# Reading error messages

## An error is a message, not a punishment

When Python can't run your code, it stops and shows an **error message**. Beginners often panic and change things at random. Instead, **read the message**: it tells you **where** Python got confused and **what kind** of problem it found.

On this platform, the error box shows:

- **the line number**, and that line is also highlighted in red in the editor,
- **the type of error** and Python's explanation,
- **a hint** in simple words.

**Tip:** in a long error message, the most useful part is the **last line**.

## The most common errors

### SyntaxError: Python can't read this line

```python
print("Hello)
```

The **syntax** is the grammar of the language. A `SyntaxError` means the line is written in a way Python can't understand. Usual causes: a missing quote, a missing bracket, a missing `:`, or `=` where you meant `==`.

**Careful:** when a bracket is missing, Python sometimes reports the error on the **next** line, because that is where it noticed the problem. Look at the line before too.

### NameError: Python doesn't know this name

```python
name = "Ana"
print(nmae)
```

```text
NameError: name 'nmae' is not defined
```

Usual causes:

- A **typo**: `nmae` instead of `name`.
- **Capital letters**: `Score` instead of `score`.
- **Missing quotes**: `print(Hello)` instead of `print("Hello")`.
- Using a variable **before** creating it.

### TypeError: these types don't go together

```python
print("Age: " + 14)
```

You are mixing types that don't work together, like joining text and a number with `+`. Convert with `str()`, `int()` or `float()`, or use an f-string.

### ValueError: the value has the wrong form

```python
int("abc")
int("4.5")
```

The type is right (text), but the **content** can't be converted. Often caused by `int(input(...))` when the user types letters or decimals.

### ZeroDivisionError: dividing by zero

```python
print(10 / 0)
```

Just like in maths, you can't divide by zero.

### IndentationError: unexpected spaces at the start of a line

```python
print("One")
    print("Two")
```

```text
IndentationError: unexpected indent
```

The **indentation** is the space at the start of a line. For now, every line starts at the very left. From week 7, indentation becomes **very** important: it shows which lines belong to an `if`. For now, remember: **don't add spaces at the start of a line** unless Python needs them.

### EOFError: no more answers

On this platform, this means your program called `input()` more times than there were answers in the **Inputs** box. Add more answers, one per line.

## A strategy for fixing errors

1. **Read** the last line of the error and the line number.
2. **Predict** the cause before you change anything.
3. **Change one thing** only.
4. **Run** again. Did the error change? A **different** error often means progress!

## Practice: name the error

For each program, predict which error it gives. Rate your confidence.

**1.**

```python
price = input("Price: ")
print(price * 1.19)
```

<details>
<summary>Check</summary>

`TypeError`. `price` is text, because `input()` gives text. Fix: `price = float(input("Price: "))`.

</details>

**2.**

```python
Total = 50
print(total)
```

<details>
<summary>Check</summary>

`NameError: name 'total' is not defined`. `Total` and `total` are different names.

</details>

**3.**

```python
print("Result:", (5 + 3)
```

<details>
<summary>Check</summary>

`SyntaxError`. There are two `(` but only one `)`.

</details>

## Summary

- Read the **last line** and the **line number** first.
- `SyntaxError`: written wrong (quotes, brackets, colons).
- `NameError`: unknown name (typo, capitals, missing quotes).
- `TypeError`: mixing types.
- `ValueError`: impossible conversion.
- `IndentationError`: unexpected spaces at the start of a line.
- Change one thing at a time, and run again.
