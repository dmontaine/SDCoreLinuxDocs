Title: The Scripts SD Runs For Itself
Subtitle: The scripts the installer, the administrator verbs, the uninstaller and SD itself call, which nobody types.

This page continues [The Installed Scripts](09-the-installed-scripts.html).

## The ones the installer runs

**You should not need any of these**, and running one out of order can undo
work rather than repeat it - most of them must run *after* the step that
secures the data tree, or inheritance puts back exactly what they took away.
They are listed so that a name in a log or an error message can be looked up.

| | |
|---|---|
| `adopt-account.ps1` | gives the installing user an SD account. Without it SD installs and then refuses the person who installed it |
| `deny-logon.ps1` | denies a local group the console and Remote Desktop, which is what confines an account to ssh |
| `finish-install.ps1` | the two steps that happen after the installer closes - SD opens so you can set your own password, then the post-install check runs |
| `install-service.ps1` | creates, starts and removes the Windows service **String Database (SD)** |
| `install-editors.ps1` | makes sure the editors the `edit` and `micro` verbs run are on the machine |
| `ssh-preflight.ps1` | asks whether SD may install here at all, and refuses a machine carrying an ssh server SD does not own. Runs before the wizard is drawn |
| `sync-route-groups.ps1` | creates the two groups that decide which remote route an account may use, and seeds `sdssh` so an existing install does not lose ssh |
| `upgrade-dicts.ps1` | brings an upgraded install's dictionaries up to the release. Runs on an upgrade only |
| `upgrade-voc.ps1` | brings every existing account's VOC up to the release, by running `update.accounts all`. Runs on an upgrade only |
| `secure-accounts.ps1` | the containers account directories are created in |
| `secure-account-dirs.ps1` | the ACL on each account's own directory |
| `secure-audit.ps1` | creates the audit trail and makes it append-only |
| `secure-cred.ps1` | locks the credential store to SYSTEM and Administrators |
| `secure-dumps.ps1` | makes the process-dump directory write-only to SD users, so a dump can be added and nobody else's can be read |
| `secure-gcat.ps1` | locks the global catalogue, and separately the compiled objects it is loaded from |
| `secure-log.ps1` | creates a log only administrators can see or write |
| `secure-osusers.ps1` | locks a permission list so only an administrator can change who is on it. The installer calls it four times - twice for `os.users` and twice for `batch.jobs` |
| `secure-pcode.ps1` | locks the pcode library, which is the interpreter every session runs |
| `secure-psdir.ps1` | the directory privileged scripts are written into |
| `secure-reclaim.ps1` | creates the profile-reclaim store and locks it to SYSTEM |
| `secure-sysdirs.ps1` | takes Modify off the system directories that nothing writes |

**THE `secure-` FAMILY IS WHAT KEEPS SD's USERS OUT OF SD's OWN FILES.** The
data tree grants the `sdusers` group Modify, because every SD user needs it to
use the database at all, and that grant is inherited everywhere. Each of these
scripts takes it back off one thing that must not carry it.

## The ones an administrator verb calls

Four SD verbs change the machine rather than the database, and each of them
works by running one of these. **Prefer the verb.** It asks the questions that
need asking, reports what happened in the product's own words, and refuses
when it cannot act; the script does the work and assumes the caller knew what
they were doing.

| | Called by |
|---|---|
| `install-ssh.ps1` | `ssh.server install` |
| `remove-ssh.ps1` | `ssh.server remove` - takes the Windows OpenSSH server capability off the machine. The removal completes at the next restart |
| `ssh-firewall.ps1` | `remote.ssh on` \| `off` - scopes the shared Windows rule `OpenSSH-Server-In-TCP` rather than disabling it |
| `api-listener.ps1` | `remote.api on` \| `off` - writes or comments out the `APIPORT` line in `sd.conf` |
| `api-firewall.ps1` | `remote.api on` \| `local` - opens or restricts the API port |
| `sd-path.ps1` | `append.sd.path on` \| `off` - puts SD's program directory on the system PATH, or takes it off |
| `restart-sd.ps1` | offered by `remote.api on` and `off`, because the listener is only read at start-up |

The verbs are covered in the SD Core for Windows administrator documentation,
under *Remote access and the machine*.

## The ones the uninstaller runs

| | |
|---|---|
| `remove-sdaccounts.ps1` | takes away the Windows accounts SD created. Only runs if you ask for the data to be removed |
| `reclaim-profiles.ps1` | removes the Windows profiles SD had to leave behind at the time |
| `restore-sshonly.ps1` | puts every non-administrator SD account back into `sdsshonly`, reading the account register rather than anything local |

`restore-sshonly.ps1` is the repair for a half-finished removal: an account
that lost its deny rights but still exists would otherwise become an ordinary
ssh login on the machine.

## The ones SD runs for itself

These are launched by SD while it is running rather than by the installer.
**Do not run them by hand**; they are listed because they appear in logs and in
Task Manager.

| | |
|---|---|
| `sd-elevate.ps1` | the unelevated half of an administrator session, called by SD's `ELEVATE` program with `-Start`, `-Run` or `-Stop`. Exit 0 done, 1 failed, **5 not elevated or elevation refused** |
| `sd-elevate-helper.ps1` | the elevated half. `sd-elevate.ps1` launches it, which is where the UAC prompt appears, and it serves one SD session until that session ends |
| `micro-home.ps1` | gives the calling user a `micro` configuration home they can write to, and prints where it is. Run by the `EDIT` program before it launches `micro` |
| `reconcile-accounts.ps1` | removes register records whose Windows account has gone, and the account directory with them. Runs at every service start |

**A Windows process's token is fixed when it is created**, so nothing can
elevate a running process. That is why administrator work is done by a separate
helper process rather than by an elevated `sd.exe`: SD stays unelevated for its
whole life.

## See also

[Installation and the service](08-sd-installation.html) covers what the
installer puts on the machine and what an upgrade replaces.
[Remote access and the machine](05-remote-access-and-the-machine.html) covers
the four verbs that call seven of these scripts, and is the supported way to
change any of those settings.
