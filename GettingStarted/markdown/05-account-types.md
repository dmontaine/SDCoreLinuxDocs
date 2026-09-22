Title: Accounts
Subtitle: Ordinary accounts, SDSYS, Suspended and Group — what each one may do, and how to make one.

**Every ordinary account gets the same VOC.** SD Core used to divide accounts
into three capability tiers — Standard, Programmer, Administrator — each with
a different, smaller VOC. **The tiers are gone** (owner's ruling, 18 September
2026: *"the only privileged account is SDSYS"*). An account you create today
gets every verb there is, the same set SDSYS has for running applications and
building them. What it does **not** get is administration — that is not a
verb an account can be given, it is a separate account.

**Suspended** is a state, not a tier — it denies entry and nothing else. Group
accounts are a different thing again: a shared place, not a person.

## SDSYS is the only administrator

**SDSYS is a single Windows account made by the installer, not something
`create.account` can produce.** Administering SD — creating, deleting or
granting accounts, changing system-wide state, reaching another account's
files without a grant — means signing in to *Windows* as SDSYS and running
`sd`, elevated. Being a Windows administrator grants nothing by itself: the
account that ran this installer is an ordinary account like any other once
setup finishes, and **elevating a session does not make it SDSYS**.

> **This is a full reversal of how SD Core 1.0 worked**, where a Windows
> administrator's own account was automatically an SD administrator. If you
> read that in an older document or in W1.0 release notes, it no longer
> holds. The reasoning is in the *Administrator* set's *Accounts and
> security* chapter.

**SDSYS's Windows sign-in password** is asked for once, during installation,
in the window that appears after the wizard closes — that is what you type
at the Windows login screen to reach it at all, and changing it afterward is
an ordinary Windows administrative action, not an SD verb. SDSYS also has its
own SD credential (`modify.password`, run from within an SDSYS session,
changes its own), but that credential secures nothing remote: `remote.api`,
`remote.ssh` and every other door out of SDSYS are refused outright, on
purpose — see [Reaching the operating system](06-administrator-commands.html).

## Creating an account

```
create.account user <name> {ssh | api | both | none} {no.query}

create.account group <name> {no.query}

create.account other <name> <pathname> {no.query}
```

**Creating an account needs an elevated SDSYS session.** Creating a Windows
account needs an elevated token, and only SDSYS carries the identity that
makes an elevated session mean anything to SD — see
[SDSYS is the only administrator](#sdsys-is-the-only-administrator) above.

### The route keyword is optional now

**Say nothing and the account gets `both`** (ssh and the API). Name one to be
narrower: `ssh` for ssh only, `api` for the API only, `none` for neither —
an account reached only with `logto`, from inside another session.

**`create.account user … ssh` and `… both` are refused when the machine has no
ssh server**, with a warning saying why: the account would have no way to
arrive over ssh. `api` and `none` still work. The test is made against the
machine when you type the command, so installing an ssh server later makes
`ssh` start working. See [Installing SD Core](01-installation.html#what-you-are-asked).

### What creating a user account actually does

| | |
|---|---|
| Makes a Windows local account | created disabled, then enabled when the password is set |
| Creates the group `sdu_<name>` | and writes it to the account record |
| Joins `sdusers` | which is what grants access to the data tree |
| Joins `sdsshonly` | this is what denies the console and Remote Desktop — every ordinary account gets it now; only SDSYS's own Windows account does not |
| Joins `sdssh` and/or `sdapi` | to match the route keyword — see below |
| Prompts for a password | in SD, masked; it never goes on a command line |

**A user account cannot be created without a password.** Refusing the prompt
creates nothing at all. Previously it left an account you could not sign in
to.

**`sdssh` and `sdapi` govern the ssh and API doors specifically, separately
from `sdsshonly`.** An account with route `none` still joins `sdsshonly` like
every other ordinary account — that has always denied the *Windows* console
and Remote Desktop, and has nothing to do with ssh — it simply also has
neither `sdssh` nor `sdapi`, so it has no remote door of any kind and can
only be reached with `logto`.

### What every account can do

**Every verb, from the moment it is created.** Compile, catalogue, edit,
define files and indexes, run the bulk record editors, inspect processes —
none of that is withheld any more. What an account cannot do is administer:
create, delete, grant, or suspend another account; change system-wide
configuration; or reach the operating system through `sh` or `OS.EXECUTE`
unless SDSYS has switched that on for it — see
[Reaching the operating system](05a-managing-accounts.html#reaching-the-operating-system).

> **None of this is a wall inside SD.** The VOC is the same for every
> ordinary account; what actually stops one account reaching another's data
> is the operating system's file permissions, the ssh confinement, and the
> `os.users` permit list for `sh`/`OS.EXECUTE` — not the contents of a VOC.
> See the *Administrator* set's *Accounts and security* chapter.

## Suspended — a state, not a tier

**A suspended account cannot be entered.** It is for an account that should
stop working for a while — somebody on leave, a login being looked into —
and it is refused at all three ways in:

| | |
|---|---|
| ssh, or the console | `Account FRED is suspended` |
| **`logto`** from another account | `Account FRED is suspended` |
| the API | `User not allowed in requested account` |

The API wording is deliberately the same one it gives for an account that
does not exist and for one you are not granted, so the API cannot be used to
find out which accounts exist or what state they are in.

**It takes nothing away, which is why lifting it is free.** The VOC is left
exactly as it is and no Windows group membership moves — suspending sets one
field and unsuspending clears it. Suspending is not a substitute for
deleting: it is reversible on purpose. See
[Changing an account afterwards](05a-managing-accounts.html#changing-an-account-afterwards).

**SDSYS can still `logto` into a suspended account.** That is deliberate —
looking at a suspended account is the usual reason to have one. **What a
suspension denies is the account's own user.**

## Continued in

[Managing accounts](05a-managing-accounts.html) — group accounts, sharing
one, changing an account afterwards, and deleting it.
