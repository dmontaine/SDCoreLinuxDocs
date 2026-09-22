Title: Other hardening
Subtitle: The catalogue and pcode locks, the logs, line endings, and the rest of the smaller changes.

Everything on this page is a change you may notice while testing, grouped by
what it touches. The identity model and the file permissions are on
[Security](12-security.html); this is the remainder.

## The global catalogue

**Adding to or removing from the system-wide catalogue requires SDSYS,
whichever way you ask for it.**

This matters because the system-wide catalogue holds the programs SD runs for
everybody, `$login` among them. **Replacing one runs your code in every session
on the machine, SDSYS included; deleting one stops everybody signing
in.**

**Nothing changes for local and private cataloguing**, which is what
programmers use day to day:

```
catalog bp myprog          private catalogue, this account
catalog bp myprog local    this account's VOC
```

Both still work, in any account you are allowed to **`logto`** into. The only thing
an ordinary user cannot do is catalogue a program whose name starts with
`*`, `!`, `_` or `$` — those characters mean *system-wide*. Name it without
one.

**To catalogue system-wide you need to be SDSYS** — logged in to the
machine locally, as `sdsys`. There is no other route in to try instead.

## The pcode library

`/usr/local/sdsys/bin` holds the pcode library — the interpreter itself,
which SD loads into shared memory at start-up and every session then runs.

It is readable by SD users and writable only by SDSYS. Nothing needs to
write it after an install — only the process that starts SD reads it, and
`sd -start` already runs privileged (see [Running SD](03-running-sd.html)).

## Scheduled jobs

A cron job or systemd timer can run an SD command without SDSYS rights,
and only the commands an administrator has named for it. The permit list
is the SDSYS file `batch.jobs`, locked read-only to SD users
(`sdsys:sdusers 750`).

It has its own page: **[Scheduled jobs](04-scheduled-jobs.html)**.

## The logs

There are two SD keeps itself, and they are not interchangeable.

| File | Where | For |
|---|---|---|
| `audit` | `/usr/local/sdsys` | **who did what** — logins, refusals, **`logto`**, account grants. See [Security and the operating system](12a-security-and-the-operating-system.html#the-audit-trail) |
| `errlog` | `/usr/local/sdsys` | diagnostics |

**A third place is worth checking, and it is not a file SD writes at
all: `journalctl`.** API connections and `sd-elevate`'s own actions go to
syslog (`syslog(3)`, `logger`), not to `errlog` — a real difference from
SD Core for Windows, which keeps a dedicated file for both. Filter by tag:

```sh
journalctl -t sd-elevate
journalctl SYSLOG_IDENTIFIER=sdlnxd
```

**`sd-elevate` itself keeps no comprehensive action log the way SD Core for
Windows's elevation helper does — a real, honestly-stated gap, not a
different mechanism standing in for it.** What exists: one `logger` call
recording when an account's own SD password is set, the SD-level `audit`
trail for account creation/deletion/grants (which `sd-elevate` performs on
SD's behalf), and `sudo`'s own logging of every invocation it authorizes
(`journalctl _COMM=sudo`, or `/var/log/auth.log` depending on the
distribution's syslog configuration) — which is where to look for *"the
account was not created — what actually happened"* until a dedicated log
exists.

### API connections in the journal

Every accepted API connection is logged with the address and port it came
from:

```
API connection over TCP from 203.0.113.4 port 51322 (SD login required)
```

or, over the Unix socket used for a local connection:

```
Connection over Unix socket /run/sd/api.sock from uid 1000 (don)
```

**Nothing is refused on the strength of it.** This records who connected; it
does not decide who may. The API's own checks are unchanged.

**A connection forwarded over ssh shows the tunnel's own endpoint, not the
person at the far end** — the same limitation SD Core for Windows has, for
the same reason: the tunnel genuinely does terminate on this machine.

## Line endings

**Directory files exist so you can edit their records with an ordinary text
editor**, and a file that started life on a Windows machine — a CSV saved
from Excel, a record pasted from Notepad — may still carry CR+LF line
endings. SD reads either ending correctly on this port: only the CR+LF
pair that ends a line is treated as a line ending, so a bare CR that
happens to be data is left exactly as it is.

**What SD itself writes follows the platform's own convention**, LF only,
for `writeseq`/`writecsv` output, `como`-captured output and the error
log. **SD's CSV statements are documented as following RFC 4180**, which
technically asks for CR+LF — if you need output another program expects to
be CR+LF-terminated, check that program's own tolerance for LF-only lines
rather than assume SD supplies the pair.

**Dynamic files are unaffected** — they are stored in SD's own format and
are not readable by other programs.

## The terminal

**The default terminal type is `linux`.** `term` on its own should report
your session's actual `TERM` — over ssh, whatever your client sent;
locally, whatever the terminal emulator or console set.

**63 definitions ship, compiling to 100 terminal names** — the extra names
are variants such as `vt100-w` and `vt220-at` — so `term wyse60` still
works.

**A name that is not installed is refused and your current type is kept** —
*"Unrecognised terminal name"* — so a typo costs you nothing. **`term` with no
argument reports the type actually in force**, which is how to check.

Watch for near-misses all the same. There is no plain `vt320` — the shipped
name is `vt320-at`. `terminfo.src` ships with SD, so `sdtic` can add a
definition that is not there.

**Backspace works**, at the prompt and when you are asked for a password.

### The page is 120 × 36, not 80 × 24

**SD's default terminal size is 120 columns by 36 lines.** It is not a
cosmetic default: the shipped `@` dictionary records and the default `list`
report layouts are formatted for 120 columns. **A terminal narrower than
that makes ordinary reports look wrapped or truncated**, which reads as a
formatting bug and is not one.

`term` reports the size in force, above the `Device` line:

```
:term
Page width: 120
Page depth: 36
Device    : linux
```

**The size is worked out at login**, in this order: the `LINES` and `COLUMNS`
environment variables if they are numeric, otherwise the terminfo entry's
`lines` and `cols`, **otherwise 36 and 120** — then raised to a minimum of
10 × 20 if smaller. So a console or ssh session normally gets its real window
size and 120 × 36 is the fallback when nothing answers, which is the case for a
phantom or a piped script.

> **`term default` restores it, and it prints nothing when it does.** It sets
> the same 120 × 36 the login path falls back to and returns silently, so run a
> bare `term` after it to see the result. `term 120,36` does the same by hand.

## Running SD

| | |
|---|---|
| The unit | `sd.service`, `sdclient.socket` |
| After an unclean shutdown | SD starts anyway, once the daemon's own liveness — not just the segment's presence — is checked. See [Running SD](03-running-sd.html) |
| `sd <command>` | needs SDSYS, or an entry in `batch.jobs` — see above |

## Setting no password

**An SD password only ever matters for the API.** An account with none set
still works normally at the console and over ssh — Linux has already
authenticated it — but has no way to authenticate an API connection, so a
client trying to reach it there is refused as if the password were simply
wrong. You can still choose one at any time; `modify.password` asks again
whenever you run it.
