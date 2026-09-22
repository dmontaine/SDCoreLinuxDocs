#
# linkup.py <markdown-dir>
#
# Turn *SD Basic - X* into a real link, but ONLY for pages that exist.  A
# reference to a document not yet written stays in italics, so the link checker
# stays meaningful and nobody ships a link to a 404.
#
# It reports what it changed and what it left alone, and refuses to write if it
# changed nothing - a substitution that silently matches nothing is the usual
# way this kind of script looks like it worked.
#
import io
import os
import re
import sys

md_dir = sys.argv[1]

titles = {}
for name in sorted(os.listdir(md_dir)):
    if not name.endswith('.md'):
        continue
    path = os.path.join(md_dir, name)
    with io.open(path, encoding='utf-8', newline='') as f:
        head = f.read(400)
    m = re.search(r'^Title:\s*(.+?)\s*$', head, re.M)
    if not m:
        sys.exit('%s has no Title: line - refusing' % name)
    titles[m.group(1)] = name[:-3] + '.html'

if not titles:
    sys.exit('no documents found - refusing')

print('pages that exist and can be linked to:')
for t in sorted(titles):
    print('  %-34s -> %s' % (t, titles[t]))
print()

changed_total = 0
left_total = 0
for name in sorted(os.listdir(md_dir)):
    if not name.endswith('.md'):
        continue
    path = os.path.join(md_dir, name)
    with io.open(path, encoding='utf-8', newline='') as f:
        src = f.read()
    orig = src
    changed = 0

    def sub(m):
        global changed
        title = m.group(1).strip()
        target = titles.get(title)
        # never link a page to itself
        if target and target != name[:-3] + '.html':
            changed += 1
            return '[%s](%s)' % (title, target)
        return m.group(0)

    # BOTH SETS.  The User folder now holds the SD Basic reference and the
    # SD TCL reference, and a TCL page refers forward to TCL pages not yet
    # written exactly as a Basic page did.  titles{} is built from every
    # Title: line already, so only the prefix needed widening.
    src = re.sub(r'\*(SD (?:Basic|TCL) - [^*]+?)\*', sub, src)

    left = len(re.findall(r'\*SD (?:Basic|TCL) - [^*]+?\*', src))
    left_total += left
    changed_total += changed
    if src != orig:
        with io.open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(src)
    print('  %-42s linked %2d   left in italics %2d' % (name, changed, left))

print()
print('links made               : %d' % changed_total)
print('references left unlinked : %d  (documents not written yet)' % left_total)
if changed_total == 0:
    sys.exit('nothing was linked - the pattern matched nothing, which is a fault')
