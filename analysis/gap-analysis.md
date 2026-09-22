Title: SD Core Documentation - Gap Analysis
Subtitle: A comparison of upstream OpenQM and SD documentation against the current SD Core for Windows docs, identifying gaps and recommending how to fill them.

This report compares the upstream OpenQM 2.6.6 documentation (PDF
reference, tutorial, conversion manual, and index), the SD Linux Help
documents (ODT source and SD Manual), and the SD API Headers against the
current SD Core for Windows documentation set (01-34, 94-95).

The goal is to identify what the SD Core docs do not cover and to
recommend how those gaps should be filled.

Features confirmed as shipped in SD Core for Windows are included.
Features that have been removed from the Windows port are excluded.

## Features excluded from this analysis

The following upstream features were investigated in the source tree
and confirmed as **not shipping** in SD Core for Windows. They are
excluded from all proposals below.

| Feature | Status | Evidence |
|---|---|---|
| QMNet / remote files | Removed | `netfiles.c` deleted; `server;file` VOC handling removed from `op_dio1.c`; `NETFILES` config parameter parsed but inert |
| Embedded Python | Removed | `sdext_py.c`, `op_sdpyobj.c` deleted; `OP_SDPYOBJ` opcode retired to `op_illegal`; Makefile drops PY_HDRS and PY_LDFLAGS |
| `sdlnxd` background daemon | Linux-only | The monitoring daemon has no Windows equivalent |
| `ENCRYPT.FIELD` verb | Removed | VOC entry pointed at `$CRYPTO` which never existed in the GPL release |

## What the SD Core docs currently cover

The current set is 34 documents plus two syntax references:

| Range | Category | Coverage |
|---|---|---|
| 01-18 | SDBasic | Program structure, control flow, math, strings, dynamic arrays, data conversion, file handling, select lists, indexes, sequential files, CSV, terminal I/O, printing, locks/transactions, sockets, system/environment, debugging, modern program structure |
| 19-31 | TCL | Command processor, files/records, query processor, select lists, indexes, programs/catalogue, ED, EDIT, MICRO, printing/spooling, terminal/session, processes/phantoms, locks |
| 32 | VOC | Structure and usage |
| 33-34 | Dictionaries | Record structure, conversions and formatting |
| 94-95 | Syntax | BASIC syntax, TCL syntax |

This is strong coverage of the programming language and the TCL command
layer. The gaps are below.

## Gap 1: No getting started / introduction

**What is missing.** The upstream docs have a tutorial that introduces
the multivalue concept, explains what SD is, walks through first steps
(creating a file, entering data, listing it), and gives an overview of
the system architecture. Our docs jump straight into SDBasic program
structure with no orientation.

**What upstream covers that we don't:**
- What is a multivalue database? (the order-processing example, the
  history from Dick Pick through to SD)
- What SD is — a fork of ScarletDME/OpenQM, GPL v3, community-supported
- The four components: command processor, query processor, SDBasic,
  SDClient API
- First steps: logging in, creating a file, entering a record, listing
  it, editing a program
- Document conventions (bold = literal, italics = variable, etc.)

**Recommendation.** One new document:

> **`00-sd-introduction.md`** — *SD Core - Introduction and Getting
> Started*

Covers: what a multivalue database is, what SD is and its lineage, the
four components, logging in for the first time, creating a file, adding
a record, listing it, writing and cataloguing a one-line program,
document conventions. Numbered 00 so it sits before the BASIC sequence.

## Gap 2: No system administration documentation

**What is missing.** The upstream docs have an entire system
administration section covering configuration, accounts, users,
security, process management, and file system monitoring. Our docs have
nothing on administration — no `CONFIG`, no `CREATE.ACCOUNT`, no
`CREATE.USER`, no `LISTU`, no `PSTAT`, no `LIST.FILES`, no `ANALYSE.FILE`,
no `FSTAT`, no `LIST.LOCKS`.

**What upstream covers that we don't:**
- Configuration parameters (`CONFIG` command, the configuration file,
  all ~30 parameters: CMDSTACK, DEADLOCK, ERRLOG, FSYNC, GRPSIZE,
  MAXIDLEN, MUSTLOCK, NUMFILES, NUMLOCKS, OBJECTS, OBJMEM, PDUMP,
  PRECISION, PTYPES, etc.)
