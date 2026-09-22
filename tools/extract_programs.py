#
# extract_programs.py <page.md> <outdir>
#
# Pull every complete BASIC program out of a documentation page so each one can
# be handed to the compiler.
#
# ***WHY IT EXISTS.***  A tutorial's programs are the one thing on a page that
# can be checked completely and mechanically: they either compile or they do
# not.  Nothing had ever compiled the ones in User 40, and during the W1.0-0
# audit SIX OF THE TEN substantial programs failed - including the 106-line
# application the tutorial builds toward, which had four errors.
#
# What was wrong, and every one of them is the kind of mistake reading cannot
# catch:
#
#   - "loop while readnext(id) from 1 do" in three places.  readnext is a
#     STATEMENT; written as a function the compiler reads it as a matrix
#     reference and complains about a dim statement that is not there.
#   - "program get.field" followed by "subroutine get.field(...)" - both
#     declarations, in a block whose own prose says a subroutine starts with
#     one and a program with the other.
#   - the same double declaration on the function example.
#   - a caller using fmt.phone(raw) with no deffun, which fails the same
#     misleading way readnext does.
#   - @system.error.text, three times.  There is no such variable; status()
#     carries the code and !ERRTEXT turns it into a sentence.
#
# HOW TO USE IT.  Extract, then compile each file with tools\sdcompile.ps1:
#
#     python tools\extract_programs.py User\markdown\40-sd-programming-tutorial.md out
#     # then, per file:
#     tools\sdcompile.ps1 -Source out\ZZT06_listcust.b -ExpectErrors
#
# -ExpectErrors is right for a sweep: it makes a clean compile the reportable
# outcome rather than an abort, so a run over ten files does not stop at the
# first success.
#
# ***IT ONLY TAKES COMPLETE PROGRAMS, AND THAT MATTERS FOR THE COUNT.***  A
# block is compilable only if it declares itself and ends with END; a fragment,
# a TCL transcript or an output sample is skipped.  The script prints how many
# of the page's fenced blocks it took, so "12 of 41" is visible rather than
# implied - a sweep that silently found nothing would otherwise look like a
# sweep that found nothing wrong.
#
import io
import os
import re
import sys

if len(sys.argv) < 3:
    sys.exit('usage: extract_programs.py <page.md> <outdir>')

SRC = sys.argv[1]
OUT = sys.argv[2]

text = io.open(SRC, encoding='utf-8').read()
blocks = re.findall(r'```\n(.*?)```', text, re.S)

os.makedirs(OUT, exist_ok=True)
n = 0
for b in blocks:
    lines = [l.rstrip() for l in b.split('\n')]
    body = [l for l in lines if l.strip()]
    if not body:
        continue
    first = body[0].strip().lower()
    if not (first.startswith('program ') or first.startswith('subroutine ')
            or first.startswith('function ')):
        continue
    if body[-1].strip().lower() != 'end':
        continue
    n += 1
    name = re.sub(r'[^a-z0-9]', '', first.split()[1].lower())[:8] or ('p%d' % n)
    path = os.path.join(OUT, 'ZZT%02d_%s.b' % (n, name))
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines).rstrip() + '\n')
    print('%2d  %-12s %3d lines  %s' % (n, name, len(lines), path))

print('')
print('%d complete program(s) extracted of %d fenced block(s)' % (n, len(blocks)))
if n == 0:
    sys.exit('extract_programs: no complete programs found - that is not a result')
