Title: SD Basic - Dynamic Arrays
Subtitle: Fields, values and subvalues - reading, changing and searching the structure that holds every SD record.

A dynamic array is a string with structure in it. Three mark characters divide
it into **fields**, **values** and **subvalues**, and every record SD reads or
writes is one. This page covers the statements and functions that work on that
structure.

The functions that treat the same string as plain text are in
[SD Basic - String Functions](04-sd-basic-string-functions.html); the two pages overlap where a function is used
both ways, and each says so.

SD folds case, so a program may be written in either case. Keywords are shown
here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

> **In the examples below, `^` stands for a field mark, `|` for a value mark
> and `\` for a subvalue mark.**

## The marks

| | Name | Constant | Code |
|---|---|---|---|
| ^ | field mark | `@fm` | 254 |
| \| | value mark | `@vm` | 253 |
| \\ | subvalue mark | `@sm` | 252 |

They nest: a field contains values, a value contains subvalues. There is a
fourth, `@tm` (text mark, 251), used by `fmt()` and by some conversions, and
`@im` (item mark, 255), which SD uses internally.

```
a = 'f1' : @fm : 'v1' : @vm : 'v2' : @fm : 'f3'
```

gives `f1^v1|v2^f3` — three fields, the second of which holds two values.

**The marks are ordinary characters and they are counted.**
`len(a)` is `11` for the array above — eight data characters and three marks.
Everything in [SD Basic - String Functions](04-sd-basic-string-functions.html) sees them.

```
dcount(string, delimiter)
```

counts the pieces a delimiter divides a string into. On the array
above, `dcount(a, @fm)` is `3` and `dcount(a<2>, @vm)` is `2`.

> **`dcount()` of an empty string is `0`, not `1`.** That is what makes
> `for i = 1 to dcount(rec, @fm)` correct — an empty record does nothing.

## Reading a piece

```
array<field {, value {, subvalue}}>
extract(array, field {, value {, subvalue}})
```

The angle-bracket form and `extract()` are the same operation.

| Expression on `f1^v1\|v2^f3` | Result |
|---|---|
| `a<2>` | `v1\|v2` — the whole field, marks and all |
| `a<2,2>` | `v2` |
| `a<2,1,1>` | `v1` |
| `extract(a, 2, 1)` | `v1` |
| `a<9>` | *empty* |

**Reading past the end is not an error.** `a<9>` on a three-field array
returns the null string, exactly as a genuinely empty field would. **There is
no way to tell "field 9 is empty" from "there is no field 9"** — use
`dcount()` if the difference matters.

Asking for a value of a field that has none returns the whole field: `a<1,1>`
is `f1`.

## Changing a piece

```
array<field {, value {, subvalue}}> = expression
replace(array, field, value, subvalue, expression)
insert(array, field, value, subvalue, expression)
delete(array, field {, value {, subvalue}})
```

| Expression on `f1^v1\|v2^f3` | Result |
|---|---|
| `b<2,2> = 'NEW'` | `f1^v1\|NEW^f3` |
| `replace(a, 2, 2, 0, 'R')` | `f1^v1\|R^f3` |
| `insert(a, 2, 2, 0, 'I')` | `f1^v1\|I\|v2^f3` — pushes the rest along |
| `delete(a, 2, 1)` | `f1^v2^f3` — removes one value |
| `delete(a, 2)` | `f1^f3` — removes the whole field |

The assignment form is what almost all code uses. `replace()` and `insert()`
exist for when you need the result as an expression rather than assigned back.

> **`replace()` and `insert()` count their arguments greedily, and the short
> forms need a semicolon.** `replace(a, 2, 2, 'R')` **does not compile** — the
> parser takes `2` as the value, `'R'` as the subvalue, and then demands the
> replacement string it never got. Either give all five arguments, or separate
> the final one with a semicolon.
>
> | Call | Result |
> |---|---|
> | `replace(a, 2, 2, 0, 'R')` | `f1^v1\|R^f3` |
> | `replace(a, 2; 'S')` | `f1^S^f3` — replaces the whole field |
> | `replace(a, 2, 2; 'T')` | `f1^v1\|T^f3` |
> | `replace(a, 2, 2, 'R')` | **compile error** |

### Appending

A subscript of `-1` appends:

| | Result |
|---|---|
| `b<-1> = 'APP'` | `f1^v1\|v2^f3^APP` — a new field at the end |
| `b<2,-1> = 'AV'` | `f1^v1\|v2\|AV^f3` — a new value in field 2 |

**Writing past the end pads with empty fields rather than failing.**
`insert(a, 9, 0, 0, 'FAR')` on a three-field array gives
`f1^v1|v2^f3^^^^^^FAR` — five empty fields appear to fill the gap. A loop with
an off-by-one index therefore grows the record silently instead of raising
anything.

### The statement forms

```
del array<field {, value {, subvalue}}>
ins string before array<field {, value {, subvalue}}>
```

`del` and `ins` change the variable in place. `del b<2>` gives
`f1^f3`, and `ins 'X' before b<2>` gives `f1^X^v1|v2^f3`.

## Searching

### `locate`

```
locate expression in array<field {, value {, subvalue}}> {by order} setting variable
   then statements
