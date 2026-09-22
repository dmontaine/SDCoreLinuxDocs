Title: SD Basic - Restricted Commands
Subtitle: The statements and functions an ordinary program cannot compile, and what the compiler says when it tries.

Nothing on this page is available to an application: every name here needs a
program compiled with `$internal`, which in turn needs an administrator in the
`SDSYS` account. They are listed because they exist, because they appear in
SD's own source, and because the errors they produce name something other than
the real cause.

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

*Italics* mark something you supply, **bold** a word typed as it stands, and
braces an optional part.

> **This page is generated from `BCOMP`'s own tables** by
> `tools/mksyntax.py`, the same script that builds the User set's syntax card,
> and the two **partition** the roster: every name the compiler accepts is on
> exactly one of them, and the script refuses to write either page if that
> stops being true.

## The three kinds, and how each one fails

| | |
|---|---|
| ***(restricted)*** | a statement in `BCOMP`'s `restricted.statements`. An ordinary account gets ***"Unrecognised statement"***, which at least names the right line |
| ***(internal)*** | a function in `BCOMP`'s `int.intrinsics`. ***The message names something else entirely***: an unknown function is read as a matrix reference, so the complaint is ***"Matrix X is not referenced in a DIM statement"*** — reported at the **last line of the program**, nowhere near the call. With three or more arguments it is *"Right bracket not found where expected"* instead, because a matrix takes at most two subscripts |
| ***(no such thing)*** | in a table with no opcode behind it. It compiles for **nobody** — `$internal` does not help |

***THE SECOND ROW IS THE ONE TO REMEMBER.*** If a function you are certain
exists produces a complaint about a `dim` statement you never wrote, it does
exist, and this account may not call it.

**`$internal` needs both halves.** `BCOMP` tests
`kernel(K$INTERNAL, -1) and kernel(K$ADMINISTRATOR, -1)` — internal mode alone
was enough until 13 Aug 2026, and it was not safe: internal programs are the
only ones that may set the administrator flag, and `sd -internal` is not itself
gated, so any account could have compiled a three-line program that granted
itself administrator rights. That was demonstrated, not theorised.


## A

| | |
|---|---|
| **`abort.cause`** | `abort.cause()` ***(internal)*** |
| **`add`** | `add` *n* `to` *variable* ***(restricted)*** |
| **`akclear`** | `akclear` *file.var*, *index* `then` … `else` … ***(restricted)*** |
| **`akdelete`** | `akdelete` *file.var*, *index*, *key* `then` … `else` … ***(restricted)*** |
| **`akenable`** | `akenable` *file.var*, *index*, *state* ***(restricted)*** |
| **`akmap`** | `akmap(`*a*, *b*`)` ***(internal)*** |
| **`akread`** | `akread` *var* `from` *file.var*, *index*, *key* `then` … `else` … ***(restricted)*** |
| **`akrelease`** | `akrelease` *file.var*, *index*, *key* ***(restricted)*** |
| **`akwrite`** | `akwrite` *var* `to` *file.var*, *index*, *key* `then` … `else` … ***(restricted)*** |
| **`analyse`** | `analyse(`*a*`)` ***(internal)*** |

## B

| | |
|---|---|
| **`break.count`** | `break.count()` ***(internal)*** |
| **`breakpoint`** | `breakpoint` *action*, *qualifier* ***(restricted)*** |
| **`btree`** | `btree(`*file.var*, *matrix*`)` — *matrix* is a `dim`med one-dimensional name ***(internal)*** |

## C

| | |
|---|---|
| **`callv`** | `callv` *name*`(`*arg*, …`)` ***(restricted)*** |
| **`changed`** | `changed(`*a*`)` ***(internal)*** |
| **`como`** | `como on` *name*   ·   `como off`   ·   `como` *name* {`on error` …} ***(restricted)*** |
| **`configure.file`** | `configure.file` *file.var*, *key*, *value* `then` … `else` … ***(restricted)*** |
| **`create.ak`** | `create.ak` *file.var*, *index*, *dict.rec* `then` … `else` … ***(restricted)*** |

## D

| | |
|---|---|
| **`debug.info`** | `debug.info(`*a*, *b*`)` ***(internal)*** |
| **`debug.off`** | `debug.off` ***(restricted)*** |
| **`debug.on`** | `debug.on` ***(restricted)*** |
| **`debug.set`** | `debug.set` *var* {, *qualifier*} `to` *value* ***(restricted)*** |
| **`delete.ak`** | `delete.ak` *file.var*, *index* `then` … `else` … ***(restricted)*** |
| **`delete.common`** | `delete.common` *name* ***(restricted)*** |

## E

| | |
|---|---|
| **`errmsg`** | ***(no such thing)*** — in the statement table with no opcode behind it |
| **`events`** | `events(`*a*, *b*`)` ***(internal)*** |
| **`expand.hf`** | `expand.hf(`*a*, *b*, *c*`)` ***(internal)*** |

## F

