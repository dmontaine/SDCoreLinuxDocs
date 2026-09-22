Title: SD Basic - String Matching and Replacing
Subtitle: Replacing, wrapping, comparing, pattern matching, quoting and phonetic matching.

This page continues [SD Basic - String
Functions](04-sd-basic-string-functions.html).

## Replacing

```
change(string, old, new {, count {, start}})
swap(string, old, new {, count {, start}})
substitute(array, old.list, new.list {, delimiter})
convert(from.characters, to.characters, string)
convert from.characters to to.characters in variable
```

**`change()` and `swap()` are the same function** — the compiler emits the
same operation for both. Use whichever reads better; there is no behavioural
difference to choose between.

The fourth and fifth arguments are frequently misread:

| | |
|---|---|
| *count* | **how many occurrences to change**, not which one |
| *start* | which occurrence to start at |

| Expression on `'banana'` | Result | |
|---|---|---|
| `change('banana', 'a', 'X')` | `bXnXnX` | all of them |
| `change('banana', 'a', 'X', 2)` | `bXnXna` | the first **two** |
| `change('banana', 'a', 'X', 1, 2)` | `banXna` | one, starting at the second |
| `change('banana', 'a', '')` | `bnn` | an empty replacement deletes |

### `convert()` works on single characters, and deletes

`convert()` maps each character of *from.characters* to the character in the
same position of *to.characters*.

| Expression | Result | |
|---|---|---|
| `convert('abc', 'xyz', 'aabbcc')` | `xxyyzz` | a → x, b → y, c → z |
| `convert('abc', 'x', 'aabbcc')` | `xx` | **b and c were deleted** |

> **A character with no opposite number is removed, not left alone.** If the
> two lists are not the same length, every character in the excess of
> *from.characters* is deleted from the string. This is the documented Pick
> behaviour and it is almost never what someone writing
> `convert(',', '', text)` expects to happen to the rest of their data —
> though it is exactly what they want when deleting is the intent.

`convert` also exists as a **statement**, which modifies a variable in place
rather than returning a value:

```
convert ',' to ';' in line
```

### `substitute()`

`substitute(array, old.list, new.list {, delimiter})` replaces whole
**elements** of a dynamic array rather than characters within them, matching
each element against *old.list*. Substituting `b` with `Z` in the values `a`,
`b`, `c` gives `a`, `Z`, `c`.

## Wrapping text into lines

```
fold(string, width {, delimiter})
```

Breaks *string* into lines of at most *width* characters, **breaking at spaces
where it can** and hard-breaking where a single word is too long.

```
fold('the quick brown fox jumps over the lazy dog', 12, '|')
```

gives

```
the quick|brown fox|jumps over|the lazy dog
```

> **The two-argument and three-argument forms use different default
> separators, which is not an obvious thing to guess.**
>
> | Call | Separator |
> |---|---|
> | `fold(s, 12)` | **field marks** — four fields |
> | `fold(s, 12, '')` | **value marks** — four values |
> | `fold(s, 12, sep)` | whatever *sep* holds — its first character only |
>
> So passing an explicit empty delimiter is **not** the same as omitting it.
> If the mark level matters, give the delimiter explicitly.

**The width may itself be a dynamic array**, giving successive lines different
lengths and reusing the last value once the list runs out:

```
fold(s, 5 : @vm : 20, '|')
```

gives `the|quick brown fox|jumps over the lazy|dog` — a five-character first
line, then twenty. This is how you wrap a paragraph around an indent.

## Comparing and testing

```
compare(string1, string2 {, justification})
alpha(string)
```

`compare()` returns `-1` if *string1* sorts first, `1` if *string2* does, and
`0` if they are equal.

| Expression | Result | |
|---|---|---|
| `compare('abc', 'abd')` | `-1` | |
| `compare('abd', 'abc')` | `1` | |
| `compare('abc', 'abc')` | `0` | |
| `compare('B', 'a')` | `-1` | upper case sorts before lower — byte order |
| `compare('a2', 'a10')` | `1` | plain text order: `2` after `1` |
| `compare('a2', 'a10', 'r')` | `-1` | right-justified: the numbers compare as numbers |

**The `r` justification is how you sort `item2` before `item10`.** Without
it, embedded numbers compare character by character and `10` sorts before `9`.
`l` is the explicit left-justified form and is the default.

`alpha()` is true if every character is a letter.

| Expression | Result | |
|---|---|---|
| `alpha('abc')` | true | |
| `alpha('ab1')` | false | |
| `alpha('')` | **false** | |

> **`alpha('')` is false and `num('')` is true.** The two tests disagree about
> the empty string, so a validation that uses both needs to say which answer it
> wants for an empty field rather than assuming they behave alike. `num()` is
> covered in [SD Basic - Math Functions](03-sd-basic-math-functions.html).

## Pattern matching

```
string matches pattern
matchfield(string, pattern, element)
```

`matches` is an operator and returns true or false. `matchfield()` returns the
part of the string that matched a given element of the pattern.

### The pattern language

