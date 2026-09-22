# SD Core for Windows — documentation

Documentation for **SD Core for Windows W1.0-0**. The server source is in a
separate repository, `sd4windows`; nothing here is needed to build SD, and
nothing in `sd4windows` is needed to build these pages.

**This repository does not have `sd4windows`'s no-binaries rule** (owner,
26 Aug 2026). It does not track the rendered pages anyway — see *Generated*
below.

## Layout

Three document sets, each with the same three folders:

| | |
|---|---|
| `GettingStarted/` | 19 pages — installing SD Core on Windows, running it, and what differs from OpenQM and from SD on Linux. Named `Testing/` until the W1.0-0 audit, when the set stopped being for pre-release testers |
| `User/` | **two references, both complete.** `01`-`18` SD BASIC by subject, where `18` is Modern Program Structure — scope, local routines and objects. `19`-`31` SD TCL by subject; the administrator verbs are not here, they are their own set. `32`-`34` VOC and dictionaries. `35`-`40` file system, standard subroutines, client API, glossary, terminfo, and a tutorial with worked programs. **The generated syntax cards live at the end, `94` onwards**, so more can be added without renumbering anything: `94` SD BASIC (411 names), `95` SD TCL (147 verbs) |
| `Administrator/` | **fourteen documents, and a separate deliverable on purpose** — `00a` copyright and licence, `01` accounts and security, `01a` account maintenance, `02` sessions and locks, `03` operating system access, `04` encryption and the SDEXT interface, `05` remote access and the machine, `06` system limits, `07` configuration, `08` installation and the service, `09` and `09a` the 37 installed scripts, `10` restricted commands, `11` features the developers could not test. Everything in it is administrator-tier or unavailable to an application, **so an administrator can withhold the whole set.** `11` is why the other two sets carry no "this was not tested" footnotes: an application programmer needs the reference to read as settled, an administrator choosing what to put into production needs the gaps in one list |

Inside each: `markdown/` is the source, `html/` and `pdf/` are generated.

### A number with a letter after it is the second half of a long page

**No page runs longer than about 14,000 characters of Markdown**, owner's
ruling, 5 September 2026, taken together with dropping the sidebar table of
contents from the HTML. A reader on screen now moves between pages rather than
within one, so a page that scrolls for twenty screens has no navigation at all.
Fourteen were over the line and were cut in two at a section boundary.

**The first half keeps the number and the second takes a letter** — `04` and
`04a`. That is deliberate and it is the same instinct that parks the syntax
cards at `94`: every link, every map entry and every reference already written
to `04` still lands on `04`, and nothing renumbered. `01-` sorts before `01a`
and both before `02-`, so directory order is still reading order.

**The one exception is `94`**, the SD BASIC syntax card, which stays whole at
24 KB on the owner's ruling. It is a lookup table read with Ctrl-F rather than
a page read start to finish, and splitting it would mean a name is on one of
two pages with no way to tell which.

`tools/split_page.py` did the cutting. It works in binary, so a CRLF page stays
CRLF, and it **proves the two halves rebuild the original body byte for byte**
before it writes either file — the one property of a split that a diff cannot
show.

### The `00` letters are the exception: they are order, not halves

`00a-copyright-and-licence` and `00b-start-here` are not two halves of one
page. **The letter there does one job: it puts the licence page first.**
`00-` sorts before `00a-`, so a set whose introduction was called `00-` opened
with the introduction and left the licence page behind it — which is what
`GettingStarted` and `User` did until 6 Sep 2026 (PRE_RELEASE 181). The two
introductions became `00b-` so that all three sets read the way
`Administrator` already did, in the HTML and in the PDF alike, on the owner's
ruling that day.

**Neither the book nor the website is ordered by hand, and that is why the
filename had to change rather than the code.** Both take `add_nav.py:78`'s
plain `sorted()`, and special-casing one of them would put the book in a
different order from the website's prev/next chain — `mkbook.py`'s own
docstring calls that "two documents claiming to be one".

### The copyright and the licence appear once per set

**Owner's instruction, 5 September 2026, looking at a PDF**: the licence block
comes off every page and is *"available once for each set of documents"*, with
*"a tag line at the bottom of each page"* carrying the copyright and the
licence name instead.

| | |
|---|---|
| every page | the footer tag line — product, version, copyright, licence name |
| `00a-copyright-and-licence` in each set | the block in full: the metadata table, the three-paragraph summary, and the licence URL |

**The words are still generated by `mkdoc.py`, not written into three files.**
A page asks for the block with a `<!--LICENCE-BLOCK-->` marker in its Markdown
and `mkdoc.py` expands it, so there is one copy of the text however many sets
there are. **`add_nav.py` refuses a set that has anything other than exactly
one page carrying it** — that is a question about a whole set, which is the one
thing `mkdoc.py` cannot see, and a set that lost its licence page would
otherwise render clean, link clean and ship.

