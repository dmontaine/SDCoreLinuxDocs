Title: Administrator commands
Subtitle: The verbs only SDSYS has, and how to use them.

**These verbs are not in an ordinary account's VOC at all.** SD Core used to
give an *administrator-tier* account a larger VOC than a *programmer*
account's; that model is gone. Every ordinary account now gets the same VOC
— see [Accounts](05-account-types.html) — and administration is not a verb
an account can be given. It is SDSYS, a single Windows account the installer
makes, reached by signing in to Windows as SDSYS and running `sd`, elevated.
Typing one of these verbs from any other account says it is not recognised,
not that you lack permission for it.

## Accounts

```
create.account  user <name> {ssh|api|both|none}
create.account  group <name>
delete.account  <name>
modify.account  <name> add|delete <user>
modify.account  <name> ssh|api|both|none
modify.account  <name> sh-on|sh-off|os-on|os-off
modify.account  <name> suspended|unsuspended
update.accounts {all}
clean.account
```

Covered in full in [Accounts](05-account-types.html) and
[Managing accounts](05a-managing-accounts.html). The points worth repeating
here:

- **Say nothing and `create.account user` gets `both`** (ssh and the API).
  Name `ssh`, `api` or `none` to be narrower.
- **`modify.account` says what the access *is*, not what to add.**
  `modify.account fred api` takes ssh away.
- **`suspended`/`unsuspended`** is a state, not a tier — nothing about the
  VOC moves either way, because every account's VOC is the whole of `newvoc`
  regardless.
- **`update.accounts`** only ever adds VOC records it finds missing, from a
  release that shipped verbs the account was created before. Since every
  account already has the whole VOC, this now matters only after an
  *upgrade* — a fresh account never needs it.

**`clean.account`** tidies an account's workspace. **`update.accounts`** is
the one you run in each account after upgrading SD.

## Grants

```
grant       <account> to   <user>
revoke      <account> from <user>
list.grants <account>
```

**A grant or a revoke does not take effect until the person signs out of
Windows and back in.** Entry to an account is Windows group membership, and
Windows fixes that at logon. **Somebody you have just revoked keeps the
account until they get a new token.** Both verbs print the reminder every
time.

## Passwords

```
modify.password {<account>}
```

**A password cannot be typed on the command line.** **`modify.password`**
refuses one given as an argument. A password on a command line is visible to
any local user through Task Manager or `Get-CimInstance Win32_Process`, so
SD prompts for it instead, masked.

Run with no argument it changes your own; from SDSYS, naming an account
changes that account's — every account, including SDSYS's own. The password
matters for **API logins only**. Console and ssh logins ask for nothing —
see [Security](12-security.html).

