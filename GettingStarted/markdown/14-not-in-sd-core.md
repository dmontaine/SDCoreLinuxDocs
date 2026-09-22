Title: Not in SD Core
Subtitle: What has been removed, why, and what to use instead.

This page exists so you do not spend time hunting for something that is not
there. **It names what is gone and what to use in its place; it does not
document the removed features themselves.**

Everything here was in OpenQM, in ScarletDME, or in SD on Linux, and is not in
SD Core for Windows.

> **If you had a use for any of these, say so.** Several were removed on the
> reasoning that nothing needed them. That reasoning is worth testing against
> real use, and for some of them an administrator can put the verb back into an
> account's VOC — the programs behind a few of them are still installed.

## Editors

| Gone | Use instead |
|---|---|
| `sed` — the full-screen editor | **`edit`**, or **`ed`** for the line editor |
| `update.record` — the full-screen record editor | **`edit`** or **`ed`** |
| `modify` — the full-screen record editor from OpenQM | **`edit`** or **`ed`** |

**SD Core's own full-screen editing is `edit` and `micro`**, which open the
record in Microsoft Edit and in micro — see
[Programmer commands](07-programmer-commands.html#editors), which also says
what they are good for and what they cannot do. The three above are
gone as *programs*; the capability is not.

`modify` is not in SD Core at all, for any account.

> **`micro` was on this page and has come off it — under its own name.** It
> was removed on 17 Aug 2026 because it launched an external editor, which is a
> way out of SD onto the machine underneath it. That was reversed on
> 26 Aug 2026, and there are now **two** full-screen editors, **`edit`** and
> **`micro`**: the same idea, done deliberately, gated by `os.users` field 2 —
> every account has the verb, not every account has the permission — and
> refused over the API regardless.

**`modify.account` and `modify.password` are not affected.** They are
different verbs with different programs behind them. `modify.account` is
SDSYS's alone; `modify.password` is every account's, for its own password —
only naming a different account needs SDSYS.

> **`ed`** was never affected by the keyboard faults that hit the full-screen
> editors — it reads whole lines and goes through the command-line editor. **If
> backspace is ever reported broken in `ed`, that is a new fault, not an old
> one returning.**

## The PROC language

`PROC` is gone. **A VOC item of type `PQ` now reports that PROC is not
supported instead of running.** Your `PQ` records are left alone — it is the
interpreter that has gone, not the records.

**Do not confuse PROC with the query processor.** `LIST`, `COUNT`, `SELECT`
and `SORT` are unaffected. They are a different thing despite the similar name.

## SDNet — remote file access

SD could open a file held on another SD server by putting `server;file` in a
VOC entry. **That is gone. A VOC entry containing a semicolon is now simply a
file name that does not resolve.**

`SET.SERVER`, `DELETE.SERVER` and `LIST.SERVERS` have gone with it. **Two of
those three had never worked in any case** — their VOC entries were malformed.

**Why it went:** each server's user name and password were kept in `sd.conf`,
obscured with a simple letter substitution that is not encryption, and the
session ran over port 4245. There was also no way to switch the feature off —
the `NETFILES` setting was read at start-up and then never consulted.

**The API is not affected.** `SDClient` and the remote API are a separate
mechanism and are unchanged. See [API access](09-api-access.html).

**`NETFILES` is still accepted in `sd.conf`** and does nothing, so an existing
configuration file will not stop SD starting.

## Virtual file systems

**SD has never been able to open a virtual file system.** Nothing in the
file-opening code ever recognised a `VFS:` pathname. What the language carried
was the *outline* of one, and none of it could be reached: a VOC F-pointer
written as `VFS:something` was reported as a virtual file system, passed the
name resolver, and then failed to open with an unrelated error.

All of it has been removed, so the language no longer offers a feature it
cannot perform.

**These names are no longer defined, and a program mentioning one will no
longer compile:**

```
FL$TYPE.VFS      SYSCOM KEYS.H
ER$VFS.NAME      SYSCOM ERR.H
ER$VFS.CLASS     SYSCOM ERR.H
ER$VFS.NGLBL     SYSCOM ERR.H
```

`FTYPE` no longer returns `VFS` for a `VFS:` pathname. **Error numbers 3038,
3039 and 3040 are retired and will not be given a new meaning.**

**IF ONE OF YOUR PROGRAMS REFERS TO ANY OF THESE, it was testing for a state
SD could not reach, and the test can be deleted.**

Two unreachable pieces went with it: `_EXTENDLIST`, installed into the SDSYS
`GPL.BP` file and loaded at every start-up although nothing ever called it; and
the debugger's `(Networked)` file type, which no file could report once SDNet
was gone.

## Language and locale

`NLS`, `SET.LANGUAGE` and `LOAD.LANGUAGE` are removed. **SD Core is English
only**, and these were the only callers of the message-language machinery.

## Embedded Python — reversed again, and reversed differently

**Python inside `sd.exe` is dropped, permanently — but calling Python from
SD BASIC is back**, as a separate, native helper process SD talks to over a
pipe rather than a library loaded into the server. The distinction is not
cosmetic: the earlier removal was because Python and the MSYS2 runtime
`sd.exe` is built on cannot share one process safely (§5.3 — `long` is a
different width on each side). The helper avoids that by never being the
same process at all.

**21 `gpl.bp/PY_*` programs** are BASIC-callable (`CALL !PY_CREATEDICT`,
and so on) — there is no TCL verb, so this is a programming capability, not
a command you type at the prompt. Access is gated per session, at the
moment Python starts, by the same `os.users` field 2 permission that gates
`OS.EXECUTE` — a session without it cannot start the helper at all.

## Field-level encryption

**`encrypt.field` is gone, and with it field-level encryption from TCL.** The
verb is in **no account's VOC at any tier** — it left
`newvoc/TIER.ADD.ADMINISTRATOR` before W1.0-0. While it was still there it could not
have worked: the `$CRYPTO` program behind it is not in the distribution, and
every form of the verb failed at load, before it looked at what you typed.

**Encryption in SD BASIC is unaffected and is the supported route.**
`sdencrypt()` and `sddecrypt()` ship — see *SD Basic - System and Environment*
— and replaced the older `encrypt()` and `decrypt()` functions. What has gone
is the TCL verb that encrypted a field in place, and **nothing replaces that**.

## Account and configuration items

| Gone | Notes |
|---|---|
| `RDPACCOUNT`, `NO.RDPACCOUNT` | typing it now stops **`create.account`** with *Unexpected token (RDPACCOUNT)* and makes no account |
| `CREATUSR` | **`config`** no longer lists it; `config('CREATUSR')` returns nothing. A `CREATUSR` line in `sd.conf` is still accepted and ignored |
| `umask` | removed entirely. It controls POSIX file-mode bits, which Windows does not use for security — see [Security](12-security.html#what-ships-secured-before-you-change-anything) for what does the equivalent job here |
| Field 4 of an `ACCOUNTS` record | the list of accounts allowed in. **`list.grants`** answers that question now |

**Accounts already created with `RDPACCOUNT` keep their Windows sign-in.**
Nothing goes round and takes it back, because SD did not record which accounts
they were. If you have any, either delete and recreate them, or add them to the
restricted group by hand:

```
net localgroup sdsshonly <name> /add
```

## The five programs SD used to ship into the SDSYS BP file

`PCL` and `PCL.GRID` (printer control), `U0032` and `U50BB` (user exits) and
`VFS.CLS` (a template class module) are no longer installed there.

**PCL is unaffected as a printer feature** — the `PCL` keyword and the
catalogued `PCL` routine are both still there. What has gone is a second, older
copy of the source sitting in `BP`.

**SD now ships nothing into the SDSYS bp file.** It is created empty and is
yours — and because of that, **`bp` and its compiled objects are now preserved
when you upgrade**, alongside your accounts and the rest of your own data.

## Things that were never features, and are not coming

These are not removals. They are stated here because a reader coming from
another MultiValue system will otherwise assume they exist.

**Multi-user access over remote Desktop is not supported.** It follows from
the access model and is settled. One Windows setting covers Remote Desktop and
the physical keyboard together, so allowing one allows the other. A verb that
lifted the restriction was built and deleted the next day for exactly that
reason. If you want it, you want Windows Server, RDP client access licences and
probably a commercial product built for it. See
[ssh access](08-ssh-access.html).

**SD cannot be installed silently.** `/SILENT` and `/VERYSILENT` are refused,
with a message saying why, and there is no switch to override it. Installing
ends by asking for a password and a silent install has nobody to ask — it used
to finish with **no password on any account** and say nothing about it.
Unattended deployment is not supported.

**scp AND sftp DO NOT WORK INBOUND ONCE SD HAS CONFIGURED THE ssh SERVER**,
for anybody, administrators included. This is the accepted cost of putting
every ssh session straight into SD. **Pull files rather than pushing them** —
see [ssh access](08-ssh-access.html#the-cost-scp-and-sftp-stop-working-inbound).
A machine with no ssh server is unaffected, because SD has configured nothing.

**The cleartext API login is gone**, and a client that still sends a password
in clear is refused outright. See [API access](09-api-access.html).

## Linux-only mechanisms

The Linux privilege model does not survive the move and has been replaced
rather than emulated. Most of this is invisible unless you are reading source,
but two consequences show:

- **`chmod` does nothing.** The MSYS2 mount is `noacl`, so file-mode bits are
  not a security control here. Windows ACLs are, and SD sets them.
- **There is no `sdsys` uid to drop to.** Privilege is elevation, and the
  operating system's groups are the whole of the authorisation model. See
  [Security](12-security.html).
