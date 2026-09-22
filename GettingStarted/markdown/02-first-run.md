Title: Your first thirty minutes
Subtitle: From a finished install to a working account, a file and a second user signing in over ssh.

This page assumes SD Core is installed and you have never used this port
before. It is a walkthrough, not a reference — every step links to the page
that explains it properly.

**Do this first, before anything else.**

## 1. Sign out of Windows and back in

**Not optional, and not a tidiness step.** The installer put your Windows
account into the `sdusers` group, and **Windows fixes group membership when you
sign in**. Until you get a new logon token you cannot read the database at all.

**The symptom looks like a broken install, not a permissions problem**, which
is why it is step 1. The post-install check knows this: the run it offers at the
end of the installer is **always the incomplete one**, for exactly this reason.

Sign out, sign back in, then run **Check the SD installation** from the Start
Menu. It closes on a keypress.

## 2. Start SD

```
sd
```

You land in **the SD account named after your Windows login**. Nothing asks for
a password — Windows has already authenticated you.

**SD is already running.** It is a Windows service, `String Database (SD)`, and
Windows starts it at every boot. You do not type `sd -start`. See
[Running SD](03-running-sd.html).

If `sd` answers *Account ... not in register*, you are in the wrong account or
step 1 has not taken effect. If it answers *not registered for SD use*, you are
not in `sdusers`.

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
| **`term`** | your terminal type and page size — should say `Device : windows` |

**If `term` says something else and your arrow keys do not work**, run
`term windows` for this session and see
[Other hardening](13-hardening.html#the-terminal). An account created before
the `WINDOWS` definition shipped keeps its old setting until **`update.accounts`**.

**`term` also reports the page size, and SD's default is 120 × 36 — not
80 × 24.** The shipped dictionaries and the default `list` layouts are
formatted for 120 columns, so **a console window narrower than that makes
ordinary reports look wrapped or truncated** and the report is not at fault.
Widen the window, or set it for the session with `term default` — which puts
the 120 × 36 back and prints nothing while doing it, so check with a bare
`term` afterwards. `term 120,36` is the same thing typed out. See
[Other hardening](13-hardening.html#the-terminal).

## 4. Make a file and put something in it

```
create.file customers
ed customers 1001
```

**`ed`** is the **line** editor, and it needs nothing installed. If you would
rather have a full screen, **`edit`** opens the same record in Microsoft Edit
and **`micro`** opens it in micro — see
[Programmer commands](07-programmer-commands.html#editors). The old
full-screen editors `sed`, `update.record` and `modify` are all gone; see
[Not in SD Core](14-not-in-sd-core.html).

In **`ed`**: `i` to insert, type your lines, a full stop on its own line to stop
inserting, then `fi` to file and exit.

> **You do not have to write programs in `ed`.** An account's `bp` file is a
> **directory file** — an ordinary Windows folder with one file per program —
> so Notepad++, VS Code or any text editor works on it just as well:
>
> ```
> C:\ProgramData\SD\user_accounts\<account>\bp
> ```
>
> Save the file, then **`basic`** and **`catalog`** it from inside SD as usual.
> SD folds CR+LF line endings on the way in, so a Windows editor's output needs
> nothing done to it — see
> [Other hardening](13-hardening.html#line-endings).

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

**Leave this session** — `exit`, or close the window — and start a new one
signed in to Windows as `SDSYS`, the account the installer made. From that
Windows sign-in, at the machine:

```
sd
```

started **elevated**, lands you directly in SDSYS. **There is no `logto`
route into SDSYS from any other account, however elevated** — SDSYS's own
Windows sign-in is the only way in. See
[Accounts](05-account-types.html#sdsys-is-the-only-administrator).

**IF YOU ARE OVER ssh, THIS WILL NOT WORK AT ALL.** SDSYS has no ssh access,
local or remote. Sign in at the machine itself, or through a remote desktop
or remote-control product installed as a service.

## 6. Create an account for somebody else

```
create.account user jane both
```

Two things about that line, and each has caught people out:

| | |
|---|---|
| `both` | say nothing and this is the default. Name `ssh`, `api` or `none` to be narrower. See [Accounts](05-account-types.html) |
| it needs SDSYS | creating a Windows account cannot be done from any other identity |

You will be prompted for Jane's password, masked. **Refusing the prompt
creates nothing at all** — a user account cannot exist without a password.

**The password is for the API.** Console and ssh logins ask for nothing.
**Every account gets the same VOC** — there is no `programmer`/`standard`
choice to make any more.

## 7. Sign in as Jane

```
ssh jane@localhost
```

**You land directly inside SD**, not at a Windows prompt. That is the forced
command, and it applies to everyone who can reach ssh at all.

**Jane cannot log in to Windows at this machine.** She is denied the console
and Remote Desktop by group membership, deliberately. She reaches SD over ssh
or through an API client — which is what the `ssh`/`api`/`both` keyword chose.
See [ssh access](08-ssh-access.html).

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
2. **A client program against the API.** Point it at port 4243 — **not** an ssh
   tunnel any more. It needs a client library from this release, because the
   old cleartext login is gone. **The architecture must match the
   application**, and **The DLL goes in the same directory as the application
   that loads it** — Windows searches there before `PATH`.
   **If you have no client of your own, mvDeveloper is free** and is a 32-bit
   application, so it wants the 32-bit `qmclilib.dll`:
   <https://www.brianleach.co.uk/mvDeveloper>. See
   [API access](09-api-access.html) and
   [Client distribution](10-client-distribution.html).
3. **Locking an account down.** Every account gets the full VOC now, so
   confining one to just your application is a hardening step you take by
   hand — see [Security](12-security.html#what-ships-secured-before-you-change-anything).
4. **An upgrade.** Install over the top and check your data survived and
   **`update.accounts`** brought the VOC forward.

## When something goes wrong

| | |
|---|---|
| Something SD did, and who did it | `audit`, in `C:\ProgramData\SD\sdsys` |
| Diagnostics, and API connections | `errlog`, same place |
| *"the account was not created — what happened"* | `sd-elevate.log`, in `C:\ProgramData\SD` |
| The installation itself | **Check the SD installation** on the Start Menu |

[Other hardening](13-hardening.html#the-logs) explains which log answers which
question — they are not interchangeable.

**When you report something, say which build.** The release stamp is on the
sign-on banner and in `C:\Program Files\SD\changelog`.
