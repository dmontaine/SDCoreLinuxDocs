# qmclilib - 32-bit QM-compatible build of sdclilib

A 32-bit Windows DLL named `qmclilib.dll`, exporting the original QMClient
entry-point names, so that a 32-bit application written against QMClient can
connect to an SD server.

It is not a separate library. It is the same `sdclilib.c` as the 64-bit build,
compiled for i686 and given an export table that answers to both name sets.
The source lives in the SD for Windows tree at
`../sd4windows/sdb_ai/sd64/gplsrc/sdclilib`, and this project builds straight
from it.

## What differs from the 64-bit build

|                | 64-bit build            | here                            |
| -------------- | ----------------------- | ------------------------------- |
| DLL            | `sdclilib.dll`          | `qmclilib.dll`                  |
| second name    | `sdclient.dll`          | `qmclient.dll`                  |
| Architecture   | x86-64                  | i386                            |
| C runtime      | UCRT                    | msvcrt                          |
| Exports        | 50 `SD*`                | 50 `SD*` + 49 `QM*`             |
| Toolchain      | `ucrt64` GCC            | `mingw32` GCC                   |
| libgcc         | not linked              | linked statically               |
| System DLLs    | ws2_32, bcrypt          | ws2_32, bcrypt                  |

`bcrypt.dll` arrived with the SCRAM-SHA-256 login on 19 Aug 2026. It is part
of Windows, so `qmclilib.dll` is still a single file that can be copied next
to an application - which is the constraint that chose PBKDF2 over Argon2 in
the first place, a 32-bit process being the weakest client that has to run the
key derivation.

Everything else - the protocol, the error codes, the buffer handling - is the
same code. The wire format is unaffected by the word size: the packet structs
are `#pragma pack(2)` over `int16_t` and `int32_t` only, so they have the same
layout in both builds.

## Requirements

32-bit MinGW GCC, from an MSYS2 shell:

```sh
pacman -S mingw-w64-i686-gcc
```

It installs into `C:\msys64\mingw32` and does not disturb the UCRT64 toolchain
that builds the 64-bit library.

## Build

From a Windows command prompt or PowerShell:

```bat
build.cmd
```

From an MSYS2 shell:

```sh
make
make check
```

Both routes build the DLL and run all three tests. Both refuse to run if the
compiler is not an i686 one, because the alternative is a 64-bit DLL under a
32-bit name, and the only thing Windows says about that is "%1 is not a valid
Win32 application".

Outputs:

- `qmclilib.dll` - the 32-bit runtime DLL
- `libqmclilib.dll.a` - GCC/MinGW import library
- `qmclilib.h` - QM-named C/C++ declarations
- `qmclilib.def` - the export list, including the QM aliases

## The QM names

Windows resolves imports by name, so renaming the file is not enough: an
application that imports `QMConnect` needs an export called `QMConnect` or it
will not load at all. `qmclilib.def` supplies those names as **aliases** -
extra export-table entries pointing at the SD implementations, not wrappers.
`QMConnect` and `SDConnect` are one function with two names, which is also
what makes it work for the variadic `QMCall` and `QMCallx`, where a forwarding
wrapper could not pass on the argument list.

Of the 49 entry points the original QM `qmclilib.c` exported:

- **48** are aliases onto the SD function of the same base name.
- **`QMConnectLocal`** is a stub that always fails. It starts a local server
  process over a pipe in the Linux build, which is a Linux path; this library is
  Winsock-only. It is exported anyway so that an application which merely
  imports the symbol still loads - see `qmcompat.c`. Use `QMConnect`.

`SDCallx` and `SDGetArg` have no QM counterpart, because the original QMClient
had none. They are still exported under their SD names.

Type differences between the two APIs - `QMDebug` takes `bool` where `SDDebug`
takes `int16_t`, `QMEnterPackage` returns `bool` where `SDEnterPackage`
returns `int16_t` - are ABI-compatible under 32-bit cdecl: both occupy one
4-byte stack slot, and both returns arrive in `AX` with the value in `AL`.

## Calling convention

`__cdecl`, as the original QMClient library used, and undecorated in the export
table - `QMConnect`, not `_QMConnect` or `QMConnect@20`.

That suits C, C++, Delphi and FreeBASIC declarations marked `cdecl`. It does
**not** suit Visual Basic 6 or VBA `Declare` statements, which are always
`__stdcall` and would leave the stack unbalanced on every call. A VB6 client
needs a stdcall shim in front of this DLL; that is a separate piece of work.

## Two names, one library

The build produces `qmclilib.dll` and `qmclient.dll`. They are the same object
code from the same `sdclilib.c` in the same build, each with its own matching
import library.

`qmclilib.dll` is the name an existing QMClient application already asks for
and does not move — that name is the whole reason this project exists.
`qmclient.dll` is the name to use for new work, and the one the installer's
PATH entry is aimed at.

They are two links rather than one link and a file copy. An import library
records the name of the DLL its symbols come from, and here the `.def` file
carries a `LIBRARY` statement that sets it — so a renamed copy, or a second
link using the first `.def`, would produce `libqmclient.dll.a` sending the
application to `qmclilib.dll` regardless of what `-o` said.

