Title: Account types
Subtitle: Standard, Programmer, Administrator, Suspended and Group — what each one may do, and how to make one.

OpenQM gives every account the same VOC and leaves privilege to `SYSTEM`
membership. SD Core does not. **An account is created into one of three tiers,
and the tier decides what verbs its VOC contains.** There is a fourth tier,
**suspended**, which is not a capability at all — it denies entry. Group
accounts are a different thing again: a shared place, not a person.

**The tier is no longer fixed at creation.** **`modify.account`** moves an
account between all four, in either direction, and rebuilds its VOC to match at
once. See [Changing an account afterwards](#changing-an-account-afterwards).

## The three capability tiers at a glance

| | Standard | Programmer | Administrator |
|---|---|---|---|
| Verbs | 81 | 81 + 42 | 81 + 42 + 20 |
| VOC records on creation | 354 | 396 | 416 |
| Can run an application | yes | yes | yes |
| Can compile, catalogue, edit | **no** | yes | yes |
| Can create or configure files | **no** | yes | yes |
| Can administer accounts | no | no | yes |
| Windows `Administrators` | no | no | **yes** |
| Local console and Remote Desktop | denied | denied | allowed |

**`administrator` implies `programmer`.** You do not need both keywords.

### Standard — 82 verbs

What an application needs and no more: query and list (**`select`**, **`list`**,
**`get.list`** and family), spool and print, session and environment (**`logto`**,
**`date`**, **`who`**, **`set`**), screen and message, prompt and input state, and eight
read-only inspectors — **`search`**, **`list.diff`**, **`list.item`**, **`list.common`**,
**`list.vars`**, **`report.src`**, **`report.style`**, **`format`**.

Everything an application built on SD invokes, and nothing that edits code or
data in bulk.

### Programmer — 42 more

The development set: the compilers, the two full-screen editors, the
cataloguer, the file and index definition verbs, the bulk record editors and
the process introspection verbs. See [Programmer commands](07-programmer-commands.html) for what each one
is for.

### The counts are arithmetic, not observation

Installed `NEWVOC` holds 395 names, of which `%t` is a dynamic-file artefact
and the two tier lists are never copied — so **392 records reach a full VOC**.
**`create.account`** then adds four of its own (`$command.stack`, `$hold`,
`$savedlists`, `bp`):

```
ADMINISTRATOR   392 + 20 + 4 = 416
PROGRAMMER      392      + 4 = 396
STANDARD        392 - 42 + 4 = 354
```

**A standard account's total did not move when `micro` was added**, because
**`micro`** joined `NEWVOC` and `TIER.OMIT.STANDARD` at once — it is on both sides
of the subtraction.

If your counts differ, one of the two tier lists differs — which is worth
reporting.

**The same two numbers are what a tier change reports**, so you can predict
them: moving between standard and programmer is **42** records either way, and
between programmer and administrator **20**. A change that reports a different
number, or zero where it should have moved something, is worth reporting for
the same reason.

### Administrator — 20 more

Account and grant administration, system-wide state, and the shell escapes. See
[Administrator commands](06-administrator-commands.html).

> **None of the three is a wall.** An administrator can copy any verb into
> any account's VOC afterwards. **The reduced VOC is the posture an account
> starts in, not a boundary anything enforces.** The boundaries that are
> enforced are the operating system's file permissions, the ssh confinement,
> and the `os.users` permit list — not the contents of a VOC.

## Suspended — the fourth tier, and the only one that is a wall

**A suspended account cannot be entered.** It is for an account that should
stop working for a while — somebody on leave, a login being looked into — and
it is refused at all three ways in:

| | |
|---|---|
| ssh, or the console | `Account FRED is suspended` |
| **`logto`** from another account | `Account FRED is suspended` |
| the API | `User not allowed in requested account` |

The API wording is deliberately the same one it gives for an account that does
not exist and for one you are not granted, so the API cannot be used to find
out which accounts exist or what state they are in.

**It takes nothing away, which is why lifting it is free.** The VOC is left
exactly as it is, no Windows group membership moves, and the tier it displaced
is remembered — so bringing the account back puts it exactly where it was, with
nothing for you to write down. Suspending is not a substitute for deleting: it
is reversible on purpose.

**An elevated administrator can still `logto` into a suspended account.**
That is deliberate — looking at a suspended account is the usual reason to have
one, and anybody elevated could lift the suspension anyway. **What a suspension
denies is the account's own user.**

> **And a suspended administrator is still a Windows administrator.** SD
> refuses them; Windows does not. They keep their `Administrators` membership
> and their `os.users` record, so they can still elevate on the machine and
> still reach any account they could reach before. **If you are suspending an
> account to contain somebody rather than to park it, suspend it in Windows
> too.**

## Creating an account

```
create.account user <name> {administrator | programmer}
                           <ssh | api | both | none> {no.query}

create.account group <name> {no.query}

create.account other <name> <pathname> {no.query}
```

### One of `ssh`, `api`, `both`, `none` is required

**There is no default, on purpose.** An account that should only ever be
reached with **`logto`** says `none` and means it. The old silent behaviour — ssh
yes, API no — could not tell that apart from somebody who had not thought about
it.

**An administrator account always gets both and needs no keyword.** Group
accounts take none of this: they have no Windows account.

### What creating a user account actually does

| | |
|---|---|
| Makes a Windows local account | created disabled, then enabled when the password is set |
| Creates the group `sdu_<name>` | and writes it to the account record |
| Joins `sdusers` | which is what grants access to the data tree |
| Joins `sdsshonly` | **unless** `administrator` — this is what denies the console and Remote Desktop |
| Joins `Administrators` | **only** with the `administrator` keyword |
| Writes the tier to `ACCOUNTS` field 5 | so `LOGIN` cannot undo it at the next update |
| Prompts for a password | in SD, masked; it never goes on a command line |

**A user account cannot be created without a password.** Refusing the prompt
creates nothing at all. Previously it left an account you could not sign in to.

**Elevation is not optional.** Creating a Windows account needs an elevated
token, and an ordinary SD session has a filtered one. Account creation works
from the installer and from an elevated terminal, and not from a normal
session.

**`create.account user … ssh` and `… both` are refused when the machine has no
ssh server**, with a warning saying why: the account would be denied the
console and Remote Desktop and have no ssh to arrive on, so it could sign in
nowhere. `api` and `none` still work. The test is made against the machine when
you type the command, so installing an ssh server later makes `ssh` start
working. See [Installing SD Core](01-installation.html#what-you-are-asked).

## Continued in

[Managing accounts](05a-managing-accounts.html) — group accounts, sharing an
account, changing one afterwards, and deleting it.
