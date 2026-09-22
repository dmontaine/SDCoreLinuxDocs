#
# verbcounts.py <sd4windows>/sdb_ai/sd64/sdsys/newvoc
#
# Compute the number of VERBS an ordinary account and SDSYS each get, then
# check every verb count written in prose across all four document sets
# against it.
#
# ***WHY IT EXISTS - PRE_RELEASE 80, ITEM (a).***  "Nothing compares the prose
# figures against the generated roster."  mktclsyntax.py printed standard 81 in
# the generated card for a week while the tester set said 77; the two halves of
# the documentation disagreed and nothing noticed, because the generators read
# the VOC and the hand-written pages do not.
#
# ***IT IS A VERB COUNT AND NOT A RECORD COUNT, AND CONFLATING THEM IS THE
# TRAP.***  A record count - "count voc" - is exact and arithmetic; a reader of
# the documentation wants to know how many COMMANDS they can type, which is the
# subset of those records that are verbs.  The two are different numbers and
# neither is wrong.  Do not "correct" one to the other.
#
# ***THE THREE-TIER MODEL THIS SCRIPT ORIGINALLY COMPUTED IS GONE.***
# RELEASE_1.1 64 (18 Sep 2026) removed the account tiers and the two lists
# (newvoc/TIER.OMIT.STANDARD, newvoc/TIER.ADD.ADMINISTRATOR) this script read
# to build standard/programmer/administrator - it crashed outright against a
# tree that has moved past that model, the same way mktclsyntax.py and
# tclmap.py did.  What replaced it: every ordinary account's VOC is `newvoc`
# in full; SDSYS's is `voc_template`, a superset.  Two counts, not three.
#
# THE RULE FOR WHAT IS A VERB is tclmap.py's, deliberately, so the two cannot
# disagree: field 1 begins V, or - for the records that are a keyword AND a
# verb - field 3 does.
#
# HOW THE PROSE CHECK WORKS.  Every "<n> verbs" in the markdown is found and
# required to be one of the computed figures, or to be registered in ALLOWED
# below with a reason.  A figure nobody can account for is the defect this
# exists to catch.  The pattern is deliberately narrow; see the note above it.
#
# EXITS NON-ZERO on a prose figure that matches no computed count and is not
# registered, or on a roster that came out empty.
#
import io
import os
import re
import sys

if len(sys.argv) < 2:
    sys.exit('usage: verbcounts.py <path to sdsys/newvoc>')

NEWVOC = sys.argv[1]
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETS = ('GettingStarted', 'User', 'Administrator')


def field(rec, n):
    return rec[n - 1] if len(rec) >= n else ''


def is_verb(path):
    with io.open(path, encoding='latin-1', newline='') as f:
        rec = [l.rstrip('\r\n') for l in f.read().split('\n')]
    t1 = field(rec, 1)[:1].upper()
    t3 = field(rec, 3)[:1].upper()
    return t1 == 'V' or (t1 == 'K' and t3 == 'V')


def verb_roster(directory):
    found = set()
    for name in sorted(os.listdir(directory)):
        path = os.path.join(directory, name)
        if os.path.isfile(path) and is_verb(path):
            found.add(name.lower())
    return found


TEMPLATE = os.path.join(os.path.dirname(NEWVOC), 'voc_template')

ordinary = verb_roster(NEWVOC)
sdsys = ordinary | verb_roster(TEMPLATE)

if not ordinary:
    sys.exit('verbcounts: roster came out empty')

COUNTS = {
    'ordinary account': len(ordinary),
    'sdsys': len(sdsys),
}
# The full roster is the one tclmap.py computes.
COUNTS['roster'] = len(sdsys)
# What SDSYS gets on top of an ordinary account - written in prose as a
# difference.
COUNTS['sdsys adds'] = len(sdsys) - len(ordinary)

# ***THE DISPATCH BREAKDOWN IS COMPUTED FOR THE SAME REASON THE TIERS WERE.***
# User/32 carries a table saying how many of the shipped verbs are catalogued
# programs, how many are internal, and so on.  Those were typed, and the
# internal figure had drifted to 45 against a real 42.  Field 2 of a verb record
# is the dispatch type; SDSYS's roster is the whole of it, so the SDSYS-only
# records are read from voc_template where they live.

def dispatch_of(name):
    for d in (NEWVOC, TEMPLATE):
        path = os.path.join(d, name)
        if os.path.isfile(path):
            with io.open(path, encoding='latin-1', newline='') as f:
                rec = [l.rstrip('\r\n') for l in f.read().split('\n')]
            return field(rec, 2).strip().upper()[:2]
    return ''

by_type = {}
for v in sdsys:
    by_type[dispatch_of(v)] = by_type.get(dispatch_of(v), 0) + 1
for t, n in by_type.items():
    COUNTS['dispatch %s' % (t or '(none)')] = n

VALID = set(COUNTS.values())

# Figures that are legitimately about something other than a tier's verb count.
# Each needs a reason; an unexplained entry here is the check being switched off.
ALLOWED = {
    411: 'SD BASIC names accepted by the compiler - docmap.py computes it',
    372: 'SD BASIC names an application may use - the 94 syntax card',
    447: 'the SD BASIC roster, application plus restricted - mksyntax.py',
    75:  'SD BASIC names an application may NOT use - Administrator/10',
}

# ***THE PATTERN IS NUMBER-THEN-PLURAL-VERBS AND NOTHING ELSE, WHICH IS A
# DELIBERATE NARROWING.***  The first draft also matched "verbs ... <n>" within
# forty characters, to catch a count written the other way round.  It found 28
# figures where 4 were real: "internal verb 29", "field 2 of a verb record",
# "120 x 36" and "the verb prints 43 of them" all matched.  A check whose output
# is mostly noise is one nobody reads, which is how 81 survived for a week.
#
# Every genuine disagreement is written "<n> verbs" - "81 verbs", "the 20 verbs
# an administrator gets", "= 123 verbs", "**143** verbs" - so that is what it
# matches.  Bold markers are allowed around the number.  Singular "verb" is
# excluded because "internal verb 14" is a verb NUMBER, not a count.
pattern = re.compile(r'(\d{1,4})\*{0,2}\s+verbs\b', re.I)

problems = []
seen = []

for s in SETS:
    d = os.path.join(HERE, s, 'markdown')
    if not os.path.isdir(d):
        continue
    for name in sorted(os.listdir(d)):
        if not name.endswith('.md'):
            continue
        path = os.path.join(d, name)
        for i, line in enumerate(io.open(path, encoding='utf-8'), 1):
            for m in pattern.finditer(line):
                n = int(m.group(1))
                where = '%s/markdown/%s:%d' % (s, name, i)
                seen.append((where, n, line.strip()[:70]))
                if n in VALID or n in ALLOWED:
                    continue
                problems.append((where, n, line.strip()[:70]))

print('computed from %s' % NEWVOC)
for k in sorted(COUNTS):
    print('  %-20s %d' % (k, COUNTS[k]))
print('')
print('prose figures found : %d' % len(seen))
print('unaccounted for     : %d' % len(problems))

if problems:
    print('')
    print('=== %d PROBLEM(S) ===' % len(problems))
    for where, n, text in problems:
        print('  %-58s %4d  %s' % (where, n, text))
    print('')
    print('Every figure must be one of the computed counts above, or listed in')
    print('ALLOWED with a reason.')
    sys.exit(1)

print('')
print('verbcounts: every verb count in the documentation matches the VOC')
