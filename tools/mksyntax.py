#
# mksyntax.py <gpl.bp/BCOMP> <user-94.md> <administrator-10.md>
#
# Build TWO pages that partition every name BCOMP accepts:
#
#   User 94       SD Basic - Syntax, one alphabetical run of everything an
#                 application may use, syntax only.
#   Admin 10      SD Basic - Restricted Commands, the ones it may not -
#                 restricted statements, internal-only functions, and the
#                 names that are in a table with no opcode behind them.
#                 It sat in a two-page Technical set until the W1.0-0 audit,
#                 when the owner ruled that set dissolved into Administrator.
#
# The split is the owner's ruling of 26 Aug 2026.  The script checks that the
# two pages partition the roster, so a name cannot fall down the gap.
#
# WHY IT IS GENERATED.  The card's whole value is that every name is on it.  A
# hand-written list of four hundred entries is a list with omissions nobody
# notices, so the roster comes from BCOMP's own tables and this script REFUSES
# to write the page if any name lacks a line.  The same reason docmap.py
# exists, one level down: docmap says each name is described somewhere, this
# says each name is looked up here.
#
# WHERE THE SYNTAX COMES FROM, said plainly because it is not all one thing:
#
#   * ARGUMENT COUNTS FOR FUNCTIONS ARE MECHANICAL.  BCOMP dispatches each
#     intrinsic to an argument handler through an "on i goto" list that is
#     POSITIONAL against the name list, and each entry carries the name in a
#     trailing comment.  So the count can be read off, and the comment is a
#     free alignment control - this script asserts the two lists are the same
#     length and that every comment matches its name.  If BCOMP is edited and
#     the two drift apart, this stops rather than emitting a wrong card.
#
#   * EVERYTHING ELSE IS IN syntax-shapes.txt, one NAME = syntax per line.
#     Statements have clauses rather than argument lists, and functions whose
#     handler is a special case (CSVDQ, OPEN.SOCKET, SYSMSG and about twenty
#     more) have shapes the count cannot express.  Those lines were taken from
#     documents 01 to 17, where they were measured, and from BCOMP's own
#     statement compilers where no page covers them.
#
# The data file wins wherever both have an opinion, so a measured shape always
# beats a derived one.
#
import io
import os
import re
import sys

BCOMP = sys.argv[1]
OUT = sys.argv[2]          # User 94, the SD BASIC syntax card
OUT_RESTRICTED = sys.argv[3]   # Administrator 10, the restricted commands
SHAPES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      'syntax-shapes.txt')

src = io.open(BCOMP, encoding='latin-1', newline='').read()
lines = src.split('\n')
WORD = re.compile(r'"([A-Z][A-Z0-9.$]*)"')

# ---------------------------------------------------------------- the tables

def table(name):
    """The same matcher docmap.py uses, which is checked at 411 of 411."""
    got = set()
    for line in lines:
        s = line.strip()
        if s.startswith('*'):
            continue
        if re.match(re.escape(name) + r'\s*(<[^>]*>)?\s*:?=', s):
            got.update(WORD.findall(s))
    if not got:
        sys.exit('EMPTY table %s - refusing to build a card from nothing' % name)
    return got


def ordered(prefix):
    """The names of one list IN SOURCE ORDER, initialiser and appends alike."""
    out = []
    pat = re.compile(r'^' + re.escape(prefix) + r'\s*(?:<-1>)?\s*=\s*"([A-Z][A-Z0-9.$]*)"')
    for line in lines:
        s = line.strip()
        if s.startswith('*'):
            continue
        m = pat.match(s)
        if m:
            out.append(m.group(1))
    return out


def handlers(start):
    """(handler, commented name) from an 'on i goto' dispatch block."""
    out = []
    i = start
    while i < len(lines):
        s = lines[i].strip()
        m = re.match(r'(?:on i goto\s+)?(in\.[a-z0-9.]+)\s*,?\s*;\*\s*(\S+)', s)
        if m:
            out.append((m.group(1), m.group(2)))
        elif out:
            break
        i += 1
    return out


