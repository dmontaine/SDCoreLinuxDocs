Title: SD Basic - Data Conversion
Subtitle: Dates, times, numbers and text between the form SD stores and the form people read.

SD stores a date as a day number and a time as a second count. Neither is
readable, and neither is what a user types. `iconv()` turns what a person wrote
into what SD stores; `oconv()` turns it back. `fmt()` lays a value out in a
fixed width. This page covers all three, and the character-level conversions
beside them.

SD folds case, so a program may be written in either case. Keywords and
conversion codes are shown here in lower case; **the codes themselves are not
case sensitive**. In the tables, *italics* mark something you supply.

## The two directions

```
iconv(expression, conversion)
oconv(expression, conversion)
```

| | |
|---|---|
| `iconv()` | **in** — external form to internal. Use it on input |
| `oconv()` | **out** — internal to external. Use it on output |

`iconvs()` and `oconvs()` do the same to every element of a dynamic array.

**A failed `iconv()` returns the null string and sets `status()`.**
`iconv('nonsense', 'D')` returns empty and `status()` afterwards is **1**.

```
d = iconv(typed.date, 'D')
if status() then
   print 'That is not a date.'
end
```

**This is the validation idiom, and the return value alone is not enough** — a
user who typed nothing also gets an empty result, so testing the result cannot
tell an empty input from a bad one. `status()` can.

## Dates

```
iconv(text, 'D')
oconv(daynumber, 'D{n}{separator}{format}')
```

**Day zero is 31 December 1967.** `oconv(0, 'D4/')` is
`12/31/1967`. Dates before that are negative. `26 AUG 2026` is day **21423**.

| Conversion | Result for day 21423 |
|---|---|
| `oconv(d, 'D')` | `26 AUG 2026` |
| `oconv(d, 'D2/')` | `08/26/26` |
| `oconv(d, 'D4-')` | `08-26-2026` |
| `oconv(d, 'DMA')` | `AUGUST` |
| `oconv(d, 'DW')` | `3` — day of the week |
| `oconv(d, 'DWA')` | `WEDNESDAY` |
| `oconv(d, 'DQ')` | `3` — quarter |
| `oconv(d, 'DY')` | `2026` |

The digit after `D` is how many digits of year to show; the character after
that is the separator.

> **The default order is month, day, year.** `D2/` gives
> `08/26/26` for the 26th of August. **`E` puts it in day-month-year order**:
> `D2/E` gives `26/08/26` and `D4/E` gives `26/08/2026`. A site that
> expects day-first must say `E` on **every** conversion; a report that mixes
> the two is a formatting bug that reads as a data bug.

`iconv()` accepts a wide range of typed forms — `26 AUG 2026`, `08/26/2026`,
`26-8-26` — and resolves a two-digit year against a sliding window. **Always
check `status()`**: `13/13/26` is not a date and will come back empty.

## Times

```
iconv(text, 'MT')
oconv(seconds, 'MT{H}{S}')
```

A time is the number of seconds since midnight. `14:30:05` is
**52205**.

| Conversion | Result |
|---|---|
| `oconv(t, 'MT')` | `14:30` |
| `oconv(t, 'MTS')` | `14:30:05` |
| `oconv(t, 'MTH')` | `02:30pm` |
| `oconv(t, 'MTHS')` | `02:30:05pm` |

`s` adds seconds, `h` switches to a 12-hour clock. `date()` and `time()` give
today's day number and the current second count; `timedate()` gives both,
already formatted.

## Numbers

### Scaling and separators

```
oconv(number, 'MD{n}{separator}')
```

`md`*n* moves the decimal point *n* places **left**, so the stored value is an
integer and the displayed one has decimals.

| Conversion | Result |
|---|---|
| `oconv(1234567, 'MD2')` | `12345.67` |
| `oconv(1234567, 'MD2,')` | `12,345.67` |
| `oconv(1234567, 'MD0,')` | `1,234,567` |
| `oconv(-42, 'MD2')` | `-0.42` |

> **`MD2` divides by 100 — it does not round to two places.**
> `oconv(-42, 'MD2')` is `-0.42`, not `-42.00`. It is for money held as whole
> pence or cents. **To show two decimals of a value that is already scaled, use
> `fmt()`** with a `2` after the justification.

### Other bases

| Conversion | Result |
|---|---|
| `oconv(255, 'MX')` | `FF` |
| `iconv('FF', 'MX')` | `255` |
| `oconv(5, 'MB')` | `101` |
| `oconv(8, 'MO')` | `10` |

`mx` hexadecimal, `mb` binary, `mo` octal. `xtd()` and `dtx()` do the same for
hex without going through `oconv()` — see *Characters and codes* below.

### Selecting characters

