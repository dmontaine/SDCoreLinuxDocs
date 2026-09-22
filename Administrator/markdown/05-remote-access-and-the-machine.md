Title: Remote access and the machine
Subtitle: The two verbs that change the machine rather than SD, and the one thing they both require.

Most administrator verbs change something inside SD. These two change the
machine SD is running on: who may reach it over ssh, and whether SD opens
its API socket at all.

| | |
|---|---|
| `remote.ssh` | decides who may reach the machine's ssh server |
| `remote.api` | decides whether SD opens its API socket, and who may reach it |

**Neither of these installs or removes anything.** `sshd` is the
distribution's own service — installed, started and kept current the way
every other Linux service is, outside SD's remit entirely. These two verbs
only move the firewall rule and the API socket that sit in front of it;
they were built after the SD Core for Windows model of the same name,
under the owner's ruling that a behaviour prevented on one port must be
prevented on both, with the mechanism free to differ where the operating
system does.

> **Neither gives SDSYS remote access, and no setting does.** Opening ssh
> or the API to other computers opens it for ordinary accounts only.
> **SDSYS has no remote route at all, under any setting these two verbs
> control** — refused at the door, not merely ungranted. Administration
> needs a real login as `sdsys` at the machine's own keyboard, or a
> desktop-sharing view of it. See [Accounts and
> Security](01-accounts-and-security.html#read-this-before-anything-else-being-sdsys-is-the-whole-of-it).

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

SD folds case, so a command may be typed in either case. Commands are shown
here in lower case.

## Both need SDSYS, including to report

Each of them begins by testing the administrator flag — a real `sdsys`
login, not merely elevation — and stops if it is not set:

```
:remote.ssh
Command requires administrator privileges
```

That was run from an ordinary account. **The test runs before the keyword
is read, so the reporting forms are refused too** — there is nothing softer
about asking one of these verbs to just report the current setting, because
reading the answer means reading the firewall and the socket state, which
costs the same standing as changing them.

## Both report when given no keyword

```
remote.ssh
remote.api
```

With no keyword each reports the current state and changes nothing. This
is the supported way to answer "how is this machine set up?"

## remote.ssh

```
remote.ssh {on | off}
```

| | |
|---|---|
| `on` | other computers on the network may connect over ssh |
| `off` | only this computer may connect |

**It moves the firewall rule and never the ssh server itself.** `sshd` is
the distribution's own service, and an administrator's own shell may be
reaching this machine through it right now — there is nothing here
resembling SD Core for Windows's `ssh.server install`/`remove`, because
installing or removing packages is the distribution's job, not SD's. The
rule this verb moves is the one the installer itself wrote (`ufw allow
22/tcp`).

**Where the firewall gates nothing, this refuses rather than lie about
it.** With `ufw` absent, inactive, or already allowing incoming
connections by default, a rule change for port 22 changes nothing about
who can actually connect — and reporting "remote ssh access is now OFF"
in that state would be exactly the reassuring falsehood a verifier must
never print. The verb exits with a distinct status (3) having changed
nothing, prints what the firewall actually says, and names why.

**Administrator only, and every change is audited**, the same as
`remote.api`.

## remote.api

```
remote.api {on | local | off}
```

| | |
|---|---|
| `on` | SD listens on port 4243 on every address, and the firewall allows it: other computers may connect |
| `local` | SD listens on `127.0.0.1:4243` only: only this computer may |
| `off` | SD opens no API socket at all, TCP or local |

**There are two axes here and the verb sets both, the same shape as SD
Core for Windows's verb of the same name — the mechanism is entirely
different underneath.** Whether SD listens at all is `systemd`'s
`sdclient.socket` unit; who may reach it is `ufw`. The verb drives both and
reads them back, so what it reports after a change is the machine's own
answer, not the verb's intention. The firewall rule is the installer's own
(`ufw allow 4243/tcp`), so this verb and the install describe one state.

**No SD session is ever ended by this verb**, which is where it differs
most from the Windows original. SD Core for Windows's own listener opens
only when SD itself starts, so changing it there restarts the whole
program and ends every session, the caller's included — and asks first.
Here the listener belongs to the socket unit, not to any running `sd`
process: `on` and `local` restart the *socket*, and `off` stops it. A
connection already accepted is its own separate service instance, so
nothing already talking to the API is disturbed by a later change.

**Administrator only** — the same gate `modify.account` uses, because this
changes what the machine offers the network rather than anything about one
account — **and every change is audited**, a Linux addition matching how
the port's own account-tier changes used to be audited before tiers were
removed.

## When a change fails

Both report a failure rather than falling silent, and name what did not
happen. `remote.ssh` exits 3, unchanged, when the firewall would not have
gated anything anyway (see above) — a refusal, not a silent success.
