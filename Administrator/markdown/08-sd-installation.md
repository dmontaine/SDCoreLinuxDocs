Title: Installation and the daemon
Subtitle: What the installer puts on the machine, what an upgrade replaces, and how the daemon behaves.

This page covers the parts of installation an administrator has to live with
afterwards: the groups and permissions the installer creates, the daemon, and
what an upgrade does and does not touch.

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

The installer itself — the prompts and their defaults — is covered in the
GettingStarted set, under *Installing SD Core*, and is not repeated here.

## Two things to know before the first install

**SD cannot be installed unattended.** `installsdai.sh` asks for
confirmation, two yes/no questions about remote access, and ends by
setting three passwords at the terminal — there is no flag to skip any of
it.

The reason for the passwords is the same one Windows has: an account
without one cannot be used through the API at all, and the closing summary
would otherwise finish silently with a gap nobody noticed.

**The installer refuses to start if SD is already installed.**
`/usr/local/sdsys/bin/sd` existing is the test; uninstall with
`deletesdai.sh` first. It also refuses if run as root, or if the calling
user cannot `sudo` at all — both checked before anything on the machine
changes.

**Unlike SD Core for Windows, this installer does not refuse to run
because of a pre-existing ssh server.** `openssh-server` is installed as
an ordinary package regardless, and the ssh boundary (below) is applied to
whatever `sshd_config` it finds, non-fatally: a customised configuration
gets a warning and the command to apply the boundary by hand, not a
refusal to install at all.

## What lands where

| What | Where |
|---|---|
| Binaries | `/usr/local/bin` |
| The client library, for applications | alongside the server, under `/usr/local/sdsys/bin` |
| The elevation helper and ssh boundary script | `/usr/local/sbin` |
| Configuration | `/etc/sd.conf` |
| The SDSYS account | `/usr/local/sdsys` |
| User accounts | `/home/sd/user_accounts` |
| Group accounts | `/home/sd/group_accounts` |

Neither root can be changed. The installer does not ask.

## What the installer creates

| | |
|---|---|
| `sdusers` group | the Linux group every SD account belongs to |
| `sdsys` user | the one administrator account — a real Linux user, its own home, shell and password |
| `sdu_<name>` | one supplementary group per account, created by `create.account` |
| `sd.service`, `sdclient.socket` | the `systemd` units, enabled at boot |
| the ssh boundary | a fenced block in `/etc/ssh/sshd_config` — see [Remote access and the machine](05-remote-access-and-the-machine.html) |

Group membership takes effect at the next login, the same as any Linux
service account. An administrator added to `sdusers` while already logged
in does not have it until they log out and back in, and until then cannot
read the data tree at all. The symptom looks like a broken install and is
not one.

## The daemon

| | |
|---|---|
| Unit | `sd.service` (the daemon), `sdclient.socket` (the API listener) |
| Start type | enabled — `systemd` starts both at every boot |
| Starting | `systemctl start sd.service`, or `sd -start` |
| Stopping | `systemctl stop sd.service sdclient.socket`, or `sd -stop` |
| Created by | the installer |
| Removed by | the uninstaller |

**Stopping the daemon ends every session on the machine**, without asking. It
signals every entry in the user table and has no "are users logged in" check,
so treat it as a machine-wide action rather than an administrative
convenience.

### After an unclean shutdown

SD's shared state is a System V IPC segment (`shmget`), which **does not
survive a reboot** — a real difference from SD Core for Windows, where the
equivalent segment does and needed its own discard-and-restart logic. A
crash the machine itself rebooted from always leaves a clean slate here.
What can still happen is the daemon dying while the box stays up (killed,
or `sd.service` restarted); `sd -start` checks the actual process, not
merely the segment's presence, and says so rather than reporting a false
success — see [Running SD](../GettingStarted/03-running-sd.html).

## Upgrading

Uninstalling with the database kept, then installing again, replaces the
shipped files and preserves everything the site owns.

| Replaced | Preserved |
|---|---|
| the catalogue and compiled programs | your accounts and their passwords |
| the BASIC source | the private catalogue |
| the messages and include records | your print queue and held reports |
| the VOC templates and library routines | everything under your own accounts, and `sd.conf` |
| terminfo, the licence, the contributor list | |

**An upgrade asks nothing** at the two remote-access prompts — no tasks
page is shown, on the principle that the machine already carries the
answers and every setting has a verb that changes it afterwards
(`remote.ssh`, `remote.api` — see *Remote access and the machine*).

### Unlike SD Core for Windows, the VOC refresh is a step you run, not one the installer runs for you

**The installer does not run `update.accounts all`.** Checked directly
against `installsdai.sh`: there is no such call anywhere in it. After an
upgrade, log in as `sdsys` and run it yourself — see [Upgrading and
uninstalling](../GettingStarted/01a-upgrading-and-uninstalling.html). Until
you do, existing accounts keep working exactly as before, with the
release's fixes in the catalogue but not reachable by name.

**The dictionaries are reapplied automatically.** The definitions the
release ships are added and updated by the install step that writes them
(`write_install_dicts`), and any you added are left alone. If that step
cannot run, the installer says so rather than finishing quietly.

Neither step can take anything away. `update.accounts` only ever adds
records, so an account created before a verb was withdrawn keeps it.

## Uninstalling

```sh
./deletesdai.sh
```

**The default does not touch your accounts or your configuration.**
Removing the database needs an explicit `DELETE` confirmation beyond the
initial keep/discard prompt — see [Upgrading and
uninstalling](../GettingStarted/01a-upgrading-and-uninstalling.html).

**The uninstaller does not remove the `openssh-server` package.** It may
predate SD or be in use for something else. It does remove the ssh
boundary block it wrote, leaving the rest of `sshd_config` as it was.