- Account management (`CREATE.ACCOUNT`, `DELETE.ACCOUNT`, the QMSYS
  account, how accounts map to directories)
- User management (`CREATE.USER`, `DELETE.USER`, `LIST.USERS`,
  `ADMIN.USER`, passwords)
- Security (`SECURITY` command, privileged vs. non-privileged users)
- Process management (`LISTU`, `PSTAT`, `LOGOUT`)
- File system monitoring (`LIST.FILES`, `LIST.LOCKS`, `LIST.READU`,
  `UNLOCK`, `FSTAT`, `ANALYSE.FILE`)

**Note.** The `NETFILES` and `FILERULE` configuration parameters are
inert in the Windows port (QMNet was removed) and should be listed but
marked as non-functional.

**Recommendation.** Two new documents:

> **`35-sd-admin-configuration.md`** — *SD Administration -
> Configuration*
>
> Covers: the `CONFIG` command, the configuration file, every
> configuration parameter that is active in the Windows port (grouped:
> system limits, file system, locking, printing, diagnostics), global
> vs. private parameters, licence management (`UPDATE.LICENCE`).
> Parameters that are inert due to removed features (NETFILES, FILERULE)
> are listed but marked as non-functional.

> **`36-sd-admin-accounts-and-security.md`** — *SD Administration -
> Accounts, Users and Security*
>
> Covers: accounts and how they map to directories, `CREATE.ACCOUNT`,
> `DELETE.ACCOUNT`, the QMSYS account, user management (`CREATE.USER`,
> `DELETE.USER`, `LIST.USERS`, `ADMIN.USER`), passwords, the `SECURITY`
> command, privileged users, process management (`LISTU`, `PSTAT`,
> `LOGOUT`), file system monitoring (`LIST.FILES`, `LIST.LOCKS`,
> `LIST.READU`, `UNLOCK`, `FSTAT`, `ANALYSE.FILE`).

## Gap 3: No installation, startup, or shutdown documentation

**What is missing.** The upstream docs cover installation, startup and
shutdown of the server, and deinstallation. Our docs don't cover
installation or the service lifecycle.

**What upstream covers that we don't:**
- Installation (directory structure, licence entry, initial setup)
- Startup and shutdown of the SD server
- Deinstallation

**Note.** The upstream docs reference the `sd -start` / `sd -stop` /
`sd -restart` command-line invocations and the `sdlnxd` background
daemon. The daemon is Linux-only and does not ship on Windows. Startup
and shutdown on Windows uses the service or the `sd` command with
start/stop flags.

**Recommendation.** One new document:

> **`37-sd-installation.md`** — *SD Core for Windows - Installation and
> Setup*
>
> Covers: system requirements, installation procedure, directory
> structure, starting and stopping the server, licence entry, initial
> account creation, verifying the installation.

## Gap 4: No SDClient API documentation

**What is missing.** The upstream docs have a QMClient API section
covering the C client library, and the SD API Headers file documents
~45 functions across four language bindings (Gambas3, PureBasic,
Free Pascal, Python ctypes). The `sdclilib` shared library ships in the
Windows port. Our docs have nothing on the client API.

**What upstream covers that we don't:**
- The SDClient API concept (external applications connecting to SD)
- Connection management (`SDConnect`, `SDConnectLocal`,
  `SDDisconnect`, `SDDisconnectAll`, `SDConnected`)
- File operations (`SDOpen`, `SDRead`, `SDReadu`, `SDWrite`,
  `SDWriteu`, `SDDelete`, `SDDeleteu`, `SDClose`, `SDMarkMapping`)
- Record manipulation (`SDExtract`, `SDIns`, `SDDel`, `SDLocate`)
- String functions (`SDField`, `SDDcount`, `SDChange`, `SDMatch`,
  `SDSubstr`)
- Command execution (`SDExecute`, `SDEndCommand`, `SDCall`/`SDCallx`
  with 0-20 argument variants)
- Select lists (`SDSelect`, `SDSelectv`, `SDClearSelect`,
  `SDReadNext`, `SDRelease`)
