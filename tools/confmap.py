#
# confmap.py <sd4windows>/sdb_ai/sd64
#
# Assign every CONFIGURATION PARAMETER to exactly one document, check the
# document actually documents it, and - the half that matters for W1.0-0 -
# report which parameters are still READ by the product and which survive only
# as a branch that accepts a value nothing consumes.
#
# ***WHY IT EXISTS.***  docmap.py does this for the SD BASIC roster and
# tclmap.py for the TCL verbs.  Nothing did it for sd.conf, and the gap showed:
# the configuration page listed 19 parameters and named one, PTYPES, that does
# not exist, while config.c parses 52.  A page written from another product's
# documentation cannot be checked by reading it.
#
# ***AND IT ANSWERS THE OWNER'S SECOND DIRECTIVE, 4 Sep 2026 - "there may be new
# features that are not documented".***  A checker that only asked "is every
# documented parameter real" would have passed a page listing three parameters.
# The roster is computed from the source, so a parameter added to config.c
# turns this red until somebody writes it down.
#
# ***THE INERT TEST IS THE POINT, NOT A BONUS.***  Owner, 4 Sep 2026: "some of
# those config settings may have been for features removed such as qmnet (sdnet)
# and PROCS ... do not include documentation for features the source code no
# longer supports."  A parameter whose struct field is written by config.c and
# read by nothing else is a parameter that does nothing.  It must still be
# DOCUMENTED - a site with it in sd.conf needs to know - but documented as
# accepted and inert, never as a control.
#
# HOW THE INERT TEST WORKS.  A parameter has TWO ways of being read and the
# first draft of this script knew only one, which is why the comment below is
# longer than the code.
#
#   1. THE C SIDE.  config.c assigns the value to a struct member; a .c file
#      outside config.c and op_config.c mentions that member.
#   2. ***THE BASIC SIDE, WHICH IS THE ONE THAT WAS MISSED.***  gpl.bp reads the
#      value back through the config() function by NAME - CREATEF:359 takes
#      GRPSIZE, CREATEA:391 takes USRDIR, _VOC_REF:131 takes FILERULE.  None of
#      those touches the struct member, so a C-only test calls all three inert.
#
# ***THE FIRST VERSION DID EXACTLY THAT AND WOULD HAVE PRINTED IT.***  It named
# nine parameters inert, three of them being GRPSIZE, GRPDIR and USRDIR - the
# default group size and the two directories every account is created in.  A
# page saying those do nothing would have been worse than the page that omitted
# them.  The check was widened rather than the finding trusted.
#
# WHAT IT STILL CANNOT SEE: a member reached only through a macro, or a config()
# call built from a variable rather than a literal.  So the script REPORTS the
# readers rather than deciding, and anything it calls inert is confirmed by
# reading the sources before a page repeats it.
#
# EXITS NON-ZERO on: a parameter assigned nowhere, assigned twice, assigned to a
# page that does not evidence it, an assignment naming a parameter that is not
# in config.c, or a roster that came out empty.
#
import io
import os
import re
import sys

if len(sys.argv) < 2:
    sys.exit('usage: confmap.py <path to sdb_ai/sd64>')

TREE = sys.argv[1]
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_C = os.path.join(TREE, 'gplsrc', 'config.c')

if not os.path.isfile(CONFIG_C):
    sys.exit('confmap: no config.c at %s' % CONFIG_C)

# ---------------------------------------------------------------- the roster
#
# A parameter is a branch in read_config()'s chain.  Both spellings are used:
# sscanf(rec, "NAME=%d", ...) for values, strncmp(rec, "NAME=", n) for strings.

src = io.open(CONFIG_C, encoding='latin-1').read()
lines = src.split('\n')

PARAM = re.compile(r'(?:sscanf\(rec, "|strncmp\(rec, ")([A-Z][A-Z0-9_]*)=')
MEMBER = re.compile(r'(?:cfg->|pcfg\.)([a-z_][a-z0-9_]*)')

roster = []          # parameter names, in file order
member_of = {}       # parameter -> struct member it assigns, or None
line_of = {}         # parameter -> line number in config.c

for i, line in enumerate(lines, 1):
    m = PARAM.search(line)
    if not m:
        continue
    name = m.group(1)
    if name in member_of:
        continue
    roster.append(name)
    line_of[name] = i
    # The assignment is on this line or the few that follow, before the next
    # branch.  Take the first struct member mentioned.
    member = None
    for probe in lines[i - 1:i + 6]:
        if probe is not lines[i - 1] and PARAM.search(probe):
            break
        mm = MEMBER.search(probe)
        if mm:
            member = mm.group(1)
            break
    member_of[name] = member

if not roster:
    sys.exit('confmap: roster came out empty - the parse found no parameters')

# ------------------------------------------------------------- who reads it

CSRC = os.path.join(TREE, 'gplsrc')
sources = {}
for name in sorted(os.listdir(CSRC)):
    if not name.endswith('.c'):
        continue
    if name in ('config.c', 'op_config.c'):
        continue
    sources[name] = io.open(os.path.join(CSRC, name), encoding='latin-1').read()

