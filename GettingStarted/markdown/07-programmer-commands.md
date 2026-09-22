Title: Development and file commands
Subtitle: Compiling, editing, and the verbs that maintain files, indexes and records in bulk.

**Every account has these, from the moment it is created.** SD Core used to
hold them back from a *standard* account and only give them to a
*programmer* or *administrator* one; that split is gone — see
[Accounts](05-account-types.html). This page is now a reference for what
each of them does, not a list of what you have been given.

**One thing, named as it comes up below, still needs more than the verb**:
cataloguing globally is gated separately from the VOC — see
[What actually gates these](#what-actually-gates-these) at the foot of this
page. Unlike SD Core for Windows, the full-screen editors need nothing
extra at all.

## Compile, catalogue and run

| | |
|---|---|
| **`basic`** | compile SD BASIC source |
| **`catalog`** · **`catalogue`** | add to the catalogue |
| **`delete.catalog`** · **`delete.catalogue`** | remove from it |
| **`compile.dict`** | compile dictionary items |
| **`run`** | run a compiled program |
| **`map`** | show a program's map |
| **`generate`** | generate source |
| **`phantom`** | start a background process |

> **Cataloguing globally is SDSYS's alone.** Adding to or removing from the
> system-wide catalogue needs SDSYS; private and local cataloguing work from
> any account. That is a separate control from having the verb at all — see
> [Administrator commands](06-administrator-commands.html).

## Edit and debug

| | |
|---|---|
| **`ed`** | the line editor. Needs nothing installed. `edit` is an alias for it |
| **`nano`** | a **full-screen** editor — opens the record in `nano` |
| **`micro`** | a **full-screen** editor — opens the record in `micro` |
| **`debug`** | the BASIC debugger |
| **`pstat`** · **`pdebug`** · **`pdump`** · **`dump`** | process introspection |

### Editors

**`edit` is not a full-screen editor here** — a real difference from SD
Core for Windows, where it opens Microsoft Edit. There is no Linux
equivalent to alias it to, so `edit` runs the **line** editor, `ed`,
instead. The two full-screen editors are named for the program each runs:

| | |
|---|---|
| **`nano`** | ships with Debian and Ubuntu already |
| **`micro`** | installed by the SD installer as an ordinary package |

```
nano  bp myprog
micro bp myprog
nano  dict customers name
```

Either verb writes the record to a working copy, opens the editor on it,
reads it back, and asks whether to save. For a `bp` record it then offers
the compile and the catalogue.

**Both are terminal editors**, so both work over ssh as well as at the
console.

**Both highlight SD BASIC — a difference from SD Core for Windows, where
only `micro` did** (Microsoft Edit has no syntax highlighting at all).
`micro`'s highlighting is per-user (`~/.config/micro/syntax`, staged by
the installer where it can); `nano`'s is system-wide
(`/usr/share/nano/sdbasic.nanorc`, included by `/etc/nanorc`) — one copy
serves every account on the machine:

| | |
|---|---|
| **`nano`**, **`micro`** | statements, reserved words, intrinsic functions, `@variables`, `$directives`, labels, strings, numbers and comments |

**It applies to a `bp` record and to nothing else.** SD names the working
copy so the editor can recognise the language — a record edited out of any
other file is treated as plain text, which is correct for a VOC entry or a
data record.

> **The word lists are generated from the compiler.** They come out of
> `bcomp`'s own tables — **182 statements, 37 reserved words and 176
> intrinsic functions** — so the highlighting cannot drift from the
> language. **If a name you expect is not coloured, that is worth
> reporting**: it means the two have come apart, which is exactly what
> generating them was meant to prevent.

**`ed` is unaffected and is still there.**

### What the editors are good for, and what they are not

**They are text editors**, so they suit a record whose content is lines of
text:

| | |
|---|---|
| **BASIC source** in a `bp` file | what they are for |
| **VOC records** | fine — a VOC record is a few short fields |
| **Dictionary records** | fine for a simple one; see the limit below |
| **Data records with multivalues** | fine — see the tokens below |
| **Data records with subvalues** | fine — see the tokens below |

**A field is a line and that part needs no explanation.** SD writes the
working copy with one field per line, so moving between fields is moving
between lines.

**A value mark is not a line, and neither is a subvalue mark.** Both are
control characters an editor cannot show, so each has a token you can type:

| Type | To get |
|---|---|
| `~~` | a **value** mark |
| `` ~` `` | a **subvalue** mark |

SD converts marks to tokens on the way into the editor and tokens back to
marks on the way out, so multivalues and subvalues are both ordinary text
while you are editing.

```
SMITH~~JONES~~BROWN
```

is a three-value field, and

```
RED~`BLUE~~GREEN
```

is two values, the first of which has two subvalues.

**A record that cannot be written this way is refused, not mangled.** Some
records would come back different from how they went in — one that already
contains `~~` as data, for instance, or one with a `~` sitting immediately
before a mark, where the tilde and the token run together. Before opening
the editor, SD converts the record and converts it back; **if the result is
not what it started with, the verb refuses and names `ed`**, which needs
none of this.

**Text marks are not converted**, and are covered by the same refusal
rather than being left to surprise you.

**A compiled dictionary record is truncated to its first 15 fields** while
you edit it, and recompiled with `cd` when you save.

### An editor is not a hole, but it is worth thinking about

**An editor can write anywhere its user can write.** It opens the record
you named, but nothing stops the person then opening any other file on the
machine that their Linux account may open — inside the SD data tree or
outside it altogether. **That is not a gap in SD; it is what an editor
is** — and it is exactly the same reach that account's own login shell
already has, since SD keeps no second wall behind Linux's own permissions.
See [Security and the operating system](12a-security-and-the-operating-system.html).

Neither editor can run a command, so neither is a shell. **What they are is
read and write access to the filesystem, with the account's own Linux
permissions.**

### Over ssh

**A terminal editor is the point of an ssh session.** An ssh session
reaches SD through a terminal like any other, and SD hands the editor that
terminal rather than reading it through a pipe.

**If an editor misbehaves over ssh and not at the console, that is worth
reporting** with the terminal you connected from.

The removed full-screen editors are a different matter: `sed`,
`update.record` and `modify` are gone and are not coming back. See
[Not in SD Core](14-not-in-sd-core.html).

## Files

| | |
|---|---|
| **`create.file`** · **`delete.file`** · **`clear.file`** | the life of a file |
| **`configure.file`** | change a file's configuration |
| **`analyse.file`** · **`analyze.file`** | report on a file's internals |
| **`fstat`** | file statistics |
| **`hsm`** | hashed-file statistics monitoring |
| **`set.trigger`** | attach a trigger |
| **`cd`** | change directory |

## Indexes

**`create.index`** · **`delete.index`** · **`build.index`** · **`make.index`** · **`list.index`**

## Bulk record editing

| | |
|---|---|
| **`copy`** · **`copyp`** | copy records |
| **`delete`** | delete records |
| **`rename`** | rename records |
| **`reformat`** · **`sreformat`** | reformat |
| **`sort.item`** | sort |
| **`cname`** | change a record's name |
| **`delete.common`** | clear a common block |

## What actually gates these

**Having the verb is not the whole story for one thing above: cataloguing
globally.** It needs more than being in the VOC — and since every account
has the VOC now, this is the part worth knowing before you rely on
anything in this page as a boundary.

| | |
|---|---|
| File permissions | ordinary Linux file permissions on the data tree — see [Security](12-security.html) |
| Reaching the operating system | none, for `sh`, `OS.EXECUTE`, or either editor — every account has it, unconditionally |
| What an API session may open | the containment gate, rooted at the account the session stands in |

**Unlike SD Core for Windows, the full-screen editors need no separate
permission — they run the moment the verb is typed, for every account.**
There is no `os.users` file, and nothing to grant before `nano` or `micro`
work. The gate that page describes (`os.users` field 2) does not exist on
this port at all: this account's own Linux permissions are already the
only wall an editor — or a shell — ever runs into. See
[Security and the operating system](12a-security-and-the-operating-system.html).

**A session with no terminal is refused**: an API session or a piped
script has nowhere to draw a full screen.

## Two things to know when you compile

**`basic` no longer creates an object file it can never open again.**
Compiling into a reused file name previously produced an object SD could
not subsequently open.

**Object code and the catalogue are replaced on upgrade.** The compiled
programs, the BASIC source SD ships, the messages, include records and VOC
templates are all overwritten by a new release. **Anything you have written
into the SDSYS `bp` file, and anything you have compiled from it, survives
an upgrade untouched** — SD now ships nothing into that file at all, so it
is created empty and is yours.