- Session management (`SDGetSession`, `SDLogto`, `SDGetArg`,
  `SDEnterPackage`, `SDExitPackage`)
- Error handling (`SDError`, `SDDebug`)
- Server status codes (SV_OK, SV_ON_ERROR, SV_ELSE, SV_ERROR,
  SV_LOCKED, SV_PROMPT)

**Note.** `SDConnectUDS` (Unix Domain Socket) is in the header but is
not applicable on Windows. The Windows port supports local and TCP
connections only. Language bindings should reference the shared library
as `sdclilib` (the Windows build produces a `.dll`).

**Recommendation.** One new document:

> **`38-sd-client-api.md`** — *SD Client API*
>
> Covers: the sdclilib shared library, connection management (local and
> TCP only; no UDS), file operations, record manipulation, string
> functions, command execution and subroutine calls, select lists,
> session management, error handling, the six server status codes,
> language bindings (Python ctypes, Free Pascal, Gambas, PureBasic).

## Gap 5: No encryption documentation

**What is missing.** SD Core for Windows ships with libsodium-based
encryption (`sd_encrypt_sodium.c` compiles and links). The upstream SD
docs have an encryption document. Our docs don't cover it.

**What upstream covers that we don't:**
- The `SDENCRYPT` and `SDDECRYPT` SDBasic functions
- The encryption library (libsodium)
- Key management (`SD_SALT`, `SD_KEYFROMPW` keys)
- Field-level encryption from SDBasic
- SCRAM-SHA-256 authentication primitives (SHA-256, HMAC-SHA256,
  PBKDF2, random bytes, XOR, constant-time compare)

**Note.** The `ENCRYPT.FIELD` VOC verb is removed and should not be
documented. The underlying `SDENCRYPT`/`SDDECRYPT` BASIC functions and
the C-level `sd_encrypt()`/`sd_decrypt()` functions are present.

**Recommendation.** One new document:

> **`39-sd-encryption.md`** — *SD Encryption*
>
> Covers: the `SDENCRYPT` and `SDDECRYPT` SDBasic functions, the
> libsodium crypto library, key management (`SD_SALT`,
> `SD_KEYFROMPW`), field-level encryption from SDBasic, the
> SCRAM-SHA-256 authentication primitives.

## Gap 6: No SDEXT extension documentation

**What is missing.** The upstream SD docs have an SDEXT extension
document. The `op_sdext.c` source file ships in the Windows port and
handles encryption keys. Our docs don't cover the SDEXT extension.

**What upstream covers that we don't:**
- The SDEXT extension and what it provides
- How to enable and use SDEXT
- Which keys and functions are available through SDEXT

**Note.** The Python portion of SDEXT has been removed. The remaining
SDEXT functionality (encryption keys, hex/base64 encoding) is present.
The proposal should cover only what ships.

**Recommendation.** One new document:

> **`40-sd-sdext.md`** — *SD SDEXT Extension*
>
> Covers: what SDEXT is, the keys and functions it provides (encryption,
> hex encoding, base64 encoding), how to enable it. Does not cover
> removed Python SDEXT functionality.

## Gap 7: No terminal information (terminfo) documentation

**What is missing.** The upstream docs cover the terminfo database and
the `sdtic` terminfo compiler. The `sdterminfo.c` source file ships in
the Windows port. Our docs mention terminal handling in
`29-sd-tcl-the-terminal-and-the-session.md` but don't cover terminfo.

**What upstream covers that we don't:**
- The terminfo database
- The terminfo compiler utility
- Terminal capability definitions
- How SD uses terminfo for screen control

**Recommendation.** Fold into the existing terminal document or create
a new one:

> **Expand `29-sd-tcl-the-terminal-and-the-session.md`** to cover
> terminfo, or create **`41-sd-terminfo.md`** — *SD Terminal
> Information (Terminfo)*
>
> Covers: the terminfo database, the terminfo compiler, terminal
> capability definitions, how SD uses terminfo for screen control,
> customising terminal definitions.

## Gap 8: No system limits reference

**What is missing.** The upstream docs have a system limits page
documenting maximum record sizes, maximum field numbers, maximum open
files, maximum select list items, etc. Our docs don't have a
consolidated limits reference.

