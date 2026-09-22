Title: SD Core - Introduction and Getting Started
Subtitle: What a multivalue database is, what SD is, the four components, and your first session.

This page orients you to SD Core for Linux: what a multivalue database is,
where SD came from, what the pieces are, and how to take your first steps. It
is the only page in this set that assumes nothing.

## What is a multivalue database?

A multivalue database stores data in records made of **fields**, where
each field can hold **more than one value** — and each value can hold
**more than one subvalue**. A single field in a customer record can
therefore carry every phone number the customer has, without a separate
table or a join.

The model was designed by Dick Pick in the 1970s as the Pick Operating
System. It has been through PI/open, UniVerse, Unidata, D3, jBASE,
QM, and ScarletDME — and SD is one of its direct descendants.

The three delimiters that make it work are **field marks**, **value
marks** and **subvalue marks** — control characters that separate the
levels inside a single string. A dynamic array in SDBasic is a string
that carries these marks, and `extract`, `insert`, `delete` and
`replace` work on them directly.

## What SD is

SD Core for Linux is built from upstream `sdb64`, a MultiValue database
with elements found in the main SD version and in ScarletDME. ScarletDME
was a fork of the original GPL release of OpenQM 2.6.6.

**That lineage matters when you go looking for documentation.** Not all
the features of the *commercial* OpenQM 2.6.6 were in the GPL release,
and no documentation specific to the GPL version was ever released. The
OpenQM 2.6.6 documents can be used as a reference, but SD Core has
additions, changes and deletions — of features, of structure, of
security and of commands. This documentation set covers those changes.

If you have used OpenQM, or upstream `sdb64`, much of SD Core will still be
familiar: the same data model, the same query processor, the same
BASIC.

**SD Core for Linux is Linux only.** There are no `#ifdef` branches
keeping Windows alive in this source — SD Core for Windows is a separate
project, kept in behavioural parity by deliberate policy, and this is not
a build of it.

SD Core is free software under the GNU General Public Licence v3. `config gpl`
displays the licence and `config contrib` the list of contributors. Installing
means cloning the source and building it — see the GettingStarted set.

## The four components

| | |
|---|---|
| **The command processor (TCL)** | reads what you type at the `:` prompt and dispatches it to a verb, a program, a paragraph or a query |
| **The query processor** | runs `list`, `select`, `count`, `sort` and the rest — the reporting language |
| **SDBasic** | the programming language: a compiled BASIC with dynamic arrays, file I/O, and the multivalue string functions |
| **The SDClient API** | a C client library (`sdclilib.so`) that lets an external application connect to SD, read and write records, execute commands and call subroutines |

## Signing in

```
sd
```

You land in **the SD account with your own name**. Nothing asks for a
password — Linux has already authenticated you, at the console or over
ssh.

If `sd` answers *Account ... not in register*, you are in the wrong
account or your group membership has not taken effect yet. If it
answers *not registered for SD use*, you are not in the `sdusers`
group.

> **You must log out and back in after being added to `sdusers`.**
> Group membership is fixed at login, the same as any Linux service.
> Until you get a new session you cannot read the data tree at all, and
> the symptom looks like a broken install.

SD is already running. It is a `systemd` service — `sd.service`,
`sdclient.socket` — enabled at every boot. You do not type `sd -start`.

## Your first file and record

```
create.file customers
ed customers 1001
```

`ed` is the line editor, and it needs nothing installed. In `ed`: `i`
to insert, type your lines, a full stop on its own line to stop
inserting, then `fi` to file and exit.

Every account can also use `nano` or `micro` (both full-screen editors
with syntax highlighting) — unconditionally, with no permission to grant
first. `edit` aliases `ed` here, not a full-screen editor.

```
list customers
count customers
```

Commands are lower case now. Typing `LIST` still works — SD tries what you
typed, then lower case, then upper, and finally with any hyphens changed to
dots, so `clear-select` reaches `clear.select` too.

## Writing a program

A program lives in a `bp` file — a directory file, which is an ordinary
Linux directory with one file per program. You can write it in `ed`,
in `nano`, in `micro`, or in any text editor you like — the folder is on
disk at:

```
/home/sd/user_accounts/<account>/bp
```

Compile and catalogue it from inside SD:

```
basic bp myprog
catalog bp myprog
```

Then run it by name:

```
myprog
```

## Becoming an administrator

**There is no `logto` route to it.** SDSYS, the one administrator account,
is reached only by logging in to the machine itself, locally, as the
`sdsys` account, its own password — a fresh session, not a command typed
from inside one you already have. `logto sdsys` from any other account is
refused outright, whatever route it came in by.

**This needs the console, or a desktop-sharing view of it** (VNC,
TeamViewer) — a real local login, which counts as local because it *is*.
`sdsys` has no ssh or API route to arrive over, ever, from anywhere.

## What is not in SD Core

The following were in OpenQM, in ScarletDME, or in upstream `sdb64`, and
are not in SD Core for Linux:

| Gone | Why |
|---|---|
| SDNet (remote files) | Removed; the API is the supported way to reach another SD server |
| `ENCRYPT.FIELD` verb | Removed; `sdencrypt()` and `sddecrypt()` in SDBasic are the supported route |
| `sed`, `update.record`, `modify` editors | Gone; use `nano`, `micro` or `ed` |
| PROC language | Removed; use paragraphs instead |
| NLS, `SET.LANGUAGE` | Removed; SD Core is English only |
| Unattended install | Not supported; the installer asks questions and sets passwords that cannot be scripted around |

**Embedded Python is not on this list** — a real difference from SD Core
for Windows, which dropped and later restored a narrower form of it. This
port never removed it.

## Document conventions

| | |
|---|---|
| **bold** | a word typed as it stands |
| *italics* | something you supply |
| braces `{ }` | an optional part |
| `code` | a command, a function name, or something you type |
