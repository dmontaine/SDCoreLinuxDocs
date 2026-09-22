Title: Security and the operating system
Subtitle: Reaching the machine from inside SD, how privileged work is done, and the audit trail.

This page continues [Security](12-security.html).

## There is no second wall

**Unlike SD Core for Windows, there are no ways out of SD that need a
separate permission — all four already run for every account,
unconditionally:**

| | What it is |
|---|---|
| **`sh`** and `!` | a shell at the `:` prompt |
| `OS.EXECUTE` | the operating system from inside a BASIC program |
| **`nano`** and **`micro`** | a text editor, running outside SD |

Windows keeps a second permission list (`os.users`) behind all four,
because Windows gives SD no native way to sandbox what a shelled-out
process can reach. **This port does not keep that list, and it is not a
gap — it is a deliberate consequence of Linux already providing the wall
SD would otherwise have to build itself**: what an account's Linux user
may read, write or run outside SD is exactly what it may do through `sh`
inside SD, because they are the same operating-system permissions, checked
by the kernel either way.

**Nothing in SD limits what you then do**, and that was already true on
the port this description was ported from too — the boundary is the
account's own Linux permissions, and nothing else. A shell gets pipes and
redirection; an editor can open any file its account may open, in the data
tree or outside it.

> **So `sh` and the editors are a statement of trust in an account from
> the moment it is created.** Every account gets them, so an account's
> Linux permissions are the whole of what limits it — set those
> deliberately, the way you would for any other account with a shell on
> the machine, because that is exactly what it has.

**A session with no terminal is refused regardless** — an API session or a
piped script has nowhere to draw a full screen for an editor; see
[API access](09-api-access.html) for what `sh`/`OS.EXECUTE` do over the API
specifically, which is also unrestricted on this port, for the same reason.

## Privileged work is done through a helper, not a raw command line

When SD creates an account, sets a password or edits a group, it does not
build a shell command containing a password or run one as an arbitrary
string. **`sd-elevate`**, a `sudo`-scoped helper installed to
`/usr/local/sbin`, is the only thing an SD session can reach with root's
help — and it re-derives the legality of each request itself (whose
account it is, what the operation actually is) rather than trusting what
SD's own session claims.

**A credential is never an argument.** Where a password has to reach the
helper — setting an account's own SD password, for instance — it goes to
`sd-elevate` on **stdin**, through a file in a private, mode-`0700`
directory that only the calling session can read, never on a command line
where any local user could see it through `ps`.

**If `sd-elevate` is missing or refuses, SD refuses the privileged work**
rather than falling back to doing it unprotected. You see the command
fail rather than quietly running with less protection than intended.

## The audit trail

`/usr/local/sdsys/audit` records **every login, every refused login, every
`logto`, every refused `logto`, and every `modify.account add`/`delete`**,
with date, time and the Linux user it belonged to.

```
2026-08-16 11:42:07 user=don uid=1 pid=8624 LOGTO account=SDSYS
```

**The refusals are the interesting half.** An entry saying somebody who is
not SDSYS asked for SDSYS by name, or asked for an account they have not
been granted, is the thing worth seeing. **Failed API logins are recorded
too, with the reason.**

**This is not the error log and does not behave like it.** The error log
throws away its oldest half when it fills; the audit file is **rotated —
renamed with the date and time and a new one started at boot, so nothing
is ever discarded within a run.** Removing the old ones is your decision —
SD will not do it for you, and they will accumulate.

**The file itself is append-only at the kernel level** (`chattr +a`), lifted
only by root at the one moment a new file starts, so an SD user cannot
remove or edit an entry even with the write permission to add to it — the
protection is a Linux filesystem attribute, not merely a permission bit.

| SD users can | SD users cannot |
|---|---|
| **add** to it | read it, change a record in it, empty it, rename or delete it |

**The kernel refuses the edit or the delete, not SD**, so a user cannot
quietly remove the line that records what they did. SDSYS can read it and
do anything else to it as well — a real login as `sdsys` can lift the
append-only attribute, the same as any root-equivalent action, so this
raises the floor against ordinary users rather than trying to constrain
the machine's own administrator.

## What is still not true

**SD accounts are not isolated from each other's data at the file level
beyond whatever this machine's own Linux permissions provide.** Everyone
who uses SD needs file access to the tree, because their own process does
the I/O. Anyone deploying SD for ten people over ssh should be told that
plainly — see [Security](12-security.html#your-own-accounts-data).

**SD has no file-level access control of its own** on the console and ssh
paths. The one place a path gate does exist is the API, where a session is
confined to the account it stands in — see
[API access](09-api-access.html#a-session-is-confined-to-its-own-account).