else statements

locate(expression, array, field {, value {, subvalue}})
```

`locate` finds a whole element and reports its position. When it does not find
one, `setting` receives **the position where it would be inserted** to keep the
order — which is what makes it the standard way to add to a sorted list.

**The number of subscripts chooses the level searched. this is the thing
people get wrong.** With `vals` holding `apple|cherry|damson` as
three values in one field:

| Statement | Result |
|---|---|
| `locate 'cherry' in vals<1> setting p` | **miss**, insert at 2 |
| `locate 'cherry' in vals<1,1> setting p` | **found at 2** |

`array<f>` searches the **fields**, starting at field *f*. `array<f,v>`
searches the **values of field f**, starting at value *v*. `array<f,v,s>`
searches subvalues. So a single subscript on an array of values finds nothing,
silently, and reports an insertion point — which looks like a working search
right up until the data has two fields.

**The statement form requires the angle brackets.** `locate 'x' in vals setting
p` does not compile: *"Field reference not found where expected"*.

The starting subscript really does start there. With
`vals<1,2>`, `locate 'apple'` — which is value 1 — **misses**, and reports an
insertion point of 4.

The function form takes the position as arguments instead, and returns the
position or zero:

| Call | Result |
|---|---|
| `locate('cherry', vals, 1)` | `0` — searched fields |
| `locate('cherry', vals, 1, 1)` | `2` — searched values |
| `locate('zebra', vals, 1, 1)` | `0` |

### Order codes

Without `by`, `locate` scans the whole list and the insertion point is the end.
With `by`, it assumes the list is already sorted that way, stops as soon as it
passes the place the value would go, and reports that place.

| Code | Order |
|---|---|
| **al** | ascending, left-justified — ordinary text order |
| **ar** | ascending, right-justified — numbers compare as numbers |
| **dl** | descending, left-justified |
| **dr** | descending, right-justified |

For `apple|cherry|damson`:

| Search | Insert at |
|---|---|
| `'aardvark' by 'al'` | `1` |
| `'banana' by 'al'` | `2` |
| `'zebra' by 'al'` | `4` |

**And the justification is not a detail.** For the values `2`, `10`,
`30`, looking for `9`:

| | Insert at |
|---|---|
| `by 'al'` | **4** — as text, `9` sorts after `30` |
| `by 'ar'` | **2** — as numbers, between `2` and `10` |

**Use `ar` for anything numeric.** `al` on numbers produces a list that looks
sorted in short test data and comes apart at ten items.

`by` on a list that is *not* actually sorted that way stops early and reports a
miss for a value that is present.

### `find` and `findstr`

```
find string in array {, occurrence} setting field {, value {, subvalue}}
findstr string in array {, occurrence} setting field {, value {, subvalue}}
```

`find` matches a **whole element**; `findstr` matches **any element containing
the string**. Both report the position as separate field, value and subvalue
numbers rather than one index.

For `p^q|r`:

| | Result |
|---|---|
| `find 'r' in d setting f, v, s` | field 2, value 2, subvalue 1 |
| `findstr 'q' in d setting f, v` | field 2, value 1 |

## Continued in

[SD Basic - Operating on Whole Arrays](05a-sd-basic-array-operations.html) —
walking an array, mark levels, the s functions, logical functions, sorting and
mark mapping.
