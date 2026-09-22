Title: SD Glossary
Subtitle: Terms used in SD Core documentation, from account to VOC.

This glossary defines the terms used throughout the SD Core for Windows
documentation set. Terms are listed in alphabetical order.

## A

**Account** — a workspace: a directory containing one or more files, a
VOC, and its own `bp` source file. An account maps to a Windows group
(`sdu_<name>` for user accounts, `sdg_<name>` for group accounts).
Entry to an account is membership of its Windows group.

**Administrator** — the highest account tier. An administrator account
is a member of the Windows `Administrators` group and receives the
full VOC: 416 records. Administration is gated on elevation, not on a
password.

**Alternate key index** — a secondary access path to records in a file,
built from the values in a nominated field. Created with
`create.index`, built with `build.index`.

**Association** — a group of dictionary fields that share multivalues.
When fields are associated, a value mark in one corresponds to a value
mark in all of them at the same position.

**Attribute** — a field in a dictionary record that defines one column
of a query report. Dictionary field 1 is the name, field 2 is the
type, field 3 is the conversion, field 4 is the correlative, field 5
is the format, field 6 is the header, field 7 is the association.

## B

**Background process** — a process started with `phantom` that runs
without a terminal. The process that starts it does not wait for it.

**Break key** — the interrupt key (Ctrl+C on Windows). Stops a running
program or query and enters the debugger if one is active.

**BASIC** — the programming language. See SDBasic.

**bp** — the source file. An account's `bp` file is a directory file —
an ordinary Windows folder with one file per program. `gpl.bp` is the
shipped source for the system programs.

## C

**Catalogue** — the registry of compiled programs. A catalogued program
can be run by name from any account that can reach it. Private
catalogue is per-account; local catalogue puts the VOC entry in the
account's own VOC; global catalogue is system-wide and requires an
administrator.

**Common block** — a named memory area shared between subroutines.
Declared with `common` or `common /name/`. Used for passing data
without arguments.

**Conversion code** — a dictionary field 3 entry that transforms data
on input (`iconv`) or output (`oconv`). Examples: `D` for dates, `MR`
for masked decimal, `MC` for case conversion.

**Correlative** — a dictionary field 4 entry that defines
pre-processing of a field value before the conversion is applied.
Examples: `A` (arithmetic), `F` (function), `I` (index).

## D

**Dictionary** — a file that defines the fields of a data file for the
query processor. Each record in a dictionary file describes one field.
The dictionary file is named `<filename>.dict` and lives beside the
data file.

**Directory file** — a file type where each record is a file on disk,
stored in an ordinary Windows folder. Record ids are file names. The
`bp` file is a directory file.

**Dynamic array** — a string containing field marks, value marks and
subvalue marks. SDBasic's primary data structure for record
manipulation. Functions: `extract`, `ins`, `del`, `replace`,
`dcount`, `locate`.

**Dynamic file** — a file type stored in SD's own binary format, with a
hash-based group structure and automatic resizing. Not readable by
ordinary Windows programs.

## F

**Field mark** — the delimiter (char 254) that separates fields in a
dynamic array.

**File** — a collection of records, each identified by a record id. A
file has a data portion and a dictionary portion. The two file types
are directory files and dynamic files.

**Format** — dictionary field 5. Controls how a value is displayed:
width, alignment, masking. The format specification syntax supports
date masks, numeric masks, and text formatting.

**F-pointer** — a VOC entry of type `F` that points to another file,
possibly in another account. A remote file pointer.

## G

**Group** — (1) a Windows group used for account membership. (2) In a
dynamic file, the bucket that holds records hashed to the same slot.

**Group account** — a shared workspace with no Windows account and no
sign-in of its own. Created with `create.account group`. Reached with
`logto` or through an F-pointer.

## I

**I-type** — a dictionary field type whose value is computed by an
SDBasic expression rather than stored in the record. The expression
is compiled and stored in field 2 of the dictionary record.

**Index** — see Alternate key index.

## L

**List** — see Select list.

