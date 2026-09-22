Title: SD Terminal Information (Terminfo)
Subtitle: The terminfo database, the 63 definitions that ship, and the compiler that ships with them.

SD uses a terminfo database to know what byte sequences a terminal sends for
each key, and what sequences to emit for screen control — cursor movement,
clear, colour, bold, underline.

Most installations never touch it. The 63 shipped definitions cover the
terminals in ordinary use, and `windows` works with any Windows console, cmd,
PowerShell or Windows Terminal session.

## The default terminal

```
term
```

```
Page width: 120
Page depth: 36
Device    : windows
```

The default terminal type is `windows`. This is an exact copy of the
`linux` definition, which had the right byte sequences for Windows
consoles, cmd, PowerShell and Windows Terminal.

> Existing accounts keep their old setting until their VOC is updated.
> Until then, `term windows` sets it for the session.

## What ships

**63 terminfo definitions ship with SD**, compiling to **100 terminal
names** — the extra names are variants. For example, `vt100-w` and
`vt220-at` are aliases that map to the same definition as their base
name.

Common names that work out of the box: `windows`, `linux`, `vt100`,
`vt220`, `wyse60`, `ansi`, `xterm`.

A name that is not installed is refused and your current type is kept:

```
:term vt320
Unrecognised terminal name
```

There is no plain `vt320` — the shipped name is `vt320-at`.

## Setting the terminal

```
term                    * report current type and page size
term windows            * set for this session
term 120,36             * set page size
term default            * restore 120 x 36 (prints nothing; check with bare term)
```

The page size is worked out at login in this order:

1. the `LINES` and `COLUMNS` environment variables if they are numeric
2. the terminfo entry's `lines` and `cols`
3. otherwise 36 and 120

A console or ssh session normally gets its real window size. 120 × 36
is the fallback when nothing answers — a phantom or a piped script.

## The page is 120 × 36

SD's default is **120 columns by 36 lines**, not 80 × 24. The shipped
dictionary records and the default `list` report layouts are formatted
for 120 columns. A console window narrower than that makes ordinary
reports look wrapped or truncated — which reads as a formatting bug and
is not one.

## The terminfo source

`terminfo.src` ships with SD. It is a text file containing all 63
definitions in source form. You can read it to see what a terminal
definition looks like, and you can use it as a template for a custom
definition.

## Compiling a definition

**The terminfo compiler ships with SD.** `sdtic.exe` is in
`C:\Program Files\SD\usr\bin`, beside `sd.exe`. Nothing needs building and
nothing needs downloading.

```
sdtic {options} src...
```

| | |
|---|---|
| `-d` | decompile a named terminal entry instead of compiling |
| `-i` | display an index of terminal names |
| `-p`*path* | use the terminfo library at *path* |
| `-t`*name* | compile only *name*; may be repeated |
| `-v` | verbose |
| `-x` | do not overwrite entries that already exist |

Without `-d` it compiles the source files you name. With `-d`, the argument is a
terminal name to decompile rather than a file.

Two things follow from `-d` that are worth knowing. It is how you read a shipped
definition without hunting through `terminfo.src`, and it is how you produce a
starting point for a variant of one:

```
sdtic -d vt220 > myterm.src
```

Edit that, then compile it back in. `-x` is the safe form while you are
experimenting, because it refuses to overwrite a definition that already
exists.

The compiled definitions live under `C:\ProgramData\SD\sdsys\terminfo`, in
single-letter directories by first letter. Writing there needs administrator
rights, so run `sdtic` from an elevated prompt when you are adding a definition
for the machine.
