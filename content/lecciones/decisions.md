# Decisions with `if`, `elif` and `else`

Programs can make decisions. To do that, we ask a **question** that Python answers with `True` or `False`.

## Comparisons

```python
print(8 > 5)     # True
print(3 == 4)    # False  (== asks "are they equal?")
print(7 != 2)    # True   (!= asks "are they different?")
print(5 >= 5)    # True
```

Don't confuse `=` (put a value in a variable) with `==` (compare two values).

## if and else

```python
temperature = 28

if temperature > 25:
    print("It's hot")
else:
    print("It's cool")
```

Just like in functions, the colon `:` and the indentation show which code depends on the condition.

## elif: more than two paths

```python
grade = 5.8

if grade >= 6:
    print("Excellent")
elif grade >= 4.5:
    print("Passed")
else:
    print("Needs more practice")
```

Python checks the conditions in order and runs **only the first one** that is true.

## Returning True or False from a function

A comparison is already `True` or `False`, so you can return it directly:

```python
def is_adult(age):
    return age >= 18

print(is_adult(14))   # False
```