STATEMENTS = table('statements') | table('non.debug.statements')
RESTRICTED = table('restricted.statements')
RESERVED = table('reserved.names')
INTRINSICS = table('intrinsics')
EVERYTHING = STATEMENTS | RESTRICTED | RESERVED | INTRINSICS

pub = ordered('intrinsics')
starts = [n for n, ln in enumerate(lines) if 'on i goto' in ln and 'in.' in ln]
if len(starts) < 2:
    sys.exit('cannot find both intrinsic dispatch blocks - refusing')
hp = handlers(starts[1])
internal = ordered('int.intrinsics')
hi = handlers(starts[0])
if len(internal) != len(hi):
    sys.exit('int.intrinsic name list is %d and its dispatch list is %d - they '
             'are positional and have drifted apart.  Refusing.'
             % (len(internal), len(hi)))

if len(pub) != len(hp):
    sys.exit('intrinsic name list is %d and its dispatch list is %d - they are '
             'positional and have drifted apart.  Refusing.' % (len(pub), len(hp)))
# The comments are informal, so a couple are abbreviations rather than the
# name.  Listed one by one ON PURPOSE: loosening the comparison to let them
# through would throw away the only control there is on the two lists being
# in step.  A new abbreviation should stop this script and be added here after
# somebody has looked at it.
COMMENT_ALIASES = {'ARG.COUNT': 'ARGCT'}
drift = [(a, b[1]) for a, b in zip(pub, hp)
         if a.replace('.', '') != b[1].replace('.', '')
         and COMMENT_ALIASES.get(a) != b[1]]
if drift:
    sys.exit('dispatch comments do not match their names: %s' % drift[:5])

# The placeholders are italic because the page says italic means "you supply
# it".  A derived line that used plain letters would contradict its own key.
# They are generic on purpose: what the dispatch table knows is the COUNT, and
# inventing a meaningful name for each argument would be inventing.
ARITY = {
    'in.none': 0,
    'in.one': 1,
    'in.two': 2,
    'in.three': 3,
    'in.four': 4,
    'in.five': 5,
}
LETTERS = ['a', 'b', 'c', 'd', 'e']
derived = {}
for name, (hnd, _c) in list(zip(pub, hp)) + list(zip(internal, hi)):
    if hnd in ARITY:
        n = ARITY[hnd]
        if n == 0:
            # no empty inline-code span between the brackets
            derived[name] = '`%s()`' % name.lower()
        else:
            args = ', '.join('*%s*' % LETTERS[i] for i in range(n))
            derived[name] = '`%s(`%s`)`' % (name.lower(), args)

# ------------------------------------------------------------- the data file

shapes = {}
with io.open(SHAPES, encoding='utf-8', newline='') as f:
    for n, line in enumerate(f, 1):
        line = line.rstrip('\r\n')
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        if '=' not in line:
            sys.exit('%s:%d has no "=": %r' % (SHAPES, n, line))
        key, val = line.split('=', 1)
        key = key.strip().upper()
        val = val.strip()
        if key in shapes:
            sys.exit('%s:%d duplicates %s' % (SHAPES, n, key))
        shapes[key] = val
if not shapes:
    sys.exit('syntax-shapes.txt is empty - refusing')

# ------------------------------------------------------- the three exclusions

# NAMES THAT COME OFF THE USER CARD, on the owner's ruling of 26 Aug 2026.
# They are not things an application programmer can use, and a lookup card that
# lists them invites somebody to try.  They go to the Technical set instead,
# where the audience is somebody working on SD rather than with it.
#
#   RESTRICTED   the 36 in BCOMP's restricted.statements.  An ordinary account
#                compiling one gets "Unrecognised statement".
#   INTERNAL     the 38 in BCOMP's int.intrinsics.  Worse than unavailable -
#                the compiler reads an unknown function name as a MATRIX, so
#                the complaint is "Matrix X is not referenced in a DIM
#                statement" at the last line of the program.
#   NO_SUCH_THING  in a table with no opcode behind it.  It compiles for
#                nobody, restricted or not.  Enumerated by hand because the
#                only way to find one is to compile it: ERRMSG's opcode was
#                removed on 28 Jul 24 and the name was left in the table.
#                Measured - "Unrecognised statement", in an ordinary account
#                and with the DEBUGGING keyword alike.
NO_SUCH_THING = {'ERRMSG'}

