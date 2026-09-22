Title: Start here
Subtitle: What this set covers, who it is for, and what it deliberately leaves out.

You already know MultiValue. This set does not teach it.

SD Core for Linux is built from **upstream `sdb64`**, a MultiValue database
with elements found in the main SD version and in ScarletDME. ScarletDME was
a fork of the original GPL release of OpenQM 2.6.6.

**That lineage matters when you go looking for documentation.** Not all the
features of the **commercial** OpenQM 2.6.6 were in the GPL release, and **no
documentation specific to the GPL version was ever released**. So even the
OpenQM documents are not authoritative here.

**The OpenQM 2.6.6 documents can be used as a reference**, but SD Core has
additions, changes and deletions — of features, of structure, of security and
of commands. **These pages cover those changes.**

If you have used OpenQM, or upstream `sdb64`, much of SD Core will still be
familiar: the same data model, the same query processor, the same BASIC.

**SD Core for Windows is a separate port, built independently** — see
[SD Core for Windows](https://github.com/dmontaine/sd4windows). The two are
kept in behavioural parity by deliberate policy (this port's `CLAUDE.md`,
"Project stance": *"conformity with SD Core for Windows is the goal"*) —
what a verb does, what it refuses and why, its messages — while the
mechanism underneath is free to differ where the operating system does.
Where this set says something differs from SD Core for Windows, that is
usually why.

## What "used to" means in these pages

These pages describe changes, so **used to**, **no longer** and **now**
run all through them. **The comparison is against the code this version was
made from** — upstream `sdb64`, and ScarletDME and OpenQM 2.6.6 behind it.

**It never means an earlier release of SD Core for Linux**, because this is
the first one. Some of the changes are Linux-only and have no upstream
original to differ from; those say **earlier builds of this port** instead,
so the two are never confused.

## The pages

**There are nineteen, and they are numbered.** Read them in numerical order the
first time; after that they stand alone.

**A number with a letter after it is the second half of a long page**, split so
that no page runs longer than a reader will scroll: `01a` continues `01`, and
so on. Nothing was renumbered when they were split.

| | | |
|---|---|---|
| **00** | Start here | this page — what the set is and what it leaves out |
| **00a** | [Copyright and licence](00a-copyright-and-licence.html) | The copyright and the licence for this set, in full and in one place |
| **01** | [Installing SD Core](01-installation.html) | What the installer does, and the choices it offers |
| **01a** | [Upgrading and uninstalling](01a-upgrading-and-uninstalling.html) | Installing a new release over an existing one, and taking SD off the machine |
| **02** | **[Your first thirty minutes](02-first-run.html)** | **Start here if you just want it working** — install to a second user signing in, in eight steps |
| **03** | [Running SD](03-running-sd.html) | The daemon, starting and stopping, and recovering from an unclean shutdown |
| **04** | [Scheduled jobs](04-scheduled-jobs.html) | Running an SD command on a timer, and the permit list that decides which ones |
| **05** | [Accounts](05-account-types.html) | Ordinary accounts, SDSYS, Suspended and Group — what each one may do, and how to make one |
| **05a** | [Managing accounts](05a-managing-accounts.html) | Group accounts, sharing one, changing an account afterwards, and deleting it |
| **06** | [Administrator commands](06-administrator-commands.html) | The verbs only SDSYS has, and how to use them |
| **07** | [Development and file commands](07-programmer-commands.html) | Compiling, editing, and the verbs that maintain files, indexes and records in bulk |
| **08** | [ssh access](08-ssh-access.html) | How people reach SD on this machine over ssh |
| **09** | [API access](09-api-access.html) | The client API, its port, and the login that replaced the old one |
| **10** | [Client distribution](10-client-distribution.html) | Which library an application needs, and the one file no installer can update |
| **11** | [Lower case](11-lower-case.html) | Case in commands, file names, record ids and account names |
| **12** | [Security](12-security.html) | The identity model, and what protects the database |
| **12a** | [Security and the operating system](12a-security-and-the-operating-system.html) | Reaching the machine from inside SD, how privileged work is done, and the audit trail |
| **13** | [Other hardening](13-hardening.html) | Auditing, the shell permit list, and the rest |
| **14** | [Not in SD Core](14-not-in-sd-core.html) | What has been removed, and what to use instead |

## The five things most likely to surprise you

**1. Signing in asks for no SD password.** Linux has already authenticated
you — at the console, or over ssh with your own key or password. `sd` puts
you in the SD account with your own Linux user name; if there is no such
account, or you are not in the `sdusers` group, you are refused.
Administration is gated on being logged in to the machine, locally, **as**
the `sdsys` Linux user, at its own password — not on being a Linux
administrator, `sudo` or not, and not on a secret SD holds. See
[Security](12-security.html).

**2. Every ordinary account has ssh and API access, and there is no
per-account choice.** All of them, except SDSYS — the owner's ruling is
literal: *"All accounts, other than SDSYS, will have remote ssh and API
access."* `create.account` does not ask, and there is no `ssh`/`api`/`none`
keyword the way an earlier design once offered. **SDSYS has no remote
route at all**, ssh or API, from anywhere — administration is a real login
at this machine's own keyboard, or a desktop-sharing view of it. See
[ssh access](08-ssh-access.html) and [API access](09-api-access.html).

**3. An ordinary account is not denied the console, and that is not a
gap.** Unlike some MultiValue ports, SD keeps no second permission wall
behind ssh — `sh` and `os.execute` already run at the account's own Linux
permissions, unconditionally, the moment the account exists. A local login
at the machine and an ssh session that reaches a shell land at the
identical native permissions, so there is nothing a console login would
grant that ssh does not already. See [Security and the operating
system](12a-security-and-the-operating-system.html).

**4. Every account gets the same VOC.** There is no reduced starting set —
there is no account-tier model at all. What an account cannot do is
administer: that is SDSYS alone, and SDSYS is not something
`create.account` can produce. See [Accounts](05-account-types.html).

**5. Commands and names are lower case now, completely.** Everything that
can be lower case is — names on disk, VOC entries, program and include
names, and the files `create.file` makes — with upper-case input converted
on the fly, so no command, file or record id can exist in two casings. See
[Lower case](11-lower-case.html).

**And one that carries over unchanged: the API login is SCRAM**, and the
old cleartext one is gone. Clients built against the old protocol will not
connect.

## What this release is

**L1.0-0.** Linux only. There are no `#ifdef` branches keeping Windows alive
in this source — SD Core for Windows is a separate project and this is not a
build of it.

**It is a hobby project with no release schedule.**

This set is the delta. It covers installing SD Core on Linux, running it, and
what differs from OpenQM and from SD Core for Windows. The reference for the
language and the command processor is a separate set, and so is the
administrator's.

## Where the source is

**Both repositories are public, and everything in them is open source.** SD is
GPL software — `config gpl` at an `sd` prompt displays the licence, and the
installed tree carries it as a file.

| | |
|---|---|
| The server, the client libraries and the installer | <https://github.com/dmontaine/SDCore4Linux> |
| These pages | <https://github.com/dmontaine/SDCoreLinuxDocs> |

**Neither repository contains a built binary, deliberately** — no compiled
executable, no `.so`, no object files. A clone builds. That is why installing
means building, and why there is no download of a compiled artefact in the
repository itself.

The documentation repository holds the **Markdown only**; the HTML and PDF you
are reading (once this set's own rendering toolchain exists — see the
repository's own README) are generated from it and are not stored there.

## Reporting what you find

**Open an issue on the server repository** — <https://github.com/dmontaine/SDCore4Linux/issues>
— for anything about SD itself, and on the documentation repository for an
error in these pages. If you are not sure which, the server one is the right
guess.

**Issues rather than pull requests.** Both repositories are readable by anyone
and **writable only by the author**, so a change cannot be merged from outside;
a clear issue is worth more than a patch nobody can apply. A patch attached to
an issue is welcome, it just travels that way.

The two things worth reporting in most detail are **anything that behaves
differently from OpenQM and is not described here**, and **anything in these
pages that turns out not to be true of the build you are running**. The second
is as valuable as the first.

**Quote the version as `L1.0-0`** — the string in the header bar of every
page here, and in what `sd --version` reports. The bare `1.0-0` is the same
release; the `L` says it is the Linux one, and that is the part worth
keeping in a report.
