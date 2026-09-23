Title: Embedded Python
Subtitle: The CPython interpreter built into SD, the dictionary, list and string objects it exposes, and the twenty-one catalogued functions that reach it from BASIC.

SD Core for Linux embeds CPython so a BASIC program can run Python code and
exchange data with it. Twenty-one catalogued routines carry this - counted
alongside the rest of SD's global catalogue in the User set's *SD Standard
Subroutines* page, which does not repeat them; this page is where they are
documented.

## The short version

A BASIC program declares each function it uses, then calls it like any other:

```
deffun PY_CREATEDICT(dictname) calling '!PY_CREATEDICT'
status = PY_CREATEDICT('mydict')
```

All twenty-one are `$internal`-compiled and ship already catalogued, so no
account needs to compile or catalogue anything to use them - only `deffun`
and a call. Failure is always `status()`, not the returned value: several of
these functions return an empty string on both "genuinely empty" and
"failed," so `status()` is what tells them apart. **Every one of the
twenty-one refuses an empty object, dictionary, list or string name before
making the underlying call**, setting `status()` to 1 - checked directly in
`sdsys/gpl.bp/py_*`, not assumed.

**There is no permission gate on any of this.** `$internal` controls who may
*compile* a new internal-mode program (an administrator, at `$internal`'s own
check); it is not re-checked when an already-catalogued routine like
`PY_CREATEDICT` is *called*. So embedded Python runs unconditionally for any
signed-on account - the same shape S.27 left `sh` and `os.execute` in, not a
separate gate of its own. There is nothing here for an administrator to turn
on or off.

**The installer brings what this needs.** `installsdai.sh` installs
`python3-dev` (Debian/Ubuntu) or the equivalent `-devel` package on the other
three supported distributions itself, and refuses to proceed if `python3` and
`python3-config` do not already resolve. Nothing is left for an administrator
to install separately afterwards.

## Interpreter lifecycle

| Function | Returns |
|---|---|
| `PY_INITIALIZE()` | 0 if the interpreter is already running or starts cleanly. Also points Python's own `stdout`/`stderr` at CRLF line endings, to match a terminal session |
| `PY_IS_INITIALIZED()` | 1 if the interpreter is running, 0 if not |
| `PY_FINALIZE()` | Shuts the interpreter down. The source's own note on it: probably not needed, kept in case SD's shutdown path turns out to want it |
| `PY_RUNSTRING(script)` | Runs `script` as Python source in the interpreter |
| `PY_RUNFILE(path)` | Runs the Python file at `path`, checked by the same `valid_os_path()` gate other file-taking verbs use. `path` is bounded by Linux's `PATH_MAX` (4096 bytes) |

## Dictionaries

A "dictionary" here is a Python `dict`, held by name in the interpreter's own
namespace - `dictname` is a handle, not a value.

| Function | Returns |
|---|---|
| `PY_CREATEDICT(dictname)` | Creates an empty dictionary |
| `PY_CLEARDICT(dictname)` | Empties it. The name stays in the namespace |
| `PY_DICTVALSETS(dictname,key,value)` | Sets (or creates) `key` to the string `value` |
| `PY_DICTVALGETS(dictname,key)` | Returns the string value of `key` |
| `PY_DICTIDEL(dictname,key)` | Deletes `key` |
| `PY_DICTGETKEYS(dictname)` | Returns every key, tab-separated |
| `PY_DICTGETVALUES(dictname)` | Returns every value, field-mark (`@FM`) separated - not tabs, unlike the keys |

## Lists

A Python `list`, likewise held by name.

| Function | Returns |
|---|---|
| `PY_LISTCRTE(listname)` | Creates an empty list. Added 22 Sep 2026 - see below |
| `PY_LISTCLR(listname)` | Empties it |
| `PY_LISTAPPD(listname,objname)` | Appends the named Python object to the list |
| `PY_LISTGETS(listname)` | Returns every item, tab-separated |

**`PY_LISTCRTE` is the newest of the twenty-one.** The opcode
(`SD_PyListCrte`, key 2220) was reserved alongside the other three list
functions from the start, but nothing implemented or called it - a list
could be appended to and read but never made. SD Core for Windows found the
identical gap in its own verb-surface audit and fixed it the same day; this
port had not independently found it. Fixed to `PY_CREATEDICT`'s own shape:
`PyList_New()` against the interpreter's global dictionary, not a
helper-process call.

**The name differs from SD Core for Windows.** Windows calls the same
function `PY_LISTCREATE`; this is the one name out of twenty-one that does
not match between the two ports. Confirmed by direct comparison, 22 Sep
2026 - not a typo on either side, just an unreconciled choice, left as
found rather than renamed after the fact.

## Strings