`qmclient.def` is **generated** from `qmclilib.def` by rewriting that one line,
and is not kept in the repository. Two hand-maintained copies of a 99-name
export list would eventually differ by one name, and that failure appears only
at run time and only for whoever called it. `make check` runs the QM alias test
through both import libraries, which is what would catch either mistake.

## Deployment

Copy `qmclilib.dll` (or `qmclient.dll`) next to the application. It imports
only `KERNEL32.dll`, `msvcrt.dll`, `WS2_32.dll` and `bcrypt.dll` — all part of
Windows, so nothing else has to travel with it. `bcrypt` arrived with the
SCRAM-SHA-256 login and was chosen precisely to keep that true.

**Beside the executable beats PATH.** Windows searches the application's own
directory first, so a copy there wins over any installed one — which is the
answer if two versions ever disagree.

## Installer

`qmclient.iss` builds a Windows installer for the 32-bit client:

```bat
build.cmd
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" qmclient.iss
```

It packages what the build has already produced and compiles nothing itself,
the same arrangement as the server's `gplbld/sd.iss`. The result is
`Output\sd-client-x86-setup-<version>.exe`, installing to
`C:\Program Files (x86)\SD Client (32-bit)` as `bin\`, `lib\` and
`include\`, with an opt-out task that appends `bin\` to the system PATH.

It is deliberately **not** marked `ArchitecturesInstallIn64BitMode`, so it stays
a 32-bit install: `{autopf32}` then resolves to `Program Files (x86)` on 64-bit
Windows and to `Program Files` on 32-bit, which is right in both cases. Marking
it would also refuse to run on 32-bit Windows — the one platform with no
alternative package.

Its AppId and directory differ from the 64-bit package, so both may be
installed at once, which is the normal case on a development machine.

The DLL is not stripped, which is why it is larger than its code - the same
convention as the 64-bit build.

Two failures worth telling apart when testing:

- *"%1 is not a valid Win32 application"* - wrong architecture. The
  application is 64-bit, or the DLL was built by the wrong compiler.
- *"The procedure entry point ... could not be located"* - wrong name. The
  application wants an entry point this library does not have; `objdump -p
  qmclilib.dll` lists what it does have.

## Diagnosing a failed connection

An application that reports only "cannot connect" has discarded the useful
half of the failure. `QMError()` holds the real message, and `sd-connect.exe`
prints it:

```bat
make sd-connect.exe
sd-connect.exe 10.0.0.5 4243
```

Two arguments test the transport only and need no credentials. Five - host,
port, user, password, account - test the login as well.

The four failures it separates want four different fixes:

| What it reports | Where the problem is |
| --- | --- |
| `gethostbyname()` failed | the name does not resolve |
| `connect()` refused, error 10061 | nothing is listening on that port |
| connection accepted, no ACK | the port is open but the sdclient service behind it is misconfigured |
| ACK received, `QMConnect` fails | transport is fine; the server rejected the user, password or account |

The ACK is the dividing line. The server sends `0x06` as soon as it is ready
to talk, and `OpenSocket()` in sdclilib.c waits for it before any login data
is sent - so everything up to the ACK is network and service configuration,
and everything after it is credentials.

The default port is 4243.

## Tests

`make check` and `build.cmd` run three:

- **smoke** and **internal-state**, from the 64-bit project, confirming the
  library still behaves when built for i386.
- **qm-alias**, from `tests/`, confirming what this project adds: that the QM
  names resolve at load time, that they are the same addresses as their SD
  counterparts, and that they return what the SD functions return.

None of them needs a server.

## Source layout

There is no copy of the library source here. The Makefile's `SRCDIR` points at
`../sd4windows/sdb_ai/sd64/gplsrc/sdclilib`, so both DLLs are built from one
`sdclilib.c`. This is deliberate: a duplicated client library goes stale
quietly, and a 32-bit DLL that disagreed with the 64-bit one about the protocol
would be worse than none. Only what is specific to this build lives here - the
export aliases, the `QMConnectLocal` stub, the alias test, and the two build
scripts.

**It pointed at `../winsdclilib` until 19 Aug 2026, and the change was made
because the risk above stopped being hypothetical.** That project had not moved
since 15 Aug while the SD for Windows tree added `SDConnectLocal`, the
socket-or-pipe transport and then SCRAM-SHA-256 — so this build was quietly
producing a `qmclilib.dll` that still sent the password in clear, and nothing
here would have said so. `winsdclilib` now carries the same source, but it is a
mirror; the source is developed in the SD for Windows tree, and building from
it directly removes the hop that could lag.

To build against a different tree, set `SRCDIR` (make) or edit it in
`build.cmd`.

## License

Licensed under the GNU Lesser General Public License, version 3 or later
(LGPL-3.0-or-later), with the same linking exception as the 64-bit project.
See [LICENSE](../winsdclilib/LICENSE) and [GPLv3.txt](../winsdclilib/GPLv3.txt).