# The BASIC side.  CONFIG itself only PRINTS every parameter, so it is excluded
# for the same reason op_config.c is: reporting a value is not consuming it.
BSRC = os.path.join(TREE, 'sdsys', 'gpl.bp')
basic = {}
if os.path.isdir(BSRC):
    for name in sorted(os.listdir(BSRC)):
        path = os.path.join(BSRC, name)
        if not os.path.isfile(path) or name.upper() == 'CONFIG':
            continue
        # ***COMMENT LINES ARE STRIPPED, AND THAT IS NOT TIDINESS.***  Both
        # CREATEA and DELACC carry a line recording that the config('CREATUSR')
        # gate was REMOVED on 14 Aug 2026.  Matched raw, the note that a
        # parameter is dead is read as evidence that it is alive - the exact
        # direction the owner ruled against.  A BASIC comment opens with * or !
        # in the first non-blank column.
        text = io.open(path, encoding='latin-1').read()
        basic[name] = '\n'.join(l for l in text.split('\n')
                                if not l.lstrip().startswith(('*', '!')))

readers = {}
for param in roster:
    member = member_of.get(param)
    hits = []
    if member:
        word = re.compile(r'\b%s\b' % re.escape(member))
        hits += sorted(n for n, text in sources.items() if word.search(text))
    # config('NAME') / CONFIG("NAME"), either case, either quote
    call = re.compile(r'''config\(\s*['"]%s['"]\s*\)''' % re.escape(param), re.I)
    hits += sorted(n + ' (BASIC)' for n, text in basic.items() if call.search(text))
    if member is None and not hits:
        readers[param] = None          # nothing assigned and nothing reads it
    else:
        readers[param] = hits

# ------------------------------------------------------------- the documents
#
# One parameter, one page.  Edit this map when a page changes; the script
# refuses a name that is not on the roster, so it cannot drift silently.

DOCUMENTS = {
 # 22 Sep 26 - LINUX FORK.  APIPORT and NETDIRS are not parameters this
 # port's config.c accepts at all: whether SD listens for the API is
 # systemd's sdclient.socket unit, not a start-up config value, and there
 # is no config-file mechanism here widening an API session's file access
 # beyond its own account (see 07's own "The API" section).
 'Administrator/markdown/07-sd-admin-configuration.md': """
   APILOGIN CMDSTACK CODEPAGE CREATUSR DEADLOCK DEBUG DUMPDIR ERRLOG
   EXCLREM FDS FILERULE FIXUSERS FLTDIFF FSYNC GDI GRPDIR GRPSIZE INTPREC
   JNLDIR JNLMODE LPTRHIGH LPTRWIDE MAXCALL MAXIDLEN MUSTLOCK NETFILES
   NUMFILES NUMLOCKS NUMUSERS OBJECTS OBJMEM PDUMP PORTMAP RECCACHE RINGWAIT
   SAFEDIR SDCLIENT SDSYS SH SH1 SORTMEM SORTMRG SORTWORK SPOOLER STARTUP
   TEMPDIR TERMINFO TXCHAR USRDIR YEARBASE
 """,
}

assigned = {}
problems = []

for doc, names in DOCUMENTS.items():
    for name in names.split():
        if name not in member_of:
            problems.append(('NOT A PARAMETER', name,
                             'claimed by %s' % doc))
            continue
        if name in assigned:
            problems.append(('ASSIGNED TWICE', name,
                             '%s and %s' % (assigned[name], doc)))
            continue
        assigned[name] = doc

for name in roster:
    if name not in assigned:
        problems.append(('NO PAGE', name,
                         'is a parameter and is on no page'))

# ------------------------------------------------------- evidence on the page
#
# Same rule as tclmap: the name backticked, or opening a line inside a fenced
# block, or in the first column of a table row.  Prose alone is not evidence.

def evidences(path, name):
    full = os.path.join(HERE, path)
    if not os.path.isfile(full):
        return False
    text = io.open(full, encoding='utf-8').read()
    if re.search(r'`%s`' % re.escape(name), text):
        return True
    if re.search(r'^\|\s*%s\s*\|' % re.escape(name), text, re.M):
        return True
    if re.search(r'^%s\b' % re.escape(name), text, re.M):
        return True
    return False

for name, doc in sorted(assigned.items()):
    if not evidences(doc, name):
        problems.append(('NOT EVIDENCED', name,
                         '%s does not document it' % doc))

# ------------------------------------------------------------------- report

inert = [p for p in roster if readers.get(p) == []]
discarded = [p for p in roster if readers.get(p) is None]

print('config.c parses : %d parameter(s)' % len(roster))
print('assigned        : %d' % len(assigned))
print('documents       : %d' % len(DOCUMENTS))
print('')
print('=== ACCEPTED AND DISCARDED - config.c stores nothing (%d) ===' % len(discarded))
for p in discarded:
    print('  %-12s config.c:%d' % (p, line_of[p]))
print('')
print('=== STORED BUT READ BY NO OTHER SOURCE FILE (%d) ===' % len(inert))
for p in inert:
    print('  %-12s -> %-22s config.c:%d' % (p, member_of[p], line_of[p]))
print('')
print('=== READ BY THE PRODUCT (%d) ===' % (len(roster) - len(inert) - len(discarded)))
for p in roster:
    r = readers.get(p)
    if not r:
        continue
    shown = ' '.join(r[:6]) + (' +%d' % (len(r) - 6) if len(r) > 6 else '')
    print('  %-12s -> %-22s %s' % (p, member_of[p], shown))

if problems:
    print('')
    print('=== %d PROBLEM(S) ===' % len(problems))
    for kind, name, detail in problems:
        print('  %-15s %-18s %s' % (kind, name, detail))
    sys.exit(1)

print('')
print('confmap: every parameter is documented exactly once')
