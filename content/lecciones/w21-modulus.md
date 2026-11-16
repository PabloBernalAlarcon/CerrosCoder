# Even, odd and repeating patterns

**This week's question:** How can a program tell even from odd, or find a pattern that repeats?

## Hook

*It's 10:00 now. What time will it be in 50 hours?*

Solve it on paper. Then explain **how** you calculated it.

<details>
<summary>Check your answer</summary>

**12:00.** 50 hours is 2 full days (48 hours) and 2 more hours. The full days don't change the clock, so only the **remainder**, 2 hours, matters: 10 + 2 = 12.

</details>

## Two new operators

- `//` divides and keeps only the **whole part**: `50 // 24` is `2` (2 full days).
- `%` (modulus) gives the **remainder**: `50 % 24` is `2` (2 hours left over).

## Predict

Rate your confidence for each one.

```python
print(10 % 3)
print(12 % 4)
print(7 % 10)
print(2026 % 4)
print(50 // 24)
print(50 % 24)
```

<details>
<summary>Check your prediction</summary>

| Code | Result | Why |
|---|---|---|
| `10 % 3` | `1` | 10 = 3 × 3 + **1** |
| `12 % 4` | `0` | 12 = 4 × 3 + **0** |
| `7 % 10` | `7` | 7 = 10 × 0 + **7** |
| `2026 % 4` | `2` | 2026 = 4 × 506 + **2** |
| `50 // 24` | `2` | 24 fits **2** whole times in 50 |
| `50 % 24` | `2` | 50 = 24 × 2 + **2** |

</details>

## Investigate

In the **Week 21 lab**:

1. Print `n % 3` for every `n` in `range(12)`. What pattern appears? Why does it repeat?
2. Which condition tests whether a number is **even**? Test it with negative numbers too.

<details>
<summary>Check: what did you find?</summary>

1. `0 1 2 0 1 2 0 1 2 0 1 2`. The remainder when you divide by 3 can only be 0, 1 or 2, and it cycles.
2. `n % 2 == 0` means even. In Python it works for negative numbers too: `-4 % 2` is `0`.

`a % b == 0` means "a is **divisible** by b".

</details>

## Make: choose one

The exercises in this unit include:

- **Leap year checker:** divisible by 4, except century years, unless divisible by 400. Test with 2024, 1900, 2000 and 2026.
- **Minutes converter:** turn total minutes into hours and minutes.
- **Ping-Pong:** print 1 to 30, with `Ping` for multiples of 3, `Pong` for multiples of 5, and `PingPong` for both.

## Before you leave

Complete these in your log:

1. `%` gives me ___.
2. A problem from my own life where `%` would help is ___.
