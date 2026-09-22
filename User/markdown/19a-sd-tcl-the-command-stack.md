Title: SD TCL - The Command Stack
Subtitle: Recalling and re-running commands, the @variables, and the session verbs.

This page continues [SD TCL - The Command
Processor](19-sd-tcl-command-processor.html).

## The command stack

Every line you type is kept. The stack is edited with commands beginning with a
dot, and `n` below is a stack position — 1 is the most recent.

| | |
|---|---|
| **`.l`**{*n*} | list the last *n* stack lines. Defaults to 20, or a screenful |
| **`.l`** *name* | show a VOC record, one numbered line per field |
| **`.r`**{*n*} | recall line *n* to the top of the stack |
| **`.r`** *name* | load a sentence or paragraph from the VOC into the stack |
| **`.s`** *name* *s* *e* | save stack lines *s* to *e* into the VOC as *name* |
| **`.a`**{*n*} *text* | append *text* to line *n* |
| **`.i`**{*n*} *text* | insert *text* as line *n* |
| **`.c`**{*n*}`/`*old*`/`*new*`/`{`g`} | change *old* to *new* in line *n*; `g` for every occurrence |
| **`.d`**{*n*} | delete line *n* |
| **`.d`** *name* | delete a sentence or paragraph from the VOC, after asking |
| **`.u`**{*n*} | convert line *n* to upper case |
| **`.x`**{*n*} | execute line *n* |
| **`.x`** *file* *id* | execute a sentence or paragraph held in any file, not just the VOC |
| **`.?`** | print this list |

**`n` defaults to 1 everywhere, and the spaces shown are required.** `.d2`
deletes the second stack line and `.d 2` looks for a VOC record called `2`.

`.s` and `.r` together are the whole workflow: type the lines, then save them
under a name, then recall them later to edit. **`.s` writes a sentence when the
range is one line and a paragraph when it is more**, so the record type follows
from what you saved rather than from anything you say.

`.x` *file* *id* is the one that reaches outside the VOC — the file name and the
record id are each folded as typed, then lower, then upper.

**A dot command that is not one of these is not an error.** It is left alone and
run as an ordinary command, so a verb whose name begins with a dot still works.

> **`.d` does not find a lower-case VOC record typed in upper case, and `.l`
> and `.r` do.** `.l` and `.r` try the name as typed, then lower case, then
> upper case. `.d` tries only as typed and then upper case. A paragraph saved as
> `daily` can be listed and recalled by typing `DAILY` and cannot be deleted by
> typing `DAILY`. **Type the name in the case you saved it in and all three
> work.**

### Editing the line you are on

**There are two help texts and they are different.** `?` on its own prints the
key map below; `.?` prints the dot-command list above. Neither is the `help`
verb, which does not exist — see *What is not here*.

The key map is the same whether you reached the line by typing it or by
recalling it:

| Key | | Also |
|---|---|---|
| `Ctrl-A` | start of line | Home |
| `Ctrl-E` | end of line | End |
| `Ctrl-B` / `Ctrl-F` | back / forward one character | Cursor left / right |
| `Ctrl-P` / `Ctrl-N` | previous / next command | Cursor up / down |
| `Ctrl-Z` | previous command | Cursor up |
| `Ctrl-R` | reverse search | |
| `Ctrl-D` | delete character | Delete |
| `Ctrl-H` | backspace | Backspace |
| `Ctrl-K` | kill line | |
| `Ctrl-O` | toggle overlay | Insert |
| `Ctrl-T` | transpose characters | |
| `Ctrl-U` | upcase all | |
| `Ctrl-G` | exit the stack | |

**A line ending in `?` is put on the stack without being run.** That is the way
to park a half-written command while you go and look something up.

### Saving the stack across sessions

| | |
|---|---|
| **`save.stack`** {*name*} | write the stack to a named record |
| **`get.stack`** {*name*} | read it back |
| **`clear.stack`** | empty it |

