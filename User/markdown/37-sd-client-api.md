Title: SD Client API
Subtitle: The sdclilib client library, its functions across four language bindings, and the server status codes.

The SDClient API lets an external application connect to SD, open
files, read and write records, execute commands, call subroutines,
and manage select lists — all through a single shared library.

**The API is a normal way for any account to use SD**, not a facility reserved
for developers and administrators. A person running a custom GUI program that
talks to SD needs API access and may need nothing else.

## The library

Four DLLs are installed. They are built from one source: each pair is the same
code compiled twice under two output names, so the two files are not identical
on disk but behave identically.

| | |
|---|---|
| 64-bit | `sdclilib.dll` and `sdclient.dll` |
| 32-bit | `qmclilib.dll` and `qmclient.dll` |

The `*clilib` names are what existing applications ask for; the `*client` names
are for new work. **Renaming one to the other does not work**: an import library
records the DLL name its symbols come from, so an application built against
`sdclilib` loads `sdclilib.dll` whatever you call the file on disk. That is why
both names are built rather than one being a copy of the other.

> **The architecture must match the application, not the machine.** A 32-bit
> application on 64-bit Windows needs the 32-bit DLL. The 32-bit build is a
> shipping deliverable rather than a testing convenience.

### Where they are, and how to use them

```
C:\Program Files\SD\usr\clients\client64\     sdclilib.dll  sdclient.dll
C:\Program Files\SD\usr\clients\client32\     qmclilib.dll  qmclient.dll
```

Copy the DLL your application needs either **beside the application's own
executable** or into `C:\Windows\System32`. Those are the two supported routes
and either works.

> **`C:\Program Files\SD\usr\bin` is normally on the system PATH**, because the
> installer offers to put it there — the *"Add SD Core to the system PATH"*
> task, which is ticked unless you untick it, and it is what makes `sd` run from
> any directory. **All four client DLLs live in that directory too**, so an
> application may find one without your having copied anything. That is
> convenient, and it is not the same as choosing which copy it loads: PATH order
> decides, and a stale copy earlier on the PATH wins. **Put the DLL where your
> application will find it deliberately.**

`usr\clients` holds the DLLs **and one import library for each** — `.dll.a`
files, GNU-style, for linking rather than loading:

```
client64\     libsdclilib.dll.a  libsdclient.dll.a
client32\     libqmclilib.dll.a  libqmclient.dll.a
```

They sit beside the DLLs so that everything a client *build* needs is in one
place. **No header travels with them**: `sdclilib.h` reaches every installation
at `C:\ProgramData\SD\sdsys\syscom\sdclilib.h`.

**All four DLLs also appear in `C:\Program Files\SD\usr\bin`, beside `sd.exe`**,
and each copy is byte-identical to the one under `usr\clients`. The 32-bit pair
is there because `usr\bin` is on the PATH, and that is where a **32-bit
administrative utility** finds its client. Those copies are the server's own and
are not the ones you should be taking — with one exception, which is the next
section. **The import libraries are deliberately not in `usr\bin`**: a linker
input has no business in a directory that goes on the PATH.

## Connection

| | |
|---|---|
| `SDConnect(host, port, user, pass, account)` | over the network, to port **4243** |
| `SDConnectLocal(account)` | on the same machine. Sends no password and never did |

> `SDConnectUDS` (Unix Domain Socket) appears in the header but is not
> applicable on Windows. The Windows port supports local and TCP
> connections only.

### SDConnectLocal has a requirement the other does not

`SDConnectLocal` starts a session by running `sd.exe`, and **it looks for
`sd.exe` beside itself** — in the directory the loaded DLL came from, not on
the PATH.

So a copy of the DLL sitting next to your own application will not make a local
connection: there is no `sd.exe` there. Two ways round it:

| | |
|---|---|
| Load the copy in `usr\bin` | it is beside `sd.exe`, which is why that copy exists |
| Use `SDConnect` instead | connect to `127.0.0.1` on port 4243 like any other client |

