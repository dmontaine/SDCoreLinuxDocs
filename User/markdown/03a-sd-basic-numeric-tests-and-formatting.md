Title: SD Basic - Numeric Tests and Formatting
Subtitle: Reducing arrays to a number, testing what is numeric, bit operations, checksums and print formatting.

This page continues [SD Basic - Math
Functions](03-sd-basic-math-functions.html).

## Reducing a dynamic array to a number

These take a dynamic array and give a single value, or a shallower array.

```
sum(array)
summation(array)
maximum(array)
minimum(array)
```

| | |
|---|---|
| `sum()` | adds the elements at the **lowest mark level present** and returns an array one level shallower. Subvalues become values, values become fields |
| `summation()` | adds **every** element at every level and returns one number |
| `maximum()` | the largest numeric element |
| `minimum()` | the smallest numeric element |

### Worked through

With `a` holding `1`, `2`, `3` as values, and `b` holding a field of
`10`ˢ`20` and `30`, where ˢ is a subvalue mark:

| Expression | Result |
|---|---|
| `sum(a)` | `6` |
| `sum(b)` | `30` and `30` as two values — the subvalues collapsed, the value did not |
| `summation(b)` | `60` |
| `maximum(a)` | `3` |
| `minimum(a)` | `1` |

> **All four silently skip anything that is not a number.** With `1`, `two`,
> `3` in an array, `sum()` returns `4` and `maximum()` returns `3`. Nothing is
> reported. **If a non-numeric element means your data is wrong, you have to
> test for it yourself** — walk the array with `num()` before summing.
>
> `maximum()` and `minimum()` return the **null string**, not zero, when there
> is no numeric element at all. Test for that with `if result = '' then`,
> because a numeric test would read the null string as zero and cannot tell it
> from a genuine maximum of zero.

While developing, `option non.numeric.warning` makes SD report a non-numeric
value used where a number was expected, which turns a class of silent wrong
answers into something you can see. It is off by default. `option` on its own
lists every option and its current state; `option all off` clears them.

Negative values are handled correctly: `maximum()` of `-5` and `-3` is `-3`.

### Comparing two values

```
max(expr1, expr2)
min(expr1, expr2)
```

These take **two values, not an array**, and return the larger or smaller.
Unlike the four above they are not restricted to numbers: they use SD's general
comparison, so `max('abc', 'abd')` returns `abd`. `max(3, 7)` returns `7`.

## Testing whether a value is a number

```
num(expr)
```

Returns true if *expr* would be accepted as a number, false otherwise.

### What it accepts

| Expression | Result | |
|---|---|---|
| `num('12')` | true | |
| `num('12.5')` | true | |
| `num('.5')` | true | a leading decimal point is fine |
| `num('+3')` | true | a leading sign is fine |
| `num('')` | **true** | **the null string is numeric** |
| `num(' 12')` | false | no leading space |
| `num('12 ')` | false | no trailing space |
| `num('3-')` | false | a trailing sign is not accepted |
| `num('1e3')` | false | no exponent notation |
| `num('123456789012345')` | true | 15 digits before the point |
| `num('1234567890123456')` | false | 16 is too many |

> **`num('')` is true, and it is the single most common source of a wrong
> answer from this function.** An empty field passes the test and then
> evaluates as zero, so a validation written as `if num(value) then ...`
> accepts a blank. **Test for the null string first:**
>
> ```
> if value # '' and num(value) then
>    ...
> end
> ```
>
> The rule is consistent with the rest of SD, where an empty value is zero in
> a numeric context — but the function reads like a validator and is not one.

`nums()` applies the same test to every element of a dynamic array. See
[SD Basic - Dynamic Arrays](05-sd-basic-dynamic-arrays.html) for the whole family of `s` functions.

## Bit operations

These work on **32-bit signed integers**. A value outside that range is
truncated to fit.

```
bitand(expr1, expr2)      bitset(expr, bit)
bitor(expr1, expr2)       bitreset(expr, bit)
bitxor(expr1, expr2)      bittest(expr, bit)
bitnot(expr)              shift(expr, distance)
```

| | |
|---|---|
| `bitand()` | bitwise AND. `bitand(12, 10)` is `8` |
| `bitor()` | bitwise OR. `bitor(12, 10)` is `14` |
| `bitxor()` | bitwise exclusive OR. `bitxor(12, 10)` is `6` |
| `bitnot()` | bitwise NOT — every bit inverted. `bitnot(0)` is `-1` |
| `bitset()` | returns *expr* with the given bit set. `bitset(0, 3)` is `8` |
| `bitreset()` | returns *expr* with the given bit cleared. `bitreset(15, 0)` is `14` |
| `bittest()` | true if the given bit is set. `bittest(8, 3)` is true, `bittest(8, 2)` is false |
| `shift()` | shifts the bits. **A negative distance shifts left, a positive distance shifts right** |