**Lock** — a claim on a record or file that prevents other sessions
from updating it simultaneously. Update locks (`readu`, `writeu`,
`deleteu`) are exclusive; shared locks (`readl`) are not. Task locks
are per-session and never block the same session.

## M

**Mark mapping** — the translation of dynamic array marks to and from
the separators used by sequential file I/O. Controlled per file with
`SDMarkMapping` in the API, or by the `setmark` and `setemark`
statements in SDBasic.

**Matrix** — a two-dimensional array in SDBasic. Declared with
`dimension` or `dim`. Indexed from 1.

**Multivalue** — a value within a field, separated by a value mark
(char 253). A field can hold any number of multivalues; each multivalue
can hold any number of subvalues.

## O

**Overflow** — in a dynamic file, the condition where a group has more
data than fits in its primary bucket and additional buckets are
chained to it. Excessive overflow degrades performance and is reported
by `analyse.file`.

## P

**p-code** — the compiled bytecode that SD executes. Stored in the
pcode library in `<sysdir>\bin` and loaded into shared memory at
start-up.

**Paragraph** — a VOC entry of type `PA` that holds a sequence of
TCL commands. Replaces the removed PROC language.

**Phantom** — see Background process.

**Programmer** — the middle account tier. Gets 82 + 42 = 124 verbs:
everything a standard account has, plus the development set (compile,
catalogue, edit, file creation, index management, bulk record editing,
process introspection).

## Q

**QMSYS** — what the system account is called in OpenQM. In SD it is
`SDSYS`, and `sdsys` on disk. Nothing in SD Core answers to the name
QMSYS; it is here so that a reader coming from OpenQM finds the entry.

**Query processor** — the reporting language: `list`, `select`,
`count`, `sort`, `sum`, and the rest. Reads dictionary definitions to
format output. Invoked from TCL or from SDBasic with `select`,
`readnext`, `getlist`.

## R

**Record** — a single entry in a file, identified by a record id. A
record is a dynamic array: a string of fields, values and subvalues.

**Record id** — the unique key of a record within a file. In a
directory file, the record id is the file name.

## S

**SDBasic** — the programming language of SD. A compiled BASIC with
dynamic arrays, multivalue string functions, file I/O, select lists,
sockets, sequential files, CSV handling, and transaction support.

**Select list** — an ordered list of record ids, built by `select`,
`sselect`, `getlist`, or the API's `SDSelect`. Read with `readnext`
or `SDReadNext`. Stored in the `$savedlists` file.

**Sentence** — a VOC entry of type `S` that holds a single TCL command
with substitution parameters.

**Session** — one connection to SD, from sign-in to `off`. Each
session runs as the invoking user's Windows identity.

**Standard** — the lowest account tier. Gets 82 verbs: enough to run
an application and nothing that edits code or data in bulk. The default
when no tier keyword is given on `create.account`.

**Subvalue mark** — the delimiter (char 252) that separates subvalues
within a multivalue.

**Suspended** — a fourth account tier that denies all entry. Reversible
with `modify.account <tier>`. Does not touch the VOC or Windows group
membership.

## T

**TCL** — the command processor. Reads what you type at the `:`
prompt and dispatches it.

**Terminfo** — the terminal capability database. Defines what
sequences a terminal sends for keys and what sequences to use for
screen control. SD ships 63 definitions compiling to 100 terminal
names. The terminfo compiler (`sdtic`) is not shipped with SD Core.

**Transaction** — a group of file updates that succeed or fail together.
Declared with `start transaction` and committed with `commit` or
rolled back with `rollback`.

## V

**Value mark** — the delimiter (char 253) that separates multivalues
within a field.

**VOC** — the Vocabulary file. Maps command names to the programs
behind them. Each account has its own VOC. VOC entries are of types
`V` (verb), `F` (file pointer), `PA` (paragraph), `S` (sentence),
`K` (key), and `W` (external command).

## W

**Windows service** — how SD runs on Windows. The service **String
Database (SD)** is created by the installer, starts automatically at
boot, and is removed by the uninstaller. Stopping it ends every
session on the machine.