`SDConnectLocal` sends no password at all. It takes the identity of the process
that called it and checks that account's grants, so the account has to be one
the calling Windows user may enter.

**The login is SCRAM-SHA-256.** A client that sends a password in
clear is refused. The server sets a puzzle only someone who knows the
password can answer, and the password itself is never sent in any
form. The server also proves itself to the client — another program
that grabbed the port before SD started cannot pretend to be SD.

> **Run `modify.password` again for every account that uses the API**
> after upgrading. The stored credentials changed shape and the old
> ones cannot be converted — the password was never kept anywhere, by
> design.

A session is confined to its own account. An API session can open
everything inside its own account and the shipped SDSYS files every
account needs, but cannot open, rename, delete or list anything else.

## Server status codes

| Constant | Value | Meaning |
|---|---|---|
| `SV_OK` | 0 | success |
| `SV_ON_ERROR` | 1 | an `ON ERROR` clause fired |
| `SV_ELSE` | 2 | an `ELSE` clause fired |
| `SV_ERROR` | 3 | an error occurred |
| `SV_LOCKED` | 4 | the record is locked by another session |
| `SV_PROMPT` | 5 | the command issued a prompt and is waiting for input |

## Function reference

### Connection management

| Function | Returns | Description |
|---|---|---|
| `SDConnect(host, port, user, pass, account)` | Boolean | connect over TCP |
| `SDConnectLocal(account)` | Boolean | connect on the same machine |
| `SDConnected()` | Boolean | is a session active |
| `SDDisconnect()` | none | end the current session |
| `SDDisconnectAll()` | none | end all sessions |
| `SDGetSession()` | Integer | get the current session number |
| `SDSetSession(session)` | Boolean | switch to a session |
| `SDLogto(account)` | Boolean | switch to another account |

### File operations

| Function | Returns | Description |
|---|---|---|
| `SDOpen(filename)` | Integer (file number) | open a file |
| `SDClose(fileNo)` | none | close a file |
| `SDRead(fileNo, id, err)` | String | read a record |
| `SDReadl(fileNo, id, wait, err)` | String | read with a shared lock |
| `SDReadu(fileNo, id, wait, err)` | String | read with an update lock |
| `SDWrite(fileNo, id, data)` | none | write a record |
| `SDWriteu(fileNo, id, data)` | none | write with an update lock |
| `SDDelete(fileNo, id)` | none | delete a record |
| `SDDeleteu(fileNo, id)` | none | delete with an update lock |
| `SDRecordlock(fileNo, id, updateLock, wait)` | none | set a record lock |
| `SDRelease(fileNo, id)` | none | release a record lock |
| `SDMarkMapping(fileNo, state)` | none | enable/disable mark mapping |

### Record manipulation

| Function | Returns | Description |
|---|---|---|
| `SDExtract(src, fno, vno, svno)` | String | extract a field, value or subvalue |
| `SDIns(src, fno, vno, svno, newdata)` | String | insert into a dynamic array |
| `SDDel(src, fno, vno, svno)` | String | delete from a dynamic array |
| `SDReplace(src, fno, vno, svno, newdata)` | String | replace a field, value or subvalue |
| `SDLocate(item, src, fno, vno, svno, pos, order)` | Boolean | find a position for ordered insert |

### String functions

| Function | Returns | Description |
|---|---|---|
| `SDField(str, delim, first, occurrences)` | String | extract a field from a delimited string |
| `SDDcount(src, delim)` | Long | count delimiters |
| `SDChange(str, old, new, occurrences, start)` | String | replace substrings |
| `SDMatch(src, template)` | Boolean | match a string against a pattern |
| `SDMatchfield(src, template, component)` | String | extract a matched component |
| `SDSubstr(...)` | String | substring (language-specific) |

### Command execution

