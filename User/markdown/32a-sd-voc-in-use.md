Title: SD VOC - Using and Managing the VOC
Subtitle: How the command processor reads the VOC, the verbs that manage it, and what account creation puts there.

This page continues [SD VOC - Structure and
Usage](32-sd-voc-structure-and-usage.html).

## How the command processor uses the VOC

The command processor is a BASIC program, `$CPROC`, and it runs a loop:
show any waiting messages, print the prompt, read a line, dispatch it,
repeat. The first word of the line is looked up in the account's `voc`
file.

### Name resolution

A name is tried **as typed, then lower case, then upper case**. This is
the change that lets a lower-case `voc`, `bp` and `newvoc` on disk
coexist with code and habits that still type names in upper case.

**Account names are the deliberate exception.** They are still folded
upward, which is what makes signing in case-insensitive.

### If the VOC has nothing, the catalogue is tried

A name that is not in the VOC is looked for in the **private catalogue**
of the account and then in the **global catalogue**, `gcat`. A hit is
treated exactly as though the VOC had held `V` / `CA` / *name*. This is
why a program you have catalogued can be run by typing its name with no
VOC record of its own.

If neither has it, the command is refused by name.

## Verbs that manage the VOC

### set.file — write a Q-pointer

```
set.file account file.name pointer.name
```

Writes a Q-pointer into the VOC — field 1 `Q`, field 2 the account name,
field 3 the file name. After it, *pointer.name* is usable wherever a file
name is, and the data stays where it is.

**The account must be in the accounts register.** The name is folded to
upper case before the register is read. If it is not there you get
*Account name '...' is not in register* and nothing is written.

### update.accounts — refresh from NEWVOC

```
update.accounts
```

Re-runs `LOGIN`'s `update.voc` paragraph, which copies any changed
records from the system `NEWVOC` into the account's VOC. **Since 17 Aug
2026 this is incremental** — it re-copies only the records whose stamp has
changed, not the whole file. `TIER.OMIT.STANDARD` and
`TIER.ADD.ADMINISTRATOR` in `NEWVOC` control what each account type
receives.

**The tier test is the one this record exists for.** `update.accounts`
on a standard account must not give back the verbs that were withheld
when the account was created. A standard account starts with fewer verbs
than an administrator account, and `update.accounts` preserves that
difference.

### copy — copy records into the VOC

```
copy from voc messages,myname
copy from src.file to dict tgt.file record.id
```

`copy` can write into the VOC the way it writes into any file. The
`from voc` form copies a VOC record under a new name, which is how an
alias is made without `alias`.

### delete — remove a VOC record

```
delete voc name
```

Removes the record. **`.d` *name* at the command prompt asks first**;
`delete voc name` does not.

### .s and .r — save and recall

```
.s name s e
.r name
```

`.s` writes stack lines *s* to *e* into the VOC as *name* — a sentence
when the range is one line, a paragraph when it is more. `.r` loads a
sentence or paragraph from the VOC into the stack. **The record type
follows from what you saved** rather than from anything you say.

### The LIST family

Ten verbs list VOC entries by type. They are all R-records into
`SD.VOCLIB`:

| Verb | Lists |
|---|---|
| `listf` | all files (F-records) |
| `listfl` | local files only |
| `listfr` | remote files only |
| `listk` | all keywords (K-records) |
| `listpa` | all paragraphs (PA-records) |
| `listph` | all phrases (PH-records) |
| `listq` | all Q-pointers |
| `listr` | all remote references (R-records) |
| `lists` | all sentences (S-records) |
| `listv` | all verbs (V-records) |

### count — count the records

```
count voc
count voc with v = "V"
```

`count` over the VOC gives the total record count. With a selection
clause it counts by type or by any other field.

### ct — display a record

```
ct voc name
```

Displays the record field by field. This is the way to see what a VOC
entry actually contains without an editor.

## The VOC and account creation

`CREATE.ACCOUNT` copies the VOC from `voc_template` in the system
directory. The template holds 426 records; `NEWVOC` holds 395. The
difference is that `voc_template` carries the A-verbs — `abort`,
`alias`, `all`, `after`, `and` and the rest — that are also keywords, and
`NEWVOC` does not. An account gets the union of the two, less whatever
its tier omits.

| Tier | What it gets |
|---|---|
| **administrator** | everything in `voc_template` plus everything in `NEWVOC`, less `TIER.OMIT.STANDARD` |
| **standard** | everything in `voc_template` plus everything in `NEWVOC`, less `TIER.OMIT.STANDARD` (42 names) |
| **programmer** | standard plus the programmer verbs from `TIER.ADD.ADMINISTRATOR` |

**The tier is in the VOC, not in the verb.** A standard account does
not have `create.file` because the VOC record for it is not there, not
because a security subroutine refuses it. The name is simply not
recognised. This is the design: tiering is done by giving or withholding
the record.

## Case on disk

Since 18 Aug 2026 the VOC ids are stored in lower case — `list`,
`create.account` and so on. This changes nothing about what you type —
SD tries a name as typed, then lower, then upper. What it changes is what
SD prints back: `CT VOC LIST` answers `VOC list`.

The file-pointer entries — `bp`, `bp.out`, `gpl.bp`, `gpl.bp.out` — moved
to lower case on 19 Aug 2026. `VOC`, `NEWVOC`, `ACCOUNTS`, `MESSAGES`,
`SYSCOM` and `QFILE` are still upper case on disk and are next.

## What is not here

**There is no verb that edits the VOC directly.** `ED` edits any file,
and `ED VOC`*name* is how you edit a VOC record by hand. But there is no
verb whose purpose is to create or modify VOC entries — `set.file` writes
one kind, `.s` writes two, and everything else is done with `ED` or with
`copy from voc`.

**`PROC` is removed.** A `PQ`-type record is refused by name. Nothing
that ships is type `PQ`, so this can only be met in a VOC record somebody
wrote.

**`menu` records are dispatched but no menu ships.** Type `M` is handled
and there is no shipped example to look at.

**`EDIT` is in the VOC but cannot run.** Its type field reads
`Verb - Full screen editor`, which is not `V`, so the command processor
does not dispatch it. The record is there so that `EDIT` at the prompt
prints *"Full screen editor is no longer supported"* rather than *"verb
not found"*.

## See also

[SD TCL - The Command Processor](19-sd-tcl-command-processor.html) ·
[SD TCL - Files and Records](20-sd-tcl-files-and-records.html) ·
[SD Basic - File Handling](07-sd-basic-file-handling.html) ·
[SD Basic - Dynamic Arrays](05-sd-basic-dynamic-arrays.html).
