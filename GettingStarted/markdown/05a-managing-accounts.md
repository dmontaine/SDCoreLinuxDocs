Title: Managing accounts
Subtitle: Group accounts, sharing one, changing an account afterwards, and deleting it.

This page continues [Accounts](05-account-types.html).

## Group accounts

A group account is a shared workspace with **no Linux user account and no
sign-in of its own**. It is how you keep separate work separate, and it is
the one kind of account that needs no way in from outside — which makes it
the only extra account available on a machine with ssh and the API both
turned off entirely.

```
create.account group payroll
modify.account payroll add fred
```

Reach it with `logto payroll`, or through an F pointer.

## Sharing a user account

```
modify.account <account> add    <user>
modify.account <account> delete <user>
```

**Both are SDSYS's, like every other administration verb** — they are
not in an ordinary account's VOC at all, so typing them anywhere else says
the verb is not recognised, not that you lack permission for it.

**This is Linux group membership, and it *is* what a grant is** — the
account's own Linux group (`sdu_`*name* for a user account, `sdg_`*name*
for a group account) is what entry to it means. Unlike SD Core for
Windows, there is no separate `grant`/`revoke`/`list.grants` set of verbs:
`modify.account add`/`delete` folds both directions into one place, with
SD's own audit line added on top of the group change.

**Read this twice, because it is the most confusing part of how SD controls
access.** Entry to an account is membership of the Linux group named in
the account's record, and **group membership is fixed at login, the same
as any Linux service.** So:

- a grant does not reach the person until they log out and back in;
- and **somebody you have just removed keeps the account until they do the
  same.**

> From an ordinary account the register is reached as `sd.accounts`, not
> `accounts` — `list sd.accounts`, `ct sd.accounts fred`. There is no tier
> column any more; the register's only state field is the suspension.

## Changing an account afterwards

```
modify.account <account> add <user>
modify.account <account> delete <user>
modify.account <account> suspended | unsuspended
```

**All of them are SDSYS's**, the same as `create.account` and `delete.account`
— run from anywhere else, `modify.account` is not in the VOC at all.

### Suspending and unsuspending

**Nothing about the account moves except the one field.** No group
membership changes, no VOC changes — every account's VOC is the whole of
`newvoc` regardless, so there is nothing left to add back. See
[Suspended](05-account-types.html#suspended-a-state-not-a-tier).

**You cannot suspend your own account, or the one you are standing in.**

### There is no remote-route keyword, and no `sh-on`/`os-on` to set

**Unlike SD Core for Windows, `modify.account` has nothing to say about
ssh, the API, `sh`, or `OS.EXECUTE`.** Every ordinary account already has
ssh and API access, unconditionally — there is no keyword to narrow or
widen it (see [Accounts](05-account-types.html#there-is-no-route-keyword-every-ordinary-account-gets-both)).
And `sh`/`OS.EXECUTE` run at the account's own Linux permissions
unconditionally too, from the moment the account exists — there is no
per-account switch behind them to grant, because this port keeps no
second wall behind the one Linux itself already provides. See the
*Administrator* set's *Accounts and security* chapter.

**`modify.password` is now the whole of what `set.password` used to be.**
Same verb, same behaviour under either name; every account has a password
from the moment it is made, so there is nothing to *set* for the first time.
Run with no argument it changes your own; SDSYS may change any account's,
naming it — see [Administrator commands](06-administrator-commands.html).

## Deleting an account

**`delete.account`** **asks once, then removes everything but the Linux
user's home directory.** The single question names exactly what will go:
the account directory, the `sdu_`/`sdg_` group, the register record, and —
for a user account whose Linux user SD created — that Linux user itself.

**The home directory is kept unless you ask otherwise:**

```
delete.account fred remove.home
```

A person's own files and ssh keys live there, so it is removed only when
asked, only for a user SD created, and only when the path is exactly what
SD expects — never a directory it did not itself create the account under.

**It will not delete a Linux user SD did not create.** The question
uses shorter wording in that case rather than promising something it will
not do — an account made before SD's own creation stamp existed, or the
account that installed SD in the first place, is left alone.

## `sdusers` membership needs a fresh login

Same reason as a grant, above. After being added to the group, log out and
back in, or you cannot read the data tree at all — and the symptom looks
like a broken install rather than a permissions problem.
