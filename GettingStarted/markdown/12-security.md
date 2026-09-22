Title: Security
Subtitle: Who you are, what that gets you, and what actually protects the database.

The identity model in SD Core is not OpenQM's and not SD on Linux's. It is
worth understanding before you test anything else, because several behaviours
that look like bugs are consequences of it.

## What ships secured, before you change anything

**A fresh install starts closed and stays closed until an administrator
opens something.** Nothing below is a setting you have to remember to
apply — it is what `create.account` and the installer already do:

| | |
|---|---|
| Every SD account | a standard Windows account with no privileged token — see [Being a Windows administrator gets you nothing](#being-a-windows-administrator-gets-you-nothing) |
| ssh | `ForceCommand`s straight into `sd`, no shell, no `sh`, no `OS.EXECUTE` — see [ssh access](08-ssh-access.html) |
| `os.users` | empty for every account `create.account` makes — `sh`, `!`, `OS.EXECUTE` and the two full-screen editors are all refused until SDSYS grants them — see [Administrator commands](06-administrator-commands.html#how-you-grant-it) |
| The API | off (`APIPORT` unset in `sd.conf`) until an administrator turns it on — see [API access](09-api-access.html) |
| The console and Remote Desktop | denied to every ordinary account (`sdsshonly`) — see [Accounts](05-account-types.html) |

**The administrator can open any of it up — `os-on`, `sdapi`, `sdssh` — and
that is a decision for their own environment, not a default to second-guess.**
Securing the transport and shipping a closed-by-default system is what this
installer is responsible for; what an administrator does with the accounts
they create afterward is theirs.

**Further hardening beyond the defaults is available, not built-in.** An
account can be locked into a single application by removing `basic` and
`run` from its own VOC (so it can neither compile nor run anything else)
and disabling its break key (`pterm break off`, so it cannot interrupt out
to a TCL prompt). Neither is a keyword on `create.account` — both are done
by hand, per account, when that account's whole purpose is one application
and nothing else.

## Signing in asks for no password

**The operating system has already authenticated you. SD asks Windows who you
are.**

| | |
|---|---|
| `sd`, no account named, Windows login `sdsys`, elevated | you land in **SDSYS** |
| `sd`, no account named, any other Windows login | you land in **the SD account with your own name** |
| no SD account of that name | refused — *Account %1 not in register* (5018) |
| not in `sdusers` | refused at the door — *not registered for SD use* (5009) |
| `sd -A<name>` | **refused unless `<name>` is your own account** (10051) |
| `logto sdsys` from any other account | **refused unconditionally**, whether or not the session is elevated — 10002, audited `LOGTO REFUSED account=SDSYS reason=SDSYS is not reachable by LOGTO` |

**SDSYS is reached one way only: sign in to Windows as the account literally
named `sdsys`, and run `sd` elevated.** Being a Windows administrator —
elevated or not — grants nothing by itself, and there is no route from any
other account into SDSYS once a session has started. See
[Accounts](05-account-types.html#sdsys-is-the-only-administrator).

> **This reverses how SD Core 1.0 and early 1.1 builds worked**, where any
> Windows administrator's own account was an SD administrator, and `logto
> sdsys` from an elevated session was the way in. If you read that in an
> older document, or remember it from testing before 18 September 2026, it
> no longer holds.

**SDSYS has its own Windows sign-in password**, set once during installation
in the window that appears after the wizard closes. It is an ordinary
Windows password, not something SD stores or checks — see
[Accounts](05-account-types.html#sdsys-is-the-only-administrator).

**`sd <command>` never asks you to set a password.** It runs and exits, so it
is not a session anybody is being invited into. In earlier builds of this port
it walked into a prompt it could never be given input for. See
[Running SD](03-running-sd.html#the-command-line).

## Being a Windows administrator gets you nothing

**Being in the `Administrators` group, elevated or not, is not being an SD
administrator.** The one and only privileged account is SDSYS, reached the
one way described above. An elevated ordinary account starts `sd` faster —
no UAC prompt mid-session — but that is the whole of what elevation does for
it; every SD-level check is unchanged.

**This is deliberate and total, not a special case for remote sessions.**
SDSYS itself is refused ssh and the API outright, from this machine or any
other — see [ssh access](08-ssh-access.html) and
[API access](09-api-access.html). There is no "administrator, but only
locally" middle case any more.

## Taking an account out of use without deleting it

**`modify.account fred suspended`** denies entry at all three ways in — ssh and
the console, **`logto`**, and the API. It is reversible with nothing to
remember: the VOC and every Windows group membership are left exactly as they
are — suspending sets one field, unsuspending clears it.

**Understand what it is and is not, because the name oversells it.**

| | |
|---|---|
| **It is** | an SD control. The three doors SD owns are shut |
| **It is not** | a Windows control. Nothing is withdrawn there |

So a suspended user's ssh connection is still accepted and SD still starts
before refusing them. **SDSYS can still `logto` into a suspended account**,
which is deliberate — that is how you look at one.

**If you are suspending an account to contain somebody rather than to park
it, disable the Windows account too.** Everything on this page rests on
Windows identity; a control that does not touch Windows cannot be the whole
answer.

## Understand what the security position rests on

**NOTHING IN SD CHECKS A SECRET AT CONSOLE OR ssh LOGIN. ACCESS IS ENTIRELY
OPERATING-SYSTEM GROUP MEMBERSHIP.**

That is not a weakening. Every SD process opens the database directly, in your
own process, under your own token. There is no data server standing between
you and the files. So:

> **While SD runs as the invoking user, account passwords organise access; they
> do not secure it.**

A password gate inside SD is not a file security boundary. The old password
model implied one the filesystem never enforced. This states the real position
instead of dressing it up.

**Passwords still matter for the API**, which is a separate door and does
require one — see [API access](09-api-access.html).

## What actually protects the database

### The tree is private from the rest of the machine

`C:\ProgramData` grants `BUILTIN\Users` read and execute by inheritance, so the
Windows default is world-readable and snooping needs no privilege at all. The
installer **breaks inheritance first** and grants narrowly: SYSTEM,
`Administrators` and `sdusers`.

**This is the step that makes the data private, and nothing at run time
Substitutes for it.**

### Your account directory is locked to you

`C:\ProgramData\SD\user_accounts\<name>` is granted to that account's own
group, to administrators and to the system, **and to nobody else**.

Before this, every SD user could read and rewrite every other user's account
files from Explorer or a command prompt — outside SD, so none of SD's own
permission checks applied. SD has always refused to let you **`logto`** an account
you are not a member of; this makes the files agree with that.

**Nothing you type changes, and your own account is unaffected** — you are a
member of its group.

> A directory whose Windows group has been removed is **skipped deliberately**
> and named in the report. Locking it to a group that no longer exists would
> take the account away from the person who owns it.

### The system directories are read-only to ordinary users

Seven parts of the SD data area could be changed by anyone in `sdusers`. They
are now readable by everyone who needs them and writable only by an
administrator:

```
sdsys\accounts    the register of accounts
sdsys\$map        sdsys\messages    sdsys\newvoc
sdsys\bp          sdsys\cat         SD's own programs
sd.conf           the configuration read at start-up
```

**Nothing an ordinary user does needs to write them** — not the spooler, not
saved lists, not a phantom. The commands that *do* write them are already
administrator commands and are unaffected.

**`sdsys\$ipc` is deliberately unchanged.** Every session writes to it, and
it is how a **`phantom`** is given its command.

The global catalogue and the pcode library are locked the same way.

> **An existing installation is not changed by an upgrade**, because the
> installer never overwrites a data area that is already there. To apply it to
> one you already have, run this once per path from an elevated prompt:
>
> ```
> powershell -ExecutionPolicy Bypass -File "C:\Program Files\SD\secure-sysdirs.ps1" -Path "C:\ProgramData\SD\sdsys\accounts"
> ```

### The credential file

**ON INSTALLS MADE BEFORE 17 Aug 2026, EVERY SD USER COULD WRITE THE FILE SD
KEEPS ACCOUNT PASSWORDS IN.** No password is stored there — SD keeps a
scrambled verifier that cannot be turned back into a password — but **being
able to replace one was enough**: a user could put in a verifier for a password
of their own choosing and sign in as somebody else, including through the API.

The installer was always meant to lock that file down and never did. The step
ran, reported nothing, and had no effect, because of a quoting fault in how it
was called. **Nothing in the install looked wrong.**

**Reinstalling is what fixes it.** To check without reinstalling, from an
**ordinary** (not administrator) prompt:

```
icacls "C:\ProgramData\SD\sdsys\$CRED"
```

If that prints permissions, the file is still open. **If it says "Access is
denied", it is protected — which is what you want.**

## Continued in

[Security and the operating
system](12a-security-and-the-operating-system.html) — reaching the operating
system from inside SD, privileged work, and the audit trail.