| Function | Returns | Description |
|---|---|---|
| `SDExecute(cmnd, err)` | String | execute a TCL command |
| `SDRespond(response, err)` | String | respond to a prompt from `SDExecute` |
| `SDEndCommand()` | none | end a multi-line command |
| `SDCall(name, argcount, ...)` | none | call a catalogued subroutine (pass by reference) |
| `SDCallx(name, argcount, ...)` | Integer | call a catalogued subroutine (pass by value) |

> `SDCall` and `SDCallx` are variadic: 0 to 20 arguments. Each binding
> provides per-arity wrappers — `SDCall0` through `SDCall20`, and
> `SDCallx0` through `SDCallx20`.

### Select lists

| Function | Returns | Description |
|---|---|---|
| `SDSelect(fileNo, listNo)` | none | select all records in a file |
| `SDSelectIndex(fileNo, indexName, indexValue, listNo)` | none | select by index value |
| `SDSelectLeft(fileNo, indexName, listNo)` | String | select left of an index cursor |
| `SDSelectRight(fileNo, indexName, listNo)` | String | select right of an index cursor |
| `SDSetLeft(fileNo, indexName)` | none | position cursor left |
| `SDSetRight(fileNo, indexName)` | none | position cursor right |
| `SDReadNext(listNo, err)` | String | read next select list id |
| `SDReadList(listNo, err)` | String | read the whole list as a dynamic array |
| `SDClearSelect(listNo)` | none | clear a select list |
| `SDRelease(fileNo, id)` | none | release a read lock |

### Session and package management

| Function | Returns | Description |
|---|---|---|
| `SDEnterPackage(name)` | Boolean | enter a package context |
| `SDExitPackage(name)` | Boolean | exit a package context |
| `SDGetArg(argNo)` | String | get a command argument |

### Error handling

| Function | Returns | Description |
|---|---|---|
| `SDError()` | String | get the last error message |
| `SDDebug(mode)` | none | enable/disable debug mode |
| `SDStatus()` | Long | get the last server status code |
| `SDFree(ptr)` | none | free a returned pointer |

## Language bindings

The API headers define bindings for four languages. The function
signatures are identical in meaning; the syntax differs.

### Gambas3

```
Library "./sdclilib"
Extern SDConnect(Host As String, Port As Integer, UserName As String,
  Password As String, Account As String) As Boolean
Extern SDRead(FileNo As Integer, Id As String,
  ByRef Errno As Integer) As String
```

### PureBasic

```
PrototypeC.l P_SDConnect(host.p-utf8, port.l, user.p-utf8,
  pass.p-utf8, account.p-utf8)
PrototypeC.i P_SDRead(fno.l, id.p-utf8, *err)
```

Per-arity prototypes are provided for `SDCall` and `SDCallx`:
`P_SDCall0` through `P_SDCall20`, `P_SDCallx0` through `P_SDCallx20`.

### Free Pascal / Lazarus

```pascal
type
  TSDConnectFn = function(Host: PAnsiChar; Port: LongInt;
    User, Pass, Account: PAnsiChar): LongInt; cdecl;
  TSDReadFn = function(FileNo: LongInt; Id: PAnsiChar;
    Err: PLongInt): PAnsiChar; cdecl;
```

A `LoadSdCliLib` function loads the library and resolves all
function pointers; `UnloadSdCliLib` releases it.

### Python (ctypes)

```python
import ctypes
_lib = ctypes.CDLL('./sdclilib.dll')

SDConnect = _lib.SDConnect
SDConnect.argtypes = [ctypes.c_char_p, ctypes.c_int,
    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
SDConnect.restype = ctypes.c_int

SDRead = _lib.SDRead
SDRead.argtypes = [ctypes.c_int, ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_int)]
SDRead.restype = ctypes.c_char_p
```

Per-arity `CFUNCTYPE` definitions are provided for `SDCall` and
`SDCallx` wrappers.

## What the API cannot do

| | |
|---|---|
| `sh` and `OS.EXECUTE` | refused over the API |
| Open files outside the account | refused (status 3035 — *not permitted*) |
| Reach the credential file | never, and cannot be added |
| Enumerate accounts | refused; all three failure cases give the same message |
