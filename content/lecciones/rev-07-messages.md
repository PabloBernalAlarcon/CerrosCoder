# Building messages

Many programs mix fixed text and values in the same message: `Hello, Ana!` or `Total: 3600 pesos`. There are **three ways** to build a message. Each one has different rules for **spaces** and **types**.

## Way 1: commas in print

```python
name = "Ana"
print("Hello", name)
```

```text
Hello Ana
```

- Python adds **one space** between the values, automatically.
- You can mix text and numbers: `print("Age:", 14)` works.
- But you can't control the spaces. `print("Hello", name, "!")` shows `Hello Ana !`, with a space before the `!`.

## Way 2: joining with +

```python
name = "Ana"
print("Hello, " + name + "!")
```

```text
Hello, Ana!
```

- `+` glues texts **exactly**: no extra spaces. You must write every space yourself, inside the quotes.
- **Only text** can be joined. Numbers must be converted with `str()` first.

Predict, and rate your confidence:

```python
total = 3600
print("Total: " + total)
```

<details>
<summary>Check your prediction</summary>

`TypeError: can only concatenate str (not "int") to str`. `total` is a number. The fix: `print("Total: " + str(total))`.

</details>

And this one?

```python
name = "Ana"
print("Hello," + name)
```

<details>
<summary>Check your prediction</summary>

```text
Hello,Ana
```

No space! With `+`, you must put the space inside the quotes: `"Hello, " + name`.

</details>

## Way 3: f-strings

Put an `f` just **before** the opening quote. Then you can put any variable, or any calculation, between **curly braces** `{ }`:

```python
name = "Ana"
age = 14
print(f"{name} is {age} years old. Next year: {age + 1}.")
```

```text
Ana is 14 years old. Next year: 15.
```

- Spaces are **exactly** what you write.
- Numbers work without `str()`.
- You can calculate inside the braces: `{price * 2}`.

Predict:

```python
price = 1500
print(f"Two cost {price * 2} pesos")
print("Two cost {price * 2} pesos")
```

<details>
<summary>Check your prediction</summary>

```text
Two cost 3000 pesos
Two cost {price * 2} pesos
```

Without the `f`, the braces are just normal characters. A forgotten `f` is a very common mistake!

</details>

## Which way should I use?

| Way | Spaces | Numbers | Good for |
|---|---|---|---|
| Commas | added automatically | work | quick messages |
| `+` | you write them | need `str()` | joining texts |
| f-string | you write them | work | exact messages: **usually the best choice** |

## Exact output

The tests compare your output **character by character**. `Total: 3600` and `Total:3600` are different, and so are `hello` and `Hello`. When an exercise shows an example output, copy its spaces, capital letters and punctuation exactly.

If a test fails, compare the two outputs side by side: **expected** and **yours**. Look for spaces, capital letters and missing punctuation.

## Summary

- Commas: automatic spaces, any type.
- `+`: exact, text only (use `str()` for numbers).
- f-strings: `f"... {variable} ..."`, exact, any type, calculations allowed.
- Output must match exactly: spaces, capitals and punctuation.
