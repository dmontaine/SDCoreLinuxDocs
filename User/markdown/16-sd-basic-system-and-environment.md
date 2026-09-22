Title: SD Basic - System and Environment
Subtitle: Asking SD about itself, about the machine, and about the session you are in.

This page covers the enquiries: what time is it, who am I, where is the data,
what did the last thing that failed say, and what may this account do. Most of
it is one function, `system()`.

SD folds case, so a program may be written in either case. Keywords are shown
here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

> **Values that are particular to one machine — a user number, a computer
> name, a process id — are marked as examples; the shapes are not.** What you
> see back will differ in the value and match in the form.

## SYSTEM()

```
system(key)
```

### The session

| Key | | Value |
|---|---|---|
| `7` | terminal type | `linux` |
| `9` | CPU time used, ms | `45` |
| `12` | time, as `time()` | `70787` |
| `18` | **user number** | `67` (example) |
| `23` | break key enabled? | `1` |
| `24` | echo enabled? | `1` |
| `25` | is this a phantom? | `0` |
| `26` | prompt character | `?` |
| `1000` | `capturing` in effect? | `0` |
| `1001` | case inversion on? | `0` |
| `1029` | internal subroutine depth | `0` at the top, `1` inside a `gosub` |
| `1030` | login time, internal | `1851017987` |
| `1031` | operating system process id | `605` (example) |
| `1050` | administrator? | `0` |

### The machine

| Key | | Value |
|---|---|---|
| `31` | licence number | `0` |
| `42` | IP address | *empty* |
| `91` | is this Windows? | `0` — this port is never Windows |
| `1006` | Windows NT style? | `0` — vestigial, never set on this port |
| `1009` | endian — 0 little | `0` |
| `1010` | platform name | `Linux` |
| `1012` | SD version | `L1.0-0` |
| `1013` / `1014` | user limit, without / with the phantom pool | `20` / `20` |
| `1015` | computer name | `myhost` (example) |
| `1017` | port number of a tcp connection | `0` |
| `1028` | system id | `1028` |

**`system(91)` and `system(1006)` are both Windows-only questions, and
both read `0` here — that is not a keys-to-leave-alone caveat, it is the
correct answer.** `system(1010)` is the one that actually tells you the
platform: `Linux`, reliably.

### Paths — one form, no translation layer

| Key | | Value |
|---|---|---|
| `32` | the `sdsys` directory | `/usr/local/sdsys` |
| `38` | the temporary directory | `/tmp` (example — falls back to the system default when `TEMPDIR` is unset in `sd.conf`) |
| `1011` | the configuration file | `/etc/sd.conf` |
| `1024` | the directory SD was started in | `/home/don/myproject` (example) |

**Unlike SD Core for Windows, which reads paths back in up to three
different spellings** (a backslash path, a POSIX `/cygdrive/` path, and a
forward-slash drive path, because its runtime sits on top of a POSIX
emulation layer) **— there is only one spelling here.** This port runs
natively, so every path `system()` returns is an ordinary Linux path, and
`@sdsys` and `@path` agree with it without any conversion to worry about.

### Lists and structures

| Key | | |
|---|---|---|
| `1002` | the call stack | field per level: `path`, then `offset` and line pairs — `.../BP.OUT/ZZMATH` at line 41, then `$CPROC` |
| `1003` | open files | field per file, `unit` and path. **`$ipc` is always one of them** |
| `1025` | environment variables | **two fields**: field 1 every name, field 2 every value, value-mark separated |

`system(1025)` returns **2** fields, every name in the first — it is not a
list of `NAME=value` pairs.

### Time

| Key | | |
|---|---|---|
| `1005` | internal time | `date() * 86400 + time()` — the difference is **0** |
| `1020` | milliseconds since midnight | `9587454` |

`system(1020)` is the one to time something with: against a lock wait it gives
252 ms where `time()` gives 0.

## DATE, TIME and TIMEDATE

```
date()      time()      timedate()
```

Taken together at one instant:

| | |
|---|---|
| `date()` | `21423` — days since 31 December 1967 |
| `time()` | `70787` — seconds since midnight |
| `timedate()` | `19:39:47 26 AUG 2026` |
| `oconv(date(), 'D4-')` | `08-26-2026` |
| `oconv(time(), 'MTS')` | `19:39:47` |

`@date` and `@time` hold the same numbers, **but they are set once per command**
rather than read afresh, so in a long loop they do not move while `date()` and
`time()` do.

`timedate()` returns a formatted string, not a number. Do not do arithmetic on
it — see
[SD Basic - Data Conversion](06-sd-basic-data-conversion.html) for the
conversion codes.

## ENV()

```
env(name)
```

**`env()` is case sensitive, the ordinary Linux rule** — a wrong case
looks exactly like a missing variable, because on Linux it *is* a
different name.

| | |
|---|---|
| `env('PATH')` | non-empty |
| `env('path')` | **empty** — no such variable, lower case |
| `env('HOME')` | your home directory |
| `env('NOSUCHVAR')` | empty |

**Get the spelling from `system(1025)` field 1 rather than from memory**
if you are ever unsure what a variable is actually called in this
session's environment.

## CONFIG()

```
config(name)
```

On a stock installation:

| | |
|---|---|
| `config('FILERULE')` | `0` |
| `config('GRPSIZE')` | `2` |
| `config('MAXIDLEN')` | `63` |
| `config('NUMFILES')` | `80` |
| `config('NUMLOCKS')` | `100` |
| `config('SORTMEM')` | `4096` |
| `config('SPOOLER')` | empty |

**The name is case sensitive and at most eight characters. both failures now
look the same**, which is the point — a name that is too long is a name that
does not exist, and a caller cannot tell the two apart:

| | |
|---|---|
| `config('numlocks')` — right name, wrong case | empty, `status()` **1004** |
| `config('NOSUCHKEY')` — **nine** characters | empty, `status()` **1004** |

**Keep every `config()` name to eight characters and upper case.**

Neither call aborts the caller: a name that is too long comes back empty with
a status, the same as a name that does not exist.

## SYSMSG()

```
sysmsg(number {, substitution ...})
```

Returns the text of one of SD's own messages, with `%s` substitutions filled
in.

| | |
|---|---|
| `sysmsg(2831)` | `Unrecognised statement` |
| `sysmsg(6711, 'ABC')` | `Unable to find source record ABC` |
| `sysmsg(2201)` | `Account name '' is not in register` — an unfilled substitution comes back empty |
| `sysmsg(99999)` | `[99999] Message not found` |
| `sysmsg(1)` | `[1] Message not found` |

**A message number is not a `status()` code.** They are separate numbering
schemes that overlap. `status()` **3006** is *record not found*; `sysmsg(3006)`
is `Modes: `. Do not render a status code by passing it to `sysmsg()`.

`get.messages()` takes **no arguments** and returned **nothing** — zero fields
— in an ordinary session. It reports messages sent between sessions, and
nothing had sent any.

## Continued in

[SD Basic - Status, Encryption and the
Machine](16a-sd-basic-status-and-the-machine.html) — status codes, checksums,
encryption, umask, the @variables, os.execute and logmsg.