Both prompt for the name if you leave it off.

## @-variables

`set` assigns an @-variable, which is then substituted into later command lines
wherever its name appears.

```
set name value
set name eval expression
```

Without `eval` the value is taken literally. With `eval` the text is evaluated
first, and the evaluation handles the four arithmetic operators on numeric
operands. `list.vars` shows what is currently set.

The variables the system sets are readable the same way — `@system.return.code`
is the one worth knowing, because most verbs set it and `report.src` exists to
show it.

## Session verbs

| | |
|---|---|
| **`who`** | your user number and the account you are in |
| **`who.am.i`** | the same information at more length |
| **`logto`** *account* | change account without logging out |
| **`off`** · **`quit`** | end the session |
| **`option`** {*name*} {**on**\|**off**\|**display**} | set or show a session option |
| **`option all off`** | turn every session option off at once |
| **`alias`** *command* *target* | make *command* run as *target* |
| **`alias`** *command* | remove that alias |
| **`alias`** | list the aliases |
| **`clear.abort`** | clear a pending abort condition |
| **`set.exit.status`** *n* | set the numeric status SD exits with |
| **`report.src`** {**on**\|**off**} | show `@system.return.code` after each command |

`who` answers with your user number and the account you are in:

```
39 DON
```

**After a `logto` it grows a third part, and that is the useful one:**

```
29 PAYROLL from DON
```

**`from DON` is the account you logged in as**, not the one you are in and not
your Windows account. So the short form means *I am still where I started* and
the long form means *I have moved* — which makes `who` the quick way to find
out whether a `logto` actually took effect.

**`SDSYS` cannot appear after `from` here, because `logto sdsys` is refused
outright from any other account.** Administering SD means signing in to
Windows as the `sdsys` account itself and starting a fresh session, not
`logto`-ing there from one you already have — see the *Administrator* set's
*Accounts and Security* chapter.

## What is not here

**There is no online help and `help` is not a verb.** The command processor
still has internal verb 14 reserved for it and the routine is an empty stub —
its body is commented out and it returns immediately. **No VOC record points at
it**, in any account type, so the name is not even recognised. The F1 key at the
command prompt reaches the same empty routine and therefore does nothing. **This
documentation is the help system.**

**`umask` is implemented and unreachable.** Internal verb 35 is a working
routine that reports or sets the file-creation mask, and **no VOC record points
at it either**. It cannot be typed. `umask()` from SD BASIC still works — see
[SD Basic - System and Environment](16-sd-basic-system-and-environment.html).

**PROC is removed.** So are `sed` and `update.record`. A `PQ`-type VOC record
is **refused by name** rather than being reported as a bad dispatch code,
because the record itself is valid PROC and it is the interpreter that is gone.
Nothing that ships is type `PQ`, so this can only be met in a VOC record
somebody wrote.

**`menu` records are dispatched but no menu ships.** Type `M` is handled and
there is no shipped example to look at.

## Who has these verbs

Everything on this page is in a **standard** account except the last two, which
are administrator-only:

| | |
|---|---|
| **standard** | `abort` `alias` `clear.abort` `clear.stack` `display` `get.stack` `go` `if` `list.vars` `logto` `off` `option` `pause` `quit` `report.src` `save.stack` `set` `set.exit.status` `stop` `who` `who.am.i` |

**Everything on this page is in a standard account.** An account that does not
have a verb does not have the VOC record for it — the name is simply not
recognised rather than refused.

**The two `OS` verbs are the exception and are not documented here.** `sh` and
`!` reach the Windows shell, are administrator-tier, and are gated a second time
by a list of who may use them. They are in the **administrator documentation**,
under *Operating System Access*, which is a separate set.

## See also

[SD TCL - Files and Records](20-sd-tcl-files-and-records.html) ·
[SD Basic - Program Control](02-sd-basic-program-control.html) ·
[SD Basic - System and Environment](16-sd-basic-system-and-environment.html).
