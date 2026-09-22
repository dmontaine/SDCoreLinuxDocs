Title: Operating System Access
Subtitle: The `sh` and `!` verbs, the list that decides who may use them, and why the list is keyed to the person rather than the account.

`sh` runs a Windows command from the SD prompt. `!` is the same verb under a
shorter name. **They are the only way out of SD to the operating system from
TCL**, and who may use them is decided by a file in the system account rather
than by an account's tier.

> **This document is separate so that it can be withheld.** It links to
> nothing outside the administrator set. Where a user-set page is worth naming,
> it is named in words.

SD folds case, so a command may be typed in either case. Commands are shown here
in lower case.

> **Every listing on this page was produced by running it**, on SD Core for
> Windows W1.0-0, from an unelevated session in an account that is on the list.

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
SH        C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -NoLogo
SH1       C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -NonInteractive -Command
```

so a bare `sh` in a piped session, a phantom or a scheduled job hands control to
a shell with nobody at the keyboard and **waits for ever**. The `SH1` form,
which is what `sh command` uses, is `-NonInteractive`.

## The shell you get is Windows PowerShell 5.1

Not `pwsh`, and the difference bites:

```
:sh echo delta && echo epsilon
At line:1 char:12
+ echo delta && echo epsilon
+            ~~
The token '&&' is not a valid statement separator in this version.
```

**`&&` and `||` do not exist there.** Nor do the ternary, null-coalescing or
null-conditional operators. Chain with `;`, and test with `if ($?) { … }`.

**Pipes and redirection do work**, for an account that is on the list:

```
:sh echo alpha-beta | findstr alpha
alpha-beta
:sh echo gamma > zzsh.txt
:sh Get-Content zzsh.txt
gamma
```

The second and third lines are separate `sh` invocations, so **the working
directory persists between them** — the file written by one was read by the
next.

## SD refuses to nest

```
:sh sd
SD is already running in this session - type EXIT to return to it.
```

The child shell is marked, and SD checks the mark:

```
:sh Get-ChildItem Env:SD_SESSION
Name                           Value
----                           -----
SD_SESSION                     1
```

**That is worth knowing when writing a script for `sh` to run** — anything it
invokes inherits `SD_SESSION`, so a script that starts SD as part of its work
will be refused, wherever it is called from.

## Who is allowed: `os.users`

**The permission is a record in a file in the system account, not a tier.**
`sdsys/os.users` holds one record per person:

| | |
|---|---|
| **record id** | the **Windows login name** |
| **field 1** | `yes` to allow `sh` and `!` |
| **field 2** | `yes` to allow `OS.EXECUTE` from a program, and the screen editors |

Anything other than `yes` means no, and **a missing file or a missing record
means no**.

**It is keyed to `@logname`, the person, not the account.** The permission
therefore does not change when somebody `logto`s somewhere else. That is
deliberate: the question *may this person reach the operating system* has one
answer per person, and an account they can enter should not be able to change
it.

### Editing it

`os.users` is an ordinary SD file in the system account, edited with `ed`
from SDSYS — which needs an elevated session to enter. **`create.account`
writes no record at all**; both fields are off for every account until
SDSYS grants them with `modify.account`'s `sh-on`/`sh-off`/`os-on`/`os-off`
keywords.

> **The file's ACL is the whole of the protection.** `os.users` is read-only
> to `sdusers` on disk, which is what stops somebody adding their own name to
> the list from inside their own account. The command processor reads it in the
> user's own process. **Without that ACL this control is decoration** — if you
> are hardening an installation, check it rather than assume it.

## The three outcomes

The gate and the metacharacter rule are separate tests, and they combine like
this:

| | plain command | pipes, redirection, chaining |
|---|---|---|
| **on the list** | runs | **runs** |
| not listed, **is SDSYS** | runs | refused **5240** |
| not listed, not SDSYS | refused **10053** | refused **10053** |

```
don is not permitted to use the operating system shell
```

is message 10053, and it names the person rather than the account.

**The middle row is the one people misread.** SDSYS, arriving without an
`os.users` entry of its own, keeps a restricted shell: it may run a
command, but not one containing shell metacharacters. **Being on the list
is what buys a real shell** — pipes, redirection and chaining are most of
what an ordinary account wants one for, and that was the ruling behind
lifting the ban for listed accounts. Being SDSYS on its own does not lift
it.

## What this does not gate

**A program's `OS.EXECUTE` is not on this path.** `OS.EXECUTE` from SD BASIC
compiles to a different opcode and is governed by field **2** of the same
record, not by field 1 and not by the metacharacter test. So the two halves are
set independently, and `sh-off` deliberately leaves `OS.EXECUTE` alone.

**The form that does go through this gate is `execute 'sh …'` from a program**,
because that runs the TCL verb.

**The screen editors read field 2**, not field 1 — an account can be refused
`sh` and still run `edit` and `micro`, and the reverse.

## Who has these verbs

`sh` and `!` are in every account's VOC — there is no tier to withhold
them. **The VOC is not the permission** — any account, including SDSYS,
whose Windows login is not in `os.users` has the verb and is refused by
it. SDSYS is the one exception: see below.

## SDSYS is a shell on this machine, and only on this machine

State this plainly to anyone with the credential for the `sdsys` Windows
account:

**SDSYS can run operating-system commands on the server as itself, the
Windows account it signed in as — from this machine, and nowhere else.**
Signing in to SDSYS at all means being at the console (or a remote-desktop
or remote-control product installed as a service, which Windows treats the
same way) — `sdsys` is denied ssh and denied network sign-in outright, so
there is no remote session for this to ever apply to.

`os.users` is not consulted for SDSYS: the same identity check that grants
administration — see [Accounts and Security](01-accounts-and-security.html#read-this-before-anything-else-being-sdsys-is-the-whole-of-it)
— grants `sh` and `OS.EXECUTE` too, unconditionally. That is *narrower*
than the old model, not wider: an elevated session in an ordinary account
used to pass this gate as well, and no longer does.

### Why there is no tunnel to worry about here

**The old concern was an administrator tier reachable through a forwarded
ssh connection that arrives looking local.** That does not apply to SDSYS:
`sshd_config`'s `AllowGroups` never includes the `sdsys` Windows account, so
there is no ssh session for SDSYS to exist in the first place, tunnelled or
not — the refusal is at the door, before authentication, not a check on
where the connection appears to originate. The API is refused the same
way, for the same account, separately. See
[Remote access and the machine](05-remote-access-and-the-machine.html).

**An ordinary account's own `os.users` grant is a different question and
still deserves the same caution the old wording gave.** `os-on` plus API
access on *any* account puts an operating-system shell behind that
account's own credential, reachable from wherever the API is reachable
from — see [What `os-on` actually costs](01-accounts-and-security.html#what-os-on-actually-costs).
That risk did not go away with the tiers; it just no longer has anything
to do with being an administrator.

The verify suite asserts all of this — the local session working, the remote one
refused, and an ordinary account admitted over that same remote route as the
control — so a future change that quietly reopened it shows up as a failing test
rather than as a page that had silently become false.

## Leaving SDSYS by `logto` is one-way

Working in `SDSYS` is elevated. **The moment that session `logto`s anywhere
else, the administrator flag is cleared and the elevated helper is
stopped** — and there is no `logto` back.

```
:logto sales
```

This session is now `sales`, an ordinary account, permanently for its own
lifetime. `logto sdsys` from here — or from any other account — is refused
outright, whatever the session's elevation: SDSYS is reached one way only,
by signing in to Windows as the `sdsys` account and starting `sd` fresh. See
[Accounts and Security](01-accounts-and-security.html#read-this-before-anything-else-being-sdsys-is-the-whole-of-it).

**This is deliberate, and stricter than the old design it replaced.** A
session that could `logto` back into SDSYS would let the elevated helper
outlive the rights it belongs to; refusing the return closes that rather
than relying on the helper alone to behave.

The step is quiet for the ordinary case: a session moving between two
ordinary accounts never had privilege, so nothing is given up and nothing
is written to the audit trail.

## See also

[Accounts and Security](01-accounts-and-security.html) ·
[Sessions and Locks](02-sessions-and-locks.html) ·
[Remote Access and the Machine](05-remote-access-and-the-machine.html).
