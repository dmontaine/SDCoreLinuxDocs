Title: Running SD
Subtitle: The daemon, starting and stopping, and what to do after an unclean shutdown.

**SD is a `systemd` service and it is already running.** Nobody types
`sd -start` after every reboot.

| | |
|---|---|
| Unit | `sd.service` (starts the daemon), `sdclient.socket` (the API listener) |
| Start type | enabled — `systemd` starts both at every boot |
| Created by | the installer, which also starts and enables them |
| Removed by | the uninstaller |

## Starting and stopping

**Stopping SD ends every session on the machine**, which is exactly what
`sd -stop` has always done. Either is fine:

```
sudo systemctl stop sd.service sdclient.socket
sudo systemctl start sd.service
sudo systemctl start sdclient.socket
```

```
sd -stop
sd -start
```

## `sd -start` and `sd -stop` check the real process, not just the segment

SD's shared state lives in a System V shared-memory segment
(`shmget`/`SD_SHM_KEY`), which — unlike a file — can outlive the daemon
process that created it if SD is killed rather than stopped cleanly.
`sd -start` and `sd -stop` validate the daemon's actual process id rather
than trusting the segment's mere existence:

**"SD is already started" is only said when the daemon really is
running**, and it names the process id — the one `ps` and `kill` use.

**If the segment is there but the daemon is not** — what a killed or
crashed SD leaves behind — `sd -start` says so rather than silently
reporting success against a segment nothing is actually serving. Clearing
it is `sd -stop`'s job.

> Check the daemon by hand at any time:
>
> ```
> ps -C sdlnxd
> ```

**A `shmget` System V segment does not survive a reboot** — the kernel
clears its IPC state on every restart, unlike a file on disk. So unlike a
port where a stale segment can persist across a restart, a reboot here
always leaves a clean slate; the "segment present, daemon dead" case above
is specifically about a crash the machine itself did **not** restart from
(SD killed, or `sd.service` restarted, while the box stays up).

## SD will not start a second time inside itself

If you leave SD with **`sh`** and then type `sd` in that shell, it says so and
returns you to the session you already have.

Worth knowing alongside it: **`sh` runs at the account's own Linux
permissions, unconditionally** — there is no elevation or grant it needs
first, unlike an account confined by a second SD-level wall. See
[Security and the operating system](12a-security-and-the-operating-system.html).

## The command line

```
sd                  enter the SD account named after your Linux login
sd -a               prompt for an account
sd -a<name>         enter account <name>  -- refused unless it is your own
sd <command>        run one command       -- needs SDSYS, or batch.jobs
sd -quiet           suppress the displays on entry
sd -u               list current users
sd -k <n> | -k all  log out user n, or everybody
sd -start           start the system
sd -stop            stop the system
sd --version        report the version
sd --help           this summary
```

**Three of these behave differently from what you may expect.**

**`sd -a<name>` is refused unless `<name>` is your own account.** An
administrator no longer opens somebody else's account without ever being in
their own — they arrive in their own (`sdsys`) and reach the rest with
**`logto`**, which is where SD checks whether they are allowed in.

**`sd <command>` needs SDSYS**, or an entry for that account in
`batch.jobs`. **Any account can be given one** — every account has the same
VOC now, so there is nothing about the account to consider here; SDSYS's own
`batch.jobs` list is what decides what may run. That is what makes scheduled
jobs possible without giving them SDSYS's own rights — see
[Scheduled jobs](04-scheduled-jobs.html).

**`sd <command>` runs and exits, and is never asked to set a password.** Nor
is any session with no terminal — a scheduled task, or a piped script. **Only
an interactive `sd` with no command after it still asks**, and then only of
an account that has no password yet.

## Where things are

| | |
|---|---|
| Binaries | `/usr/local/bin` |
| Configuration | `/etc/sd.conf` |
| The database | `/usr/local/sdsys` |
| Accounts | `/home/sd/user_accounts`, `/home/sd/group_accounts` |
| Audit trail | `/usr/local/sdsys/audit` |
| Error log | `/usr/local/sdsys/errlog` |
| Elevation helper log | alongside the installer, `sd-elevate.log` |

## Checking the service

```
systemctl status sd.service sdclient.socket
journalctl -u sd.service
```

`systemctl` reports whether `systemd` thinks the units are running;
`sd -u` (from inside an SD session) reports who is actually connected.