A Python `str`, held by name - distinct from an ordinary BASIC string
variable.

| Function | Returns |
|---|---|
| `PY_STRSET(strname,value)` | Sets (or creates) the named Python string to `value` |
| `PY_STRGET(strname)` | Returns its value |

## Reading an object generically

These take the name of any Python object already created above - a
dictionary, a list, a string, or anything a run script left in the
namespace - rather than a type-specific handle.

| Function | Returns |
|---|---|
| `PY_OBJLEN(objname)` | Its length, as Python's own `len()` would report. Returns `SD_INT_OVERFLW` (**-10302**) if the true length does not fit a 32-bit int |
| `PY_OBJTYPE(objname)` | A numeric type code, **not a type name** - see the table below |
| `PY_GETATTR(objname)` | Its value as a string - by way of `sdext()`'s `SD_PyGetAtt`, not `SDPYOBJ` like everything else on this page. See *What calls this, underneath*, below |

`PY_OBJTYPE` returns one of six codes, checked directly against a real call
(`PY_LISTCRTE` followed by `PY_OBJTYPE` on the result returned `2`, matching
the table below, not the word "list"):

| Code | Python type |
|---|---|
| 0 | unknown - none of the five below |
| 1 | string (`str`) |
| 2 | list |
| 3 | dictionary (`dict`) |
| 4 | integer (`int`) |
| 5 | float |

## Error codes

**-12001 through -12034 are shared with SD Core for Windows** - checked
directly against its `err.h`, same numbers, same meanings, name for name:

| Code | Meaning |
|---|---|
| -12001 | interpreter not initialized |
| -12002 | `PyDict_New()` failed |
| -12003 | failed to set `__builtins__` |
| -12004 | an exception was raised running the script |
| -12005 | error reported by `PY_FINALIZE` |
| -12006 | could not open the script file |
| -12007 | key not found in the dictionary |
| -12008 | failed to convert a Python object to a string |
| -12009 | error encoding a Python string from Unicode to Latin-1 |
| -12010 | cannot import `__main__` |
| -12011 | could not get the `__main__` dictionary |
| -12012 | dictionary already exists |
| -12013 | failed to add to the namespace |
| -12014 | the named object does not exist |
| -12015 | failed to set a dictionary key/value |
| -12016 | failed to delete a dictionary key/value |
| -12017 | object is not a dictionary |
| -12018 | error encoding a string from Latin-1 to Unicode |
| -12019 | object is not a string |
| -12020 | failed to remove the object from the namespace |
| -12030 | object contains no items |
| -12031 | failed to create a Python string object |
| -12032 | failed to concatenate Python string objects |
| -12033 | failed to access a list item |
| -12034 | object is not a list |

The gap between -12020 and -12030 is not a reservation for anything
documented here - it is simply where the two error blocks were written, ten
codes apart, on both ports.

**-12035 and up are this port's own, not shared.** SD Core for Windows
defines no equivalent of -12035/-12036 at all, checked against its
`sdpy.c`: its list-append and list-clear paths reuse codes from the shared
range instead of minting their own - a wrong type reports -12034
(`NotList`) on both, but Windows reports a missing append target as -12014
(`ObjNOF`) and the append or clear call itself failing as -12033
(`LstItem`) or -12004 (`Excpt`), where this port reports -12035/-12036
directly. Its list-create function reuses -12012 (`DictExsts`) for a name
collision, rather than a dedicated "list already exists" code the way this
port's -12038 (`LstExsts`) does. Neither choice is wrong; they are simply
different, confirmed by both sides checking their own source rather than
assuming. Conversely, this port has no equivalent of Windows's
-12040/-12041/-12042, because those describe a *helper process* failing to
start or an *OS permission* being unclear or refused - neither applies here,
per *There is no permission gate on any of this*, above.

| Code | Meaning |
|---|---|
| -12035 | list append failed |
| -12036 | list clear failed |
| -12037 | `PyList_New()` failed |
| -12038 | list already exists |

**A program written against these codes and expecting to run on both ports
should treat -12001 through -12034 as portable and everything from -12035 up
as this port's own.**

## What calls this, underneath

`SDPYOBJ(arg1, arg2, objname, key)` is the entry point behind every function
on this page except five: `PY_INITIALIZE`, `PY_FINALIZE`, `PY_RUNSTRING`,
`PY_RUNFILE` and `PY_GETATTR` go through `sdext()` instead, sharing that
entry point with the cryptographic primitives in [Encryption and the SDEXT
interface](04-sd-encryption.html). Both `SDPYOBJ` and `sdext` are
internal-only C functions, reachable only from `$internal`-compiled code -
see that page for what `$internal` requires and what happens when an
ordinary program tries to call either directly.
