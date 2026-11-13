# Functions: `def` and `return`

You've already used functions that come with Python: `print()`, `input()`, `int()`. Now you'll create your own.

A **function** is a small, named program that receives some data, does something with it and **returns** a result.

```python
def triple(number):
    return number * 3

print(triple(5))    # 15
print(triple(10))   # 30
```

Here are the parts:

- `def` tells Python you're defining a function.
- `triple` is the function's name.
- `number` is the **parameter**: the data it receives.
- The colon `:` and the **indentation** (the 4 spaces) show which code belongs to the function.
- `return` sends the result back to whoever called the function.

## `return` is not the same as `print`

This is the most common mix-up. `print()` only **shows** something on the screen. `return` **hands back** the result so it can be used later:

```python
def double_wrong(n):
    print(n * 2)      # shows it, but doesn't return it

def double_right(n):
    return n * 2      # returns it

total = double_right(4) + 1    # this works: total is 9
```

In the function exercises, the tests use what your function **returns**. If you use `print` instead of `return`, the tests will fail.

## Several parameters

```python
def rectangle_area(base, height):
    return base * height

print(rectangle_area(3, 4))   # 12
```