**And the licence page is the FIRST page of every set, which is checked as
well.** Counting it was not enough: on 6 Sep 2026 all three sets carried the
block exactly once and that check was green, while two of the three sat it
after the introduction — a PDF is read from page one, and the bound book's
front matter states no licence of its own precisely because the first document
states it in full. `add_nav.py` now refuses a set whose licence page is not
first, and `mkbook.py` refuses to write a book whose first document is not the
licence page. **Both refusals were tested against the pre-fix layout**, and
`release.ps1` reads their exit codes, so a set in the wrong order stops the
release rather than shipping.

**The `User` set is measured, not compiled from the old help tree.** Its roster
comes from `BCOMP`'s own tables, and every example was run before it was
written down. `tools\probes\` holds the programs that produced the numbers and
`tools\probes\README.md` says which runner takes which.

**Sets never link to each other, and that is enforced by convention rather than
by a tool.** Each set is handed out on its own, so a link from one to another
would be a 404 for whoever was given only the first. `Administrator/` is the
reason the rule matters: withholding it must not break the `User` set. Where a
page in another set is worth naming, **name it in words**.

`analysis/` holds working material that is not part of any set and does not
ship: the gap analysis this documentation was audited against, the W1.0-0 audit
trail, the review questions from August 2026, and the documentation salvaged
from the two retired client repositories.

## Building

```
tools\release.ps1
```

That renders whatever changed, refuses if any generated page is older than its
Markdown, zips the result and prints the SHA256. `-Set User` does another set,
`-Force` re-renders everything, `-NoZip` stops before the zip.

The two steps it drives can also be run alone:

```
python tools\mkdoc.py --in GettingStarted\markdown --out GettingStarted\html
powershell -File tools\mkpdf.ps1 -In GettingStarted\html -Out GettingStarted\pdf
```

`mkdoc.py` needs **python-markdown** (`pacman -S msys/python-markdown` on the
MSYS2 python, or `pip install markdown`). `mkpdf.ps1` needs Edge or Chrome,
which every supported Windows machine already has.

**They are two steps and the second is the one that gets forgotten.** Pages 19
to 27 of the `User` set were written, rendered to HTML and pushed with **no PDF
at all**, and nothing said so — `release.ps1` exists precisely so this cannot
happen, and running the two steps by hand skips its bookkeeping.

**The check is markdown against PDF, not HTML against PDF.** Re-rendering the
HTML touches every file's mtime, so comparing those two reports the whole set
as stale and tells you nothing. Only the source answers the question:

```sh
for m in GettingStarted/markdown/*.md; do
  p="GettingStarted/pdf/$(basename "$m" .md).pdf"
  [ -f "$p" ] || echo "MISSING $p"
  [ "$m" -nt "$p" ] && echo "STALE   $p"
done
```

Both take one file as well as a directory, so a single changed page costs one
render rather than forty-three.

## Regenerating the syntax cards

**The cards live at the end, `94` onwards, so more can be added without
renumbering anything.** Owner's ruling, 27 Aug 2026: parking them high means
that when they are eventually renumbered it is only ever the cards that move.

| | |
|---|---|
| `User/markdown/94-sd-basic-syntax.md` | SD BASIC, from `mksyntax.py` |
| `User/markdown/95-sd-tcl-syntax.md` | SD TCL, from `mktclsyntax.py` |

### The SD TCL card

```
python tools\mktclsyntax.py <sd4windows>\sdb_ai\sd64\sdsys User\markdown\95-sd-tcl-syntax.md
```

Its roster is computed from SD's own VOC — the verb records in `newvoc` plus
`TIER.ADD.ADMINISTRATOR`, **147** — and it **refuses to write the page** if a
verb has no line, or if a line names something that is not a verb. It caught
`selecte` on the first run, which is a BASIC statement.

**And it caught the second half itself, 28 Aug 2026.** The roster is computed,
so it dropped to 143 the day `encrypt.field` left `TIER.ADD.ADMINISTRATOR`; the
shapes file and `tclmap`'s map are typed, so they did not. **Both generators had
been refusing to run** — `NOT A VERB encrypt.field has a shape and is not on the
roster` — which is the refusal working as designed, and it is the reason a
computed roster is worth the trouble.

**The same mechanism went the other way and nobody ran it.** The roster grew to
147 when the four machine-control verbs were added on 30 Aug 2026, and `tclmap`
was red from that day until the W1.0-0 audit found it — because it lives in this
repository and no check in `sd4windows` runs it. The lesson is in the audit
trail under `analysis/`, and the answer was more checkers rather than more
diligence.

The syntax itself lives in `tools/tcl-syntax-shapes.txt`, **not** in the
programs' `START-DESCRIPTION` blocks. Sixty-three of the ninety-seven
catalogued verbs carry one and none is used as content: they are in a different
notation and several are stale — `LIST.READU`'s omits `DETAIL`,
`CREATE.ACCOUNT`'s predates every tier and access keyword. **They are used as a
control instead**: the script reports where a block mentions a keyword the card
does not, as a lead for a person to follow. That found six real omissions on its
first run, in `cd`, `delete.index`, `fstat`, `map`, `option` and `setptr`.

**The tier column is read from the same two lists the account-creation code
uses**, so the card cannot drift from what an account actually gets.

### The SD BASIC card

`User/markdown/94-sd-basic-syntax.md` is **generated, not edited**:

```
python tools\mksyntax.py <sd4windows>\sdb_ai\sd64\sdsys\gpl.bp\BCOMP User\markdown\94-sd-basic-syntax.md
```

Its roster is `BCOMP`'s own tables and it **refuses to write the page if any
name accepted by the compiler has no line on it** — 411 of 411. Argument counts
for functions are read out of `BCOMP`'s dispatch table, which is positional
against the name list; the script asserts the two agree before using either.
Everything a count cannot express lives in `tools/syntax-shapes.txt`, one
`NAME = syntax` per line. **Edit that file, then regenerate.**

It writes **two** pages and checks that they **partition** the roster —
every name on exactly one of them, 447 of 447:

| | |
|---|---|
| `User/markdown/94-sd-basic-syntax.md` | 372 names an application may use |
| `Administrator/markdown/10-sd-basic-restricted-commands.md` | 75 it may not — 36 restricted statements, 38 internal-only functions, and `errmsg`, which is in a table with no opcode behind it |

**The restricted card is in the `Administrator` set**, on the owner's ruling of
4 Sep 2026. It lived in a two-page `Technical` set until then, and that set is
gone: the installed-scripts page went to `Administrator` too. Both belong with
material an administrator can withhold, and a two-page set had no cross-links,
so `checklinks.py` correctly refused to certify it — PRE_RELEASE 34, closed by
removing the set rather than by weakening the check.

## Checking a set

```
python tools\docmap.py <sd4windows>\sdb_ai\sd64\sdsys\gpl.bp\BCOMP
python tools\tclmap.py <sd4windows>\sdb_ai\sd64\sdsys\newvoc
python tools\linkup.py User\markdown
python tools\checklinks.py User\markdown User\html
```

**`tclmap.py` exists because `docmap.py`'s question is not enough.** A map
says where a name is *meant* to be explained. On 27 Aug 2026 the TCL coverage
was recorded as 127 of 144 and was really 118 — seven verbs counted as covered
because their name appeared inside a warning, or inside a longer word. So
`tclmap` requires **evidence on the page**: the verb backticked, or opening a
line inside a fenced syntax block. Prose alone does not count.

| | |
|---|---|
| `docmap.py` | assigns every name `BCOMP` accepts to exactly one document and exits non-zero on a gap. **411 of 411** |
| `tclmap.py` | the same for the TCL verbs, across the `User` and `Administrator` sets — **and it also checks the page actually documents the verb**, not merely that the name occurs somewhere. **147 of 147, 0 exempt** |
| `confmap.py` | the same for the configuration parameters `config.c` accepts, and it reports which of them anything still reads. **52 of 52** |
| `verbcounts.py` | every verb count written in prose, against the counts computed from the VOC. Standard **82**, programmer **124**, administrator **147** |
| `scriptmap.py` | every PowerShell script the installer leaves on the machine, against the page that lists them. **37 of 37** |
| `linkup.py` | turns `*SD Basic - X*` into a link only for pages that exist |
| `checklinks.py` | every link in the rendered pages |

**The last three were written during the W1.0-0 audit and each one found a real
gap on its first run** — a configuration page listing 19 of 52 parameters and
one that does not exist, six pages saying a standard account has 81 verbs when
it has 82, and a page claiming 26 installed scripts when 37 ship. All three take
a roster from the product and refuse to agree with a hand-kept list.

## Measuring

These five run something inside a real SD session and refuse a run that did not
measure anything. `tools\probes\README.md` says which takes which.

**They default to a user account, not `SDSYS`, and that is not only about file
permissions.** `LOGTO SDSYS` asks UAC when the session is not already elevated,
so every run against `SDSYS` puts a consent prompt in front of whoever is at the
machine — six runs, six prompts. Measure in a user account unless `SDSYS` is
itself the subject.

| | |
|---|---|
| `sdtcl.ps1` | run **TCL commands** and print what SD said; refuses a transcript with fewer command echoes than commands sent |
| `sdprobe.ps1` | run one BASIC probe; refuses without its START and END markers |
| `sdprobe2.ps1` | **two sessions at once**, for locking; refuses unless they demonstrably contended |
| `sdcompile.ps1` | compile only, for measuring what the compiler **refuses** |
| `sddebug.ps1` | compile in debug mode and drive the debugger from a script |

## Generated, not tracked

`*.html`, `*.pdf` and `*.zip` are ignored. The deliverables — a PDF download,
and eventually the pages on a web site — are built from the Markdown at release
time, so tracking a rendered copy would only add a way for the two to disagree.
`.gitignore` carries the rest of the reasoning.

## A new clone

Set the identity per repository; this machine has no global one:

```
git config user.name dmontaine
git config user.email bigriverguy@posteo.net
```