**Recommendation.** One new document:

> **`42-sd-system-limits.md`** — *SD System Limits*
>
> Covers: maximum record size, maximum field count, maximum field
> length, maximum open files, maximum locks, maximum select list
> size, maximum program size, maximum subroutine call depth, maximum
> matrix dimensions, etc.

## Gap 9: No glossary

**What is missing.** The upstream docs have a glossary of terms. Our
docs explain terms inline but have no consolidated glossary.

**Recommendation.** One new document:

> **`43-sd-glossary.md`** — *SD Glossary*
>
> Covers: account, association, attribute, background, break key,
> catalogue, command stack, common block, conversion code, correlative,
> dictionary, dynamic array, dynamic file, field, file, group, index,
> I-type, mark character, matrix, multivalue, overflow, paragraph,
> phantom, p-code, QMSYS, record, select list, subvalue, terminfo,
> transaction, VOC, etc.

## Gap 10: No format specification reference for dictionaries

**What is missing.** The `34-sd-dicts-conversions.md` document covers
format specifications, but the upstream docs have a dedicated format
specification page (`fmt_spec.htm`) with more detail than our doc
provides — particularly the full mask syntax, date format strings, and
the interaction between format and conversion.

**Recommendation.** Expand the existing document rather than create a
new one:

> **Expand `34-sd-dicts-conversions.md`** to cover the full format
> specification syntax in more detail, including the mask syntax,
> date format string elements (D, DD, M, MM, MA, ML, Y, YY, J, Q, W,
> WL, N), and the interaction between field 3 (conversion) and field
> 5 (format).

## Gap 11: No standard subroutines reference

**What is missing.** The upstream docs have a "Standard Subroutines"
page documenting the catalogued subroutines that ship with the system —
things like `!PARSER`, `!FTYPE`, `!PCL`, `!SCREEN`, etc. Our docs mention
some of these in passing (e.g. `!FTYPE` in the dictionary docs) but
don't have a consolidated reference.

**Recommendation.** One new document:

> **`44-sd-standard-subroutines.md`** — *SD Standard Subroutines*
>
> Covers: the `!`-prefixed internal subroutines (`!PARSER`, `!FTYPE`,
> `!PCL`, `!SCREEN`, `!OCONV`, `!ICONV`, `!SORT`, `!USERNAME`,
> `!ERRTEXT`, etc.), what each does, and how to call them from SDBasic.

## Gap 12: No MV file concepts document

**What is missing.** The upstream SD docs have an "MV File Concepts"
document that explains the multivalue file model in detail — the
difference between directory files and dynamic files, how groups work,
how overflow works, how the file system is organised on disk. Our docs
cover file handling (07) and alternate key indexes (09) but don't
explain the underlying file system structure.

**What upstream covers that we don't:**
- Directory files vs. dynamic files
- Group structure and overflow
- File system organisation on disk (the sub-file structure)
- The dynamic file resize mechanism
- How the hash algorithm works

**Recommendation.** One new document:

> **`45-sd-file-system.md`** — *SD File System Concepts*
>
> Covers: the two file types (directory and dynamic), group structure,
> overflow, on-disk layout, file resize, the hash algorithm, file
> analysis (`ANALYSE.FILE`), file statistics (`FSTAT`).

## Gap 13: Incomplete TCL command coverage

**What is missing.** The upstream docs cover many TCL commands our docs
don't. Some are administrative (covered in Gap 2 above), but some are
general-purpose:

| Command | What it does | Where it should go |
|---|---|---|
| `COMPILE` | compile a program | expand 24 |
| `BASIC` | compile BASIC | expand 24 |
| `COPY` | copy records | new or expand 20 |
| `DELETE` | delete records | new or expand 20 |
| `COUNT` | count records | expand 21 |
| `SEARCH` | search records | new |
| `LIST.ITEM` | list raw records | expand 21 |
| `SORT.ITEM` | sort raw records | expand 21 |
| `SUM` | sum a field | expand 21 |
| `STATS` | statistics | new |
| `REFORMAT` | reformat records | new |
| `SREFORMAT` | sorted reformat | new |
| `LIST.LABEL` | label printing | expand 28 |
| `SORT.LABEL` | sorted labels | expand 28 |
| `SHOW` | show a file | new |
| `WHERE` | where is a program | new |
| `VERIFY` | verify a file | new |

