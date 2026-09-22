#
# control.py - POSITIVE CONTROL for overlap.py.
#
# overlap.py reported zero shared runs.  That is the same output a matcher
# that loaded nothing, normalised differently on each side, or silently threw
# would produce, so the zero means nothing until this passes: plant a real
# passage FROM the reference corpus into a file shaped like one of ours, and
# require the matcher to find it.
#
import os
import re
import sys
import html

QM = sys.argv[1]
OUT = sys.argv[2]

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


# Find a reference page with a decent run of prose and take 25 words of it.
pick = None
for root, _dirs, names in os.walk(QM):
    for n in sorted(names):
        if not n.lower().endswith(('.htm', '.html')):
            continue
        t = html.unescape(TAG.sub(' ', SCRIPT.sub(' ', read(os.path.join(root, n)))))
        w = [x for x in re.split(r'\s+', t) if x]
        if len(w) > 200:
            pick = (n, ' '.join(w[80:105]))
            break
    if pick:
        break

if not pick:
    print('control: REFUSING - no reference page long enough to sample.')
    sys.exit(2)

os.makedirs(OUT, exist_ok=True)
planted = os.path.join(OUT, 'planted.md')
with open(planted, 'w', encoding='utf-8') as f:
    f.write('Title: A control fixture\n\n')
    f.write('This paragraph is lifted verbatim from the reference corpus so\n')
    f.write('that the matcher has something it MUST find:\n\n')
    f.write(pick[1] + '\n')

print('control: planted 25 words from %s' % pick[0])
print('control: fixture %s' % planted)