**Bits are numbered from zero, and zero is the least significant bit.** So
bit 3 has the value 8, and bit 31 is the sign bit. **There is no range check on
the bit number** — a value outside 0 to 31 gives an unpredictable result rather
than an error, so validate it yourself if it is calculated.

> **`shift()`'s direction is the reverse of what the name suggests, and its
> right shift does not preserve the sign.** `shift(1, -4)` is `16` — shifted
> left. `shift(256, 4)` is `16` — shifted right. And `shift(-1, 1)` is
> `2147483647`, not `-1`: the value is treated as unsigned, so a right shift
> brings in zeros rather than copying the sign bit. **Do not use `shift()` to
> divide a signed number by a power of two** — use `div()`.

## Checksums

```
checksum(expr)
```

Returns a 32-bit integer derived from the bytes of *expr*. It is cheap and it
changes when the data changes — `checksum('hello')` is `1199` and
`checksum('hellp')` is `1200` — which makes it useful for spotting that a
record has been altered since you last read it.

> **It is not a cryptographic hash and must not be used as one.** It is a
> rotate-and-exclusive-or over the bytes, and it is straightforward to
> construct a different string with the same result. It will not detect
> deliberate tampering, and it must never be used to store or compare a
> password. `checksum('')` is `0`, so an empty value and a failed read are
> indistinguishable by checksum alone.

For real cryptography this port provides `sdencrypt()` and `sddecrypt()`. The
older `encrypt()` and `decrypt()` functions **have been removed** and programs
using them will not compile.

## Controlling how numbers print

```
precision n
```

Sets how many decimal places are used when a floating-point number is converted
to a string — by `print`, by concatenation, by writing to a file. It does not
change the accuracy of the arithmetic itself, only what you see and what gets
stored.

**The default is 4.** *n* may be 0 to 14; a value outside that range is pulled
to the nearest end rather than refused.

| | |
|---|---|
| `1 / 3` at the default | `0.3333` |
| `1 / 3` after `precision 8` | `0.33333333` |
| `1 / 3` after `precision 0` | `0` |
| `1 / 3` after `precision 20` | `0.33333333333333` — clamped to 14, not refused |

> **Precision is per program and it does not travel with a call.** Every
> program starts at 4, including one you `call`, and setting it in a caller has
> no effect inside the subroutine. It is restored to the caller's value when the
> subroutine returns. **A subroutine that formats numbers must set its own
> `precision`** — a common cause of a report where the totals show four decimal
> places and the line items show something else.

Where you need a specific layout rather than a number of decimals, use `fmt()`
and the output conversion codes instead; they are covered in
[SD Basic - Data Conversion](06-sd-basic-data-conversion.html).

### Comparing floating-point numbers

Two floating-point values are treated as equal if they differ by less than the
`FLTDIFF` configuration parameter, which defaults to a very small number
(`0.0000000000291`).

**This is why `0.1 + 0.2 = 0.3` is true in SD BASIC**, where the
same test is false in C, Java, Python and JavaScript. It is a deliberate
convenience and not an accident of this port. `config('FLTDIFF')` reports the
value in force.

**It also means two values that differ in the fourteenth decimal place compare
as equal**, so a comparison is not a safe way to detect a tiny drift. If you
need to know that two numbers really are bit-identical, compare their string
forms after `precision 14`.

## Applying a function to every element

Several of the functions above have a partner ending in `s` that applies the
same operation to every element of a dynamic array instead of to a single
value: `abss()`, `negs()`, `mods()`, `nums()`.

```
abss(-1 : @vm : 2 : @vm : -3)     ;* gives 1, 2, 3 as three values
```

The whole family — including the string and comparison members — is described
in [SD Basic - Dynamic Arrays](05-sd-basic-dynamic-arrays.html).

## What is not here

These existed in OpenQM and in earlier SD releases and **are not in SD Core for
Windows**. A program using one will not compile.

| | |
|---|---|
| `encrypt()` · `decrypt()` | replaced by `sdencrypt()` and `sddecrypt()` |

Nothing else in the mathematical and logical group has been removed: every
function the OpenQM 2.6.6 documentation lists under that heading is present in
this port, and this page covers the numeric ones. The comparison and logical
members of the group — `ands()`, `ors()`, `nots()`, `eqs()`, `nes()`, `gts()`,
`ges()`, `lts()`, `les()`, `ifs()`, `not()`, `reuse()` — are documented in
[SD Basic - Dynamic Arrays](05-sd-basic-dynamic-arrays.html), where their multivalue behaviour is the point.

## See also

[SD Basic - Dynamic Arrays](05-sd-basic-dynamic-arrays.html) · [SD Basic - Data Conversion](06-sd-basic-data-conversion.html) ·
[SD Basic - String Functions](04-sd-basic-string-functions.html) · the `config` verb, for `INTPREC` and `FLTDIFF`.