**Recommendation.** Rather than create a new document for each, fold
the administrative commands into the documents proposed in Gap 2, and
expand the existing TCL docs to cover the remaining commands. The query
processor doc (21) should mention `COUNT`, `SUM`, `LIST.ITEM`,
`SORT.ITEM`, `REFORMAT`, `SREFORMAT`, `SEARCH`, `SHOW`.

## Summary: Recommended new documents

| # | Filename | Title | Priority |
|---|---|---|---|
| 00 | `00-sd-introduction.md` | SD Core - Introduction and Getting Started | High |
| 35 | `35-sd-admin-configuration.md` | SD Administration - Configuration | High |
| 36 | `36-sd-admin-accounts-and-security.md` | SD Administration - Accounts, Users and Security | High |
| 37 | `37-sd-installation.md` | SD Core for Windows - Installation and Setup | Medium |
| 38 | `38-sd-client-api.md` | SD Client API | Medium |
| 39 | `39-sd-encryption.md` | SD Encryption | Low |
| 40 | `40-sd-sdext.md` | SD SDEXT Extension | Low |
| 41 | `41-sd-terminfo.md` | SD Terminal Information (Terminfo) | Low |
| 42 | `42-sd-system-limits.md` | SD System Limits | Low |
| 43 | `43-sd-glossary.md` | SD Glossary | Low |
| 44 | `44-sd-standard-subroutines.md` | SD Standard Subroutines | Low |
| 45 | `45-sd-file-system.md` | SD File System Concepts | Medium |

**Documents to expand rather than create new:**

| Existing doc | What to add |
|---|---|
| `21-sd-tcl-query-processor.md` | `COUNT`, `SUM`, `LIST.ITEM`, `SORT.ITEM`, `REFORMAT`, `SREFORMAT`, `SEARCH`, `SHOW` |
| `24-sd-tcl-programs-and-the-catalogue.md` | `COMPILE`, `BASIC` verbs |
| `28-sd-tcl-printing-and-spooling.md` | `LIST.LABEL`, `SORT.LABEL` |
| `29-sd-tcl-the-terminal-and-the-session.md` | Terminfo overview |
| `34-sd-dicts-conversions.md` | Full format specification syntax |

## Features excluded from all proposals

The following were in the original analysis but have been removed
because SD Core for Windows does not ship them:

| Removed proposal | Reason |
|---|---|
| `39-sd-networking.md` (QMNet) | QMNet removed: `netfiles.c` deleted, `server;file` handling removed, `NETFILES` parameter inert |
| `41-sd-python.md` (Python integration) | Embedded Python removed: `sdext_py.c` deleted, `OP_SDPYOBJ` retired, Makefile drops Python headers and linker flags |
| `48-sd-connections.md` (connection types incl. UDS) | UDS is Unix-only; connection types folded into the Client API doc (local and TCP only) |
| `sdlnxd` daemon references | Linux-only background daemon, no Windows equivalent |
| `ENCRYPT.FIELD` verb | VOC entry removed, pointed at non-existent `$CRYPTO` |
| `/etc/sd.conf` path references | Linux path; Windows uses a different configuration file location |
| `sd -start` / `sd -stop` / `sd -restart` with `sudo` | Linux invocation; Windows uses the service or command without `sudo` |
| `chmod`, `chown`, `kill -9`, `/etc/group`, `/home/sd/` paths | Linux-specific commands and paths |

## What is already well covered

The current SD Core docs are strong on:
- **SDBasic language** (01-18): comprehensive coverage of statements,
  functions, and concepts
- **TCL commands** (19-31): good coverage of the core command set,
  editor, and session management
- **VOC** (32): thorough structure and usage guide
- **Dictionaries** (33-34): record types, fields, conversions, and
  formatting
- **Syntax references** (94-95): BASIC and TCL syntax

The main gaps are in **system administration**, **installation**, and
**SD-specific features** (Client API, encryption, SDEXT, terminfo) —
the things that go beyond the programming language and command layer.
