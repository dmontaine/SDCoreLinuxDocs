Title: SD TCL - The nano Screen Editor
Subtitle: nano, a status-bar reference and a dozen keys — the one to reach for when you just want to change a record.

```
nano {dict} file record
```

**Unlike SD Core for Windows, `edit` is not a screen editor here** — there is
no Linux program to alias it to the way Microsoft Edit serves that role
there, so `edit` is simply a second name for **`ed`**, the line editor (see
[ed](25-sd-tcl-ed.html)). The full-screen editor to reach for when you just
want to fix a line and move on is `nano`.

`nano` opens a record in **nano**, a small full-screen editor that ships
with Debian and Ubuntu already. It has a status bar of key shortcuts always
on screen, the shortcuts everyone already knows, and nothing else to learn.
**That is the point of it**: if you want to fix a line in a record and get
on with your day, this is the one.

It has SD BASIC syntax highlighting for a `bp` record (system-wide, part of
the installer's own setup) but no command language of its own. For split
windows, a command bar or a plugin system, use [micro](27-sd-tcl-micro.html)
instead. For a session with no terminal, or one you are driving from a
script, use [ed](25-sd-tcl-ed.html).

SD folds case, so a command may be typed in either case. Commands are shown here
in lower case. In the tables, *italics* mark something you supply and **bold**
marks a word typed as it stands; braces mark an optional part.

## Both editors are installed with SD

**You do not install anything.** `nano` normally ships with the
distribution already; the installer adds SD's own BASIC syntax
highlighting to it, system-wide, so every account SD creates gets coloured
`bp` records with nothing to configure. `micro` is installed as an
ordinary package by the same installer.

If either could not happen — an offline machine, or one whose policy blocks
the package manager — the verb says so, rather than opening nothing and
reporting the record unchanged; `ed`, which needs nothing installed, always
works.

## The keys

`Ctrl-O` writes out (saves) and `Ctrl-X` exits. Those two are most of what
anyone needs.

| | |
|---|---|
| **`Ctrl-O`** | write out (save) |
| **`Ctrl-X`** | exit |
| **`Ctrl-K`** · **`Ctrl-U`** | cut a line · paste (uncut) |
| **`Ctrl-6`** / **`Alt-A`** | start a selection (mark text) |
| **`Alt-U`** · **`Alt-E`** | undo · redo |
| **`Ctrl-W`** | search |
| **`Ctrl-\`** | search and replace |
| **`Ctrl-_`** | go to line and column |
| **`Ctrl-G`** | help |
| **`Ctrl-C`** | show the cursor position |

**The status bar is the help.** The two lines above every editing session
list the shortcuts in force; **`Ctrl-G`** opens the full help screen with
everything else.

## What SD does around the editor

The two screen editors are separate programs with a shared wrapper, so
everything in this section is equally true of [micro](27-sd-tcl-micro.html).

| | |
|---|---|
| **the working copy** | the record is copied into `$hold` as *record*`.editing`, and the editor is run on that. It is removed on every exit, including the ones that fail |
| **saving** | *"Save? &lt;Y&gt;es, &lt;N&gt;o"*, then for a `bp` record *"Compile?"* and *"Catalogue?"* |
| **a `dict` record** | is always saved and re-compiled with `cd` |
| **finishing** | *"&lt;E&gt;xit or &lt;R&gt;e-edit"*, so a compile error can be fixed without starting again |

**A compiled dictionary record is truncated to its first 15 fields while you
edit it**, which is what you want: the fields after them are the compiled form,
and `cd` rebuilds them when you save.

## Marks, and how to type one

A **field** mark is a line break, so a text editor handles fields on its own.
The other three marks are single control characters an editor would either draw
as a stray glyph or drop, so each has a token you type instead.

**Every token is `~` and one more character, and `~` is the only escape
character.**

| | |
|---|---|
| `~~` | a value mark |
| `` ~` `` | a subvalue mark |
| `~!` | a text mark |
| `~-` | a literal `~`, where one would otherwise be misread |
| `~,` | a literal `,`, where one would otherwise read as a separator |

`SMITH~~JONES~~BROWN` is a three-value field; ``RED~`BLUE~~GREEN`` is two
values, the first with two subvalues.

### Marks in a row are separated by a comma

Written token against token a run of marks cannot be read, so SD puts a comma
between them. A text mark, a text mark and a value mark, one after another, is:

```
~!,~!,~~
```

**Type the comma yourself when you enter marks in a row.** It is a separator and
not data — which is why a literal comma standing in exactly that position,
between two marks, is written `~,`.

### The conversion is lossless

**No record is refused and none is mangled**, whatever it contains. A tilde is
written `~-` **only where the character after it would make the pair look like a
token** — another `~`, a backtick, a `!`, a `-`, a `,`, or a mark. Everywhere
else a tilde is left exactly as you wrote it, so `a~b` is still `a~b` and
ordinary source reads normally.

## No gate — every account reaches both, unconditionally

**Unlike SD Core for Windows, there is no `os.users`-style permission
behind `nano` or `micro` here.** Every account has both verbs, and both run
the moment they are typed — there is no record to grant, and nothing
SDSYS needs to set up first. This port keeps no second wall behind an
editor's own reach onto the machine: what an account's Linux user may
read or write outside SD is exactly what an editor run from inside SD may
touch, because they are the same permissions. See the *Administrator*
set's *Accounts and Security* chapter, "There is no second wall for `sh`
or `os.execute`."

**A session with no terminal is still refused**, an API session or a
script driving SD down a pipe having nowhere to draw a full screen:

```
:nano bp zzed
nano needs a terminal to draw on, and this session has none.
ed, the line editor, works anywhere.
```

Both usage errors name the verb you typed rather than the program behind it:

```
:nano
No file name specified.  Usage: nano {dict} <file> <record>
:nano bp
No record name specified.  Usage: nano {dict} <file> <record>
```

## Who has these verbs

**Every account has `nano`, `micro` and `ed`, and all three simply run —
there is nothing further to check.**

## See also

[SD TCL - The micro Screen Editor](27-sd-tcl-micro.html) ·
[SD TCL - The ed Line Editor](25-sd-tcl-ed.html) ·
[SD TCL - Files and Records](20-sd-tcl-files-and-records.html).
