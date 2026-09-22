Title: Configuration
Subtitle: The sd.conf file, the two ways to read a setting, and every parameter SD accepts.

SD reads one configuration file at start-up. It sizes the shared memory
segment, sets the limits every session inherits, and names the directories SD
writes to.

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

SD folds case, so a command may be typed in either case. Commands are shown
here in lower case.

> Every listing on this page was produced by running it, on SD Core for Windows
> W1.0-0, from an unelevated session in an administrator account.

## The file

```
C:\ProgramData\SD\sd.conf
```

The server and the client both read the `SD_CONFIG` environment variable first
and fall back to that path. The file is installed only if it does not already
exist and is marked never to uninstall, so edits to it survive an upgrade and
survive removal of the product.

It is plain text in one section:

```
[sd]
SDSYS=C:\ProgramData\SD\sdsys
GRPSIZE=2
NUMUSERS=20
```

Lines beginning `#` are comments. The shipped file is heavily commented and
those comments record why each value was chosen. Read them before changing
anything.

### A name SD does not recognise stops it starting

An unrecognised parameter is not ignored. The parser abandons the file with
`Unrecognised configuration parameter`, and SD does not start.

That is why obsolete names are still parsed rather than deleted. `CREATUSR` has
done nothing since 14 August 2026, but a configuration file copied from a Linux
installation still carries it, and removing the branch would turn a tidy-up
into a failure to start.

Range failures behave the same way. `GRPSIZE`, `INTPREC`, `LPTRHIGH`,
`LPTRWIDE`, `MAXCALL`, `RECCACHE`, `SORTMRG` and `MAXIDLEN` are bounds-checked
once the file has been read, and a value outside its range stops start-up with
a message naming the parameter.

## Reading the settings

The `config` verb reports what is in force:

```
:config
Virtual Machine Version Number W1.0-0
APILOGIN  1
APIPORT   4243
CMDSTACK  99
DEADLOCK  0
DUMPDIR   C:\ProgramData\SD\sdsys\dumps
ERRLOG    50 kb
...
YEARBASE  1930
```

SD accepts **52** parameters and the verb prints **43** of them. Nine are
accepted in the file and never displayed: `CODEPAGE`, `CREATUSR`, `DEBUG`,
`FDS`, `FIXUSERS`, `NETDIRS`, `PORTMAP`, `SDSYS` and `TXCHAR`.

`NETDIRS` is the one to know about. It decides what an API session may reach
outside its own account, and the verb will not tell you what it is set to. Read
it from the file.

The `config()` function reads one parameter from a program:

```
group.size = config('GRPSIZE')
```

**49 parameters are readable this way.** The three that are not are `CREATUSR`,
which stores nothing, `SDSYS`, and `TXCHAR`. The name is truncated to eight
characters before it is matched; no parameter name is longer than eight, so
that only shows up if you pass something which is not a parameter.

Two further forms exist. `config lptr` reports the settings of the default
printer, and `config gpl` and `config contrib` display the licence and the list
of contributors.

## Changing a parameter

Editing `sd.conf` and restarting SD is the durable route, and for most
parameters it is the only one.

**28 parameters can also be changed for the current session:**

```
config sortmem 8192
```

That writes to the session's own copy of the settings, taken from shared memory
when the session started. It does not reach `sd.conf`, it does not affect any
other session, and it is gone when the session ends.

The 28 are `CODEPAGE`, `DUMPDIR`, `EXCLREM`, `FILERULE`, `FLTDIFF`, `FSYNC`,
`GDI`, `GRPSIZE`, `INTPREC`, `LPTRHIGH`, `LPTRWIDE`, `MAXCALL`, `MUSTLOCK`,
`OBJECTS`, `OBJMEM`, `RECCACHE`, `RINGWAIT`, `SAFEDIR`, `SDCLIENT`, `SH`,
`SH1`, `SORTMEM`, `SORTMRG`, `SORTWORK`, `SPOOLER`, `TEMPDIR`, `TERMINFO` and
`YEARBASE`.