INTERNAL = set(internal)
TECHNICAL = RESTRICTED | INTERNAL | NO_SUCH_THING
CARD = (EVERYTHING - TECHNICAL)
ALL_NAMES = EVERYTHING | INTERNAL

# ------------------------------------------------------------- the null case

entries = {}
for name in ALL_NAMES:
    if name in shapes:
        entries[name] = shapes[name]
    elif name in derived:
        entries[name] = derived[name]

missing = sorted(ALL_NAMES - set(entries))
bogus = sorted(set(shapes) - ALL_NAMES)

print('BCOMP accepts        : %d name(s)' % len(EVERYTHING))
print('  statements         : %d' % len(STATEMENTS))
print('  restricted         : %d' % len(RESTRICTED))
print('  reserved words     : %d' % len(RESERVED))
print('  intrinsics         : %d' % len(INTRINSICS))
print('internal-only        : %d (a separate BCOMP table)' % len(INTERNAL))
print()
print('the User card        : %d' % len(CARD))
print('the restricted page  : %d  = %d restricted + %d internal + %d no-such-thing'
      % (len(TECHNICAL), len(RESTRICTED), len(INTERNAL), len(NO_SUCH_THING)))
print('shapes given by hand : %d' % len(shapes))
print('shapes derived       : %d' % len(derived))
print('lines available      : %d of %d' % (len(entries), len(ALL_NAMES)))
print()
if len(CARD) + len(TECHNICAL) != len(ALL_NAMES):
    sys.exit('REFUSED: the two pages do not partition the roster - %d + %d != %d'
             % (len(CARD), len(TECHNICAL), len(ALL_NAMES)))
if bogus:
    print('=== IN syntax-shapes.txt, NOT ACCEPTED BY BCOMP (%d) ===' % len(bogus))
    print('  ' + ' '.join(bogus))
    print()
if missing:
    print('=== ACCEPTED BY BCOMP, NO SYNTAX LINE (%d) ===' % len(missing))
    print('  ' + ' '.join(missing))
    print()
    print('REFUSED: a page is not complete, and a lookup that is missing a name')
    print('         is worse than none - the reader concludes it does not')
    print('         exist.  Add the lines to syntax-shapes.txt.')
    sys.exit(1)
if bogus:
    print('REFUSED: a name in the data file that BCOMP does not accept is either')
    print('         a typo or a statement that has been removed.')
    sys.exit(1)

# ----------------------------------------------------------------- the pages

def kind(name):
    if name in NO_SUCH_THING:
        return 'no such thing'
    if name in INTERNAL:
        return 'internal'
    if name in RESTRICTED:
        return 'restricted'
    if name in INTRINSICS:
        return 'function'
    if name in STATEMENTS:
        return 'statement'
    return 'clause word'


CARD_HEAD = u"""Title: SD Basic - Syntax
Subtitle: Every statement and function, alphabetically, with its syntax and nothing else.

A lookup card, and nothing else. If you know what you want and have forgotten
how to spell it, it is here. If you want to know what it *does*, the other
seventeen documents in this set are where that lives.

*Italics* mark something you supply, **bold** a word typed as it stands, and
braces an optional part. SD folds case, so any of this may be written in
either case.

> **This page is generated, and it is checked for completeness rather than
> proof-read for it.** The roster comes from `BCOMP`'s own tables — the same
> extraction the rest of this set uses — and `tools/mksyntax.py` refuses to
> write the page if a single name that belongs on it has no line. Argument
> counts for functions are read out of `BCOMP`'s dispatch table, which is
> positional against the name list and carries each name in a comment; the
> script asserts the two agree before it uses either. The shapes that a count
> cannot express — every statement, and about twenty functions — come from
> documents 01 to 17, where each one is described in full.

**What is not here, and where it went.** Everything on this card is something
an application may use. Names that an ordinary program **cannot** compile are
in the administrator documentation, under *SD Basic - Restricted Commands*: the
restricted statements, the internal-only functions, and the one name that is in
the compiler's table with nothing behind it. **If you are looking for something
and it is not here, that is where to look before concluding it does not
exist.**

***ONE THING IS MARKED, AND IT IS THE ONE THAT WASTES TIME.***

| | |
|---|---|
| ***(clause word)*** | not a statement — a word that belongs inside another one's syntax |

"""

