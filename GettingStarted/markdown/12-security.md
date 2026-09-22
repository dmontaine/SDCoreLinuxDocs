Title: Security
Subtitle: Who you are, what that gets you, and what actually protects the database.

The identity model in SD Core is not OpenQM's. It is worth understanding
before you test anything else, because several behaviours that look like
bugs are consequences of it.

## What ships secured, before you change anything

**A fresh install starts closed and stays closed until an administrator
opens something remote.** Nothing below is a setting you have to remember
to apply — it is what `create.account` and the installer already do:

| | |
|---|---|
| Every SD account | an ordinary Linux user with no elevated rights of its own — see [Being able to `sudo` gets you nothing](#being-able-to-sudo-gets-you-nothing) |
| ssh | `ForceCommand`s straight into `sd`, no shell reachable that way — see [ssh access](08-ssh-access.html) |
| `sh`, `!`, `OS.EXECUTE` | run at the account's own Linux permissions, unconditionally — there is no separate permit list to keep here, unlike SD Core for Windows. This port keeps no second wall behind the one Linux itself already provides |
| The API | local-only (`127.0.0.1:4243`) until an administrator opens it to the network — see [API access](09-api-access.html) |
| SDSYS | no remote route at all, ssh or API, ever, from anywhere — the one thing this page treats as non-negotiable rather than a default |

**Unlike SD Core for Windows, an ordinary account is not denied a console
login here.** SD keeps no second wall behind the one Linux permissions
already provide, so there is nothing a console login grants an account
that its ssh session (which already reaches `sh` unconditionally) did not
already have. See [Security and the operating
system](12a-security-and-the-operating-system.html).

**The administrator can open the API to the network — `remote.api`,
`remote.ssh` — and that is a decision for their own environment, not a
default to second-guess.** Securing the transport and shipping a
closed-by-default system is what this installer is responsible for; what
an administrator does with the accounts they create afterward is theirs.

**Further hardening beyond the defaults is available, not built-in.** An
account can be locked into a single application by removing `basic` and
`run` from its own VOC (so it can neither compile nor run anything else)
and disabling its break key (`pterm break off`, so it cannot interrupt out
to a TCL prompt). Neither is a keyword on `create.account` — both are done
by hand, per account, when that account's whole purpose is one application
and nothing else.

## Signing in asks for no password

**The operating system has already authenticated you. SD asks Linux who you
are.**

| | |
|---|---|
| `sd`, no account named, logged in as `sdsys`, locally | you land in **SDSYS** |
| `sd`, no account named, any other Linux login | you land in **the SD account with your own name** |
| no SD account of that name | refused — *Account %1 not in register* (5018) |
| not in `sdusers` | refused at the door — *not registered for SD use* (5009) |
| `sd -a<name>` | **refused unless `<name>` is your own account** (10051) |
| `logto sdsys` from any other account | **refused unconditionally**, whether or not the session came in as `root` — 10002, audited |

**SDSYS is reached one way only: log in to the machine, locally, as the
account literally named `sdsys`, its own password, and run `sd`.** Being
able to `sudo` — able to or not — grants nothing by itself, and there is no
route from any other account into SDSYS once a session has started. See
[Accounts](05-account-types.html#sdsys-is-the-only-administrator).

**SDSYS has its own Linux login password**, set once during installation
(`sudo passwd sdsys`). It is an ordinary Linux password, not something SD
stores or checks — see
[Accounts](05-account-types.html#sdsys-is-the-only-administrator).

**`sd <command>` never asks you to set a password.** It runs and exits, so it
is not a session anybody is being invited into.

## Being able to `sudo` gets you nothing

**Being in the `sudo` group, having used it recently or not, is not being an
SD administrator.** The one and only privileged account is SDSYS, reached
the one way described above. SD checks the kernel's own audit loginuid,
which records who actually logged in and cannot be forged by `sudo` or
`su` — every SD-level check rests on that, not on the account a shell
happens to be running as.

**This is deliberate and total, not a special case for remote sessions.**
SDSYS itself is refused ssh and the API outright, from this machine or any
other — see [ssh access](08-ssh-access.html) and
[API access](09-api-access.html). There is no "administrator, but only
locally over the network" middle case; SDSYS's only route is a genuine
local login.

## Taking an account out of use without deleting it

**`modify.account fred suspended`** denies entry at all three ways in — ssh and
the console, **`logto`**, and the API. It is reversible with nothing to
remember: the VOC and every group membership are left exactly as they
are — suspending sets one field, unsuspending clears it.

**Understand what it is and is not, because the name oversells it.**

| | |
|---|---|
| **It is** | an SD control. The three doors SD owns are shut |
| **It is not** | a Linux control. Nothing is withdrawn there |

So a suspended user's ssh connection is still accepted and SD still starts
before refusing them. **SDSYS can still `logto` into a suspended account**,
which is deliberate — that is how you look at one.

**If you are suspending an account to contain somebody rather than to park
it, lock the Linux account too** (`usermod -L`, or `passwd -l`). Everything
on this page rests on Linux identity; a control that does not touch Linux
cannot be the whole answer.

## Understand what the security position rests on

**NOTHING IN SD CHECKS A SECRET AT CONSOLE OR ssh LOGIN. ACCESS IS ENTIRELY
OPERATING-SYSTEM GROUP MEMBERSHIP.**

That is not a weakening. Every SD process opens the database directly, in your
own process, under your own Linux identity (a real `setuid`, not a filtered
token — see [API access](09-api-access.html#an-api-session-runs-as-you)).
There is no data server standing between you and the files. So:

> **While SD runs as the invoking user, account passwords organise access; they
> do not secure it.**

A password gate inside SD is not a file security boundary. The old password
model implied one the filesystem never enforced. This states the real position
instead of dressing it up.

**Passwords still matter for the API**, which is a separate door and does
require one — see [API access](09-api-access.html).

**And ordinary Linux file permissions are the actual wall**, the same as
they would be for that user logged in directly with no SD in the picture
at all — not an SD-specific ACL scheme layered on top. `umask` (see the
*Administrator* set's *Accounts and security* chapter) governs what
permissions a file gets when SD, or a shelled-out command, creates one; it
is a real, per-session mechanism here, unlike on some ports.

## What actually protects the database

### The credential file

**`$cred`, where SD keeps the scrambled password verifiers, is owned by
`sdsys` alone and mode `700`** — nobody else can even list it, let alone
read a verifier out of it. No password is stored there in any form SD
could turn back into a password; what a verifier being readable would cost
is somebody constructing one for a password of their own choosing and
signing in as somebody else, including through the API. Check it directly:

```sh
sudo -u <some-other-account> ls /usr/local/sdsys/\$cred
```

should refuse for anyone but `sdsys`.

### `batch.jobs` is read-only to ordinary accounts

The allow-list [Scheduled jobs](04-scheduled-jobs.html) reads from is
`sdsys:sdusers`, mode `750` — every account can read it (needed, since
`login` checks it on their behalf), nobody but `sdsys` can write it. A user
who could add a line to their own record would be granting themselves
the unattended command line.

### Your own account's data

**Every SD process runs as the invoking Linux user, so ordinary Linux file
permissions are what actually separates one account's data from
another's** — not a rule SD enforces from inside itself. SD has always
refused to let you `logto` an account you are not a member of; whether the
*files* agree with that, outside SD entirely, is a question of how the
account directories under `/home/sd/user_accounts` are permissioned on
this particular machine, the same as it would be for any other Linux
service account layout. If your deployment needs guaranteed cross-account
file isolation, check and set that permission scheme deliberately rather
than assume it — this is one of the places "the only limits are those
Linux imposes" cuts both ways.

## Continued in

[Security and the operating
system](12a-security-and-the-operating-system.html) — reaching the operating
system from inside SD, privileged work, and the audit trail.
