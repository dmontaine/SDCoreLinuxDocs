Title: Administrator commands
Subtitle: The verbs only SDSYS has, and how to use them.

**These verbs are not in an ordinary account's VOC at all.** SD Core used to
give an *administrator-tier* account a larger VOC than a *programmer*
account's; that model is gone. Every ordinary account now gets the same VOC
— see [Accounts](05-account-types.html) — and administration is not a verb
an account can be given. It is SDSYS, a single Linux user the installer
makes, reached by logging in to the machine itself, locally, as `sdsys`,
its own password, and running `sd`. Typing one of these verbs from any
other account says it is not recognised, not that you lack permission for
it.

## Accounts

```
create.account  user <name>
create.account  group <name>
delete.account  <name> {remove.home}
modify.account  <name> add|delete <user>
modify.account  <name> suspended|unsuspended
update.accounts {all}
clean.account
```

Covered in full in [Accounts](05-account-types.html) and
[Managing accounts](05a-managing-accounts.html). The points worth repeating
here:

- **There is no `ssh`/`api`/`none` keyword.** Every ordinary account has
  both by default, unconditionally; only SDSYS is different, and that is
  not a setting.
- **`modify.account add`/`delete`** is the grant — Linux group membership,
  with SD's own audit line on top. There is no separate `grant`/`revoke`
  pair of verbs.
- **`suspended`/`unsuspended`** is a state, not a tier — nothing about the
  VOC moves either way, because every account's VOC is the whole of `newvoc`
  regardless.
- **`update.accounts`** only ever adds VOC records it finds missing, from a
  release that shipped verbs the account was created before. Since every
  account already has the whole VOC, this now matters only after an
  *upgrade* — a fresh account never needs it, and **the installer does not
  run it for you**: run `update.accounts all` yourself after an upgrade.
- **`delete.account`** keeps the Linux user's home directory unless you
  add `remove.home` — a person's own files and ssh keys live there.

**`clean.account`** tidies an account's workspace. **`update.accounts`** is
the one you run in each account after upgrading SD.

## Passwords

```
modify.password {<account>}
```

**A password cannot be typed on the command line.** **`modify.password`**
refuses one given as an argument. A password on a command line is visible to
any local user through `ps`, so SD prompts for it instead, masked.

Run with no argument it changes your own; from SDSYS, naming an account
changes that account's — every account, including SDSYS's own. The password
matters for **API logins only**. Console and ssh logins ask for nothing —
see [Security](12-security.html).

**SDSYS's *Linux* login password is a different thing entirely** — set
once, during installation, and changed afterward the ordinary Linux way
(`passwd`), not with this verb. See
[Accounts](05-account-types.html#sdsys-is-the-only-administrator).

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
umask {mask}
```

These set up the machine's own remote-access surface rather than any
one account's — see [ssh access](08-ssh-access.html) and
[API access](09-api-access.html) for what each one does. There is no
`ssh.server`/`append.sd.path` pair here: this port does not manage an ssh
server as an installable feature (the distribution's own package does that)
and puts `sd` on `PATH` at install time rather than as a toggle.

## The shell — `sh` and `!`

**Unlike SD Core for Windows, there is no permit list to keep and nothing
to grant.** `sh`, `!` and `OS.EXECUTE` run for every account, from the
moment it is created, at that account's own Linux permissions —
unconditionally. There is no `os.users` file, no `sh-on`/`os-on` switch on
`modify.account`, and nothing an administrator needs to do before an
account can use them. This port keeps no second wall behind the one Linux
itself already provides: what an account's Linux user may read, write or
run outside SD is exactly what it may do through `sh` inside SD, because
they are the same permissions. See the *Administrator* set's *Accounts and
security* chapter, "There is no second wall for `sh` or `os.execute`."

**`sh` gives a real, full shell** — pipes, redirection and chaining all
work: `sh dir | more`. **`!` (`os.command`), the single-line inline form,
sanitizes shell metacharacters before running** — a safety measure against
an accidental injection in a one-liner, applied uniformly to every account
rather than tied to who is running it. Neither is a permission tier;
both simply do what their shape suggests.

### Neither is available over the API

**`sh`** and `OS.EXECUTE` are refused to a session that arrived over the
API. An API session is not treated as a local session for any purpose, and
SDSYS has no API route to arrive over in the first place — see
[API access](09-api-access.html).

## The full list

**`create.account`** · **`delete.account`** · **`modify.account`** ·
**`update.accounts`** · **`clean.account`** · **`unlock`** · **`config`** ·
**`listu`** · **`list.readu`** · **`list.locks`** · **`clear.locks`** ·
**`lock`** · **`logout`** · **`set.date`** · **`remote.api`** ·
**`remote.ssh`** · **`umask`**

**`sh`, `!` and `modify.password` are not on this list** — every account
has them; what SDSYS has that an ordinary account does not is the right to
name a different account with `modify.password`.
