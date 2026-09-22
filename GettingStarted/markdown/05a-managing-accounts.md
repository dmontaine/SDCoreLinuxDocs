Title: Managing accounts
Subtitle: Group accounts, sharing one, changing an account afterwards, and deleting it.

This page continues [Accounts](05-account-types.html).

## Group accounts

A group account is a shared workspace with **no Windows account and no
sign-in of its own**. It is how you keep separate work separate, and it is
the one kind of account that needs no way in from outside — which makes it
the only extra account available on a machine with no ssh server and no API.

```
create.account group payroll
modify.account payroll add fred
```

Reach it with `logto payroll`, or through an F pointer.

## Sharing a user account

```
grant   <account> to   <user>
revoke  <account> from <user>
list.grants <account>
```

**All three are SDSYS's, like every other administration verb** — they are
not in an ordinary account's VOC at all, so typing them anywhere else says
the verb is not recognised, not that you lack permission for it.

**Read this twice, because it is the most confusing part of how SD controls
access.** Entry to an account is membership of the Windows group named in
the account's record, and **Windows fixes group membership when you sign
in**. So:

- a grant does not reach the person until they sign out of Windows and back in;
- and **somebody you have just revoked keeps the account until they do the
  same.**

Both verbs print that reminder every time.

**`list.grants`** also shows the account's own user, which is always there
and is not a grant. It is listed anyway so that what you see matches the
Windows group it is reporting.

> From an ordinary account the register is reached as `sd.accounts`, not
> `accounts` — `list sd.accounts`, `ct sd.accounts fred`. There is no tier
> column any more; the register's only state field is the suspension.

## Changing an account afterwards

```
modify.account <account> add | delete <user>
modify.account <account> ssh | api | both | none
modify.account <account> sh-on | sh-off | os-on | os-off
modify.account <account> suspended | unsuspended
```

**All of them are SDSYS's**, the same as `create.account` and `delete.account`
— run from anywhere else, `modify.account` is not in the VOC at all.

### Suspending and unsuspending

**Nothing about the account moves except the one field.** No Windows
membership changes, no VOC changes — every account's VOC is the whole of
`newvoc` regardless, so there is nothing left to add back. See
[Suspended](05-account-types.html#suspended-a-state-not-a-tier).

**You cannot suspend your own account, or the one you are standing in.**

### The remote routes

**The keyword says what the access is, not what to add.** So

```
modify.account fred api
```

gives Fred the API **and takes ssh away**. If you want both, say `both`. The
message afterwards always names both routes, so you can see what you have
left him with.

### Reaching the operating system

`sh-on`, `sh-off`, `os-on` and `os-off` set the two fields of the account's
`os.users` record without your having to edit it by hand — field 1 is the
**`sh`** verb (and **`!`**), field 2 is `OS.EXECUTE` and the two full-screen
editors, **`edit`** and **`micro`**. Both default to off for every account
`create.account` makes. See the *Administrator* set's *Restricted operating
system access* chapter.

**These four are switches, not names for one state** — `sh-off` leaves
`OS.EXECUTE` alone, and the other way round.

**`modify.password` is now the whole of what `set.password` used to be.**
Same verb, same behaviour under either name; every account has a password
from the moment it is made, so there is nothing to *set* for the first time.
Run with no argument it changes your own; SDSYS may change any account's,
naming it — see [Administrator commands](06-administrator-commands.html).

## Deleting an account

**`delete.account`** **asks once, then removes everything.** The single
question names exactly what will go, including the Windows account when
there is one to remove.

**It will not delete a Windows account SD did not create.** The question
uses shorter wording in that case rather than promising something it will
not do.

## `sdusers` membership needs a fresh logon

Same reason as a grant, above. After being added to the group, sign out of
Windows and back in, or you cannot read the data tree at all — and the
symptom looks like a broken install rather than a permissions problem.
