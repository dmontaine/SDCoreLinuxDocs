Title: System limits
Subtitle: The sizes, counts and depths compiled into SD Core for Windows, and which of them a site can change.

Two kinds of number appear on this page and they behave differently.

A **compiled limit** is fixed in the build. Changing it means rebuilding SD, and
several would change on-disk file formats, so in practice they are ceilings.

A **configured limit** is a value in `sd.conf` with a default. A site can raise
or lower it, within a range the compiled limits set. Those are covered in full
under *Configuration* in this set; this page gives the number in force and says
which parameter controls it.

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

> Every figure here was read from the sources that define it, or from a running
> W1.0-0 system, and not from documentation of another product.

## Data

| | | |
|---|---|---|
| Maximum string or record size | **1,073,741,822** bytes | compiled |
| Maximum record id length | **63** by default, up to **255** | `MAXIDLEN` |
| Fields per record | limited only by record size | — |
| Values per field, subvalues per value | limited only by record size | — |

The record size limit is just under 1 GB rather than 2 GB. It is the maximum
size of any single string SD will build, so it applies to a record, to a
concatenation, and to anything a program assembles in memory.

**A record id may be longer than 63 characters only if `MAXIDLEN` is raised**,
and the range starts at 63 rather than 0 — a lower value is refused at start-up
rather than accepted. The ceiling of 255 is compiled, and the comment in the
source notes that raising it would require major file-format changes.

## Files

| | | |
|---|---|---|
| File types | **two** — directory and dynamic | compiled |
| Group size for a dynamic file | **2 KB** by default, maximum **8** | `GRPSIZE` |
| Open files across all sessions | **80** | `NUMFILES` |
| Maximum pathname length | **255** | compiled |
| Sort keys in one query | **32** | compiled |

Group size is expressed in 1 KB units, so the compiled maximum of 8 is 8 KB.

## Sessions and locks

| | | |
|---|---|---|
| Concurrent sessions | **20** | `NUMUSERS` |
| Record locks across all sessions | **100** | `NUMLOCKS` |
| File locks | one per file | compiled |
| Windows account name | **32** characters | compiled |
| SD account name | **32** characters | compiled |

`NUMUSERS` sizes the user table in shared memory, so it is read once when SD
starts and cannot be changed in a running system.

## Programs

| | | |
|---|---|---|
| Subroutine call depth | **10,000** | `MAXCALL`, range 10 to 1,000,000 |
| Catalogued name length | **63** characters | compiled |
| Matrix dimensions | **two** | compiled |
| Compiled programs held in memory | no limit by default | `OBJECTS` |
| Memory those programs may occupy | no limit by default | `OBJMEM`, in KB |

## Select lists

| | | |
|---|---|---|
| Numbered select lists | **13**, numbered 0 to 12 | compiled |
| Items in a select list | limited by disk | — |

Thirteen is the number a session has available at once, not a limit on how many
lists can be saved. `save.list` writes to a file and is limited only by space.

## Terminals

| | | |
|---|---|---|
| Terminal definitions shipped | **63** source definitions | — |
| Terminal names they compile to | **100** | — |
| Default page size | **120 × 36** | — |
| Minimum page size | 10 lines × 20 columns | compiled |
| Default printer page | **80 × 66** | `LPTRWIDE`, `LPTRHIGH` |

The extra terminal names are aliases and variants that share a definition with
their base name.

## What an account gets

**There is no longer a tier to give three different answers for.** Every
ordinary account gets the whole of `newvoc`; SDSYS gets that plus the
records that exist only in `voc_template`.

| | VOC records |
|---|---|
| An ordinary account (`newvoc`) | **398** |
| SDSYS (`voc_template`) | **431** |

**These are record counts, not verb counts** — a VOC record may be a verb, a
keyword, a file pointer, a sentence or a paragraph, and only some are verbs.
Counted directly from the shipped directories (`newvoc`/`voc_template`),
matching what `count voc` reports in a freshly created account.

## Configuration

| | |
|---|---|
| Parameters accepted in `sd.conf` | **52** |
| Parameters the `config` verb displays | **43** |
| Parameters readable with `config()` | **49** |
| Parameters settable for the current session | **28** |
| Parameters accepted that do nothing | **6** |

The six inert parameters, and why each is inert, are listed under
*Configuration* in this set. `NETFILES` and `CREATUSR` are the two a site is
most likely to have in an existing `sd.conf`.
