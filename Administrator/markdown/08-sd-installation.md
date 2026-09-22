Title: Installation and the service
Subtitle: What the installer puts on the machine, what an upgrade replaces, and how the service behaves.

This page covers the parts of installation an administrator has to live with
afterwards: the groups and permissions the installer creates, the service, and
what an upgrade does and does not touch.

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

The wizard itself — the pages, the tick boxes and their defaults — is covered
in the SD Core for Windows release documentation, under *Installing SD Core*,
and is not repeated here.

## Two things to know before the first install

**SD cannot be installed silently.** `/SILENT` and `/VERYSILENT` are refused
with a message rather than ignored.

The reason is the password. Installing ends by asking for one, and an
unattended install has nobody to ask — it would finish with no password on any
account, and an account without a password cannot be used at all: not at the
keyboard, not over ssh, and not through the API. A `/NOPASSWORD` escape was
written and then removed, on the grounds that a switch buying a
credential-less system is a switch somebody will paste from a forum.

Remote Desktop is not unattended and is unaffected. The wizard runs and a
person answers it.

**The installer refuses to start on a machine with an ssh server it does not
own.** It changes nothing and tells you what it found. Three cases:

- another ssh server holding port 22
- an ssh service that is not part of Windows, installed even if it is not
  running
- Windows' own ssh server with settings somebody has already changed

The check runs before the wizard is drawn, so a refusal costs nothing. Remove
the other server, or put the ssh configuration back the way Windows shipped it,
and run the installer again.

This is why SD can make promises about ssh behaviour at all: it configures the
server so that SD sessions land inside SD and cannot reach a command prompt,
and it can only promise that about a server it installed and configured itself.

## What lands where

| What | Where |
|---|---|
| Binaries, and the MSYS2 DLLs beside them | `C:\Program Files\SD\usr\bin\` |
| The client DLLs, for applications | `C:\Program Files\SD\usr\clients\` |
| The installed PowerShell scripts | `C:\Program Files\SD\` |
| The changelog | `C:\Program Files\SD\changelog` |
| Configuration | `C:\ProgramData\SD\sd.conf` |
| The SDSYS account | `C:\ProgramData\SD\sdsys\` |
| User accounts | `C:\ProgramData\SD\user_accounts\` |
| Group accounts | `C:\ProgramData\SD\group_accounts\` |
| Shared memory | `C:\ProgramData\SD\shm\` |

Neither root can be changed. The installer does not ask.

> **Do not move the binaries.** `usr\bin` is load-bearing. Shipping
> `msys-2.0.dll` beside the executable relocates the POSIX root to the DLL's
> directory minus two components, so moving them moves SD's idea of the file
> system.

The client DLLs are the one thing under `Program Files` meant to be copied
elsewhere. `usr\clients\client64\` holds the 64-bit pair and
`usr\clients\client32\` the 32-bit pair, for applications that link against
SD. The 64-bit pair also appears in `usr\bin`, and that copy is the server's
own — a local client connection resolves `sd.exe` beside the DLL, so only a
copy sitting next to `sd.exe` can make one.

## What the installer creates

| | |
|---|---|
| `sdusers` group | grants access to the files under `C:\ProgramData\SD` |
| `sdsshonly` group | carries the deny rights that confine an account to ssh |
| `sdu_<name>` | one group per account, created by `create.account` |
| The service | **String Database (SD)**, automatic start |
| ACLs | inheritance broken on `C:\ProgramData\SD`, access granted narrowly |

Group membership is carried in a Windows logon token, which is issued at sign-in.
An administrator added to `sdusers` while signed in does not have it until
they sign out and back in, and until then cannot read the data tree at all. The
symptom looks like a broken install and is not one.

## The service

| | |
|---|---|
| Display name | **String Database (SD)** |
| Service name | `SD` |
| Start type | automatic — Windows starts it at every boot |
| Starting | `Start-Service SD`, or `sd -start` |
| Stopping | `Stop-Service SD`, or `sd -stop` |
| Created by | the installer |
| Removed by | the uninstaller |

**Stopping the service ends every session on the machine**, without asking. It
signals every entry in the user table and has no "are users logged in" check,
so treat it as a machine-wide action rather than an administrative
convenience.

### After an unclean shutdown

A shared memory segment left behind by an abrupt stop survives a reboot on
Windows. SD discards it and starts normally, saying so:

```
Discarding the shared segment left by the previous boot -
SD did not shut down cleanly.
```

## Upgrading

Installing a new release over an existing one replaces the shipped files and
preserves everything the site owns.

| Replaced | Preserved |
|---|---|
| the catalogue and compiled programs | your accounts and their passwords |
| the BASIC source | the private catalogue |
| the messages and include records | which Windows users are linked to which SD accounts |
| the VOC templates and library routines | your print queue and held reports |
| terminfo, the licence, the contributor list | everything under your own accounts, and `sd.conf` |

**An upgrade asks nothing.** No tasks page is shown, on the principle that the
machine already carries the answers and every setting has a verb that changes
it afterwards — `ssh.server`, `remote.ssh`, `remote.api` and `append.sd.path`,
covered under *Remote access and the machine* in this set.

### Two steps run for you, and both report

**Every account's VOC is refreshed.** The installer runs `update.accounts all`,
which walks every registered account so that a verb this release adds can be
typed in accounts that already existed.

This is newer than it sounds and is worth stating plainly: before W1.0-0 an
upgrade replaced the shipped files and **no existing account, including SDSYS,
ever gained a new verb**. A fix that added a VOC record reached only accounts
created afterwards.

**The dictionaries are reapplied.** The definitions the release ships are added
and updated, and any you added are left alone. If that step cannot run, the
installer says so at the end rather than finishing quietly, and
`upgrade-dicts.log` in `C:\ProgramData\SD` records what happened.

Neither step can take anything away. `update.accounts` only ever adds records,
so an account created before a verb was withdrawn keeps it.

## Uninstalling

Settings ▸ Apps, or `unins000.exe`.

**The default does not touch your accounts, the database or the
configuration.** Removing the data is a separate prompt that defaults to
keeping it.

**The uninstaller does not remove OpenSSH.** It may predate SD or be in use for
something else. It does restore `sshd_config`, keeping the version SD wrote as
`sshd_config.before-sd`.
