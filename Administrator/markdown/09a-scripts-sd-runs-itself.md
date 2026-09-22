Title: The Scripts SD Runs For Itself
Subtitle: What calls `sd-elevate`'s subcommands, and the handful of things Windows automated that this port does differently.

This page continues [The Installed Scripts](09-the-installed-scripts.html).

**Unlike SD Core for Windows, there is no separate category of scripts
"the installer runs" versus "a verb calls" versus "SD runs for itself" —
it is the same `sd-elevate` and the same subcommands (listed on the
previous page) either way, invoked from `installsdai.sh` directly, from
an administrator verb, or from `deletesdai.sh`.** This page is mostly
about the handful of places this port's approach genuinely differs from
what Windows automates, rather than a second catalogue to read alongside
the first.

## What has no separate script at all

**Several things Windows does through a dedicated `.ps1` file, this port
does inline, or does not do the way Windows does:**

| Windows script | Here |
|---|---|
| `deny-logon.ps1` | nothing — an ordinary account's console login is not denied here at all (S.41: no second wall behind `sh` means nothing to gain by denying it). See [Security and the operating system](../GettingStarted/12a-security-and-the-operating-system.html) |
| `install-service.ps1` | a `systemd` unit file (`sd.service`, `sdclient.socket`), installed with `install`, not a script that creates a service |
| `install-editors.ps1` | `apt-get install micro` and the `nano` syntax file copy, both inline in `installsdai.sh` |
| `sync-route-groups.ps1`, `sd-path.ps1` | nothing — there is no per-account route group to seed and no PATH toggle; `sd` is symlinked into `/usr/local/bin` at install time |
| the `secure-*` family (eleven scripts) | inline `chown`/`chmod` calls in `installsdai.sh`, at the specific paths that need them (`$cred` 700, `batch.jobs` 750, and so on — see [Security](../GettingStarted/12-security.html)) |
| `micro-home.ps1` | nothing installed — `nano`/`micro`'s own program (`gpl.bp/edit`) copies its syntax file into the caller's `~/.config/micro/syntax` itself, on first use, with no privilege needed. Self-healing, and it reaches an account made after the install without anything to re-run |

## What Windows automates that this port does not, yet

**`upgrade-voc.ps1` — `update.accounts all` on every upgrade.** Checked
directly: `installsdai.sh` has no such call. An administrator runs it by
hand after an upgrade — see [Upgrading and
uninstalling](../GettingStarted/01a-upgrading-and-uninstalling.html). This
is a real gap against the Windows port's own behaviour, not a deliberate
difference.

**`reconcile-accounts.ps1` — runs at every service start on Windows.**
This port's equivalent, `sd-reconcile-accounts`, is installed but **not**
wired into `sd.service`'s startup — checked against the unit file and
`installsdai.sh` directly. It is a manual recovery tool, run when `list
sd.accounts` and the Linux accounts disagree, not a standing safeguard.

## Restarting after a remote-access change

**Unlike SD Core for Windows, where `remote.api on`/`off` may offer to
restart the whole server** (its listener opens only when `sd.exe` itself
starts), **no SD session is ever ended by a remote-access change here.**
`remote.api`'s `on`/`local` restart only the `sdclient.socket` unit;
`remote.ssh` only moves a firewall rule. See [Remote access and the
machine](05-remote-access-and-the-machine.html).

## See also

[Installation and the daemon](08-sd-installation.html) covers what the
installer puts on the machine and what an upgrade replaces.
[Remote access and the machine](05-remote-access-and-the-machine.html)
covers the two verbs that call `sd-elevate`'s remote-access subcommands,
and is the supported way to change either setting.
