Title: Features the Developers Could Not Test
Subtitle: The parts of SD Core for Linux that were built and reasoned about but never exercised, what is known about each, and what it would take to settle it.

Everything else in this documentation describes behaviour that was run and
watched. **This page is the exception, and it exists so that the exception is
visible in one place rather than scattered through the reference as
footnotes.**

Nothing here is known to be broken. Each entry is something that **compiles,
or exists, or follows from the source, and was never put under load or into
the condition that would prove it.** Treat them as the list of things to pilot
before an application depends on them. **This list is drawn from this port's
own build and witness record, not carried over from SD Core for Windows's
own version of this page** — the two ports differ in which parts have
actually been run, not just in which parts exist.

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

**Why it is in the administrator set.** A reference page that keeps saying
*"this part was not tested"* teaches an application programmer to distrust the
whole book. An administrator deciding what to put into production needs
exactly that information. So it is gathered here, and the user-facing pages
state what SD does without qualifying every other paragraph.

## How to read an entry

| | |
|---|---|
| **Known** | what was actually run and observed |
| **Not known** | the specific gap — usually narrower than the heading suggests |
| **To settle it** | what would have to be done |

## Sessions

### Whether `sd` inside an `sh` session started from `sd` is refused

**Known.** `sh` runs a real, unrestricted shell for every account, and
starting `sd` from an ordinary Linux shell works normally.

**Not known.** Whether starting `sd` from *inside* an `sh` session that SD
itself launched is refused, or simply starts a second, genuinely nested
interactive session. SD Core for Windows specifically detects and refuses
this; no equivalent marker or guard was found in this port's `op_sh.c` or
`sd.c` while checking [Operating System
Access](03-operating-system-access.html) for this release, but the
absence of a guard in source is not the same as having watched the
attempt and seen what actually happens.

**To settle it.** `sd`, then `sh`, then `sd` again, at a real terminal,
watching what the second `sd` does.

## Locking and contention

### Semaphores under contention

**Known.** The semaphores are exercised on every record lock.

**Not known.** Whether a semaphore has been observed genuinely blocking —
one session waiting on another under real contention, as opposed to two
sessions each getting an uncontended lock in quick succession.

**To settle it.** Enough concurrent sessions to make one wait, and a watch
on what it does while it waits.

### Contention between an API session and a local one

**Known.** Two *local* sessions compete correctly, and the API's own
session-confinement gate has its own witness coverage — see *API access*
in the **Getting Started** set.

**Not known.** A lock held by a local terminal session and contested from
an API connection specifically, watched together rather than each proven
separately.

**To settle it.** An API client and a terminal session competing for one
record.

### Task locks taken twice by the same session

**Known.** From the source: taking a task lock you already hold succeeds, and
one `unlock` releases it however many times you locked it — the ownership test
is *"unowned or mine"*, and `unlock` clears the slot outright.

**Not known.** It was **read rather than run**. No program has taken the same
task lock twice and then released it once, watched.

**To settle it.** Four lines of SD BASIC.

## Application data

### A real application's data

**Known.** SD creates, writes, reads and deletes files, records, indexes,
select lists and sequential files, and the system files it bootstraps with are
real ones.

**Not known.** **No production application's data has been loaded into this
port.** Nothing here has met a file of hundreds of thousands of records, a
deep dictionary, or a schema built over years by somebody else.

**To settle it.** Restore an existing account and run it.

## Sockets

### UDP and ICMP

**Known.** TCP works: listening, connecting, accepting, reading, writing, the
blocking and non-blocking modes, and the error codes — exercised directly by
the TLS/SCRAM interop work.

**Not known.** The `0x00010000` and `0x00020000` flags are named in the
documentation because they are **in the compiler**, not because a datagram was
ever sent. No UDP or ICMP socket has been opened.

**To settle it.** A datagram to a listener and back.

## Scheduled jobs

### A cron job or systemd timer running as an account `create.account` made

**Known.** `login`'s `batch.permitted` gate (see *Scheduled jobs* in the
**Getting Started** set) is unit-tested against mutants and its message
text and audit reasons are verified directly against the running source.

**Not known.** Whether a *real* cron entry, running unattended as a Linux
account SD created, actually reaches the gate the way an interactive
`sd <command>` does — cron and `sd` interacting live, rather than the
gate logic checked in isolation.

**To settle it.** A crontab entry pointed at an SD account, and a watch on
whether it runs and is correctly permitted or refused.

## SD BASIC statements that compile but were never run

| | why not |
|---|---|
| `sendmail` | needs a mail relay configured |
| `chgphant()` | needs a phantom process to change |
| `ccall()` | needs a C function registered into the executable |

**Known.** All three compile in an ordinary account.

**Not known.** What any of them does. Nothing else in the documentation
depends on them.

## The terminal editors' key bindings

**`nano` and `micro`'s key bindings are each program's own, unmodified —
this port does not implement or alter either editor**, only launches it
and stages its syntax highlighting. If a binding surprises you, that is
each program's own documented behaviour, not something to report against
SD.

## What is NOT on this page, and why

**Anything that was tested and failed is a defect, not a gap**, and does not
belong here — it is either fixed or it is a known issue.

**Anything a reader might merely find surprising is not a gap either.** The
places where this port deliberately differs from OpenQM, ScarletDME, upstream
`sdb64`, or SD Core for Windows are documented as differences, in the pages
that describe the feature. This page is only about what nobody has watched
happen.

## See also

[Sessions and Locks](02-sessions-and-locks.html) covers the locking model that
some of the entries above qualify.
[Installation and the daemon](08-sd-installation.html) covers scheduled jobs
and the account model behind the cron entry.
[SD System Limits](06-sd-system-limits.html) states which of its figures come
from the source and which from a running system, and is the other page in this
set that distinguishes the two.
