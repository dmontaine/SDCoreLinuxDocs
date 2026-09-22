Title: Upgrading and uninstalling
Subtitle: Replacing an existing installation, and taking SD off the machine.

This page continues [Installing SD Core](01-installation.html).

## Upgrading

**Installing a new release over an existing one updates your database.**

| Replaced | Kept, and not touched |
|---|---|
| the catalogue and compiled programs | your accounts and their passwords |
| the BASIC source | the private catalogue |
| the messages and include records | which Windows users are linked to which SD accounts |
| the VOC templates and library routines | the commands each account may run |
| the SDSYS `BP` programs | your print queue and held reports |
| terminfo, the licence, the contributor list | everything under your own accounts, and `sd.conf` |

Anything SD created while it was running — your VOC included — is left exactly
as it is.

**The dictionaries are brought up to date for you.** Upgrading reapplies the
dictionary definitions the release ships: it adds and updates the entries SD
ships and leaves alone any you added. If that step cannot run, the installer
says so at the end rather than finishing quietly, and `upgrade-dicts.log` in
`C:\ProgramData\SD` says what happened.

**Every account's VOC is brought up to date for you.** The installer runs
`update.accounts all`, which walks every registered account, so a command this
release adds can be typed in accounts that already existed. This did not happen
before W1.0-0: an upgrade replaced the shipped files and no existing account —
including the system account — ever gained a new verb.

To refresh one account by hand afterwards, `update.accounts` in that account
updates it and offers the rest.

Two limits are worth knowing before you rely on it.

> **SD only ever adds records to a VOC, never removes them.** An account created
> before a verb was withdrawn keeps it. `update.accounts` cannot be relied on to
> take something away.

> **A record you have customised can be held back on purpose.** Put `[locked]`
> in field 1 after the type code and the upgrade leaves that record alone,
> naming it in a message so you know what was withheld — and therefore which
> corrections this release made that you have not taken. Verbs are the
> exception: a locked verb is updated anyway, and you are told which. The
> administrator documentation covers it under *Accounts and security*.

## Uninstalling

It is the standard Windows uninstall — Settings ▸ Apps, or `unins000.exe`.

**The default does not touch your accounts, the database or the
configuration.** Inno removes only what it installed and only removes a
directory if it is empty, so everything the running system created is invisible
to it.

**Removing the data is a separate, opt-in prompt** that defaults to keeping it,
and says exactly what it destroys and where. **A silent uninstall never
deletes the database**, whatever the prompt would have offered.

**The uninstaller does not remove OpenSSH.** It may predate SD or be in use by
something else. It does restore `sshd_config`, keeping the original as
`sshd_config.before-sd` — but it deliberately does **not** widen the firewall
rule back, because restoring it would mean opening a port on the way out.
