Title: SD VOC - Structure and Usage
Subtitle: The Vocabulary file: all ten record types, and every field of each one.

The VOC — Vocabulary — is the file that makes a command line work. Type a
name, and the command processor looks it up here. The name of a verb, a
file, a paragraph, a stored sentence, a keyword — all of them are records
in the VOC. This page is about the record types, their fields, and what
the verbs that manage the VOC do to them.

SD folds case, so a command may be typed in either case. Commands are shown
here in lower case, which is what this port uses on disk. In the tables,
*italics* mark something you supply and **bold** marks a word typed as it
stands; braces mark an optional part.

> **Every record on this page was read from a stock account VOC on SD Core
> for Windows W1.0-0.** The records were written by `CREATE.ACCOUNT`,
> which copies them from `voc_template` in the system directory. The counts
> are what a standard account holds; an administrator account holds more.

## The ten record types

Field 1, character 1, is the type. The rest of field 1 is free text and is
ignored, so a verb record whose field 1 reads `Verb to compile SD BASIC
program` is type `V` and the rest is a comment. **The first character is
load-bearing and the remaining thirty are not.**

| Type | Name | What it does |
|---|---|---|
| `V` | verb | the common case — dispatches to a program or an internal routine |
| `K` | keyword | a query-processor keyword; four of these are also verbs |
| `S` | sentence | one stored command line |
| `PA` | paragraph | several stored command lines, with flow control |
| `M` | menu | dispatched, but no menu ships |
| `Q` | Q-pointer | an indirect pointer to a file in another account |
| `F` | file | a file — local, or pointing into `@SDSYS` |
| `R` | remote | a pointer to a record in another file, re-read and re-parsed |
| `X` | text | miscellaneous data — not a command |
| `D` | descriptor | a data descriptor, which is what dictionary records are |

**`PQ` is a valid type and is refused.** PROC was removed from this port
(23 Aug 2026). A record of type `PQ` is reported as *"PROC is not
supported"* rather than being dispatched, because the record itself is
valid PROC and it is the interpreter that is gone.

### What a stock VOC holds

Read from `voc_template` in the system directory, a stock account VOC
carries 426 records:

| Type | Count |
|---|---|
| `V` | 137 |
| `K` | 248 |
| `F` | 16 |
| `R` | 10 |
| `PA` | 4 |
| `S` | 2 |
| `PH` | 2 |
| `Q` | 2 |
| `X` | 3 |
| `Verb - Full screen editor` | 2 |

The last row is `edit`, the full-screen editor that was removed on 23 Aug
2026. Its type field reads `Verb - Full screen editor` rather than `V`,
which means it is not a verb and cannot be dispatched — but it is still in
the template, and `EDIT` at the command prompt reports *"Full screen editor
is no longer supported"* rather than *"verb not found"*. **Being in the VOC
is not evidence a command works.**

## The F record — a file

```
001  F
002  bp
003
```

This is the `bp` entry — the BASIC source file. Field 1 is `F`, field 2 is
the operating-system path to the data portion, and field 3 is the path to
the dictionary portion. An empty field 3 means the file has no separate
dictionary.

| Field | |
|---|---|
| `1` | `F`, optionally followed by a comment |
| `2` | data path — a name in the account directory, or `@SDSYS/`*name* for a system file |
| `3` | dictionary path, or empty if none |

### The eight pointers into @SDSYS

A stock account VOC carries eight F-records whose data path begins
`@SDSYS/`. They point at files in the system directory that every account
needs:

| VOC id | Field 2 |
|---|---|
| `voc` | `@SDSYS/voc.dic` (field 3 — the dictionary) |
| `newvoc` | `@SDSYS/newvoc` |
| `messages` | `@SDSYS/messages` |
| `syscom` | `@SDSYS/syscom` |
| `$MAP` | `@SDSYS/...` |
| `dict.dic` | `@SDSYS/...` |
| `sd.voclib` | `@SDSYS/...` |
| `$ipc` | (system IPC file) |

These are **read-only to a network session**. The account-root gate in
the file engine allows them on read paths but sets `FV_RDONLY` on the
file variable, so every write path in the engine refuses them. An
administrator in `SDSYS` is exempt; an ordinary account cannot write
these files.

### The $ACC record

```
001  F
002  .
003
```

`$ACC` is the account itself. Field 2 is `.`, which means the current
account directory. It is how a program opens "the account I am in" by
name rather than by path.

## The V record — a verb

```
001  V
002  CA
003  $CREATEF
004
```

This is `create.file`. Field 2 is the dispatch type, field 3 is the
target, and the remaining fields carry options.