| | |
|---|---|
| **`fcontrol`** | `fcontrol(`*a*, *b*, *c*`)` ***(internal)*** |
| **`find`** | `find` *x* `in` *arr* {, *occ*} `setting` *f* {, *v* {, *sv*}} `then` … `else` … ***(internal)*** |
| **`formcsv`** | `formcsv(`*a*`)` ***(internal)*** |

## G

| | |
|---|---|
| **`getlocks`** | `getlocks(`*a*, *b*`)` ***(internal)*** |
| **`grpstat`** | `grpstat(`*a*, *b*`)` ***(internal)*** |

## I

| | |
|---|---|
| **`is.subr`** | `is.subr(`*a*`)` ***(internal)*** |
| **`ismv`** | `ismv(`*a*`)` ***(internal)*** |

## K

| | |
|---|---|
| **`kernel`** | `kernel(`*a*, *b*`)` ***(internal)*** |
| **`keyboard.input`** | `keyboard.input` *string* ***(restricted)*** |

## L

| | |
|---|---|
| **`list.common`** | `list.common()` ***(internal)*** |
| **`load.object`** | `load.object(`*a*`)` ***(internal)*** |
| **`loaded`** | `loaded(`*a*`)` ***(internal)*** |
| **`login`** | `login(`*a*, *b*`)` ***(internal)*** |
| **`login.port`** | `login.port(`*a*, *b*`)` ***(internal)*** |
| **`logout`** | `logout(`*a*, *b*`)` ***(internal)*** |

## M

| | |
|---|---|
| **`modify`** | `modify` *file.var*, *id* ***(restricted)*** |

## O

| | |
|---|---|
| **`option`** | `option(`*a*`)` ***(internal)*** |
| **`ospath`** | `ospath(`*a*, *b*`)` ***(internal)*** |
| **`osrename`** | `osrename(`*a*, *b*`)` ***(internal)*** |

## P

| | |
|---|---|
| **`pconfig`** | `pconfig(`*a*, *b*`)` ***(internal)*** |
| **`phantom`** | `phantom()` ***(internal)*** |
| **`prompt`** | `prompt` *character* ***(internal)*** |
| **`pterm`** | `pterm(`*a*, *b*`)` ***(internal)*** |
| **`pwcrypt`** | `pwcrypt(`*a*`)` ***(internal)*** |

## Q

| | |
|---|---|
| **`quit`** | `quit` ***(restricted)*** |

## R

| | |
|---|---|
| **`readpkt`** | `readpkt()` ***(internal)*** |
| **`release.lock`** | `release.lock` *n* ***(restricted)*** |
| **`remove.token`** | `remove.token` ***(restricted)*** |
| **`removef`** | `removef(`*string* {, *occurrence*}`)` ***(internal)*** |
| **`reset.modes`** | `reset.modes` *mask* ***(restricted)*** |
| **`rewind`** | `rewind` *file.var* `then` … `else` … ***(restricted)*** |
| **`run`** | `run` {*file*} *record* {*options*} ***(restricted)*** |

## S

| | |
|---|---|
| **`scan`** | `scan(`*a* {, *matrix*}`)` — *matrix* is a `dim`med one-dimensional name ***(internal)*** |
| **`sdext`** | `sdext(`*a*, *b*, *c*`)` ***(internal)*** |
| **`sdpyobj`** | `sdpyobj(`*a*, *b*, *c*, *d*`)` ***(internal)*** |
| **`set.modes`** | `set.modes` *mask* ***(restricted)*** |
| **`set.status`** | `set.status` *n* ***(restricted)*** |
| **`set.trigger`** | `set.trigger` *file.var*, *mode*, *program* {, *modes*} ***(restricted)*** |
| **`set.unassigned`** | `set.unassigned` *var* ***(restricted)*** |
| **`sortadd`** | `sortadd` *key*, *data* ***(restricted)*** |
| **`sortclear`** | `sortclear` ***(restricted)*** |
| **`sortdata`** | `sortdata()` ***(internal)*** |
| **`sortinit`** | `sortinit` *keys*, *memory* ***(restricted)*** |
| **`sortnext`** | `sortnext(`*matrix*`)` — *matrix* is a `dim`med one-dimensional name ***(internal)*** |

## T

| | |
|---|---|
| **`testlock`** | `testlock(`*a*`)` ***(internal)*** |

## U

| | |
|---|---|
| **`unload.object`** | `unload.object` *class* ***(restricted)*** |

## V

| | |
|---|---|
| **`varset`** | `varset` *var*, *value* ***(restricted)*** |

## W

| | |
|---|---|
| **`watch`** | `watch` *var* ***(restricted)*** |
| **`writepkt`** | `writepkt` *data* ***(restricted)*** |

## See also

[Operating System Access](03-operating-system-access.html) covers the `sh` and
`!` verbs, which are the other thing an ordinary account cannot reach.
[Encryption and the SDEXT interface](04-sd-encryption.html) explains why
`sdext` is on this page and what it costs an application.

The User set's *SD Basic - Syntax* card carries everything an application may
use, and the two partition the roster between them.
