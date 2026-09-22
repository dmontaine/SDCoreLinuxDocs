Title: Installing SD Core
Subtitle: What the installer does to the machine, and the choices it puts in front of you.

There is a compiler to run. `installsdai.sh` clones the source from
`github.com/dmontaine/SDCore4Linux` and builds it on your machine — there is
no prebuilt package and no installer binary. A clone builds; that is why
installing means building.

This is a real difference from SD Core for Windows, which ships as a single
installer carrying its own compiled runtime. Windows has one target and one
ABI; this port currently supports Debian and Ubuntu (detected from
`/etc/os-release`) and builds from source so that changes elsewhere in the
system — library versions, kernel, `libssl` — are accounted for at build
time rather than papered over by a bundled runtime.

## Before you start

**Run it as yourself, not as root and not with `sudo`.** The script refuses
outright if `$EUID` is 0 — building as root would leave build artefacts
root-owned, and the script needs to know who "the installing user" is to
create your own SD account. It asks for your `sudo` password itself, at the
one point where it is needed, and checks up front that you can `sudo` at
all: a caller who cannot is refused in words, before anything changes,
rather than partway through with `sudo`'s own error.

**SD cannot be installed silently.** This is deliberate, not a missing
feature. The script asks two questions whose answers cannot be defaulted
safely — whether to open ssh and the API to other computers — and ends by
setting three passwords at the terminal.