| Field 2 | Field 3 | What it does |
|---|---|---|
| `CA` | *catalogue name* | a catalogued program — 99 of the shipped verbs |
| `IN` | *number* | internal verb *n*, handled by the command processor itself — 42 verbs |
| `OS` | *text* | an operating-system command — `sh` and `!`, and nothing else |
| `CS` | *path* | a locally catalogued function |

Those four rows account for 143 of the 147 verbs an administrator account has.
The remaining four are the keyword records described above — `break`, `count`,
`display` and `off` — where field 2 holds a keyword number rather than a
dispatch type, and it is field 3 that marks the record as a verb.

Field 4 carries dispatch options and **field 5 names a security subroutine**.
If field 5 is present, that subroutine is called before the verb runs and
can refuse it. **None of the shipped verbs uses field 5** — the tiering
in this port is done by giving or withholding the VOC record, not by a
security subroutine — but the mechanism is there for a site that wants a
verb guarded rather than absent.

### Internal verbs

`IN` verbs are numbered, and the numbers are positional in the command
processor's dispatch list. Several names share one: `off` and `quit` are
both internal verb 1, `clr` and `cs` are both 2, and each of `clear.data`,
`clear.input`, `clear.prompts` and `clear.select` has a run-together
spelling (`cleardata` and the rest) pointing at the same number.

### The four keyword-verbs

Four records ship as a keyword **and** a verb in one: `break`, `count`,
`display` and `off`. Their field 2 is the keyword number the query
processor uses, and **fields 3 onward are a complete verb record**, which
the command processor re-parses when the name is typed as a command.

**This matters for counting what an account has.** A tally of VOC
records whose field 1 begins with `V` misses all four, and `count` is not
a marginal verb. A standard account has **82** verbs, not 78.

## The Q record — an indirect pointer

```
001  Q
002  SDSYS
003  accounts
```

This is `sd.accounts`. Field 2 is the account name, field 3 is the file
name in that account. `set.file` writes Q-pointers; see below.

`md` is a Q-pointer to `voc` — the VOC's own dictionary is reached
through it, and it is how `dict voc` finds its records.

## The R record — a remote record reference

```
001  R
002  SD.VOCLIB
003  listf
```

This is `listf`. Field 2 is the file name, field 3 is the record id. An
R-record is **re-read and re-parsed every time it is used**, so editing
the referenced record changes what the command does without touching the
VOC entry. The `LIST` family — `listf`, `listfl`, `listfr`, `listk`,
`listpa`, `listph`, `listq`, `listr`, `lists`, `listv` — are all
R-records pointing into `SD.VOCLIB`.

## The S record — a sentence

```
001  S
002  DISPLAY <<@PATH>>
```

This is `where`. A sentence is one stored command line. Typing its name
runs that line with anything else you typed appended, so a sentence is a
command with its first arguments filled in.

## The PA record — a paragraph

```
001  PA
002  TERM WINDOWS
003  TERM 120,36
004  PTERM CASE NOINVERT
```

This is `login`, the paragraph that runs at sign-on. A paragraph holds
several lines and has flow control: `if`, `go`, `stop`, `abort`,
`display`, `pause`. Paragraphs nest, and `abort` unwinds all of them.

**`data` lines are read ahead of the verb, not executed in sequence.**
Before a verb runs, the command processor scans forward over any
immediately following `data`, comment and blank lines and stacks their
text as typed-ahead input.

### The PH record — a phrase

```
001  PH
002  GRAND.TOTAL "'L'"
```

This is `no.grand.total`. A phrase is a stored fragment that is
substituted into a command line wherever its name appears. `PH` is
treated as `S` for most purposes — the difference is that a phrase is
designed to be used inside another command rather than typed on its own.

`without` is also `PH`, holding `WITH NO` — so `list stock without qty`
expands to `list stock with no qty`.

## The K record — a keyword

```
001  K
002  26
```

This is `#`, the comment keyword. Field 2 is the keyword number the query
processor uses. Keywords are not commands in their own right; they are
the words the query processor — `LIST`, `SELECT`, `SORT` and the rest —
recognises inside a command line. `all` is `K` with number 5; `after` is
`K` with a number; `and` is `K`.

The 248 K-records in a stock VOC are the query processor's vocabulary,
and they are what makes a sentence like `list stock with qty > 100 by
supplier` parse.

## The X record — text

```
001  X
002  Most of SD is licensed under the GPL v3.0 ...
```

This is `$licence`. An X-record is **not a command** — it is miscellaneous
data the VOC holds so that a program or a user can read it by name.
`$contrib` and `$RELEASE` are also X-records. Nobody dispatches them; they
are read with `read` from BASIC or with `ct` from the command line.

## Continued in

[SD VOC - Using and Managing the VOC](32a-sd-voc-in-use.html) — how the
command processor uses the VOC, the verbs that manage it, and account
creation.