| Conversion | Result |
|---|---|
| `oconv('abc', 'MCU')` | `ABC` |
| `oconv('ABC', 'MCL')` | `abc` |
| `oconv('hello world', 'MCT')` | `Hello World` |
| `oconv('a1b2', 'MCN')` | `12` — digits only |
| `oconv('a1b2', 'MCA')` | `ab` — letters only |

`mcn` and `mca` **discard** everything else rather than replacing it, which
makes them a quick way to strip formatting out of a typed reference.

## Laying a value out: `fmt()`

```
fmt(expression, specification)
fmts(array, specification)
```

The specification is a width, a justification, and optional extras.

| Call | Result |
|---|---|
| `fmt('ab', '10L')` | `ab␣␣␣␣␣␣␣␣` — left, padded to 10 |
| `fmt('ab', '10R')` | `␣␣␣␣␣␣␣␣ab` — right |
| `fmt('ab', '10*R')` | `******ab` — padded with `*` |
| `fmt(1234.5, '12R2')` | `␣␣␣␣␣1234.50` — two decimals, right |

The character before the justification letter is the fill character; a digit
after it is the number of decimal places.

> **A value longer than the width is wrapped, not truncated.**
> `fmt('abcdefgh', '4L')` returns `abcd` and `efgh` separated by a **text
> mark**, not `abcd`. A field written straight to a screen or a file therefore
> gains a stray character rather than being cut short. **To truncate, take a
> substring first** — `fmt(s[1,4], '4L')`.

### The format qualifier

The same thing can be written by placing the specification **straight after the
value, with nothing between them**:

```
print total '10r2'
```

With `t` holding `1234.5`, `t '10R2'` gives `␣␣␣1234.50`. **There is
no `fmt` keyword in this form** — writing `t fmt '10R2'` compiles `fmt` as a
variable name and aborts at run time with *"Unassigned variable FMT"*. The
qualifier is recognised by juxtaposition alone, which is why it is allowed only
where an expression cannot be followed by something else.

## Characters and codes

| Call | Result |
|---|---|
| `char(65)` | `A` |
| `seq('A')` | `65` |
| `seq('')` | `0` |
| `xtd('FF')` | `255` |
| `dtx(255)` | `ff` |
| `dtx(255, 4)` | `00ff` |

| | |
|---|---|
| `char()` | the character with the given code |
| `seq()` | the code of the first character. **`seq('')` is `0`**, the same as `seq(char(0))` |
| `xtd()` | hexadecimal text to a number |
| `dtx()` | a number to hexadecimal text, **in lower case**, optionally zero-padded to a width |
| `ascii()` · `ebcdic()` | translate a string between the two character sets |

`ascii(char(193))` is `A` — EBCDIC 193 is the letter A.

**`char()` is how you write a mark character or a control code as a constant**,
and `equate` is the place to put it:

```
equate esc to char(27)
equate fm to char(254)
```

## Splitting a delimited string

```
dparse string, delimiter, var1, var2, ...
```

Splits *string* on *delimiter* and assigns the pieces to the named variables in
order. It is the fixed-shape alternative to a `remove` loop: use it when you
know how many pieces there are and want them in named variables rather than an
array.

Missing pieces leave their variables empty; extra pieces are discarded.

`dparse.csv` does the same for a CSV line, honouring quoting — see
[SD Basic - CSV Files](11-sd-basic-csv-files.html).

## Dictionary conversions

```
itype(dictionary.record)
```

Evaluates a dictionary item — an I-type expression — against the record
currently being processed, and returns what it computes. It is how a program
uses the same derived field a query would, instead of duplicating the formula.

`trans()`, `rtrans()` and `xlate()` fetch a field from another file and can
apply that file's own conversion; they are covered in
[SD Basic - File Handling](07-sd-basic-file-handling.html) because they open a file to do it.

## National settings

```
getnls(key)
setnls key, value
```

Report and set the national-language settings — currency symbol, thousands and
decimal separators, date order. **`setnls` changes them for the session**, so a
program that alters them and then aborts leaves the session changed. Read the
old value, set the new, and restore it on the way out.

## What is not here

Nothing in the conversion group has been removed from this port.

`fmt()`, `char()`, `seq()`, `ascii()`, `ebcdic()` and the `convert` statement
are also mentioned in [SD Basic - String Functions](04-sd-basic-string-functions.html), where they are used on
text rather than for conversion. `precision`, which decides how many decimal
places a floating-point number shows when it becomes a string, is in
[SD Basic - Math Functions](03-sd-basic-math-functions.html).

## See also

[SD Basic - String Functions](04-sd-basic-string-functions.html) · [SD Basic - Math Functions](03-sd-basic-math-functions.html) ·
[SD Basic - File Handling](07-sd-basic-file-handling.html) · [SD Basic - CSV Files](11-sd-basic-csv-files.html).
