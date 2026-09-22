Title: The Installed Scripts
Subtitle: The three helper scripts installed beside SD, the sudoers scope that lets SD run them, and what their exit codes mean.

**Unlike SD Core for Windows, which ships thirty-seven separate PowerShell
scripts, this port does its privileged work through three: one general
helper with many subcommands, and two standalone ones.** Where Windows
needed a script per task because each ran as its own elevated PowerShell
process, this port dispatches by argument through a single `sudo`-scoped
entry point — the same shape of problem, a smaller surface because the
mechanism is free to differ.

They are in `/usr/local/sbin`, and they are there for the same two reasons
Windows's are: so that a step which failed during the installation can be
run again without reinstalling, and so that a choice made at install time
can be changed afterward.

**They are shell scripts, not SD verbs.** Nothing here is typed at an `sd`
prompt. Most need `sudo` to do anything; SD itself reaches them through a
scoped `sudoers` entry that lets `sdusers` run exactly the subcommands
each operation needs, nothing more.

*Italics* mark something you supply, **bold** a word typed as it stands, and
braces an optional part.

## What is here and what is not

**Three scripts ship.** Everything else in the project's `gplbld`
directory — the verifiers, the probes, the build and test cycle — is
development tooling and is deliberately not installed. If you have read
about `check-stale-leads.py`, `assert-current.py` or a `witness-` or
`verify-` script and cannot find it on an installed machine, that is why:
they compare an install against the source tree it was built from, and
some are destructive.

## Exit codes

| | |
|---|---|
| **0** | done. That includes *"it was already done"* — most subcommands are written to be run twice |
| **2** | **refused.** The line above names why — `die()`'s own convention, printed as `sd-elevate: REFUSED - <reason>` |
| **3** | (`remote-ssh` only) **nothing was there to change.** The firewall would not have gated anything anyway (no `ufw`, inactive, or already permissive), so reporting success would be the reassuring falsehood this project's own instrument rule refuses to print |

**There is no exit 1.** A refusal and a failure are the same event here —
`die()` is the one way this script stops short of doing what it was asked,
and it always means 2.

## `sd-elevate`

```sh
sudo /usr/local/sbin/sd-elevate [--dry-run] <subcommand> ...
```

**`--dry-run` reports what it would do and changes nothing** — the
argument, and it comes first.

| Subcommand | Does |
|---|---|
| `useradd`, `userdel`, `userdel-home` | create or remove the Linux user behind an account — `userdel-home` also removes its home directory, only for a user SD created |
| `passwd`, `setpw` | the Linux login password — `setpw` takes it on stdin, one line, never as an argument |
| `pw-check` | judges a password against SD's own complexity rule, on stdin — used before the write, not only at it |
| `groupadd`, `groupdel`, `addgroup`, `delgroup` | the account's own `sdu_`/`sdg_` group, and membership in it — this is what `modify.account add`/`delete` calls underneath |
| `setgid`, `chown-account` | ownership and the setgid bit on an account directory, at creation |
| `rmtree-account` | removes an account's directory tree, for `delete.account remove.home` |
| `remote-api on \| local \| off \| show` | the `sdclient.socket` binding and the `ufw` rule — what `remote.api` calls |
| `remote-ssh on \| off \| show` | the `ufw` rule for port 22 — what `remote.ssh` calls |
| `cred-own query \| verify \| set` | an ordinary account's own write to `$cred`, which it cannot reach directly — what self-service `modify.password` calls |

**Each subcommand re-derives whether the request is legal itself** — whose
account directory it actually is, whether a user was one SD created —
rather than trusting what the calling SD session claims. That is the whole
of the protection: a session that could talk `sd-elevate` into an
operation on somebody else's account would defeat every gate SD has above
it.

## `ssh-forcecommand`

```sh
sudo /usr/local/sbin/ssh-forcecommand --install
sudo /usr/local/sbin/ssh-forcecommand --remove
sudo /usr/local/sbin/ssh-forcecommand --check
```

Writes or removes the fenced `ForceCommand`/`DenyUsers` block in
`/etc/ssh/sshd_config` — see [Remote access and the
machine](05-remote-access-and-the-machine.html). `--install` validates the
candidate with `sshd -t` **before** touching the live file, backs up to
`sshd_config.before-sd`, and refuses rather than overwrite a
`sshd_config` that already has its own `AllowGroups`/`AllowUsers`/
`DenyGroups`/`DenyUsers` line — that is somebody else's decision. The
installer runs `--install` non-fatally; a refusal here leaves SD
installed and working, with the boundary not yet applied, and prints
the command to apply it once the conflict is resolved.

## `sd-reconcile-accounts`

```sh
sudo /usr/local/sbin/sd-reconcile-accounts          report, change nothing
sudo /usr/local/sbin/sd-reconcile-accounts --sweep  remove them
```

**Finds `accounts` records whose Linux user is gone** — removed from
outside SD entirely (`userdel`, a decommission script), so SD was never
consulted and the record outlived the user. `list sd.accounts` then
answers wrongly, and `create.account` refuses to recreate the name: true
of the record, false of the machine. Reports by default; `--sweep`
removes the stale records and their directories, and needs root. Exit
**0** the register is clean, **1** something stale is still there
(reported, refused, or would not go), **2** the question could not be
answered. Not run by the installer — a recovery tool for drift that
happened outside SD's own verbs.

## Continued in

[The Scripts SD Runs For Itself](09a-scripts-sd-runs-itself.html) — what
the daemon, the verbs and the installer invoke while running, rather than
what an administrator runs by hand.