Everything else takes effect only when SD is next started. That includes every
limit which sizes the shared memory segment and every setting the API listener
reads.

## Sessions and limits

| Parameter | Default | Effect |
|---|---|---|
| `NUMUSERS` | 20 | Maximum concurrent sessions. Sizes the user table in shared memory |
| `NUMFILES` | 80 | Maximum open files across all sessions |
| `NUMLOCKS` | 100 | Maximum record locks across all sessions |
| `MAXCALL` | 10000 | Maximum subroutine call depth. Range 10 to 1000000 |
| `CMDSTACK` | 99 | Depth of the command stack |
| `FDS` | unset | Limit on file descriptors. No limit when unset |
| `FIXUSERS` | unset | `base,range` — user numbers reserved for sessions that ask for a specific number |
| `PORTMAP` | unset | `base_port,base_user,range` — gives a session a fixed user number derived from the port its connection arrived on. Refused if the range overlaps `FIXUSERS` |

## Files and locking

| Parameter | Default | Effect |
|---|---|---|
| `GRPSIZE` | 2 | Default group size for a new dynamic file, in 1 KB units. Read by `create.file` and `configure.file` when no group size is given |
| `MAXIDLEN` | 63 | Maximum record id length. 63 is also the lower bound |
| `MUSTLOCK` | 0 | When 1, a `write` or `delete` requires the record to be locked first |
| `DEADLOCK` | 0 | When 1, SD traps deadlocks |
| `SAFEDIR` | 0 | When 1, directory files are updated by write-and-rename rather than in place |
| `RECCACHE` | 0 | Records cached per file. Range 0 to 32 |
| `FSYNC` | 0 | Bit flags controlling when SD forces data to disk |
| `FILERULE` | 0 | Bit flags deciding which special VOC file references are honoured. Bit 4 allows a `PATH:` reference to name a pathname directly |

## Directories

| Parameter | Default on a new install | Effect |
|---|---|---|
| `SDSYS` | `C:\ProgramData\SD\sdsys` | The system account. SD does not start if the global catalogue is not found beneath it |
| `USRDIR` | `C:\ProgramData\SD\user_accounts` | Where `create.account` puts a user account |
| `GRPDIR` | `C:\ProgramData\SD\group_accounts` | Where `create.account` puts a group account |
| `DUMPDIR` | `C:\ProgramData\SD\sdsys\dumps` | Where process dumps are written |
| `TEMPDIR` | `/cygdrive/c/WINDOWS/TEMP` | Temporary files |
| `SORTWORK` | `/cygdrive/c/WINDOWS/TEMP` | Work files for a sort that does not fit in memory |
| `JNLDIR` | empty | Journal directory |
| `TERMINFO` | empty | An additional terminfo directory. The shipped definitions are found without it |

`DUMPDIR` is set rather than left empty on purpose. A blank value falls back to
the system directory, which SD users can write to, and a process dump carries
the whole variable state of the session that wrote it. The installer makes the
dump directory write-only to SD users, so a dump can be added and nobody else's
can be listed or read.

`TEMPDIR` and `SORTWORK` are reported in POSIX form because that is how the
server's runtime addresses them. `C:\WINDOWS\TEMP` and
`/cygdrive/c/WINDOWS/TEMP` are the same directory.

## The API

| Parameter | Default | Effect |
|---|---|---|
| `APIPORT` | 4243 | The port the API listens on. If the line is absent no socket is created at all, which is how the API is turned off |
| `APILOGIN` | 1 | Whether the API requires authentication. `0` is the weaker setting, not the safer one |
| `NETDIRS` | unset | Directories outside its own account an API session may open, separated by semicolons because a Windows path contains a colon |
| `SDCLIENT` | 0 | Restricts what an API session may do. Non-zero disables file access outright; `2` additionally refuses any subroutine not compiled as callable from a client |

