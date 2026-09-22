Title: Not in SD Core
Subtitle: What has been removed, why, and what to use instead.

This page exists so you do not spend time hunting for something that is not
there. **It names what is gone and what to use in its place; it does not
document the removed features themselves.**

Everything here was in OpenQM, in ScarletDME, or in upstream `sdb64`, and is
not in SD Core for Linux. **Most of these removals were made independently
on SD Core for Windows too, for the same reasons** — see that port's own
version of this page — which is worth knowing if you come across a decision
recorded on one side and wonder whether it binds the other.

> **If you had a use for any of these, say so.** Several were removed on the
> reasoning that nothing needed them. That reasoning is worth testing against
> real use.

## Editors

| Gone | Use instead |
|---|---|
| `sed` — the full-screen editor | **`nano`** or **`micro`**, or **`ed`**/**`edit`** for the line editor |
| `update.record` — the full-screen record editor | **`nano`** or **`micro`** |
| `modify` — the full-screen record editor from OpenQM | **`nano`** or **`micro`** |

**SD Core's own full-screen editing is `nano` and `micro`**, which open the
record in each program by name — see
[Programmer commands](07-programmer-commands.html#editors), which also says
what they are good for and what they cannot do. **Unlike SD Core for
Windows, `edit` is not one of them here — it aliases `ed`, the line editor,
because there is no Linux program to alias it to the way Microsoft Edit
serves that role there.** The three removed programs above are gone as
*programs*; the capability is not.

`modify` is not in SD Core at all, for any account.

**`modify.account` and `modify.password` are not affected.** They are
different verbs with different programs behind them. `modify.account` is
SDSYS's alone; `modify.password` is every account's, for its own password —
only naming a different account needs SDSYS.

> **`ed`** was never affected by any full-screen keyboard fault — it reads
> whole lines and goes through the command-line editor.

## The PROC language

`PROC` is gone. **A VOC item of type `PQ` now reports that PROC is not
supported instead of running.** Your `PQ` records are left alone — it is the
interpreter that has gone, not the records.

**Do not confuse PROC with the query processor.** `list`, `count`, `select`
and `sort` are unaffected. They are a different thing despite the similar name.

## SDNet — remote file access

SD could open a file held on another SD server by putting `server;file` in a
VOC entry. **That is gone. A VOC entry containing a semicolon is now simply a
file name that does not resolve.**

`set.server`, `delete.server` and `list.servers` have gone with it.

**The API is not affected.** `!sdclient` and the remote API are a separate
mechanism and are unchanged. See [API access](09-api-access.html).

**`NETFILES` is still accepted in `sd.conf`** and does nothing, so an existing
configuration file will not stop SD starting — see
[Other hardening](13-hardening.html#the-logs) for the one place it is still
read (a dead code path with no way to reach it, not a live feature).

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

`ftype` no longer returns `VFS` for a `VFS:` pathname.

**IF ONE OF YOUR PROGRAMS REFERS TO ANY OF THESE, it was testing for a state
SD could not reach, and the test can be deleted.**

## Tape and restore

The `TAPE`/`RESTORE` subsystem is gone, along with the assumption of a
tape-backed sequential medium it was built around. Back up and restore SD
data the ordinary Linux way — at the file level, with the daemon stopped,
or through your own export/import BASIC.

## Language and locale

`NLS`, `set.language` and `load.language` are removed. **SD Core is English
only**, and these were the only callers of the message-language machinery.

## Embedded Python — kept, and this port's own decision to keep it

**Unlike SD Core for Windows, which dropped it and only later brought back a
narrower, process-isolated form, this port never removed embedded Python.**
It links directly against the interpreter, and there is no separate helper
process to talk to over a pipe.

**BASIC-callable programs** (`call !py_createdict`, and so on) are the
interface — there is no TCL verb, so this is a programming capability, not
a command you type at the prompt. **There is no permission gate on
starting it**, the same "no second wall" reasoning that applies to `sh` and
`OS.EXECUTE` — see [Security and the operating
system](12a-security-and-the-operating-system.html).

## Field-level encryption

**`encrypt.field` is gone, and with it field-level encryption from TCL.**

**Encryption in SD BASIC is unaffected and is the supported route.**
`sdencrypt()` and `sddecrypt()` ship — see *SD Basic - System and Environment*.
What has gone is the TCL verb that encrypted a field in place, and
**nothing replaces that**.

## Account and configuration items

| Gone | Notes |
|---|---|
| `CREATUSR` | `config` no longer lists it; `config('CREATUSR')` returns nothing. A `CREATUSR` line in `sd.conf` is still accepted and ignored — `create.account` always creates the Linux user, there is nothing to opt in to |
| `grant`/`revoke`/`list.grants` | folded into `modify.account add`/`delete` — see [Accounts](05-account-types.html) |
| the `ssh`/`api`/`both`/`none` route keyword | every account has both by default now; there is no keyword to narrow it |
| `sh-on`/`sh-off`/`os-on`/`os-off` | gone with the `os.users` permit list they set — `sh` and `OS.EXECUTE` are unconditional now, see [Security and the operating system](12a-security-and-the-operating-system.html) |

**`umask` is kept, deliberately, and is not on this list** — a real
difference from SD Core for Windows, where it was removed as inert. It is
a live mechanism here; see [Accounts](05-account-types.html).

## Eighteen SDSYS test and legacy programs

`bigstr_test`, `msgtest`, `pcl`, `pcl.grid`, `pcode_list`, `sdtest_v8`,
`sd_encrypt`/`_b64`/`_ext`, `sd_ext`, `test.then.else`, `testsz`, `u0032`,
`u50bb`, `vfs.cls`, `pref_t`, `sdTests` and `tilde_test` are no longer
installed into the SDSYS `bp` file — developer-era test and demonstration
programs with no product function, not something an application ever
called. **`py_json`, `py_term`, `py_test` and `py_test2` were kept
deliberately**, as the documented examples for embedded Python, above.

**`pcl` is unaffected as a printer feature** — the `pcl` keyword and the
catalogued `pcl` routine in `gpl.bp` are both still there. What has gone is
a second, older copy of the source sitting in `bp`.

**SD ships nothing into the SDSYS `bp` file at all now.** It is created
empty and is yours — and because of that, **`bp` and its compiled objects
are preserved when you upgrade**, alongside your accounts and the rest of
your own data.

## Things that were never features, and are not coming

These are not removals. They are stated here because a reader coming from
another MultiValue system will otherwise assume they exist.

**SD cannot be installed unattended.** `installsdai.sh` asks for
confirmation and, at the end, three passwords — there is no flag to skip
either. Unattended deployment from this installer is not supported; a
site that needs one builds its own automation around the same underlying
verbs and Linux tools the installer itself uses.

**scp and sftp do not work inbound over ssh, for anybody**, once SD's ssh
boundary is in place — which it is, regardless of whether remote ssh
access is turned on. This is the accepted cost of putting every ssh
session straight into SD. See
[ssh access](08-ssh-access.html#the-cost-scp-and-sftp-stop-working-inbound-over-ssh).

**The cleartext API login is gone**, and a client that still sends a password
in clear is refused outright. See [API access](09-api-access.html).
