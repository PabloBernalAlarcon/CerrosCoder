# Types of data

## Every value has a type

Python has different **types** of values. The four you need most:

| Type | Python name | Examples |
|---|---|---|
| Text | `str` (string) | `"hello"`, `"7"`, `""` |
| Whole number | `int` | `7`, `-3` |
| Decimal number | `float` | `2.5`, `7.0` |
| True or false | `bool` (boolean) | `True`, `False` |

`type()` tells you the type of a value:

```python
print(type("hello"))
print(type(7))
print(type(7.0))
print(type(True))
```

```text
<class 'str'>
<class 'int'>
<class 'float'>
<class 'bool'>
```

## "7" is not 7

Look carefully: `"7"` has quotes, so it is **text**. It looks like a number, but for Python it is just the character 7, like a letter.

The type changes what `+` does. Predict each line, and rate your confidence:

```python
print(3 + 4)
print("3" + "4")
```

<details>
<summary>Check your prediction</summary>

```text
7
34
```

With numbers, `+` **adds**. With text, `+` **joins** (glues) the texts together. `"3" + "4"` is the text `"34"`.

</details>

And this one?

```python
print("3" + 4)
```

<details>
<summary>Check your prediction</summary>

An error:

```text
TypeError: can only concatenate str (not "int") to str
```

Python doesn't know if you want to add or to join, so it stops. "Concatenate" means join.

</details>

## Converting between types

You can convert a value to another type:

| Code | Result | Meaning |
|---|---|---|
| `int("42")` | `42` | text → whole number |
| `float("2.5")` | `2.5` | text → decimal |
| `str(15)` | `"15"` | number → text |
| `float(7)` | `7.0` | whole number → decimal |
| `int(7.9)` | `7` | decimal → whole number. It **cuts off** the decimals; it doesn't round! |

Some conversions are impossible. Predict which lines give an error:

```python
int("2.5")
int("hello")
float("2,5")
float("10")
```

<details>
<summary>Check your prediction</summary>

The first three give a `ValueError`:

- `int("2.5")`: the text has a decimal point, so it is not a whole number.
- `int("hello")`: this is not a number at all.
- `float("2,5")`: Python needs a **point**, not a comma.

`float("10")` works, and gives `10.0`.

</details>

## How long is a text?

`len()` counts the **characters** in a text. Spaces and punctuation count too!

```python
print(len("Ana"))
print(len("Juan David"))
print(len(""))
```

<details>
<summary>What does it show?</summary>

```text
3
10
0
```

"Juan David" has 9 letters plus 1 space: 10 characters. `""` is the **empty text**: it has no characters.

</details>

## True and False

`True` and `False` are values too, of type `bool`. They always start with a **capital letter**: `true` (small t) is an error. You will use them a lot in lesson 8 and in week 7.

## Summary

- The main types are `str` (text), `int` (whole number), `float` (decimal) and `bool` (True/False).
- `"7"` is text; `7` is a number.
- `+` adds numbers but joins texts. Mixing them gives a `TypeError`.
- `int()`, `float()` and `str()` convert between types.
- `int()` cuts off decimals. Python needs a point for decimals.
- `len()` counts the characters in a text.
