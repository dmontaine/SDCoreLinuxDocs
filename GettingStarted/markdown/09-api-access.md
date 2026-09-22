Title: API access
Subtitle: The client API, the port it answers on, the login that replaced the old one, and what a remote session may reach.

The client API is a normal way for any account to use SD. A person running a
custom GUI program that talks to SD needs API access and may need nothing
else — no ssh, no terminal. **Every ordinary account has it, unconditionally
— there is no per-account choice, unlike SD Core for Windows:**

```
create.account user jane
```

Your application code does not change. `SDConnect()` and `SDConnectLocal()`
take the same arguments and return the same things. **What changed is
underneath: the login protocol, the port, the identity a session runs as, and
what it is allowed to open.**

> **SDSYS is the one exception, and it has no API access at all**, from
> anywhere, under any setting — see
> [Reaching the port is not getting in](#reaching-the-port-is-not-getting-in)
> below. Every other account has it by default; there is nothing to grant.

## The login is SCRAM-SHA-256, and the old one is gone

**A client that sends a password in clear is refused.** It gets *"Cleartext
login is no longer supported; this server requires SCRAM authentication"* and
the connection drops.

The API used to send the user name and password as plain text — anything able
to watch the connection could read the password. It now runs a challenge and
response: the server sets a puzzle only someone who knows the password can
answer, and **the password itself is never sent in any form.**

**The server also proves itself to you.** It finishes by returning a value
only the real server can compute, and the client refuses the connection if it
does not match. Another program that grabbed the port before SD started cannot
pretend to be SD in order to collect passwords.

### What you have to do

| | |
|---|---|
| **Use a client library from this release or later.** | An older one is refused outright |
| **Run `modify.password` again for every account that uses the API.** | The stored credentials changed shape and the old ones cannot be converted |

**An account whose password has not been re-set is refused, and the refusal
reads as a wrong password.** From the server's point of view there is no
credential to check. If a working client suddenly cannot log in after an
upgrade, this is the first thing to try.

The old credentials cannot be converted because **the password was never kept
anywhere, by design** — there is nothing to convert them from.

**Programs using the `!sdclient` class are covered.** The class module BASIC
programs use to reach another SD server speaks the new login too. Your code
does not change — `connect()` takes the same arguments — but the program has to
be running under this release **at both ends**.

**`SDConnectLocal()` connections are unaffected.** They send no password and
never did.

## The port

**Whether SD listens for the API at all is `systemd`'s `sdclient.socket`
unit**, activated independently of whether `sd` itself is running — not a
line in `sd.conf`. It defaults to `127.0.0.1:4243`, local only.

**Reaching the port from another computer is off unless you say so during
installation.** Answering yes rebinds the socket to `0.0.0.0:4243` and
adds a `ufw allow 4243/tcp` rule; answering no leaves it local-only. Change
it afterward, as SDSYS:

```
remote.api on | local | off
```

`on` and `local` restart the socket unit (not SD itself — no session is
ended); `off` stops it. See
[Administrator commands](06-administrator-commands.html).

**If you tunnel, you no longer need to.** `ssh -L 4243:127.0.0.1:4243
user@host` still works, but the design expects a direct connection to
port 4243 once you have opened it — tunnelling is only for a `local`-only
install reached from elsewhere.

> **`APILOGIN` is not an off switch.** It decides whether the API demands a
> password. `APILOGIN=0` is the **weaker** setting, not the safer one. Do not
> reach for it.

## Reaching the port is not getting in

A caller must clear two gates, in this order:

1. **Complete the SCRAM exchange** against a password held for that account —
   so **an account with no password cannot connect at all**.
2. **Not be SDSYS.** Every ordinary account already has API access; there is
   no separate group to join for it.

**SDSYS clears neither gate, ever, from any address including this
machine's own loopback.** It has no SD credential to complete a SCRAM
exchange with by design, and there is no keyword that changes this: it is
not a rule the API enforces about *where* SDSYS connects from, it is that
SDSYS has no way to authenticate over the API at all. See
[Accounts](05-account-types.html#sdsys-is-the-only-administrator).

**Failed API logins are written to the audit trail**, with the reason and
the address they came from. See [Other hardening](13-hardening.html).

## A session is confined to its own account

| | |
|---|---|
| **Allowed** | everything inside its own account, and the shipped SDSYS files every account needs — messages, `syscom`, the dictionaries, `sd.voclib`. Ordinary programs are unaffected |
| **Not allowed** | opening, renaming, deleting or listing anything else |

**A refused `OPEN` takes the `ELSE` branch**, distinguishing a containment
refusal from a genuinely missing file.

**A suspended account is refused here too, and deliberately says nothing
about why.** `modify.account fred suspended` denies the API as well as ssh,
and the message is the one this page already gives for an account that does
not exist and for one you are not granted:

```
User not allowed in requested account
```

**All three answer identically on purpose**, so the API cannot be used to
enumerate which accounts exist or what state they are in. If you are debugging
a client that has suddenly stopped connecting, `list accounts` from SDSYS
is where the answer is — a suspended account shows it in that listing.

### If your data lives outside an account

**There is no config-file mechanism here that widens an API session's
reach — a real difference from SD Core for Windows's `NETDIRS` setting,
which this port does not have** (checked against `config.c` directly:
`APIPORT` and `NETDIRS` are not parameters this port's configuration file
accepts at all). An API session's file access is exactly its own account's,
full stop — the same "no second wall" reasoning that removed the
`sh-on`/`os-on` switches (see
[Security and the operating system](12a-security-and-the-operating-system.html)).
If data needs to be reachable from more than one account, put it somewhere
every account can already open on its own terms, or reach it through a
program running in the account that owns it.

## An API session runs as you

**Records an API session creates are owned by the account that logged in**,
and the session reaches files with your Linux permissions rather than a
service account's. If your account may not read something, the API session
may not read it either.

**This is a real `setuid`, not a filtered credential** — SD drops root's
privilege entirely (`initgroups`/`setgid`/`setuid`, `K$ASSUME.USER`) before
the session is ever marked logged in. **If the identity cannot be assumed,
the login is refused outright** rather than continued under any other
identity:

```
Authentication succeeded but the session could not take your Linux identity
```

Because the privilege drop is one atomic system call that either succeeds
or is checked and refused, there is no window in which a session could
believe it is you while actually running as something else — the failure
mode SD Core for Windows had to add a specific alarm for (a filtered
access token that could silently fail to apply) does not have a Linux
equivalent to guard against here.

## `sh` and `OS.EXECUTE` over the API

**Unlike SD Core for Windows, there is no blanket refusal of `sh` or
`OS.EXECUTE` for a session that arrived over the API on this port.** Both
already run at the account's own Linux permissions unconditionally for
every session, console or API alike — the same "no second wall" reasoning
applies here too: an API session already runs as the real account
(`setuid`, above), so it already has exactly the reach that account's own
login shell has, no more. `SDCLIENT` in `sd.conf` is the configurable
control, if you want one: non-zero disables file access outright for an
API session, and `2` additionally refuses any subroutine not compiled as
callable from a client. It defaults to `0`, which permits everything — see
the *Administrator* set's *Configuration* chapter.

## Client libraries

| | |
|---|---|
| The shared library | `sdclilib.so` |
| Source | built as part of this port, or standalone at <https://github.com/dmontaine/linuxsdclilib> |

**Must come from this release or later.** A client library that predates
SCRAM is refused by the server.
