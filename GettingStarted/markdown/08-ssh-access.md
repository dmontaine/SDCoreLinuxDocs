Title: ssh access
Subtitle: How people reach SD on this machine over ssh, and the one thing it costs you.

**Every ordinary account SD creates has ssh access, unconditionally — there
is no per-account choice.** Only SDSYS is different: it has no remote route
at all, ssh or otherwise. This page covers the ssh route for ordinary
accounts; [API access](09-api-access.html) covers the other.

**Unlike SD Core for Windows, an ordinary account is *not* denied a local
login at this machine.** SD keeps no second wall behind ssh here — see
[Security and the operating system](12a-security-and-the-operating-system.html#there-is-no-second-wall)
for why that turns out not to matter: a local login and an ssh session that
reaches `sh` end up at the identical native permissions, so there is
nothing a console login would grant an account that ssh does not already.

## How it is done

**One rule, on the ssh server, not per account:**

```
Match Group sdusers,!sdsys
    ForceCommand /usr/local/bin/sd
Match User sdsys
    DenyUsers sdsys
```

Every `sdusers` member is `ForceCommand`'d into `sd` the instant they
connect over ssh — they never reach a shell that way, whatever the
connection is asked to run. `sdsys` is refused a network login outright,
before authentication even matters: there is no session for `ForceCommand`
to apply to.

**This is applied once, to the ssh server, regardless of the two questions
the installer asked.** Whether remote ssh access is turned on only decides
whether `sshd` is enabled at boot and reachable from other computers (see
[Installing SD Core](01-installation.html#what-you-are-asked)); the
boundary above is written to `sshd_config` either way, so `ssh localhost`
is confined the same as a connection from anywhere else.

## An ssh session lands inside SD

**That applies to everyone who can reach ssh at all**, except `sdsys` — see
[SDSYS has no remote door](#sdsys-has-no-remote-door) below.

### The cost: scp and sftp stop working inbound, over ssh

**No file can be pushed to this machine over ssh this way, by anybody**
who is `ForceCommand`'d into `sd`. The command is forced, so there is no
file-transfer subsystem left to run. This is the accepted cost of the
boundary above.

**The cost is inbound, over ssh, only.** `scp` or `rsync` run **on** this
machine, connecting outward, makes it the client — `sshd_config`'s
`ForceCommand` is never consulted for an outbound connection. And **unlike
SD Core for Windows, this port does not deny a local login**, so an
account can also simply log in at the machine directly to move a file, or
reach it through SD's own file access (an editor, or an API client) rather
than needing a separate remote-desktop product.

## Reaching the machine from the network

**Whether remote ssh access is turned on is a plain yes/no from the
installer**, defaulting to no (see
[Installing SD Core](01-installation.html#what-you-are-asked)). Answering
yes enables `sshd` at boot and adds a `ufw allow 22/tcp` rule; answering no
leaves `sshd` and the firewall exactly as the box already had them — the
installer does not narrow an existing, wider rule on your behalf. Change it
afterward with `remote.ssh on`/`off` — see
[Administrator commands](06-administrator-commands.html).

**Connecting to SD on your own machine is unaffected either way.**
`ssh localhost` needs no firewall rule for loopback traffic and works
whether or not remote access is turned on. **A local-only installation is
served entirely by `ssh localhost`.**

## What ssh confinement does not mean

**The `ForceCommand` rule controls *what an ssh connection may run*, not
*where an account may otherwise log in*.** Confining a session to SD over
ssh is this page's rule; there is no separate permit list gating `sh` or
`OS.EXECUTE` once inside SD — every account reaches both unconditionally,
at its own Linux permissions. See
[Security and the operating system](12a-security-and-the-operating-system.html).

**And ssh confinement does not give accounts isolation from each other's
data.** Every SD process opens the database under the invoking user's own
Linux identity, so everyone who uses SD needs file access to the tree and
can, in principle, read another account's directory from outside SD if the
file permissions allow it. See [Security](12-security.html).

## SDSYS has no remote door

**SDSYS cannot ssh in, from this machine or any other.** `Match User sdsys`
denies it outright, at the ssh server, before authentication starts — there
is no session for `ForceCommand` to ever apply to. The same is true of the
API; see [API access](09-api-access.html).

**Nothing changes for ordinary accounts.** Every account `create.account`
makes reaches ssh from wherever `sdusers` membership allows, whether or
not the Linux account behind it happens to also be in `sudo` or `wheel` —
group membership outside `sdusers` has never been what SD asks about.

### Where administration happens

**At this machine's own console only** — a real login as `sdsys`, its own
password, either physically at the keyboard or through a desktop-sharing
view of it (VNC, TeamViewer), which counts as local because it *is* a
local session from the machine's own point of view.

### Why

This is a deliberate policy choice, not a technical limitation the way it
is on some ports: SDSYS's refusal over ssh is checked against the kernel's
own audit loginuid, set once by a real login and unforgeable by `sudo`,
`su`, or a service account — there is no route to SDSYS that this check
does not catch, ssh included, because ssh authentication does not produce
the kind of login record it looks for. See
[Accounts](05-account-types.html#sdsys-is-the-only-administrator).

### If you rely on remote administration today

**It does not work, and that is deliberate.** Use the console, or a
service- or session-based remote desktop, logged in as `sdsys`. An account
that needs ordinary, non-administrative work from another machine was
never an administration question — every ordinary account already has
ssh access by default.

**Scheduled tasks are affected too.** A cron job or a systemd timer has no
terminal login either, so nothing can become SDSYS to run one. List the
command in the SD system file `batch.jobs`, run from an ordinary account —
see [Scheduled jobs](04-scheduled-jobs.html).