**SDSYS's *Windows* sign-in password is a different thing entirely** — set
once, during installation, and changed afterward the ordinary Windows way,
not with this verb. See [Accounts](05-account-types.html#sdsys-is-the-only-administrator).

## Locks and sessions

```
lock / unlock
list.locks / clear.locks
listu / list.readu
logout
```

**`unlock` is the one to know about.** It clears a record lock left behind
by a session that died holding one. Without it the only way to release such
a lock is to stop and restart SD, which disconnects everybody.

**`listu`** and **`list.readu`** report sessions and read locks; **`logout`**
ends another session.

## System state

```
config
set.date
```

**`config`** reports the configuration parameters in force.

## The remote doors

```
remote.api on | local | off
remote.ssh on | off
ssh.server ...
append.sd.path ...
```

These four set up the machine's own remote-access surface rather than any
one account's — see [ssh access](08-ssh-access.html) and
[API access](09-api-access.html) for what each one does.

## The shell escapes — `sh` and `!`

**Who may use `sh` is a list you keep, not a matter of elevation** — and
that has been true since before the tiers went, so nothing here changed
with them. `sh` and `!` are in every ordinary account's VOC; whether they
*do* anything is a separate permission, kept in `os.users`.

### The list

One record per person in `os.users`, **keyed by the name they sign in with,
not by the account name**. The login name follows the person, so it does
not change when they **`logto`** somewhere else.

### How you grant it

**Four keywords on `modify.account` do it without your editing anything:**

```
modify.account fred sh-on      the sh verb and ! at the prompt
modify.account fred sh-off
modify.account fred os-on      OS.EXECUTE, and the edit and micro editors
modify.account fred os-off
```

**They are four switches over two fields**, not four names for one state,
so `sh-off` leaves `OS.EXECUTE` alone — and the verb prints the resulting
record, both fields, every time. **Both default to off**, for every account
`create.account` makes.

### SDSYS always has both, from any session

**SDSYS reaches `sh`, `!`, `OS.EXECUTE`, `edit` and `micro` regardless of
`os.users`** — the same identity check that gates administration (see
[Accounts](05-account-types.html#sdsys-is-the-only-administrator)) grants
this too. **`modify.account sdsys` is refused outright, for every action,
not only these four** — *"Remote access is never available to SDSYS"* is
the message whatever you asked for, because the refusal comes before the
action is even parsed: SDSYS is outside this verb's reach entirely, not
only for the routes the wording names.

### Or edit the record by hand

The record is ordinary data. From SDSYS, because the file is writable only
by SDSYS:

```
ed os.users don
```

The record is two lines and nothing else. To give `don` the shell and the
editors:

```
yes
yes
```

In **`ed`**: `i` to insert, type the two lines, a full stop on its own line
to stop inserting, then `fi` to file and exit. **Field 1 is `SH`, field 2 is
`OS.EX`** — the order matters and there is nothing else in the record.

| What you want `don` to have | Field 1 | Field 2 |
|---|---|---|
| nothing outside SD | *no record at all* | |
| the editors, but no shell at the prompt | anything but `yes` | `yes` |
| a shell, but programs may not shell out | `yes` | anything but `yes` |
| both | `yes` | `yes` |

**`don` is the Windows login name, not the SD account name.** They are
usually the same; where they are not, this file wants the one the person
signs in with.

**The change takes effect on their next command**, not at their next login
— the list is read when the shell or the editor is asked for.

**To take it away, set the field to anything else or delete the record.**
Deleting the record removes both.

| Field | Controls | Value |
|---|---|---|
| 1 | `SH` — a shell at the command prompt | `yes`, or anything else for no |
| 2 | `OS.EX` — `OS.EXECUTE` from inside a program, **and the `edit` and `micro` editors** | `yes`, or anything else for no |

**Field 2 is what lets an account use the full-screen editors.** They run
an editor outside SD, so they are reaching the operating system whatever
the VOC says. An account with the verb and no `yes` in field 2 is told the
command is not available and what to ask for.

**A missing record, or a missing file, means no.** An account
`create.account` makes has no record at all until SDSYS grants one — see
[How you grant it](#how-you-grant-it) above.

### Both fields are enforced

`OS.EXECUTE` used to be unchecked entirely, so **any account that could
write a program had the operating system** and the **`sh`** restriction
could be walked around by anyone able to type BASIC. Field 2 is what
decides whether `OS.EXECUTE` may run. The refusal reads *`<name>` is not
permitted to use OS.EXECUTE*.

The two fields are independent, and the useful combination is the third
row:

```
unlisted            sh refused    OS.EXECUTE refused
SH=yes OS.EX=no     sh RUNS       OS.EXECUTE refused
SH=no  OS.EX=yes    sh refused    OS.EXECUTE RUNS      <- programs may shell
                                                          out; the person at
                                                          the prompt may not
SDSYS                sh runs       OS.EXECUTE RUNS
```

SD's own system programs are exempt, so **`create.account`** and the
**`sh`** verb work as before.

### Three rules that go with it

**Only SDSYS can edit the list.** `os.users` is read-only to everybody
else on disk, and **that ACL is the whole of what stops a user granting
themselves a shell. Do not loosen those permissions.**

**A listed person gets a real shell** — pipes, redirection and chaining all
work: `sh dir | more`. **SDSYS gets the restricted form**, which rejects
those characters — the same shape of restriction an elevated ordinary
session used to get before this model existed, now applied to the one
account it actually matters for.

### Neither is available over the API

**`sh`** and `OS.EXECUTE` are refused to a session that arrived over the
API. An API session is not treated as SDSYS for any purpose, and SDSYS has
no API route to arrive over in the first place — see
[API access](09-api-access.html).

## The full list

**`create.account`** · **`delete.account`** · **`modify.account`** ·
**`update.accounts`** · **`clean.account`** · **`grant`** · **`revoke`** ·
**`list.grants`** · **`unlock`** · **`config`** · **`listu`** ·
**`list.readu`** · **`list.locks`** · **`clear.locks`** · **`lock`** ·
**`logout`** · **`set.date`** · **`remote.api`** · **`remote.ssh`** ·
**`ssh.server`** · **`append.sd.path`**

**`sh`, `!` and `modify.password` are not on this list** — every account
has them; what SDSYS has that an ordinary account does not is the
`os.users` permission behind the first two (see above) and the right to
name a different account with the third.
