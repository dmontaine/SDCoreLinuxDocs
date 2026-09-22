#
# scriptmap.py <install root, e.g. "C:\Program Files\SD">
#
# Check that every PowerShell script the installer leaves on the machine is
# documented, and that the page names none that is not there.
#
# ***WHY IT EXISTS.***  The installed-scripts page said "twenty-six scripts ship" and
# thirty-seven were installed.  Eleven had been added since the page was
# written and nothing noticed, because the page is a hand-kept list of files
# that live in another repository.  That is the same shape as the verb roster
# and the configuration parameters, and it gets the same treatment.
#
# ***THE INSTALLED TREE IS THE AUTHORITY, NOT sd.iss.***  PRE_RELEASE 80's rule
# for the whole audit: every claim is checked against what a user actually
# receives.  A script listed in the installer script but not present, or present
# and not listed, is a difference this check should SEE rather than inherit.
# Run gplbld/assert-current.ps1 first if you need to know the install is current.
#
# EVIDENCE ON THE PAGE is the same narrow rule the other checkers use: the file
# name backticked, or opening a line in a fenced block, or in a table cell.
# Prose alone does not count.
#
# ***A SCRIPT MAY BE DELIBERATELY UNDOCUMENTED, BUT IT HAS TO SAY SO.***  EXEMPT
# below takes a reason per entry, so "we chose not to" cannot look the same as
# "we forgot".  Nothing is exempt today.
#
# EXITS NON-ZERO on an undocumented script, on a documented script that is not
# installed and not registered in NOT_SHIPPED, or on an empty scan.
#
import io
import os
import re
import sys

if len(sys.argv) < 2:
    sys.exit('usage: scriptmap.py <install root>')

ROOT = sys.argv[1]
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# TWO PAGES SINCE THE SPLIT, AND BOTH ARE READ.  09 was cut in two - the
# scripts you may run yourself stayed on it, the ones the installer, the verbs,
# the uninstaller and SD itself run went to 09a.  Reading only 09 would have
# reported about half the tree as undocumented; reading only the first of them
# that happened to exist would have been worse, because it would have looked
# like a result.  Both are required to be present.
PAGES = [os.path.join('Administrator', 'markdown', '09-the-installed-scripts.md'),
         os.path.join('Administrator', 'markdown', '09a-scripts-sd-runs-itself.md')]

if not os.path.isdir(ROOT):
    sys.exit('scriptmap: no install at %s' % ROOT)

installed = sorted(n for n in os.listdir(ROOT) if n.lower().endswith('.ps1'))
if not installed:
    sys.exit('scriptmap: found no scripts at %s - that is not a result' % ROOT)

parts = []
for p in PAGES:
    full = os.path.join(HERE, p)
    if not os.path.exists(full):
        sys.exit('scriptmap: %s is missing - refusing to report a clean result' % p)
    parts.append(io.open(full, encoding='utf-8').read())
text = '\n'.join(parts)

# Names the page may mention that are NOT installed, with the reason.  These are
# build-tree scripts named to tell the reader where the boundary is.
NOT_SHIPPED = {
    'cycle.ps1': 'build tooling in sd4windows; named to say it does not ship',
    'assert-current.ps1': 'build tooling in sd4windows; named for the same reason',
}

# Installed scripts deliberately left undocumented, with the reason.
EXEMPT = {}


def evidenced(name):
    if re.search(r'`%s`' % re.escape(name), text):
        return True
    if re.search(r'^\s*%s\b' % re.escape(name), text, re.M):
        return True
    if re.search(r'\|\s*`?%s`?\s*\|' % re.escape(name), text):
        return True
    return False


mentioned = set(re.findall(r'[A-Za-z0-9_-]+\.ps1', text))

problems = []
documented = []

for name in installed:
    if name in EXEMPT:
        continue
    if evidenced(name):
        documented.append(name)
    else:
        problems.append(('NOT DOCUMENTED', name, 'is installed and on no page'))

for name in sorted(mentioned):
    if name in installed or name in NOT_SHIPPED:
        continue
    problems.append(('NOT INSTALLED', name,
                     'the page names it and it is not on the machine'))

print('install root  : %s' % ROOT)
print('installed     : %d script(s)' % len(installed))
print('documented    : %d' % len(documented))
print('exempt        : %d' % len(EXEMPT))
print('named, not shipped : %d' % len([n for n in mentioned if n in NOT_SHIPPED]))

if problems:
    print('')
    print('=== %d PROBLEM(S) ===' % len(problems))
    for kind, name, detail in problems:
        print('  %-15s %-26s %s' % (kind, name, detail))
    sys.exit(1)

print('')
print('scriptmap: every installed script is documented, and nothing else is claimed')
