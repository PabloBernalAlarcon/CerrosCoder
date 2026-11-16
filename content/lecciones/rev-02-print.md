# Showing things with print()

## The parts of a print

```python
print("Hello, world!")
```

- `print` is the name of the instruction. Python is strict: it must be all **small letters**. `Print` or `PRINT` won't work.
- The **round brackets** `( )` hold what you want to show.
- The **quotes** `" "` mark the beginning and the end of a piece of **text**.

## Text goes between quotes

In programming, a piece of text is called a **string**. Strings go between quotes.

You can use double quotes `"` or single quotes `'`. Both work the same way, but the opening and the closing quote must match:

```python
print("Hello")    # works
print('Hello')    # works too
```

Inside the quotes, Python shows the text **exactly as you wrote it**: spaces, capital letters, punctuation, everything.

```python
print("Hello      there!")
```

<details>
<summary>What does it show?</summary>

```text
Hello      there!
```

Every space inside the quotes is kept.

</details>

**Apostrophes:** if your text contains an apostrophe, like *It's*, use double quotes around it: `print("It's raining")`. With single quotes, Python thinks the text ends at the apostrophe.

## Numbers don't need quotes

```python
print(25)
print(3.5)
```

Numbers can go without quotes. And then something interesting happens. Predict both lines, and rate your confidence:

```python
print("7 + 5")
print(7 + 5)
```

<details>
<summary>Check your prediction</summary>

```text
7 + 5
12
```

With quotes, `"7 + 5"` is **text**: Python shows those characters exactly. Without quotes, `7 + 5` is a **calculation**: Python does the maths first and shows the result.

**Quotes mean: show this exactly. No quotes mean: work this out.**

</details>

## Several things in one print

Separate the values with **commas**. Python shows them on the same line, with **one space** between each value:

```python
print("I am", 14, "years old")
```

```text
I am 14 years old
```

Notice: you don't write the spaces yourself. The commas add them.

Predict this one:

```python
print("Total:", 10 + 5, "pesos")
```

<details>
<summary>Check your prediction</summary>

```text
Total: 15 pesos
```

Python works out `10 + 5` first, then shows the three values separated by spaces.

</details>

## An empty line

`print()` with nothing inside shows an **empty line**:

```python
print("First")
print()
print("Second")
```

```text
First

Second
```

## Common mistakes

| Mistake | Example | What to do |
|---|---|---|
| Capital letter | `Print("Hi")` | Write `print`, all in small letters. |
| Missing quote | `print("Hi)` | Every text needs an opening **and** a closing quote. |
| Missing bracket | `print("Hi"` | Every `(` needs a `)`. |
| Curly quotes | `print(“Hi”)` | Copying from Word or a slide can change `"` into `“ ”`. Python only accepts straight quotes. Type them again. |
| Text without quotes | `print(Hello)` | Without quotes, Python thinks `Hello` is a variable (lesson 4). |

## Summary

- `print(...)` shows a value on a new line.
- Text (a **string**) goes between quotes and is shown exactly.
- Numbers and calculations go without quotes. Python works them out first.
- Commas show several values on one line, with spaces between them.
