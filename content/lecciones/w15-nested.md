# When is nesting clearer, and when is it a trap?

**This week's question:** You can put an `if` inside another `if`, or join conditions with `and`. Which one should you choose?

## Warm-up

Predict `x > 3 and x < 10` for each value. Rate your confidence.

1. `x = 3`
2. `x = 7`
3. `x = 10`

<details>
<summary>Check your prediction</summary>

1. `False`: 3 is not bigger than 3.
2. `True`
3. `False`: 10 is not smaller than 10.

</details>

## Two versions

Read both versions. `logged_in` and `is_admin` are each `True` or `False`.

```python
# Version A
if logged_in:
    if is_admin:
        print("Admin panel")
    else:
        print("Not an admin")
else:
    print("Please log in")
```

```python
# Version B
if logged_in and is_admin:
    print("Admin panel")
else:
    print("Access denied")
```

Predict what **both** versions print for all four combinations:

| logged_in | is_admin | Version A | Version B |
|---|---|---|---|
| True | True | | |
| True | False | | |
| False | True | | |
| False | False | | |

<details>
<summary>Check your prediction</summary>

| logged_in | is_admin | Version A | Version B |
|---|---|---|---|
| True | True | `Admin panel` | `Admin panel` |
| True | False | `Not an admin` | `Access denied` |
| False | True | `Please log in` | `Access denied` |
| False | False | `Please log in` | `Access denied` |

They agree on **when** the admin panel opens. But Version A gives a **different message for each problem**. Version B can only say "no".

</details>

## Investigate

Work in the **Week 15 lab**.

1. Are A and B the same? Find an input where they behave differently.
2. What can nesting do that a single `and` can't?
3. Rewrite this three-level nested `if` as **one** condition:

```python
if age >= 13:
    if has_ticket:
        if not banned:
            print("Come in!")
```

Which version is easier to read? Why? Discuss with the class.

<details>
<summary>Check: question 3</summary>

```python
if age >= 13 and has_ticket and not banned:
    print("Come in!")
```

**Use `and`** when you only need one answer: yes or no.
**Use nesting** when each problem needs its own message or its own action.

There is no single right answer. What matters is that you can explain your choice.

</details>

## Make: "Can I use the lab?"

A student can use the computer lab only if:

- they have their **student ID**,
- it is **before 4 pm**,
- and a **teacher is present**.

Each missing condition needs its own message. Choose nested or combined conditions. Explain your choice in a comment at the top: `# I chose ___ because ___.`

This is the exercise **Can I use the lab?** in this unit.

## Before you leave

Complete these in your log:

1. Nesting is clearer when ___.
2. `and` is clearer when ___.
3. Were my confident predictions today correct?
