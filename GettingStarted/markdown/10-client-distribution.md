Title: Client distribution
Subtitle: The shared library an application needs, why there are two names, and how to build one.

An application reaches SD Core through a shared library. **You do not have to
find it inside an installed SD system** — the source builds standalone as
well, because the person writing an application and the person running the
server are not always the same person.

## Two names, one source

```
sdclilib.so
libsdcli.so
```

Both are built from the same object files in the same step — `sdclilib.so`
is the name an application historically asks for; `libsdcli.so` follows the
ordinary Unix `lib*.so` convention (`-lsdcli` at link time). **They are not
two copies to keep in sync by hand** — one build target produces both, so
there is nothing to drift.

**This port carries no 32-bit build.** SD Core for Windows ships a separate
32-bit client for QM-heritage applications and a third-party tool
(mvDeveloper) that only runs 32-bit; neither concern applies here.

## Where it lands

Built to `bin/` under the source tree by `make sd`; a server install places
it alongside the `sd` binary itself, under `/usr/local/sdsys/bin`. There is
no separate client-only package yet — building from source, or copying the
`.so` from an existing install, is how an application gets it today.

## The library must match the release

**The cleartext API login is gone.** A client that still sends a password in
clear is refused with *"Cleartext login is no longer supported; this server
requires SCRAM authentication"*.

Two things to do, and the second is the one people miss:

1. Use a client library from this release or later.
2. **Run `modify.password` again for every account that uses the API.** The
   stored credentials changed shape and the old ones cannot be converted — the
   password was never kept anywhere, by design, so there is nothing to convert
   them from.

An account whose password has not been re-set is refused, **and the refusal
reads as a wrong password**, because from the server's point of view there is
no credential to check.

## Connecting

Your application code does not change. `SDConnect()` and `SDConnectLocal()`
take the same arguments and return the same things they always did.

| | |
|---|---|
| `SDConnect()` | over the network, to port **4243** |
| `SDConnectLocal()` | on the same machine. **Sends no password and never did**, so SCRAM does not apply |

BASIC programs reaching another SD server use the `!sdclient` class, which
speaks the new login too — `connect()` takes the same arguments, but **the
program has to be running under this release at both ends.**

Everything about what a connected session may open, the two gates it must
clear, and the identity it runs as is on [API access](09-api-access.html).

## Building from source

The source lives in the server's own repository at
`sdb_ai/sd64/gplsrc/sdclilib`, and `make sd` produces it together with the
server — <https://github.com/dmontaine/SDCore4Linux>. **No built `.so` is
committed**, so a clone builds — the same no-binaries rule the whole
repository follows.

A standalone copy of the same source, kept in sync for building the client
without the whole server tree, is at
<https://github.com/dmontaine/linuxsdclilib>.

**The C headers are shipped with the source tree.**
