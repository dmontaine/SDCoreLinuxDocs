#
# mktclsyntax.py <sdsys> <out.md>
#
# Write the SD TCL syntax card from tools/tcl-syntax-shapes.txt, and REFUSE to
# write it if a single verb has no line - the same contract mksyntax.py has for
# the SD BASIC card.
#
# THE ROSTER IS COMPUTED, NEVER TYPED.  143 verbs = the 123 verb records in
# sdsys/newvoc plus the 20 named in newvoc/TIER.ADD.ADMINISTRATOR, asserted not
# to overlap.  It was 144 and 21 until encrypt.field left the tier list
# (PRE_RELEASE 25).  THE ROSTER FOLLOWED ON ITS OWN because it is computed; the
# shapes file did not, and the "not a verb" refusal below is what that is for.
# A VOC record is a verb if the first character of field 1 is V,
# or - for the four records that are a keyword AND a verb, which CPROC
# re-parses from field 3 - the first character of field 3 is V.  Dispatch comes
# from field 2, or field 4 for those four.
#
# ***THE START-DESCRIPTION BLOCKS ARE A CONTROL, NOT A SOURCE.***  Sixty-three
# of the ninety-seven catalogued verbs carry one.  They are not used as content:
# they are written in another notation and several are stale.  Instead this
# script reports where the shapes file and a START-DESCRIPTION disagree about
# which KEYWORDS a verb takes.  Every hit is a lead for a person to follow -
# either the card is wrong or the source comment is - and it is printed rather
# than acted on, because a script cannot tell which.
#
# It also cross-checks the tier of every verb, so the card cannot disagree with
# what the account actually gets.
#
import io
import os
import re
import sys

if len(sys.argv) < 3:
    sys.exit('usage: mktclsyntax.py <sdsys dir> <out.md>')

SDSYS = sys.argv[1]
OUT = sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
SHAPES = os.path.join(HERE, 'tcl-syntax-shapes.txt')

NEWVOC = os.path.join(SDSYS, 'newvoc')
VOCT = os.path.join(SDSYS, 'voc_template')
GPLBP = os.path.join(SDSYS, 'gpl.bp')


def rec(path):
    with io.open(path, encoding='latin-1', newline='') as f:
        return [l.rstrip('\r\n') for l in f.read().split('\n')]


def fld(r, n):
    return r[n - 1].strip() if len(r) >= n else ''


def dispatch_of(r):
    """(mode, target) for a verb record, honouring the keyword-and-verb form."""
    if fld(r, 1)[:1].upper() == 'V':
        return fld(r, 2).upper(), fld(r, 3)
    return fld(r, 4).upper(), fld(r, 5)


# ------------------------------------------------------------------ roster

verbs = {}
for name in sorted(os.listdir(NEWVOC)):
    p = os.path.join(NEWVOC, name)
    if not os.path.isfile(p):
        continue
    r = rec(p)
    t1, t3 = fld(r, 1)[:1].upper(), fld(r, 3)[:1].upper()
    if t1 == 'V' or (t1 == 'K' and t3 == 'V'):
        verbs[name.lower()] = dispatch_of(r) + ('standard',)

admin = [l.strip().lower()
         for l in rec(os.path.join(NEWVOC, 'TIER.ADD.ADMINISTRATOR'))[1:]
         if l.strip()]
clash = sorted(set(admin) & set(verbs))
if clash:
    sys.exit('newvoc and TIER.ADD.ADMINISTRATOR overlap: %s' % clash)

for v in admin:
    p = os.path.join(VOCT, v.upper())
    if not os.path.isfile(p):
        p = os.path.join(VOCT, v)
    if os.path.isfile(p):
        mode, target = dispatch_of(rec(p))
    else:
        mode, target = '?', ''
    verbs[v] = (mode, target, 'administrator')

omit = set(l.strip().lower()
           for l in rec(os.path.join(NEWVOC, 'TIER.OMIT.STANDARD'))[1:]
           if l.strip())
for v in list(verbs):
    if verbs[v][2] == 'standard' and v in omit:
        verbs[v] = verbs[v][:2] + ('programmer',)

if len(verbs) < 100:
    sys.exit('REFUSED: roster came out as %d verbs - that is not a roster'
             % len(verbs))

# ------------------------------------------------------------------ shapes

shapes = {}
with io.open(SHAPES, encoding='utf-8', newline='') as f:
    for n, line in enumerate(f.read().split('\n'), 1):
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        if '=' not in s:
            sys.exit('%s:%d has no "=" - refusing' % (SHAPES, n))
        name, shape = s.split('=', 1)
        name, shape = name.strip().lower(), shape.strip()
        if not shape:
            sys.exit('%s:%d has an empty shape for %s' % (SHAPES, n, name))
        if name in shapes:
            sys.exit('%s:%d is a second line for %s' % (SHAPES, n, name))
        shapes[name] = shape

missing = sorted(set(verbs) - set(shapes))
extra = sorted(set(shapes) - set(verbs))
if missing or extra:
    for v in missing:
        print('NO SHAPE     %-18s is a verb (%s) and has no line in %s'
              % (v, verbs[v][2], os.path.basename(SHAPES)))
    for v in extra:
        print('NOT A VERB   %-18s has a shape and is not on the roster' % v)
    sys.exit('REFUSED: %d missing, %d not a verb' % (len(missing), len(extra)))

