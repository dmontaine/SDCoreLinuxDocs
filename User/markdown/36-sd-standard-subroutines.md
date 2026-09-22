Title: SD Standard Subroutines
Subtitle: The 42 catalogued names beginning with !, which of them an application may use, and how each is called.

SD ships forty-two catalogued routines whose names begin with `!`. They are in
the global catalogue, so any account reaches them without cataloguing anything
of its own.

**Most exist to support SD itself and are not an interface for applications.**
They are listed in full because a name in a stack trace, a `map` listing or an
error message has to be findable, and because a handful are genuinely useful.
Which is which is said plainly below rather than left for you to discover.

> These are not a versioned interface. A routine here can change between
> releases in ways a documented function would not. If you call one, test what
> it returns rather than assuming its shape holds.

## Some are functions and some are subroutines

Get this right first, because calling one the wrong way does not produce a
helpful error.

A **subroutine** is reached with `call`, and its results come back in its
arguments:

```
call "!ERRTEXT", text, 3035
```

A **function** is declared with `deffun` and returns a value:

```
deffun ftype(path) calling "!FTYPE"
kind = ftype(@path)
```

`SUBR()` calls a subroutine from an I-type expression in a dictionary.

Nothing here is typed at the TCL prompt. These are called from SD BASIC.

## The ones an application may reasonably use

### Paths and names

| | |
|---|---|
| `!ABSPATH` | `abspath((dir), rel)` — resolve *rel* against *dir* and return an absolute path |
| `!PATHTKN` | `pathtkn((path))` — split a path into its components |
| `!FTYPE` | `ftype(path)` — what kind of file is at *path* |
| `!VALID_OS_NAME` | `valid_os_name(name)` — is *name* usable as an operating system account name |
| `!VALID_OS_PATH` | `valid_os_path(path)` — is *path* a well-formed host path |
| `!VALID_SHELL_CMD` | `valid_shell_cmd(cmd)` — is *cmd* acceptable to hand to a shell |

The three validators are the ones SD's own administrative verbs use before
handing a value to Windows. If you are building a command line or an account
name from input, call them rather than reimplementing the rules.

### Sessions and users

| | |
|---|---|
| `!USERNAME` | `username(userno)` — the name of the session with that user number |
| `!USERNO` | `userno((name))` — the user number of a named session |

### Errors, formatting and sorting

| | |
|---|---|
| `!ERRTEXT` | `call "!ERRTEXT", expansion, errno` — the message text for a status code |
| `!FORMAT` | `call "!FORMAT", in.rec, out.rec, default.file, indent.step, case.option, errors` — the source formatter behind the `format` verb |
| `!SORT` | `call "!SORT", in.list, out.list, mode` — sort a list |
| `!VOCREC` | `call "!VOCREC", rec, (id)` — build or check a VOC record |

`!ERRTEXT` is the useful one. A program that traps a status code and wants to
log something a person can read should call it rather than keep its own table
of numbers.

### Selection lists on screen

| | |
|---|---|
| `!PICK` | `call "!PICK", item, top.line, item.list, title, pick.pos` — a scrolling chooser |
| `!PICKLST` | `call "!PICK.LIST", value, …` — the list variant |

Both need a real terminal. Neither does anything useful in a phantom, a
scheduled job or an API session.

### Printing and program information

| | |
|---|---|
| `!PCL` | `pcl(key, arg1 … arg6)` — printer control sequences, variable arguments |
| `!PROG_INFO` | `call "!PROG_INFO", obj_dir_path, obj_name, prog_name, prog_obj_sz, prog_comp_time, prog_comp_date, error_msg` |

### The command parser

| | |
|---|---|
| `!PARSER` | `call "!PARSER", key, type, string, keyword, voc.rec, quote.char` — variable arguments |

`!PARSER` is the tokeniser SD's own verbs use to read their arguments, and the
keys it takes are defined in `SYSCOM/PARSER.H`. It is the most useful of the
internal routines and the one most likely to change.

## The internal ones

These exist for SD's own use. They are catalogued because SD's programs are
ordinary compiled programs and reach them the same way anything else does.

**Calling them from an application is not supported.** Several refuse a session
that is not elevated or not administrative, and some change the state of the
machine.

| | |
|---|---|
| `!ATVAR` `!SETVAR` | read and set the `@` variables |
| `!GETPU` `!SETPU` | read and set per-user values |
| `!CREATE_USER` `!DELETE_USER` `!SET_PASSWD` | the Windows account half of `create.account`, `delete.account` and `modify.password` |
| `!CRED_SET` `!CRED_VERIFY` | write and check a credential in the credential store |
| `!SD_GET_SALT` `!SD_KEY_FROM_PW` | the key derivation behind that credential |
| `!EUID_SET` `!EUID_RESTORE` | the POSIX effective identity calls |
| `!ELEVATE` | starts, uses and stops the elevated helper |
| `!PS_SCRIPT` `!PS_SCRIPT_OUT` | run a PowerShell script through that helper, without and with its output |
| `!IS_USER` `!IS_GROUP` `!IS_GRP_MEMBER` `!IS_SD_USER` `!OS_GROUP` | Windows account and group questions |
| `!PROFILE_DIR` | `profile_dir(username)` — where a Windows profile lives |
| `!SDCLIENT` | the server side of the client API |

## What is not here

Documentation for other MultiValue systems describes `!`-prefixed routines SD
Core for Windows does not have. Three a reader may come looking for:

| | |
|---|---|
| `!OCONV` `!ICONV` | not catalogued. `oconv()` and `iconv()` are ordinary BASIC functions and do the same work |
| `!SCREEN` | not catalogued, and there is no equivalent |

**To settle the question for any name, use `map` in the account.** It lists what
the catalogue holds. A name that is not there is not available, and calling it
fails at run time rather than at compile time.

## See also

[SD Dictionaries - Conversions and Formatting](34-sd-dicts-conversions.html) ·
[SD TCL - Programs and the Catalogue](24-sd-tcl-programs-and-the-catalogue.html) ·
[SD Basic - Program Structure](01-sd-basic-program-structure.html).