Unset is the strict value for `NETDIRS`. With nothing there, an API session can
open files in the account it is standing in and nothing else. It never grants
the credential store, the global catalogue, `os.users` or the account register,
and naming those has no effect. A directory listed here is reachable by every
API session in every account, so it is a decision about the machine rather than
about one account.

`SDCLIENT` is not reported by the `config` verb and has no entry in the shipped
`sd.conf`. It defaults to 0, which permits everything.

## Printing

| Parameter | Default | Effect |
|---|---|---|
| `LPTRWIDE` | 80 | Default page width for the printer. Range 10 to 1000 |
| `LPTRHIGH` | 66 | Default page depth for the printer. Range 10 to 32767 |
| `SPOOLER` | empty | The spooler to hand print jobs to |
| `GDI` | 0 | Selects the Windows printing interface used by default |

## Sorting

| Parameter | Default | Effect |
|---|---|---|
| `SORTMEM` | 4096 kb | Above this much data a sort works on disk instead of in memory |
| `SORTMRG` | 4 | Files merged at once in a disk sort. Range 2 to 10 |

## Numbers and dates

| Parameter | Default | Effect |
|---|---|---|
| `INTPREC` | 13 | Digits of precision in integer arithmetic. Range 0 to 14 |
| `FLTDIFF` | 0.00000000002910 | Two floating point numbers closer together than this compare equal |
| `YEARBASE` | 1930 | The century a two-digit year is read into |

## Diagnostics

| Parameter | Default | Effect |
|---|---|---|
| `ERRLOG` | 50 kb | Size of the error log. A non-zero value below 10 KB is raised to 10 KB, and the oldest entries are discarded when it fills |
| `PDUMP` | 0 | Bit flags controlling when a process dump is written |
| `DEBUG` | unset | Bit flags enabling debugging features |
| `STARTUP` | empty | A command run when SD starts |
| `JNLMODE` | 0 | Journalling mode |
| `OBJECTS` | 0 (no limit) | Compiled programs held in memory at once |
| `OBJMEM` | 0 (no limit) | Memory those programs may occupy, in KB |

## The shell

| Parameter | Default | Effect |
|---|---|---|
| `SH` | PowerShell, interactive | The shell a bare `sh` starts |
| `SH1` | PowerShell, non-interactive | The shell `sh command` uses |

Both are full paths on a real install:

```
SH        C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -NoLogo
SH1       C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -NonInteractive -Command
```

The difference between them matters. `SH1` carries `-NonInteractive` and `SH`
does not, so a bare `sh` in a phantom or a scheduled job hands control to a
shell with nobody at the keyboard. Operating system access has its own page in
this set.

## Parameters that are accepted and do nothing

These are parsed so that an existing `sd.conf` still loads. None of them
changes SD's behaviour, and none should be offered to a site as a control.

| Parameter | Why it is inert |
|---|---|
| `NETFILES` | SDNet was removed from this port. `netfiles.c` is deleted, a `server;file` VOC reference is refused, and the request that reports open SDNet connections returns an empty list. The value is still stored and still reported, and setting it opens nothing |
| `CREATUSR` | SD has accounts rather than accounts and users, so `create.account` always creates the operating system account and there is nothing to opt in to. The value is discarded as it is read |
| `CODEPAGE` | Stored, readable and settable. Nothing acts on it |
| `EXCLREM` | Stored, readable and settable. It described exclusive access to a remote file, and there are no remote files |
| `RINGWAIT` | Stored, readable and settable. Nothing acts on it |
| `TXCHAR` | Stored, and not readable — there is no `config('TXCHAR')` |

`FILERULE` is **not** in this list, and is easy to mistake for it. Its remote
bits died with SDNet, but bit 4 is live and decides whether a `PATH:` VOC
reference may name a pathname directly.

There is no licence parameter and no licence verb. SD Core for Windows is
GPL v3 and is not licensed per site or per user; `config gpl` displays the
licence text.
