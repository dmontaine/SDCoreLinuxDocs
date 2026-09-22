Title: Operating System Access
Subtitle: The `sh` and `!` verbs, and why there is no permit list behind them any more.

`sh` runs a Linux command from the SD prompt. `!` is the same verb under a
shorter name. **Unlike SD Core for Windows, there is no permit list gating
either of them here — both run for every account, unconditionally, at
that account's own Linux permissions.**

> **This document is separate so that it can be withheld.** It links to
> nothing outside the administrator set. Where a user-set page is worth naming,
> it is named in words.

SD folds case, so a command may be typed in either case. Commands are shown here
in lower case.

## The two verbs

```
sh command
! command
```

Everything after the verb is handed to the shell as typed:

```
:sh echo hello-from-the-shell
hello-from-the-shell
:! echo via-the-bang-form
via-the-bang-form
```

**Never type `sh` with nothing after it in a script.** The configured shell
for the bare form is interactive — `config` reports it as

```
SH        /bin/bash -i
SH1       /bin/bash -c
```

so a bare `sh` in a piped session, a phantom or a scheduled job hands control to
a shell with nobody at the keyboard and **waits for ever**. The `SH1` form,
which is what `sh command` uses, is non-interactive.

## The shell you get is `bash`

Pipes, redirection and chaining all work, for every account:

```
:sh echo alpha-beta | grep alpha
alpha-beta
:sh echo gamma > zzsh.txt
:sh cat zzsh.txt
gamma
```

The second and third lines are separate `sh` invocations, so **the working
directory persists between them** — the file written by one was read by the
next.

## There is no permit list, and that is a deliberate difference

**SD Core for Windows keeps a file, `os.users`, that decides per person
whether `sh`, `!`, `OS.EXECUTE` and the two full-screen editors run at
all.** It has to: Windows gives a shelled-out process no native way to be
sandboxed per SD-account, so SD built its own second wall.

**This port has no such file, and builds no second wall**, because Linux
already provides one: `sh` and `!` run at exactly the Linux permissions
the account's own Linux user already has, the same permissions that user
would have logged in at the console directly. There is nothing to grant,
nothing to withhold, and no record to edit — every account has both verbs
from the moment it is created.

## `!` sanitizes shell metacharacters; `sh` does not

**The one restriction that remains applies to a command form, not to a
person.** `!command` (and `execute 'command'` from a program) rejects shell
metacharacters before running — a sanitizer against an accidental
injection in a one-line form, applied uniformly to every account
including SDSYS. `sh command` and an interactive `sh` session give a real,
unrestricted shell to whoever reaches them — which, on this port, is
everyone, since there is no gate to reach past first.

```
:! echo hi; rm -rf /
Error 2 executing operating system command
```

## What this does not gate

**A program's `OS.EXECUTE` is not on this path either**, and needs no
permission of its own — it runs at the account's own Linux permissions,
the same as `sh`.

**The screen editors, `nano` and `micro`, need no permission either** —
see [Development and file commands](../GettingStarted/07-programmer-commands.html#editors).

## Who has these verbs

`sh` and `!` are in every account's VOC, and — unlike SD Core for
Windows — **having the verb is having the permission.** There is nothing
further to check.

## SDSYS's own shell

**SDSYS reaches `sh` and `OS.EXECUTE` the same unconditional way every
other account does**, as the `sdsys` Linux user, on a session that is
already a real local login — see [Accounts and
Security](01-accounts-and-security.html#read-this-before-anything-else-being-sdsys-is-the-whole-of-it).
Reaching SDSYS at all means being at the console, or a desktop-sharing
view of it: `sdsys` is denied ssh and network sign-in outright, so there
is no remote session for this to ever apply to.

## See also

[Accounts and Security](01-accounts-and-security.html) ·
[Sessions and Locks](02-sessions-and-locks.html) ·
[Remote Access and the Machine](05-remote-access-and-the-machine.html).