**The installer does not ask where to put SD.** The roots are fixed. See
[What lands where](#what-lands-where).

**It refuses to start, and changes nothing, if SD is already installed** —
`/usr/local/sdsys/bin/sd` existing is the test. Uninstall first (see
[Upgrading and uninstalling](01a-upgrading-and-uninstalling.html)).

## Getting the installer

Clone the repository, or fetch `installsdai.sh` on its own — the script
itself clones the source it actually builds from, so having the whole
repository first is a convenience, not a requirement:

```sh
git clone https://github.com/dmontaine/SDCore4Linux
cd SDCore4Linux
chmod +x installsdai.sh
./installsdai.sh
```

The script downloads its own working copy of the source to
`~/.sdb64tmp`, builds from there, and deletes it when the install
finishes — it does not use the clone you ran it from as the build tree.

## What you are asked

After confirming you want to continue, two questions, both defaulting to
**no**:

```
Allow ssh access from other computers? enables sshd at boot, opens port 22 (y/N)
Allow API access from other computers? opens TCP port 4243 (y/N)
```

**Answering "no" to both is a real, supported deployment**, not a degraded
one — it gives a working SD reachable only at this machine's own keyboard,
over `ssh localhost`, or by a local API client. Both settings have a verb
that changes them later (`remote.ssh`, `remote.api` — see the Administrator
set's *Remote access and the machine*), so nothing here is a one-time
choice.

**Neither question is about whether an ssh server or an API listener
exist.** They always do — `openssh-server` is installed as an ordinary
package regardless of the answer, and SD's API socket is always defined
(`sdclient.socket`, activated by `systemd` independently of whether `sd`
itself is running). What the two questions actually decide:

| Question | "no" (default) | "yes" |
|---|---|---|
| ssh | `sshd` is left however the box already had it; the SD boundary (below) is written to `sshd_config` regardless, ready for whenever ssh is turned on | `sshd` is enabled at boot and `ufw allow 22/tcp` is added |
| API | `sdclient.socket` listens on `127.0.0.1:4243` only — a remote client reaches it by tunnelling over ssh (`ssh -L 4243:127.0.0.1:4243 <host>`) | the socket is rebound to `0.0.0.0:4243` and `ufw allow 4243/tcp` is added |

**The ssh boundary is applied either way, and it is what actually confines
SD accounts.** Every account except SDSYS is `ForceCommand`'d into `sd` the
moment it connects over ssh — it never reaches a plain shell that way — and
SDSYS is refused a network login outright, at the door, however the two
questions above were answered. This step is **non-fatal**: if `sshd_config`
has already been customised, the installer warns rather than aborting (SD
is otherwise installed and working) and prints the exact command to apply
it by hand once the conflict is resolved:

```sh
sudo /usr/local/sbin/ssh-forcecommand --install
```

## What lands where

| What | Where |
|---|---|
| Binaries | `/usr/local/bin` |
| The changelog | shipped with the source tree |
| Configuration | `/etc/sd.conf` |
| The SDSYS account | `/usr/local/sdsys` |
| User accounts | `/home/sd/user_accounts` |
| Group accounts | `/home/sd/group_accounts` |

### Configuration

Server and client both read `SD_CONFIG` first and fall back to
`/etc/sd.conf`. It is installed once and left alone on a later install over
a kept database, so your edits survive both an upgrade and a reinstall.

## What the installer creates on the machine

| | |
|---|---|
| `sdusers` | the Linux group every SD account belongs to. Everyone who uses SD needs it |
| `sdsys` | the one administrator account — a real Linux user with its own home, shell and password, never `root` |
| `sdu_<name>` | one supplementary group per account, created by `create.account` |
| `sd.service`, `sdclient.socket` | the `systemd` units that run SD and its API listener, enabled to start at boot |
| the ssh boundary | a fenced block in `/etc/ssh/sshd_config`, `ForceCommand`ing every `sdusers` member except `sdsys` into `sd`, and denying `sdsys` a network login outright |

**Group membership needs a fresh login to take effect**, the same as on any
Linux box — if you were just added to `sdusers`, log out and back in (or
start a new session) before expecting `sd` to work.

## Ownership and administration

**Being SDSYS means being logged in to the machine as the `sdsys` Linux
user, at its own password, on a local session** — the keyboard, or a
desktop-sharing view of it (VNC, TeamViewer). There is no `sudo` or `su`
route into it: a session that reaches the `sdsys` account any way other
than a real login as `sdsys` is refused, and `sdsys` cannot sign in over
ssh at all. See [Security](12-security.html).

## The full-screen editors

**The installer installs `micro` as an ordinary package**, because the
`micro` verb runs it. `nano` normally ships with Debian and Ubuntu already;
if `/usr/share/nano` exists, the installer adds SD's own BASIC syntax
highlighting to it system-wide (`/usr/share/nano/sdbasic.nanorc`). Neither
is offered as a choice — an account with an editor verb that does nothing
is worse than either answer. **`ed`**, the line editor, needs nothing and
always works.

If `micro`'s package install fails, the install still succeeds; `micro`'s
own syntax file still needs a per-user copy (`~/.config/micro/syntax`),
which the installer also stages where it can.

## Changing any of it afterwards

Both remote-access settings have a verb that changes them later, which is
why an upgrade does not ask the two questions again. Both are SDSYS's, and
both report when given no keyword:

| | |
|---|---|
| `remote.ssh on` \| `off` | who may reach the ssh server from off this machine |
| `remote.api on` \| `local` \| `off` | whether SD opens its API socket, and who may reach it |

They are covered in the Administrator set, under *Remote access and the
machine*.

## At the end

The install ends by setting three passwords, at the terminal, each with its
own numbered heading — asked at most three times, and skipped with a clear
"kept from the previous install" if one from an earlier install (or an
earlier attempt) is already there:

```
1 of 3: Password for the SD <you> account
2 of 3: Password for the LINUX sdsys account
3 of 3: Password for the SD sdsys account
```

**These are three different things, deliberately kept apart:**

| | What it unlocks |
|---|---|
| 1. Your own SD password | reaching your account through the SD API (SCRAM) — not needed at all for a local `sd` session, which your Linux login already reaches |
| 2. `sdsys`'s Linux password | logging in to the machine **as** `sdsys` — the only way to administer SD |
| 3. `sdsys`'s SD password | reaching SDSYS through the API — and even with it, SD admits `sdsys` over the API only from a process already running as `sdsys` on this machine |

All three are required — the closing summary names any that are still
missing and prints the exact `MODIFY.PASSWORD` command to set it,
afterward, as `sdsys`.

The closing summary also restates: **SD is administered only by logging in
as `sdsys`, its own password, and running `sd`** — that session has every
admin verb. There is no `sudo` or `su` route into it, and `sdsys` cannot
log in over ssh; a desktop-sharing view of the console works because it is
a local login.

It then offers to reboot, so that group membership changes and the
`systemd` units take effect cleanly. After rebooting (or a fresh login),
open a terminal and type `sd`.

## Continued in

[Upgrading and uninstalling](01a-upgrading-and-uninstalling.html) — upgrading
an existing installation, and uninstalling.