CARD_TAIL = u"""
## See also

[SD Basic - Program Structure](01-sd-basic-program-structure.html) ·
[SD Basic - Program Control](02-sd-basic-program-control.html) ·
[SD Basic - File Handling](07-sd-basic-file-handling.html) ·
[SD Basic - System and Environment](16-sd-basic-system-and-environment.html).
"""

TECH_HEAD = u"""Title: SD Basic - Restricted Commands
Subtitle: The statements and functions an ordinary program cannot compile, and what the compiler says when it tries.

Nothing on this page is available to an application: every name here needs a
program compiled with `$internal`, which in turn needs an administrator in the
`SDSYS` account. They are listed because they exist, because they appear in
SD's own source, and because the errors they produce name something other than
the real cause.

> This document is separate so that it can be withheld. It links to nothing
> outside the administrator set. Where a page in another set is worth naming,
> it is named in words.

*Italics* mark something you supply, **bold** a word typed as it stands, and
braces an optional part.

> **This page is generated from `BCOMP`'s own tables** by
> `tools/mksyntax.py`, the same script that builds the User set's syntax card,
> and the two **partition** the roster: every name the compiler accepts is on
> exactly one of them, and the script refuses to write either page if that
> stops being true.

## The three kinds, and how each one fails

| | |
|---|---|
| ***(restricted)*** | a statement in `BCOMP`'s `restricted.statements`. An ordinary account gets ***"Unrecognised statement"***, which at least names the right line |
| ***(internal)*** | a function in `BCOMP`'s `int.intrinsics`. ***The message names something else entirely***: an unknown function is read as a matrix reference, so the complaint is ***"Matrix X is not referenced in a DIM statement"*** — reported at the **last line of the program**, nowhere near the call. With three or more arguments it is *"Right bracket not found where expected"* instead, because a matrix takes at most two subscripts |
| ***(no such thing)*** | in a table with no opcode behind it. It compiles for **nobody** — `$internal` does not help |

***THE SECOND ROW IS THE ONE TO REMEMBER.*** If a function you are certain
exists produces a complaint about a `dim` statement you never wrote, it does
exist, and this account may not call it.

**`$internal` needs both halves.** `BCOMP` tests
`kernel(K$INTERNAL, -1) and kernel(K$ADMINISTRATOR, -1)` — internal mode alone
was enough until 13 Aug 2026, and it was not safe: internal programs are the
only ones that may set the administrator flag, and `sd -internal` is not itself
gated, so any account could have compiled a three-line program that granted
itself administrator rights. That was demonstrated, not theorised.

"""

TECH_TAIL = u"""
## See also

[Operating System Access](03-operating-system-access.html) covers the `sh` and
`!` verbs, which are the other thing an ordinary account cannot reach.
[Encryption and the SDEXT interface](04-sd-encryption.html) explains why
`sdext` is on this page and what it costs an application.

The User set's *SD Basic - Syntax* card carries everything an application may
use, and the two partition the roster between them.
"""


def render(names, head, tail, mark_kinds):
    out = [head]
    letter = None
    for name in sorted(names):
        if name[0] != letter:
            letter = name[0]
            out.append(u'\n## %s\n\n' % letter)
            out.append(u'| | |\n|---|---|\n')
        line = entries[name]
        k = kind(name)
        if k in mark_kinds and ('(%s)' % k) not in line:
            line += u' ***(%s)***' % k
        out.append(u'| **`%s`** | %s |\n' % (name.lower(), line))
    out.append(tail)
    return u''.join(out)


card = render(CARD, CARD_HEAD, CARD_TAIL, {'clause word'})
tech = render(TECHNICAL, TECH_HEAD, TECH_TAIL,
              {'restricted', 'internal', 'no such thing'})

for path, text, label in ((OUT, card, 'User 94 syntax card'),
                          (OUT_RESTRICTED, tech, 'Administrator 10 restricted')):
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print('wrote %-52s %6d bytes, %3d entries'
          % (path, len(text), text.count('\n| **`')))
sys.exit(0)
