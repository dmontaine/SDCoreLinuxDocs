Title: Installing SD Core
Subtitle: What the installer does to the machine, the two kinds of installation, and the choices it puts in front of you.

There is no compiler to run and no dependency to resolve. SD Core for Windows
ships as a single `sd-setup-W1.0-0.exe`, carries its own runtime beside
`sd.exe`, and installs in one pass.

This is the largest single difference from the regular SD version — that, and
the fact that this version is for Windows and not Linux. In regular SD,
`installsdai.sh` existed because ScarletDME targeted four distributions and the
end user had to compile; Windows has one target and one ABI, so none of that
transfers.

## Before you start

**You need an elevated session.** The installer creates local groups, sets
file permissions, registers a service and assigns user rights. You can start
the install from a normal console session — you will get an elevation prompt.

**SD cannot be installed silently.** This is deliberate, not a missing
feature. The installer asks questions whose answers cannot be defaulted safely
— which kind of installation, whether to expose ports, and the password on the
account it makes for you.

**The installer does not ask where to put SD.** Both roots are fixed. See
[What lands where](#what-lands-where).

### It checks the machine before it changes anything

The installer refuses to start, and changes nothing, if it finds:

- another ssh server using port 22, or
- an ssh service that is not part of Windows, installed even if it is not
  running, or
- Windows' own ssh server with settings somebody has already changed.

It tells you what it finds — the service and its path, or the directive that
was added — so you can decide what to do. You may **remove the other ssh
server, or put the ssh configuration back the way Windows shipped it, and run
the installer again.**

Why it is this strict: accounts SD creates cannot log in to Windows at all, so
ssh is one of only two ways they reach the machine — and SD configures the ssh
server so those sessions land inside SD and cannot reach a command prompt. **SD
can only promise that about a server it installed and configured itself.**

## What you are asked

There is one kind of installation. What varies is how the machine can be
reached afterwards, and that is three tick boxes on one page.

The boxes appear only on a **first** install. An upgrade shows no tasks page at
all: the machine already carries the answers, and every one of these settings
has a command that changes it afterwards.

### 1. System integration

| | Default |
|---|---|
| Add SD Core to the system PATH, so `sd` runs from any directory | **ticked** |

Changed afterwards with `append.sd.path on` or `off`.

### 2. The ssh server

**Installing an ssh server is optional, and the box is not ticked.** It
downloads from Windows Update and can take several minutes — up to about an
hour on a slow machine or connection — which is why it is offered rather than
done.

What you see depends on what the machine already has:

| Machine | Boxes | Defaults |
|---|---|---|
| No ssh server | *Install the OpenSSH server*, and indented under it *Let other computers connect* | both unticked |
| Server present, firewall shut | *Let other computers connect* | unticked |
| Server present, firewall open | *Let other computers connect* | **ticked** |

The second box is a child of the first, so Windows greys it out until the
parent is ticked. You cannot ask for remote ssh access without an ssh server.

The last row matters on a machine that already uses ssh: the box shows the
**current** firewall scope, so leaving it alone changes nothing in either
direction. `OpenSSH-Server-In-TCP` is Windows' own shared rule and not SD's, so
defaulting it to unticked and applying that would silently loopback-lock the
ssh a site already relies on.

Changed afterwards with `ssh.server install` or `remove`, and `remote.ssh on`
or `off`.

### 3. The API

| | Default |
|---|---|
| Provide the SD Core API (port 4243) | **unticked** |
| Let other computers on your network reach it | **unticked** |

**The API is off unless you ask for it.** Decline it and SD is installed with a
configuration carrying no `APIPORT` line, so no socket is opened at all — not a
listener behind a closed firewall, but no listener.

Again the second box is a child of the first. The pair appears only when there
is no existing configuration file to read the answer from.

Changed afterwards with `remote.api on`, `local` or `off`.

### An installation with neither is a supported choice

Leaving every remote box unticked gives a working SD that nothing outside the
machine can reach. That is a real deployment rather than a degraded one.

**Be aware of what it means for accounts.** Accounts SD creates are denied the
Windows console and Remote Desktop, so they reach SD over ssh or over the API
and nothing else — including at this keyboard, where an ssh account arrives by
`ssh localhost`. With no ssh server on the machine, `create.account … ssh` and
`… both` are refused, because the account could sign in nowhere. `api` and
`none` still work, and `none` is meaningful: an application account reached only
by `logto`.

The refusal is tested against the machine when you type the command, not
against a decision recorded at install time. Install an ssh server later and
`create.account … ssh` simply starts working.

## What lands where

| What | Where | Was, on Linux |
|---|---|---|
| Binaries, and the MSYS2 DLLs beside them | `C:\Program Files\SD\usr\bin\` | `/usr/local/bin` |
| The changelog | `C:\Program Files\SD\changelog` | — |
| Configuration | `C:\ProgramData\SD\sd.conf` | `/etc/sd.conf` |
| The SDSYS account | `C:\ProgramData\SD\sdsys\` | `/usr/local/sdsys` |
| User accounts | `C:\ProgramData\SD\user_accounts\` | `/home/sd/user_accounts` |
| Group accounts | `C:\ProgramData\SD\group_accounts\` | `/home/sd/group_accounts` |
| POSIX shared memory | `C:\ProgramData\SD\shm\` | `/dev/shm` |

**`usr\bin` is load-bearing, not tidiness.** Shipping `msys-2.0.dll` beside the
executable relocates the POSIX root to the DLL's directory minus two
components, so only that depth puts `/` on `C:\Program Files\SD\`. Do not move
the binaries.

**The DLLs ship beside `sd.exe` on purpose.** Do not change their location.

### Configuration

Server and client both read `SD_CONFIG`, then fall back to
`%ProgramData%\SD\sd.conf`.

`sd.conf` is installed `onlyifdoesntexist` and marked never to uninstall, so
your edits survive both upgrade and removal.

## What the installer creates on the machine

| | |
|---|---|
| `sdusers` | grants access to the files under `C:\ProgramData\SD`. Everyone who uses SD needs it |
| `sdsshonly` | carries the two deny rights that confine an account to ssh. Every account **`create.account`** makes joins it, unconditionally |
| `sdu_<name>` | one per account, created by **`create.account`** |
| the service | **String Database (SD)** |
| ACLs | inheritance is broken on `C:\ProgramData\SD` and access granted narrowly. This is what makes the database private from the rest of the machine |

**You must sign out and back in after being added to `sdusers`.** Windows
group membership is carried in your logon token. Until you get a new one, you
cannot read the data tree at all, and the symptom looks like a broken install.

## OpenSSH

**The OpenSSH server is installed only if you ask for it**, and the box is not
ticked. This section covers what happens when you do ask.

Accounts SD creates cannot log in to Windows, so they reach the machine over
ssh or through an API client. An installation offering neither is usable by
nobody but you — which is a legitimate choice, and worth making knowingly. A
local-only machine is served by `ssh localhost`, which needs no network.

**It is slow and it looks like a hang.** `Add-WindowsCapability` hands off to
`TiWorker` and can work for minutes with nothing on screen. **Never kill it** —
interrupting Windows servicing mid-flight is how the component store gets
corrupted. It may also leave a reboot pending, which is real; SD itself needs
none.

**If it cannot be installed, the install still succeeds.** It is a Features on
Demand capability and can be blocked by policy, a WSUS with no source, a
metered connection or an offline machine. The installer reports it in as many
words, with the command to retry — and you should read that report, because in
that state **no account but yours can sign in anywhere.**

It is the same command either way, and it is repeated here because the closing
report is easy to close. From an elevated prompt:

```
powershell -ExecutionPolicy Bypass -File "C:\Program Files\SD\install-ssh.ps1"
```

It exits **0** installed and running, **2** installed but Windows wants a
restart before the service exists, **1** failed — and it prints which, so run
it in a window you can read rather than expecting a log. It is safe to run
twice: on a machine that already has the server it says so and changes
nothing.

## The full-screen editors

**The installer makes sure the two terminal editors are on the machine**,
because the **`edit`** and **`micro`** verbs run them. Current Windows builds
already carry `edit.exe`; micro never ships with Windows, so it is always a
winget install. Neither is offered as a choice, for the same reason the ssh
server is not: an account with a verb that does nothing is worse than either
answer.

**If one cannot be installed, the install still succeeds.** No winget, no
network or a policy in the way all end the same: SD is complete and one editor
verb is not — **`ed`**, the line editor, needs nothing. What happened is in
`C:\ProgramData\SD\install-editors.log`, and to do it by hand afterwards,
from an elevated prompt:

```
winget install -e --id Microsoft.Edit --scope machine
winget install -e --id zyedidia.micro --scope machine
```

**The scope is not optional.** Without it winget installs into the profile of
whoever ran it, and accounts SD creates cannot log in to Windows at all — so a
per-user copy is one they can never reach.

## Changing any of it afterwards

Every choice on the tasks page has a verb that changes it later, and that is
why an upgrade does not ask again. All four are SDSYS's — signed in to
Windows as SDSYS, elevated — and all four report when given no keyword:

| | |
|---|---|
| `ssh.server install` \| `remove` | add or remove the OpenSSH server |
| `remote.ssh on` \| `off` | who may reach it |
| `remote.api on` \| `local` \| `off` | whether SD opens its API socket, and who may reach it |
| `append.sd.path on` \| `off` | whether `sd` runs from any directory |

They are covered in the SD Core for Windows administrator documentation, under
*Remote access and the machine*.

`remote.api on` and `off` change whether SD opens a socket at all, which it
decides at start-up, so they offer to restart SD — and that restart ends every
session including the one that asked. `local` and `on` differ only in the
firewall and take effect at once.

The underlying scripts are still on the machine and can be run directly if you
prefer, from an elevated prompt:

```
powershell -ExecutionPolicy Bypass -File "C:\Program Files\SD\api-firewall.ps1" -Open
```

## At the end

The wizard's last page lists what Setup did, and any step that did not
complete with the command to run. There are no popups. The installer then
**finishes, and opens a window** with three steps in turn: the SDSYS password,
your own SD Core password if you have none yet, and the installation check. It
does not leave a wizard page waiting behind the session.

A Start Menu entry, **Check the SD installation**, runs the check again at any
time. It closes on a keypress.

## Warnings and things to know

**The installer's own screens give options and results, and nothing else.**
Every reason, warning and caveat that used to appear on them is here.

### Before you install

- **What Setup changes in Windows.** It creates the group `sdusers` and adds you
  to it, and the group `sdsshonly`, whose members are denied console and Remote
  Desktop sign-in (accounts SD Core creates go in it; yours does not). It
  restricts `C:\ProgramData\SD` to SYSTEM, administrators and `sdusers`,
  installs a Windows service that starts SD Core after every restart, and adds
  SD Core to the system PATH unless you clear that option. The program files
  (`C:\Program Files\SD`) and the database (`C:\ProgramData\SD`) cannot be
  moved.
- **Sign out and back in afterwards.** Windows applies a new group membership
  only when you sign in. Until you do, `sd` answers that it is not recognized
  (in a window opened before the install — a new window cures that) or that it
  cannot open its files (only signing out cures that).
- **A silent install is refused.** The install ends by asking for a password
  and a silent install has nobody to ask, so it would finish with no password
  set. Run the installer normally, at the keyboard or through Remote Desktop.
- **Another ssh server stops the install.** SD supports only the OpenSSH
  server that ships with Windows, so that it knows how the server is
  configured. If a different ssh server is installed or using port 22, or
  somebody has changed how the Windows ssh server is configured, the installer
  says so and stops before changing anything. Remove the other server, or
  return the configuration to the way Windows shipped it, and run the
  installer again.
- **Installing OpenSSH takes time.** It downloads from Windows Update and can
  take several minutes with nothing on screen — up to about an hour on a slow
  connection. Do not stop it, and expect it to want a restart: until you
  restart, nobody can sign in over ssh.
- **What ssh does once SD is installed.** SD limits ssh to SD Core users, and
  every ssh session goes straight into SD Core rather than a command prompt,
  so an SD Core account cannot get a shell on the computer. Port forwarding is
  off for every ssh session. **`scp` and `sftp` stop working for everyone on
  the computer**, because the command is forced and there is no subsystem left
  to run; remote-control tools that copy files, the console and Remote Desktop
  are unaffected. Any existing `sshd_config` is kept as
  `sshd_config.before-sd`; uninstalling removes SD's block and restarts the ssh
  server, which leaves the file as it was.
- **If you do not ask for the ssh server**, SD touches no ssh configuration,
  opens no port, and leaves `scp` and `sftp` as they are.
- **If OpenSSH is already installed**, SD uses it and configures it the same
  way. Who may reach it is the one box offered, and it starts out matching the
  computer's current firewall rule, so leaving it alone changes nothing. Open
  ssh sessions are dropped when the service restarts, so check that your
  server accepts SD Core accounts.
- **Accounts are separate from each other.** The permissions on each account's
  directory allow only SYSTEM, administrators and that account's own `sdu_`
  group. Administrators and SDSYS can read everything.

### After the install

- **The SDSYS password.** SDSYS is the administrator account: sign in to
  Windows as SDSYS and start SD Core from an **elevated** prompt. It is the
  only way to administer SD Core. In the finishing window, pressing Enter keeps
  the current SDSYS password; typing a new one changes it (asked twice, not
  shown; at least 8 characters with a lower-case letter, an upper-case letter,
  a digit and a symbol). On a fresh install, pressing Enter keeps the generated
  password and shows it. If you do not know the SDSYS password, set one from an
  elevated PowerShell prompt:

  ```
  Set-LocalUser -Name SDSYS -Password (Read-Host -AsSecureString)
  ```

- **Your own SD Core password.** It is not your Windows password and does not
  replace it. It is needed only to reach SD Core from another computer, over
  ssh or the SD API. Without one, your account works at the keyboard but not
  from another computer, and SD Core asks for one at the next elevated
  sign-in. Change it at any time with `MODIFY.PASSWORD` in SD Core.
- **Giving somebody else access.** At the machine itself, sign in to Windows
  as SDSYS and type `sd`, elevated, then `CREATE.ACCOUNT USER <name> SSH`.
  Windows asks you to confirm at the UAC prompt: do it at the machine,
  because over a remote-control tool that cannot display it the screen
  freezes instead. The new account then signs in with `ssh <name>@localhost`.
- **After a reinstall over a kept database**, the Windows groups that decide
  who may reach SD were recreated: the ssh-only confinement is restored from
  the account register, ssh is restored for every member of `sdusers` (including
  an account whose ssh you had withdrawn), and **API access is not restored**.
  Set access per account with `modify.account <name> ssh | api | both | none`;
  the keyword sets access to exactly what it names, so `api` on its own takes
  ssh away. If the API is listening but no firewall rule admits other
  computers, `remote.api on` (or `remote.api local`) fixes it.
- **Upgrading** keeps your database, accounts and settings, replaces SD Core's
  own system files, and does not change `sd.conf` or your ssh, API and PATH
  settings. Every account is given the release's new commands. Change the
  settings with `remote.ssh`, `remote.api`, `ssh.server` and `append.sd.path`
  (see *Changing any of it afterwards*).

### When a step reports that it did not complete

The installer prints what failed and the command to run, from an **elevated**
PowerShell prompt. This is what each failure means until it is put right:

| The installer says | What it means until you fix it |
|---|---|
| The account directories were NOT locked | Any SD Core user can read and rewrite any other account's files outside SD Core |
| The shell permission list was NOT locked | Any SD Core user can add themselves to it and obtain a command shell |
| The batch command list was NOT locked | Any SD Core user can add commands to their own record and run them from the command line |
| The global catalogue was NOT locked | Any SD Core user can replace the programs SD Core runs for every session |
| The pcode library was NOT locked | Any SD Core user can replace the interpreter every session runs |
| An SD Core system directory was NOT locked | Any SD Core user can rewrite the account register, the system programs SDSYS runs, or the configuration SD Core reads at start-up |
| The credential store was NOT locked | Any SD Core user can overwrite another account's stored password and then sign in as them |
| Accounts were NOT confined to ssh / the ssh-only confinement was NOT restored | Accounts SD Core created can sign in at the console and over Remote Desktop; if `restore-sshonly.ps1` is missing, add them back to the `sdsshonly` group |
| The ssh and API access groups were NOT set up | ssh is refused to everyone except administrators |
| ssh was NOT limited | Usually OpenSSH has not started yet: restart and run the command. It also stops if `sshd_config` already says who may connect, and that setting is left alone |
| Who may reach ssh could not be set | Port 22 is open to the local network, which is the Windows default |
| Who may reach the SD Core API could not be set | No firewall rule was created, so other computers cannot reach port 4243 |
| SD Core could NOT create its administrator account | There is no way into SD Core until it exists; the reason is in `install-sdsys.log` |
| SD Core could NOT create an SD Core account for you | SD only admits accounts it creates and will not create one for a Windows account that already exists, so this is the one moment such an account can be made: running the installer again will not create it. The reason is in `attach-account.log` |
| The OpenSSH server could NOT be installed | Usually a policy that blocks optional features, a metered connection, or no connection. Accounts cannot sign in over ssh until it is there (API-only accounts can use the API meanwhile) |
| The dictionary, vocabulary or case-conversion step did not run | The upgrade kept what it had: SD Core works, a field added by the release may not be recognized, a command added by the release cannot be typed until `update.accounts` is run in SDSYS (answer Y), and records are still found typed in any case. If two record ids differ only by case the file is left unchanged: rename or delete one of each pair, then run `CONFIGURE.FILE NO.CASE` on it |

### Uninstalling

- **The database and the configuration file are separate questions**, and
  **Keep** is the normal answer to both: a reinstall finds the database again
  and reuses the settings. **Deleting the database is permanent**: every SD
  Core account, every password and all data stored in them, including SDSYS.
  If you delete only the configuration file, a reinstall writes a fresh one.
- **Accounts you keep** remain ordinary Windows accounts, with their
  passwords, and are no longer confined to ssh. Your own account is always
  kept. A profile whose registry hive is still loaded cannot be deleted until
  the next restart (the log names any that were left), and the sweep refuses
  to run rather than remove the last account able to sign in to Windows.
- **`sdusers` is always left behind**, because deleting it would orphan the
  permissions on your database. `sdssh`, `sdapi` and `sdsshonly` are removed
  without asking.
- **If something could not be removed**, it may be in use by a running SD Core
  process; treat anything marked for deletion as gone.

## Continued in

[Upgrading and uninstalling](01a-upgrading-and-uninstalling.html) — upgrading
an existing installation, and uninstalling.
