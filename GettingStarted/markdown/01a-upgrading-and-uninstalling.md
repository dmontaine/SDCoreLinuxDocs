Title: Upgrading and uninstalling
Subtitle: Replacing an existing installation, and taking SD off the machine.

This page continues [Installing SD Core](01-installation.html). SD must be
uninstalled before `installsdai.sh` will run again — it refuses outright if
`/usr/local/sdsys/bin/sd` already exists — so "upgrading" here means
uninstalling with accounts kept, then installing again.

## Upgrading

**Uninstalling with your database kept, then installing again, updates
your database in place.**

| Replaced | Kept, and not touched |
|---|---|
| the catalogue and compiled programs | your accounts and their passwords |
| the BASIC source | the private catalogue |
| the messages and include records | the commands each account may run, unless you refresh them (see below) |
| the VOC templates and library routines | your print queue and held reports |
| the SDSYS `BP` programs | everything under your own accounts, and `sd.conf` |
| terminfo, the licence, the contributor list | |

Anything SD created while it was running — your VOC included — is left exactly
as it is.

**The dictionaries are brought up to date for you.** The install step that
writes them (`write_install_dicts`) adds and updates the entries SD ships
and leaves alone any you added. If that step cannot run, the installer says
so rather than finishing quietly.

**Existing accounts do *not* pick up a release's new commands
automatically — that is a real difference from SD Core for Windows, whose
installer runs the equivalent sweep for you.** After an upgrade, log in as
`sdsys` and run:

```
:update.accounts all
```

This walks every registered account and updates its VOC from `newvoc` — a
command this release adds can then be typed in accounts that already
existed. Refusing to run it leaves those accounts working exactly as
before, with the release's fixes in the catalogue but not reachable by
name until you do. To refresh one account instead, `update.accounts` (no
`all`) run **in that account** updates just it and offers to do the rest.

Two limits are worth knowing before you rely on it.

> **SD only ever adds records to a VOC, never removes them.** An account
> that already has a verb keeps it even after a release withdraws it.
> `update.accounts` cannot be relied on to take something away.

> **A record you have customised can be held back on purpose.** Put
> `[locked]` in field 1 after the type code and the update leaves that
> record alone, naming it in a message so you know what was withheld —
> and therefore which corrections this release made that you have not
> taken. Verbs are the exception: a locked verb is updated anyway, and you
> are told which. The administrator documentation covers it under
> *Accounts and security*.

## Uninstalling

```sh
./deletesdai.sh
```

Two separate questions, each defaulting to keeping what you have:

```
Keep your existing accounts? (Y/n)
Keep your existing configuration? (Y/n)
```

**Answering "no" to accounts does not delete them on its own** — you must
then type `DELETE` at a second prompt to confirm. **A silent or partial
answer never deletes the database**; only an explicit `DELETE` does.
Deleting is permanent: every SD account, every password (including
SDSYS's), and all data stored in them.

**The uninstaller removes the ssh boundary it installed** — the
`ForceCommand` block in `/etc/ssh/sshd_config` and the helper script that
manages it — and leaves the rest of `sshd_config` as it was. **It does not
remove the `openssh-server` package itself.** It may predate SD, or be in
use by something else; taking a package off the machine is not SD's
decision to make.

The `sdusers` Linux group and the `sdsys` user are removed only on a full
`DELETE` of accounts — kept accounts need `sdusers` to remain readable, and
removing the group would orphan the permissions on your database.

## Continued in

[Your first thirty minutes](02-first-run.html) — install to a second user
signing in, in eight steps.
