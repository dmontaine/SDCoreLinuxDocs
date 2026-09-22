Title: Development and file commands
Subtitle: Compiling, editing, and the verbs that maintain files, indexes and records in bulk.

**Every account has these, from the moment it is created.** SD Core used to
hold them back from a *standard* account and only give them to a
*programmer* or *administrator* one; that split is gone — see
[Accounts](05-account-types.html). This page is now a reference for what
each of them does, not a list of what you have been given.

**A few, named as they come up below, still need more than the verb**:
cataloguing globally, and reaching the operating system through the two
full-screen editors, are gated separately from the VOC — see
[What actually gates these](#what-actually-gates-these) at the foot of this
page.

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
| **`ed`** | the line editor. Needs nothing installed |
| **`edit`** | a **full-screen** editor — opens the record in Microsoft Edit |
| **`micro`** | a **full-screen** editor — opens the record in micro |
| **`debug`** | the BASIC debugger |
| **`pstat`** · **`pdebug`** · **`pdump`** · **`dump`** | process introspection |

### Editors

**There are two, and they behave identically.** The verb chooses the editor
and nothing else changes:

| | |
|---|---|
| **`edit`** | **Microsoft Edit** — ships in current Windows builds |
| **`micro`** | **micro** — never ships with Windows; the installer fetches it |

```
edit  bp myprog
micro bp myprog
edit  dict customers name
```

Either verb writes the record to a working copy, opens the editor on it,
reads it back, and asks whether to save. For a `bp` record it then offers
the compile and the catalogue.

**Both are terminal editors**, so both work over ssh as well as at the
console. Where a machine does not have one, the SD installer installs it; if
that could not be done, the verb says so and names the command that
installs it. `C:\ProgramData\SD\install-editors.log` records what the
installer found.

**Only `micro` highlights SD basic.** Microsoft Edit has no syntax
highlighting at all, which is the one real difference between the two
verbs:

| | |
|---|---|
| **`micro`** | statements, reserved words, intrinsic functions, `@variables`, `$directives`, labels, strings, numbers and comments |
| **`edit`** | plain text |

**It applies to a `bp` record and to nothing else.** SD names the working
copy so that micro can recognise the language — a record edited out of any
other file is treated as plain text, which is correct for a VOC entry or a
data record.

> **The word lists are generated from the compiler.** They come out of
> `BCOMP`'s own tables — **218 statements, 37 reserved words and 176
> intrinsic functions** — so the highlighting cannot drift from the
> language. **If a name you expect is not coloured, that is worth
> reporting**: it means the two have come apart, which is exactly what
> generating them was meant to prevent.

**Nothing is installed into your profile.** SD ships the rules with itself
and points micro at them, so they work for every account on the machine.

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

### Give these verbs only to people you trust

**An editor can write anywhere its user can write.** It opens the record
you named, but nothing stops the person then opening any other file on the
machine that their Windows account may open — inside the SD data tree or
outside it altogether. **That is not a hole in SD; it is what an editor
is**, and it is the reason these two verbs are behind `OS.EXECUTE`
permission and not merely behind having the verb — see
[What actually gates these](#what-actually-gates-these).

**So `os.users` field 2 is a statement of trust in a person, not a
convenience.** Before granting it, ask the same question you would ask
before giving somebody the shell — because in terms of what they can reach
on disk, you are.

Neither editor can run a command, so neither is a shell. **What they are is
read and write access to the filesystem, with the account's own Windows
permissions.** See [Security](12-security.html).

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

**Having the verb is not the whole story for two things above: cataloguing
globally, and the two full-screen editors.** Both need more than being in
the VOC — and since every account has the VOC now, this is the part worth
knowing before you rely on anything in this page as a boundary.

| | |
|---|---|
| File permissions | Windows ACLs on the data tree — see [Security](12-security.html) |
| Where an account may sign in | the `sdsshonly` deny rights — see [ssh access](08-ssh-access.html) |
| Reaching the operating system | the `os.users` permit list, both **`sh`** and `OS.EXECUTE` |
| What an API session may open | the containment gate, rooted at the account the session stands in |

### The editors need `OS.EXECUTE` permission as well as the verb

**An editor runs outside SD, so reaching one is reaching the operating
system** — and who may do that is **field 2 of your record in
`os.users`**, the same field that governs `OS.EXECUTE` from inside a
program. Two gates, and both have to pass:

| | |
|---|---|
| the VOC | everyone has **`edit`** and **`micro`** |
| `os.users` field 2 | decides **whether either one runs** |

**SDSYS passes this on its own**, exactly as `sh` does, so an empty list
cannot lock the machine's own administrator out. **A missing record, or a
missing file, means no**, for every ordinary account — the same direction
`sh` fails in.

If you have the verb and not the permission you get told so by name, and
told what to ask for:

```
edit is not available to fred.
It runs an editor outside SD, so it needs OS.EXECUTE permission: field 2
of your record in the SD system file os.users, which only SDSYS can change.
ed, the line editor, needs none of this.
```

SDSYS grants it — see [Administrator commands](06-administrator-commands.html#how-you-grant-it).

**A session with no terminal is refused first and separately**: an API
session or a piped script has nowhere to draw a full screen, and is told
that rather than being told about `os.users`.

> **WHAT AN EDITOR CAN REACH, and it is worth knowing before you grant it.**
> An editor can open any file the person running it is allowed to open, so
> both verbs reach beyond SD's own files. Neither is a shell — neither
> editor can run a command. That is what field 2 is deciding, and it is why
> the verb alone was never enough. See [Security](12-security.html).

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