| Element | Matches |
|---|---|
| *n**a** | exactly *n* alphabetic characters |
| *n**n** | exactly *n* digits |
| *n**x** | exactly *n* characters of any kind |
| **0a** · **0n** · **0x** | **any number, including none** |
| *n*`-`*m**a** · *n*`-`*m**n** · *n*`-`*m**x** | between *n* and *m* characters |
| `"literal"` | the quoted text, as it stands |
| `~`*element* | anything the element would **not** match |

Elements are written one after another with no separator.

### How the codes combine

| Test | Result |
|---|---|
| `'abc' matches '3a'` | true |
| `'ab12' matches '2a2n'` | true |
| `'abc' matches '0a'` | true |
| `'' matches '0a'` | true |
| `'ab' matches '3x'` | false |
| `'12' matches '2-4n'` | true |
| `'1' matches '2-4n'` | false |
| `'12345' matches '2-4n'` | false |
| `'abc' matches '~3n'` | true |
| `'123' matches '~3n'` | false |
| `'ab-12' matches '2a"-"2n'` | true |
| `'ab12' matches '0a0n'` | true |
| `'a1b2' matches '0a0n'` | false |

**A pattern may be a dynamic array, and the values are alternatives.**
`'ab' matches ('2a' : @vm : '2n')` is **true** — the string need only
match one of them. This is how you accept several formats without writing the
test three times:

```
valid = code matches ('3n' : @vm : '2a4n' : @vm : '"X"5n')
```

### Picking out the parts

`matchfield(string, pattern, element)` returns the text that matched the
*element*-th part of the pattern. On `'ab12'` against `'2a2n'`:

| | |
|---|---|
| `matchfield('ab12', '2a2n', 1)` | `ab` |
| `matchfield('ab12', '2a2n', 2)` | `12` |

That makes a pattern a parser as well as a test — validate with `matches`,
then pull the pieces out with `matchfield()` rather than counting character
positions by hand.

## Quoting

```
quote(expr)
dquote(expr)
squote(expr)
```

| | |
|---|---|
| `quote()` · `dquote()` | wrap in double quotes — `"a"` |
| `squote()` | wrap in single quotes — `'a'` |

**`quote()` and `dquote()` are the same function** — the compiler emits the
same operation for both, so there is nothing to choose between them.

For CSV output do not build quoting by hand: `csvdq()` and the CSV statements
handle embedded quotes and separators to RFC 4180, and are covered in
[SD Basic - CSV Files](11-sd-basic-csv-files.html).

## Phonetic matching

```
soundex(string)
```

Returns a four-character code that is the same for words that sound alike, for
finding a name someone has spelled by ear.

| Expression | Result |
|---|---|
| `soundex('Smith')` | `S530` |
| `soundex('Smyth')` | `S530` |
| `soundex('Robert')` | `R163` |
| `soundex('Rupert')` | `R163` |
| `soundex('O Brien 123')` | `O165` — non-letters are ignored |
| `soundex('')` | **`0000`** |

> **`soundex('')` returns `0000`, not an empty string.** A blank name therefore
> gets a code, and every blank name gets the *same* code — so a search keyed on
> soundex will match all of them together unless you exclude empty input
> first.

Soundex is tuned for English and does poorly on names of other origins. It is a
way to narrow a search, not to decide a match.

## Applying a function to every element

Most functions here have a partner ending in `s` that applies the same
operation to every element of a dynamic array:

| | |
|---|---|
| `lens('one' : @vm : 'three')` | `3` and `5` |
| `counts('a-b' : @vm : 'c-d-e', '-')` | `1` and `2` |
| `fields('a-b' : @vm : 'c-d-e', '-', 1)` | `a` and `c` |
| `trims(' x ' : @vm : '  y  ')` | `x` and `y` |
| `indexs('Ab' : @vm : 'cD', 'b', 1)` | `2` and `0` |
| `soundexs('Smith' : @vm : 'Smyth')` | `S530` and `S530` |
| `spaces(2 : @vm : 3)` | two spaces and three |

The full family, and the rules for how they pair elements when given two
arrays, is in [SD Basic - Dynamic Arrays](05-sd-basic-dynamic-arrays.html).

## What is not here

| | |
|---|---|
| `encrypt()` · `decrypt()` | **removed** — replaced by `sdencrypt()` and `sddecrypt()` |

Nothing else in the string-handling group has been removed. `dparse` and
`dparse.csv` are statements rather than functions and are covered in
[SD Basic - Data Conversion](06-sd-basic-data-conversion.html) and [SD Basic - CSV Files](11-sd-basic-csv-files.html); `iconv()`, `oconv()`,
`fmt()`, `char()`, `seq()`, `ascii()` and `ebcdic()` are in
[SD Basic - Data Conversion](06-sd-basic-data-conversion.html); `extract()`, `insert()`, `delete()`, `replace()`,
`locate`, `remove`, `raise()`, `lower()`, `vslice()` and `dcount()` used
against marks are in [SD Basic - Dynamic Arrays](05-sd-basic-dynamic-arrays.html).

## See also

[SD Basic - Dynamic Arrays](05-sd-basic-dynamic-arrays.html) · [SD Basic - Data Conversion](06-sd-basic-data-conversion.html) ·
[SD Basic - Math Functions](03-sd-basic-math-functions.html) · [SD Basic - CSV Files](11-sd-basic-csv-files.html).
