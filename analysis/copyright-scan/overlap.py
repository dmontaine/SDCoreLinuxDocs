#
# overlap.py - find verbatim runs shared between our documentation and the
# OpenQM 2.6-6 help.  Reports the LONGEST runs first, with a location on each
# side, so a person can judge each one.  It does not filter: a syntax line and
# a paragraph of prose look the same to a matcher, and only a reader can tell
# a reserved word from copied expression.
#
# Method: seed on an exact N-word window, then extend the match greedily in
# both directions.  Comparison is on lower-cased words with runs of whitespace
# collapsed; punctuation is KEPT, because dropping it invents matches that are
# not there.
#
import os
import re
import sys
import html
from collections import defaultdict

QM = sys.argv[1]
OURS = sys.argv[2]
SEED = int(sys.argv[3]) if len(sys.argv) > 3 else 8

TAG = re.compile(r'<[^>]+>')
SCRIPT = re.compile(r'(?is)<(script|style)\b.*?</\1>')


def read(path):
    for enc in ('utf-8', 'cp1252', 'latin-1'):
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, LookupError):
            continue
    return ''


def html_text(s):
    s = SCRIPT.sub(' ', s)
    s = TAG.sub(' ', s)
    return html.unescape(s)


WITH_CODE = len(sys.argv) > 4 and sys.argv[4] == 'withcode'


def md_text(s):
    # Fenced code blocks are stripped by default: a shared command example is
    # not copied prose, and leaving them in buries the real findings.  Pass
    # "withcode" to keep them, which is the run that asks the separate
    # question of whether SYNTAX matches - it should, since SD implements the
    # same verbs, and that is compatibility rather than copying.
    if WITH_CODE:
        return s
    s = re.sub(r'(?ms)^```.*?^```', ' ', s)
    s = re.sub(r'`[^`]*`', ' ', s)
    return s


def words(s):
    return [w for w in re.split(r'\s+', s.lower()) if w]


# ---------------------------------------------------------------- the corpus
qm_files = []
for root, _dirs, names in os.walk(QM):
    for n in sorted(names):
        if n.lower().endswith(('.htm', '.html')):
            qm_files.append(os.path.join(root, n))

index = {}          # seed tuple -> (file index, position)
qm_words = []       # per-file word lists
for fi, path in enumerate(qm_files):
    w = words(html_text(read(path)))
    qm_words.append(w)
    for i in range(len(w) - SEED + 1):
        key = tuple(w[i:i + SEED])
        if key not in index:
            index[key] = (fi, i)

print('overlap: %d reference page(s), %d word(s), %d distinct %d-gram(s)'
      % (len(qm_files), sum(len(w) for w in qm_words), len(index), SEED))

our_files = []
for root, _dirs, names in os.walk(OURS):
    if os.sep + 'html' in root or os.sep + 'pdf' in root:
        continue
    for n in sorted(names):
        if n.lower().endswith('.md'):
            our_files.append(os.path.join(root, n))
print('overlap: %d of our page(s)' % len(our_files))
if not our_files or not qm_files:
    print('overlap: REFUSING - one side is empty, so this measured nothing.')
    sys.exit(2)

# ------------------------------------------------------------- the comparison
runs = []
for path in our_files:
    raw = md_text(read(path))
    w = words(raw)
    i = 0
    while i <= len(w) - SEED:
        hit = index.get(tuple(w[i:i + SEED]))
        if not hit:
            i += 1
            continue
        fi, qi = hit
        qw = qm_words[fi]
        # extend right
        a, b = i + SEED, qi + SEED
        while a < len(w) and b < len(qw) and w[a] == qw[b]:
            a += 1
            b += 1
        # extend left
        c, d = i, qi
        while c > 0 and d > 0 and w[c - 1] == qw[d - 1]:
            c -= 1
            d -= 1
        runs.append((a - c, path, os.path.basename(qm_files[fi]),
                     ' '.join(w[c:a])))
        i = a          # do not re-report the same run

runs.sort(key=lambda r: -r[0])
print('overlap: %d run(s) of >= %d consecutive words' % (len(runs), SEED))
print('')
seen = set()
shown = 0
for length, ours, theirs, text in runs:
    if text in seen:
        continue
    seen.add(text)
    shown += 1
    if shown > 40:
        break
    rel = ours.replace('\\', '/').split('/')
    rel = '/'.join(rel[-3:])
    print('%3d words  %-46s  <- %s' % (length, rel, theirs))
    print('           %s' % (text[:150] + ('...' if len(text) > 150 else '')))
    print('')
if not runs:
    print('overlap: no run of %d consecutive words is shared.' % SEED)
