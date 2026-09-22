Title: Accounts and Security
Subtitle: Making and changing accounts, passwords, and who may enter an account.

These are the verbs that decide **who may use this installation and what
they may do with it.** They are SDSYS's set — not in any other account's
VOC at all — and almost all of them need more than the verb before they
will do anything.

> **This document is separate so that it can be withheld.** Everything in
> the administrator set describes verbs an ordinary account does not have
> and cannot run. It is a complete set on its own and **links to nothing
> outside itself**, so that handing somebody the user documentation without
> this never leaves them at a page that is not there. Where a user-set page
> is worth naming, it is named in words rather than linked.

SD folds case, so a command may be typed in either case. Commands are shown
here in lower case. In the tables, *italics* mark something you supply and
**bold** marks a word typed as it stands; braces mark an optional part.

## Read this before anything else: being SDSYS is the whole of it

**Having the verb is not having the right to use it — and there is exactly
one gate, one route in, and nothing that widens it.** Every verb on this
page is refused outright to any session that is not actually SDSYS:

```
:modify.account don suspended
Command requires administrator privileges
:delete.account sdsys
Command requires administrator privileges
:modify.password sdsys
Command requires administrator privileges
```

**Every one of those refusals came before the command was looked at.**
`delete.account sdsys` would have been refused anyway — you cannot delete
`SDSYS` — and it never got that far.

**Being SDSYS means being logged in to the machine as the `sdsys` Linux
user, at its own password, on a local session** — the keyboard, or a
desktop-sharing view of it (VNC, TeamViewer). Nothing else grants it:

| route | result |
|---|---|
| a real login as `sdsys`, local | granted |
| `sudo sd` as root | refused — root is treated as *another* administrator, not SD's |
| `sudo -u sdsys sd` / `su - sdsys` | refused — the session runs as the `sdsys` Linux user, but the login that started it was somebody else's, and the kernel's own audit trail (unforgeable without root) says so |
| `sdsys` over ssh, or the API | refused at the door — SDSYS has no remote access at all |

**This is not the elevation model SD Core for Windows uses**, and the
difference is deliberate, not a gap: Windows checks whether the session is
*elevated*; Linux checks whether the session *is* the `sdsys` account,
reached the one way that account can be reached. A `sudo`'d shell looks
like `sdsys` to the file system, but the login it came from was not — and
that distinction is exactly what closed the class of bug Windows found in
its own elevation check (an administrator's *own* account picking up SD
privilege it should never have had). There is no `sdsys` session that isn't
also a real login as `sdsys`, so there is nothing for that bug shape to
hide in here.

**Start SD as yourself, from the `sdsys` login, in an ordinary terminal —
`sd` needs no elevation, no `sudo`, because being SDSYS already *is* the
privilege.**

## Making an account: `create.account`

```
create.account user <name> {no.query}

create.account group <name> {no.query}

create.account other <name> <pathname> {no.query}
```

| | |
|---|---|
| **`user`** | an SD account **and** a Linux user account to log in as |
| **`group`** | a shared workspace with no Linux account, reached only with `logto` |
| **`other`** | an SD account over a directory you name |

> **It prompts for a password and `no.query` does not suppress that.**
> `no.query` covers the confirmation, not the credential — a password is
> never an argument anywhere in SD. **`create.account user` therefore
> cannot be driven from a script**, and a group account, which has no
> password, can.

**Every account gets the same VOC**, the whole of `newvoc` — there is no
tier, and no per-account choice of remote access either. **Every account
except SDSYS has ssh and API access by default; nothing narrows that at
creation time.** SDSYS is the one exception and it is not a setting — see
above.

### There is no second wall for `sh` or `os.execute`

SD Core for Windows gates its shell and operating-system verbs behind an
account setting (`os.users`, granted independently of everything else) —
because Windows gives a process no native way to sandbox what a shelled-out
command can reach. **Linux already has that wall, and SD does not build a
second one**: `sh`, `!` and `os.execute` run at the account's own Linux
permissions, unconditionally, the moment the account exists. There is
nothing to grant and nothing to withhold — what the account's Linux user
may read, write or run outside SD is exactly what it may do through `sh`
inside SD, because they are the same permissions.

This is why account creation asks nothing about OS access: **the answer is
already decided by every other file permission, group membership and
`umask` on the machine**, the same way it would be for that Linux user
logged in directly.

```
umask {mask}
```

With no argument `umask` reports the session's current value; with one, it
sets it — the standard Unix meaning, applied to files SD itself creates as
well as anything a shelled-out command creates. **This is a real,
per-session mechanism here for exactly the reason above** — it has no
Windows equivalent because Windows already reaches the same guarantee a
different way, one inheritable ACL entry set once by the installer, applied
by NTFS below the runtime rather than by a value a process can forget to
set.

## Changing one: `modify.account`

```
modify.account account add <user.name>
modify.account account delete <user.name>
modify.account account suspended
modify.account account unsuspended
```

### `suspended`/`unsuspended` is a state, not a tier

**Nothing about the account moves except the one field.** No group
membership changes, no VOC changes — every account's VOC is the whole of
`newvoc` regardless of the field. Three doors refuse a suspended account:
signing in, `logto`, and the API.

### `add`/`delete` is the grant

```
:modify.account don add pete
:modify.account don delete pete
```

**This is Linux group membership, and it *is* what a grant is** —
`usermod -aG` under `sd-elevate`, with SD's own audit line added. There is
no separate `grant`/`revoke`/`list.grants` set of verbs the way SD Core for
Windows has: on Windows, group membership is Windows' own mechanism and SD
wraps it with three verbs of its own name and an audit trail; on Linux the
wrapping is folded into `modify.account` instead, for the same reason
Windows's own reference names its `grant` as "not an extra capability" —
`usermod -aG` reaches the identical Linux group directly, outside SD, at
any time, by an administrator with a shell. `modify.account`'s value is the
audit line, not a gate nothing else could reach.

**`delete` is deliberately unguarded** — taking access away is always
allowed.

## Passwords: `modify.password`

```
modify.password {account}
```

With no account name it changes **your own**, and asks for the current
password first. With one, from SDSYS, it changes that account's — any
account, including SDSYS's own — and does not ask for the old password: an
administrator resetting a forgotten password does not know it.

**The password is never an argument, and a trailing token is refused rather
than ignored:**

```
:modify.password don hunter2
A password is never given on the command line; MODIFY.PASSWORD prompts for it
```

**That refusal is the point of the verb's design.** The older behaviour set
the password from the prompt and threw the extra word away without a word,
so every visible sign said it had worked — while the password had already
reached SD's command stack, and a shell's history and process list if the
verb was reached from one. Refusing does not put it back, but it says so.

The prompts are hidden, asked twice, and the account must already exist in
the register. **`modify.password` cannot be scripted**, by design.

**Under the hood, an ordinary account's own write goes through a
privileged helper it cannot bypass** (`sd-elevate cred-own`), because the
credential file (`$cred`) belongs to `sdsys` alone; an administrator — a
real `sdsys` login — writes it directly. Both follow the same visible
process from the terminal; only what happens underneath differs, and only
because the account writing its own record has no other way to reach a
file it does not own.

**SDSYS's own *Linux* login password is a separate thing** — set once,
during installation (`sudo passwd sdsys`), and changed afterward the
ordinary Linux way, not with this verb.

## Continued in

[Account Maintenance](01a-account-maintenance.html) — clean.account,
update.accounts, [locked], config, set.date and delete.account.
