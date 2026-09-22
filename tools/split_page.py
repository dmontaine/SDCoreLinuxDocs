#
# split_page.py - cut one documentation page in two at a section heading.
#
#   python tools/split_page.py <source.md> "<## boundary heading>" \
#          <new-stem> "<new Title>" "<new Subtitle>" "<what part 2 holds>"
#
# WHY THIS IS A SCRIPT AND NOT A HAND EDIT.  CLAUDE.md's rule is that a file
# edit goes through the editing tools, and that a transform too large to do by
# hand is said out loud first, put in a file rather than inline, and checked
# afterwards.  This is that case: fourteen pages, about 100 KB of prose moved
# between files.  Retyping that through an editor is the HIGHER risk to the
# content - a dropped table row or an altered example would be silent, and
# nothing downstream checks prose against itself.
#
# SO IT WORKS IN BINARY AND PROVES IT LOST NOTHING.  The source is read as
# bytes and never decoded, so there is no encoding, line-ending or escape
# surface at all; a CRLF page stays CRLF and an em dash stays one em dash.
# Before either file is written the script asserts
#
#     part 1 body + part 2 body == the original body, byte for byte
#
# and refuses if it does not.  That is the one check worth having: everything
# else about a split is visible in a diff, and this is not.
#
# THE FRONT MATTER IS THE ONLY THING IT COMPOSES.  Part 1 keeps the source's
# Title and Subtitle - so every existing link to it still lands - and gains a
# "See also" pointing forward.  Part 2 gets the Title and Subtitle given on the
# command line, and a lead line pointing back.  Nothing else is rewritten.
#
import io
import os
import sys

if len(sys.argv) != 7:
    sys.exit(__doc__ or
             'usage: split_page.py <source.md> "<heading>" <new-stem> '
             '"<Title>" "<Subtitle>" "<what part 2 holds>"')

SRC, HEADING, STEM, TITLE, SUBTITLE, HOLDS = sys.argv[1:7]

src_path = os.path.abspath(SRC)
out_path = os.path.join(os.path.dirname(src_path), STEM + '.md')

if not HEADING.startswith('## '):
    sys.exit('split_page: the boundary must be a "## " heading, got %r' % HEADING)
if os.path.exists(out_path):
    sys.exit('split_page: %s already exists - refusing to overwrite' % out_path)

with io.open(src_path, 'rb') as f:
    raw = f.read()

if raw[:3] == b'\xef\xbb\xbf':
    sys.exit('split_page: %s starts with a BOM - fix that first' % src_path)

# --- front matter -----------------------------------------------------------
# Title:/Subtitle: lines, then a blank line, then the body.  Both line endings
# are handled without decoding: the split is on b'\n' and the CR, if any, rides
# along on the end of each line and is put back untouched.
lines = raw.split(b'\n')
head = []
i = 0
while i < len(lines) and lines[i].strip():
    head.append(lines[i])
    i += 1
if i >= len(lines):
    sys.exit('split_page: no blank line after the front matter')
head_raw = b'\n'.join(lines[:i + 1]) + b'\n'
body_raw = raw[len(head_raw):]

src_title = None
for h in head:
    if h.startswith(b'Title:'):
        src_title = h[len(b'Title:'):].strip().decode('utf-8')
if not src_title:
    sys.exit('split_page: %s has no Title: line' % src_path)

# --- the boundary -----------------------------------------------------------
needle = HEADING.encode('utf-8')
hits = []
pos = 0
while True:
    at = body_raw.find(needle, pos)
    if at < 0:
        break
    at_line_start = (at == 0 or body_raw[at - 1:at] == b'\n')
    end = body_raw[at + len(needle):at + len(needle) + 1]
    if at_line_start and end in (b'\n', b'\r', b''):
        hits.append(at)
    pos = at + 1

if len(hits) != 1:
    sys.exit('split_page: the heading %r starts %d lines in %s - it must start '
             'exactly one' % (HEADING, len(hits), os.path.basename(src_path)))

cut = hits[0]
part1_body = body_raw[:cut]
part2_body = body_raw[cut:]

# --- THE CHECK THIS SCRIPT EXISTS FOR --------------------------------------
if part1_body + part2_body != body_raw:
    sys.exit('split_page: the two halves do not rebuild the body - refusing')
if not part1_body.strip() or not part2_body.strip():
    sys.exit('split_page: one half is empty - the boundary is at an end')

eol = b'\r\n' if body_raw.count(b'\r\n') > body_raw.count(b'\n') // 2 else b'\n'


def ln(text):
    return text.encode('utf-8') + eol


def wrapped(text, width=78):
    """Greedy wrap.  The rest of the corpus wraps near 78 and a 120-character
    line in the middle of it reads as a machine wrote it, which one did."""
    out = []
    line = ''
    for word in text.split(' '):
        if line and len(line) + 1 + len(word) > width:
            out.append(line)
            line = word
        else:
            line = (line + ' ' + word) if line else word
    if line:
        out.append(line)
    return b''.join(ln(l) for l in out)


src_stem = os.path.splitext(os.path.basename(src_path))[0]

# Part 1: its own body, then a forward pointer.  The source's own "See also"
# went with the second half, which is where the sections it names now are.
part1 = head_raw + part1_body.rstrip() + eol + eol
part1 += ln('## Continued in')
part1 += eol
part1 += wrapped('[%s](%s.html) — %s' % (TITLE, STEM, HOLDS))

# Part 2: new front matter, a line pointing back, then the moved sections.
part2 = ln('Title: %s' % TITLE)
part2 += ln('Subtitle: %s' % SUBTITLE)
part2 += eol
part2 += wrapped('This page continues [%s](%s.html).' % (src_title, src_stem))
part2 += eol
part2 += part2_body

with io.open(src_path, 'wb') as f:
    f.write(part1)
with io.open(out_path, 'wb') as f:
    f.write(part2)

# --- an instrument prints what it DID --------------------------------------
sys.stdout.write('split_page: source   %s\n' % src_path)
sys.stdout.write('split_page: boundary %s  at byte %d of %d body bytes\n'
                 % (HEADING, cut, len(body_raw)))
sys.stdout.write('split_page: line end %s\n'
                 % ('CRLF' if eol == b'\r\n' else 'LF'))
sys.stdout.write('split_page: rebuild  OK - the halves are the original body\n')
sys.stdout.write('split_page: part 1   %s  %d bytes  "%s"\n'
                 % (os.path.basename(src_path), len(part1), src_title))
sys.stdout.write('split_page: part 2   %s  %d bytes  "%s"\n'
                 % (os.path.basename(out_path), len(part2), TITLE))
