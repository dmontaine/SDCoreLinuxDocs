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

**SDSYS is a single Linux user made by the installer, not something
`create.account` can produce.** Administering SD — creating, deleting or
changing an account, changing system-wide state, reaching another account's
files without a grant — means logging in to the **machine itself**, locally,
as `sdsys`, at its own password, and running `sd`. There is no elevation
step because being logged in as `sdsys` already *is* the privilege: `sudo`,
`su`, or any route into the `sdsys` account other than a genuine login is
refused, checked against the kernel's own audit trail (which records who
actually logged in, not which account a shell is currently running as).

> **This matches SD Core for Windows's own model exactly at the result
> level**, even though the mechanism differs (a real login vs. elevation
> checked against the running session). Neither port lets an administrator
> of the underlying operating system pick up SD privilege by virtue of
> that — being a Linux `sudo`er, like being a Windows administrator,
> grants nothing by itself. The reasoning is in the *Administrator* set's
> *Accounts and security* chapter.

**SDSYS's Linux login password** is set once, during installation
(`sudo passwd sdsys`) — that is what you type at the machine's own login
prompt to reach it at all, and changing it afterward is an ordinary Linux
action (`passwd`), not an SD verb. SDSYS also has its own SD credential
(`modify.password`, run from within an SDSYS session, changes its own),
but that credential secures nothing remote: `sdsys` has no ssh or API
access at all, from anywhere, under any setting — see
[Reaching the operating system](06-administrator-commands.html).

## Creating an account

```
create.account user <name> {no.query}

create.account group <name> {no.query}

create.account other <name> <pathname> {no.query}
```

**Creating an account needs a real SDSYS session.** Creating a Linux user
account needs root, and only a genuine login as `sdsys` carries the
identity SD's own elevation helper checks before granting it — see
[SDSYS is the only administrator](#sdsys-is-the-only-administrator) above.

### There is no route keyword — every ordinary account gets both

**Unlike SD Core for Windows, there is no `ssh`/`api`/`both`/`none`
choice at creation.** The owner's ruling is literal: *"All accounts, other
than SDSYS, will have remote ssh and API access."* `create.account` does
not ask, and there is nothing to narrow — the only account with a
different remote-access shape is SDSYS itself, which has none at all, and
that is not a setting either.

### What creating a user account actually does

| | |
|---|---|
| Makes a Linux user account | `useradd -m`, password locked until SD sets it |
| Creates the group `sdu_<name>` | and writes it to the account record |
| Joins `sdusers` | which is what grants access to the data tree, and is what the ssh boundary matches against |
| Prompts for a password | in SD, masked; it never goes on a command line |

**A user account cannot be created without a password.** Refusing the
prompt creates nothing at all.

**Joining `sdusers` is the whole of the remote-access grant.** Every
`sdusers` member — every ordinary account, unconditionally — is
`ForceCommand`'d into `sd` over ssh and reachable over the API; only
`sdsys` is excluded, refused at the door on both routes rather than left
ungranted. There is no separate ssh-only or API-only membership to choose.

### What every account can do

**Every verb, from the moment it is created.** Compile, catalogue, edit,
define files and indexes, run the bulk record editors, inspect processes —
none of that is withheld any more. What an account cannot do is administer:
create, delete, or suspend another account; change system-wide
configuration. Reaching the operating system through `sh` or `OS.EXECUTE`
needs **no permission at all** — see
[There is no second wall](12a-security-and-the-operating-system.html#there-is-no-second-wall).

> **None of this is a wall inside SD.** The VOC is the same for every
> ordinary account; what actually stops one account reaching another's data
> is the operating system's own file permissions and the ssh confinement —
> not the contents of a VOC, and not a second SD-level gate on `sh`, which
> this port does not have. See the *Administrator* set's *Accounts and
> security* chapter.

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
exactly as it is and no group membership moves — suspending sets one
field and unsuspending clears it. Suspending is not a substitute for
deleting: it is reversible on purpose. See
[Changing an account afterwards](05a-managing-accounts.html#changing-an-account-afterwards).

**SDSYS can still `logto` into a suspended account.** That is deliberate —
looking at a suspended account is the usual reason to have one. **What a
suspension denies is the account's own user.**

## Continued in

[Managing accounts](05a-managing-accounts.html) — group accounts, sharing
one, changing an account afterwards, and deleting it.
