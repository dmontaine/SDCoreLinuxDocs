Title: Your first thirty minutes
Subtitle: From a finished install to a working account, a file and a second user signing in over ssh.

This page assumes SD Core is installed and you have never used this port
before. It is a walkthrough, not a reference — every step links to the page
that explains it properly.

**Do this first, before anything else.**

## 1. Log out and back in

**Not optional, and not a tidiness step.** The installer put your Linux
user into the `sdusers` group, and **group membership is fixed at login,
the same as any Linux service.** Until you get a new session you cannot
read the database at all.

**The symptom looks like a broken install, not a permissions problem**,
which is why it is step 1.

Log out, log back in (or reboot, if you took the installer's offer), then
open a terminal.

## 2. Start SD

```
sd
```

You land in **the SD account named after your Linux login**. Nothing asks
for a password — Linux has already authenticated you, at the console or
over ssh.

**SD is already running.** It is a `systemd` service, `sd.service`, enabled
at every boot; `sdclient.socket` is what actually opens the API port. You
do not type `sd -start`. See [Running SD](03-running-sd.html).

If `sd` answers *Account ... not in register*, you are in the wrong account
or step 1 has not taken effect. If it answers *not registered for SD use*,
you are not in `sdusers`.

## 3. Look around

```
who
listf
term
```

| | |
|---|---|
| **`who`** | the account you are standing in |
| `listf` | the files in it |
| **`term`** | your terminal type and page size |

**`term` also reports the page size, and SD's default is 120 × 36 — not
80 × 24.** The shipped dictionaries and the default `list` layouts are
formatted for 120 columns, so **a terminal narrower than that makes
ordinary reports look wrapped or truncated** and the report is not at
fault. Widen the window, or set it for the session with `term default` —
which puts the 120 × 36 back and prints nothing while doing it, so check
with a bare `term` afterwards. `term 120,36` is the same thing typed out.
See [Other hardening](13-hardening.html#the-terminal).

## 4. Make a file and put something in it

```
create.file customers
ed customers 1001
```

**`ed`** is the **line** editor, and it needs nothing installed —
**`edit`** is an alias for it, not for a full-screen editor (a difference
from SD Core for Windows, where `edit` opens Microsoft Edit; there is no
Linux equivalent to alias it to). For a full screen, **`nano`** opens the
record in `nano` and **`micro`** opens it in `micro` — see
[Programmer commands](07-programmer-commands.html#editors). The old
full-screen editors `sed`, `update.record` and `modify` are all gone; see
[Not in SD Core](14-not-in-sd-core.html).

In **`ed`**: `i` to insert, type your lines, a full stop on its own line to stop
inserting, then `fi` to file and exit.

> **You do not have to write programs in `ed`.** An account's `bp` file is a
> **directory file** — an ordinary Linux directory with one file per program —
> so any text editor works on it just as well:
>
> ```
> /home/sd/user_accounts/<account>/bp
> ```
>
> Save the file, then **`basic`** and **`catalog`** it from inside SD as usual.

```
list customers
count customers
```

**Commands are lower case now**, and so are the VOC records behind them. Typing
`LIST` still works — SD tries what you typed, then lower case, then upper. See
[Lower case](11-lower-case.html).

**THIS IS THE POINT AT WHICH MOST THINGS SHOULD FEEL LIKE OpenQM.** If
anything in ordinary data work behaves differently and is not described in this
set, that is worth reporting.

## 5. Become SDSYS

**Leave this session** — `exit`, or close the window — and log in to the
machine itself, locally, **as** `sdsys`, its own password. From there, at
the machine:

```
sd
```

lands you directly in SDSYS, with no elevation needed — being logged in
as `sdsys` already *is* the privilege. **There is no `logto` route into
SDSYS from any other account, however `sudo`'d.** See
[Accounts](05-account-types.html#sdsys-is-the-only-administrator).

**IF YOU ARE OVER ssh, THIS WILL NOT WORK AT ALL.** SDSYS has no ssh
access, local or remote, under any setting. Log in at the machine itself,
or through a desktop-sharing view of it (VNC, TeamViewer).

## 6. Create an account for somebody else

```
create.account user jane
```

Two things about that line, and each has caught people out:

| | |
|---|---|
| no `ssh`/`api` keyword | every ordinary account gets both by default now — there is no per-account choice at creation. See [Accounts](05-account-types.html) |
| it needs SDSYS | creating a Linux user account cannot be done from any other identity |

You will be prompted for Jane's password, masked. **Refusing the prompt
creates nothing at all** — a user account cannot exist without a password.

**The password is for the API.** Console and ssh logins ask for nothing.
**Every account gets the same VOC** — there is no `programmer`/`standard`
choice to make any more.

## 7. Sign in as Jane

```
ssh jane@localhost
```

**You land directly inside SD**, not at a Linux shell. That is the forced
command, and it applies to everyone who can reach ssh at all except
`sdsys`.

Jane can, however, log in to the console at this machine directly, the
same as any Linux user — SD keeps no second wall behind ssh here (see
[Security and the operating system](12a-security-and-the-operating-system.html)).
What she cannot do is reach SD's own administration, which is `sdsys`'s
alone regardless of how she logged in.

`ssh localhost` needs no network and works on a machine with no network
connection at all.

## 8. Leave

```
off
```

## What to try next, in rough order of how likely it is to find something

1. **Your own application data.** **There is no restore utility**, so the
   way in is a short BASIC program that reads your exported data and writes the
   records. Then query it — the query processor is where most of the surface
   area is.
2. **A client program against the API.** Point it at port 4243. It needs a
   client library from this release, because the old cleartext login is
   gone — `sdclilib.so`, built as part of this port, or the source at
   <https://github.com/dmontaine/linuxsdclilib>. See
   [API access](09-api-access.html) and
   [Client distribution](10-client-distribution.html).
3. **Locking an account down.** Every account gets the full VOC now, so
   confining one to just your application is a hardening step you take by
   hand — see [Security](12-security.html#what-ships-secured-before-you-change-anything).
4. **An upgrade.** Install over the top and check your data survived, then
   run **`update.accounts all`** as `sdsys` to bring existing VOCs forward —
   see [Upgrading and uninstalling](01a-upgrading-and-uninstalling.html).

## When something goes wrong

| | |
|---|---|
| Something SD did, and who did it | `audit`, in `/usr/local/sdsys` |
| Diagnostics, and API connections | `errlog`, same place |
| *"the account was not created — what happened"* | `sd-elevate.log`, alongside the installer |

[Other hardening](13-hardening.html#the-logs) explains which log answers which
question — they are not interchangeable.

**When you report something, say which build.** The release stamp is on the
sign-on banner and in `sd --version`.