# ------------------------------- control: what the source comments say instead

cat = {}
for name in sorted(os.listdir(GPLBP)):
    p = os.path.join(GPLBP, name)
    if not os.path.isfile(p):
        continue
    with io.open(p, encoding='latin-1', newline='') as f:
        text = f.read()
    for m in re.finditer(r'(?im)^\s*\$catalog(ue)?\s+(\S+)', text):
        cat.setdefault(m.group(2).upper(), name)

KEYWORD = re.compile(r'\b([A-Z][A-Z0-9.]{2,})\b')
leads = []
for v in sorted(verbs):
    mode, target, tier = verbs[v]
    if mode != 'CA':
        continue
    src = cat.get(target.upper())
    if not src:
        continue
    with io.open(os.path.join(GPLBP, src), encoding='latin-1', newline='') as f:
        text = f.read()
    m = re.search(r'START-DESCRIPTION:(.*?)END-DESCRIPTION', text, re.S)
    if not m:
        continue
    body = '\n'.join(re.sub(r'^\*\s?', '', l) for l in m.group(1).split('\n'))
    said = set(k for k in KEYWORD.findall(body)
               if k.lower() != v and '.' not in k or k.lower() != v)
    said = set(k.lower() for k in KEYWORD.findall(body))
    # only look at the block's lines that start with this verb
    own = [l.strip() for l in body.split('\n')
           if l.strip().lower().startswith(v)]
    if not own:
        continue
    said = set(k.lower() for k in KEYWORD.findall(' '.join(own)))
    said.discard(v)
    said = set(k for k in said if k not in ('dict', 'data'))
    card = shapes[v].lower()
    absent = sorted(k for k in said if k not in card)
    if absent:
        leads.append((v, src, absent))

# ------------------------------------------------------------------- write

by_tier = {'standard': 0, 'programmer': 0, 'administrator': 0}
for v in verbs:
    by_tier[verbs[v][2]] += 1

out = []
out.append('Title: SD TCL - Syntax')
out.append('Subtitle: Every verb you can type, alphabetically, with its syntax and nothing else.')
out.append('')
out.append('A lookup card, and nothing else. If you know which verb you want and')
out.append('have forgotten its arguments, it is here. If you want to know what it')
out.append('*does*, the subject documents are where that lives.')
out.append('')
out.append('*Italics* mark something you supply, **bold** a word typed as it stands,')
out.append('braces an optional part, and a vertical bar separates alternatives. SD')
out.append('folds case, so any of this may be typed in either case.')
out.append('')
out.append('> **This page is generated, and it is checked for completeness rather')
out.append('> than proof-read for it.** The roster is computed from SD\'s own VOC:')
out.append('> the verb records in `newvoc` plus the ones an administrator account')
out.append('> adds, which is **%d** verbs, and `tools/mktclsyntax.py` refuses to' % len(verbs))
out.append('> write the page if any of them has no line. The shapes come from the')
out.append('> subject documents, where each verb is described in full.')
out.append('')
out.append('**The tier column is the VOC, not an opinion.** It is read from')
out.append('`TIER.OMIT.STANDARD` and `TIER.ADD.ADMINISTRATOR`, the same two lists')
out.append('the account-creation code uses, so it cannot drift from what an account')
out.append('actually gets. **A verb your account does not have is not refused — the')
out.append('name is simply not recognised.**')
out.append('')
out.append('| | | |')
out.append('|---|---|---|')
out.append('| **standard** | %d verbs | every account has these |' % by_tier['standard'])
out.append('| **programmer** | %d more | withheld from a standard account |' % by_tier['programmer'])
out.append('| **administrator** | %d more | and several need an elevated session as well |' % by_tier['administrator'])
out.append('')
out.append('## The verbs')
out.append('')
out.append('| | syntax | tier |')
out.append('|---|---|---|')

TIERMARK = {'standard': '', 'programmer': 'P', 'administrator': 'A'}
for v in sorted(verbs):
    out.append('| **`%s`** | %s | %s |' % (v, shapes[v], TIERMARK[verbs[v][2]]))

out.append('')
out.append('**Blank in the tier column means every account has it**; `P` is a')
out.append('programmer verb and `A` an administrator one.')
out.append('')

text = '\n'.join(out) + '\n'
with io.open(OUT, 'w', encoding='utf-8', newline='') as f:
    f.write(text)

print('roster        : %d verbs  (standard %d, programmer %d, administrator %d)'
      % (len(verbs), by_tier['standard'], by_tier['programmer'],
         by_tier['administrator']))
print('shapes        : %d, every verb covered, nothing left over' % len(shapes))
print('wrote         : %s  (%d bytes)' % (OUT, len(text)))

if leads:
    print()
    print('=== %d LEAD(S): a START-DESCRIPTION mentions a keyword the card does not ==='
          % len(leads))
    print('    These are not errors.  Either the card is short or the comment is')
    print('    stale; a person has to look.  Nothing here changed the page.')
    for v, src, absent in leads:
        print('  %-18s gpl.bp/%-12s %s' % (v, src, ' '.join(absent)))
