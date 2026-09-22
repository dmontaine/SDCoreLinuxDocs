#
# normalise_emphasis.py [--apply]
#
# Turn the documentation's inherited shouting into ordinary professional
# emphasis, across all four sets.
#
# ***WHY THIS IS A SCRIPT AND NOT A HAND EDIT.***  CLAUDE.md's rule is that a
# file edit goes through the editing tools, and that a transform too large to do
# by hand is said out loud first, put in a file rather than inline, and checked
# afterwards for BOM, CR count, mojibake and diff size.  This is that case: 591
# ***...*** spans across 59 files, 235 of them fully capitalised.
#
# WHAT IT DOES, AND IT IS ONE RULE:
#
#   ***ANY SPAN***  ->  **Any span**
#
# No *** survives.  A span that was capitalised is lowered to sentence case; a
# span that was already mixed case simply loses the italic.  The owner's
# instruction, 4 Sep 2026: plain professional prose, with warnings kept as "a
# short bold lead sentence" rather than a capitalised shout.
#
# ***THE CANONICAL SPELLINGS ARE HARVESTED, NOT TYPED, AND THAT IS THE PART
# WORTH READING.***  Lowering "THE SD API REFUSES A UAC PROMPT" needs to know
# that SD, API and UAC keep their capitals and THE does not.  A hand-typed list
# of proper nouns would be wrong the first time somebody added a page.
#
# So the script reads every word in the corpus that is NOT inside a capitalised
# span, and records how each spelling appears in ordinary prose.  A word inside
# a capitalised span is then restored to the spelling the rest of the
# documentation uses - "SD" stays SD because the prose says SD, "ssh" becomes
# lower case because the prose says ssh.  Words with no evidence either way are
# lowered, which is the safe direction: a missed capital is a typo, an invented
# one is a false claim about a name.
#
# BACKTICKED SPANS ARE UNTOUCHED.  `APILOGIN` is a parameter name and its case
# is the product's, not the prose's.
#
# It prints a report and changes nothing unless --apply is given.
#
import io
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETS = ('GettingStarted', 'User', 'Administrator')
APPLY = '--apply' in sys.argv

SPAN = re.compile(r'\*\*\*(.+?)\*\*\*', re.S)
CODE = re.compile(r'`[^`]*`')
WORD = re.compile(r"[A-Za-z][A-Za-z0-9./_-]*'?[A-Za-z]?")

# Spellings the corpus cannot settle, because they appear only inside shouted
# spans or not at all in prose.  Each one is a name, not a preference.
OVERRIDE = {
    'SD': 'SD', 'SDSYS': 'SDSYS', 'VOC': 'VOC', 'NEWVOC': 'NEWVOC',
    'TCL': 'TCL', 'BASIC': 'BASIC', 'API': 'API', 'UAC': 'UAC',
    'ACL': 'ACL', 'ACLS': 'ACLs', 'DLL': 'DLL', 'DLLS': 'DLLs',
    'CSV': 'CSV', 'POSIX': 'POSIX', 'GPL': 'GPL', 'PDF': 'PDF',
    'HTML': 'HTML', 'PATH': 'PATH', 'RDP': 'RDP', 'SCRAM': 'SCRAM',
    'OPENQM': 'OpenQM', 'SCARLETDME': 'ScarletDME', 'OPENSSH': 'OpenSSH',
    'POWERSHELL': 'PowerShell', 'WINDOWS': 'Windows', 'MICROSOFT': 'Microsoft',
    'EXCEL': 'Excel', 'NOTEPAD': 'Notepad', 'PICK': 'Pick',
    'MULTIVALUE': 'MultiValue', 'LOCALSYSTEM': 'LocalSystem',
    'SSH': 'ssh', 'SCP': 'scp', 'SFTP': 'sftp', 'SSHD': 'sshd',
    'CR': 'CR', 'LF': 'LF', 'CRLF': 'CRLF', 'BOM': 'BOM',
    'KB': 'KB', 'MB': 'MB', 'GB': 'GB', 'ID': 'id', 'IDS': 'ids',
    'OS': 'operating system',
    'PROC': 'PROC', 'SDCLIENT': 'SDClient', 'SDBASIC': 'SDBasic',
    'INNO': 'Inno', 'WSUS': 'WSUS',
}
# ***THREE ENTRIES WERE REMOVED FROM THE LIST ABOVE AFTER THE FIRST RUN, AND
# EACH ONE IS A LESSON ABOUT OVERRIDE LISTS.***
#   'A': 'a'       - the article.  Eight spans open with "A PROGRAM'S ...", and
#                    forcing the override's lower-case form defeated the
#                    sentence-initial capital, producing "**a program's ...**".
#   'I': 'I'       - same shape, and no span actually needs it.
#   'SYSTEM'       - it means Windows' SYSTEM account in some places and "the
#                    system account" in others, and the list cannot tell them
#                    apart.  The corpus can: prose says "system account".
# The rule this leaves behind: an override earns its place only when the word
# has ONE right spelling everywhere it occurs.

# Names that are genuinely lower case even at the start of a sentence.
ALWAYS_LOWER = {'ssh', 'scp', 'sftp', 'sshd'}


def strip_code(text):
    return CODE.sub(' ', text)


def is_shout(s):
    letters = [c for c in strip_code(s) if c.isalpha()]
    return bool(letters) and all(c.isupper() for c in letters)


# ---------------------------------------------------- harvest the prose forms

prose = Counter()
files = []
for s in SETS:
    d = os.path.join(HERE, s, 'markdown')
    if not os.path.isdir(d):
        continue
    for name in sorted(os.listdir(d)):
        if name.endswith('.md'):
            files.append(os.path.join(d, name))

for path in files:
    text = io.open(path, encoding='utf-8').read()
    # Everything that is NOT a shouted span, and not code, is prose evidence.
    plain = SPAN.sub(lambda m: '' if is_shout(m.group(1)) else m.group(1), text)
    plain = strip_code(plain)
    for w in WORD.findall(plain):
        prose[w] += 1

canonical = {}
for word, n in prose.items():
    key = word.upper()
    # Prefer the most common spelling that is not itself all upper case, so a
    # word shouted in prose does not vote for its own shouted form.
    if key not in canonical or n > canonical[key][1]:
        if not (word.isupper() and len(word) > 1):
            canonical[key] = (word, n)


def spell(word, first):
    key = word.upper()
    if key in OVERRIDE:
        out = OVERRIDE[key]
    elif key in canonical:
        out = canonical[key][0]
    else:
        out = word.lower()
    # Sentence-initial capital, unless the word is a name that is genuinely
    # lower case.  This runs AFTER the override, so an override supplying a
    # lower-case ordinary word (the article "a", once) is still capitalised
    # here rather than defeating the capital.
    if first and out[:1].islower() and out.split()[0] not in ALWAYS_LOWER:
        out = out[:1].upper() + out[1:]
    return out


def lower_span(s):
    """Sentence-case a shouted span, leaving backticked code alone."""
    parts = re.split(r'(`[^`]*`)', s)
    seen_word = False
    for i, part in enumerate(parts):
        if part.startswith('`'):
            if part.strip('`').strip():
                seen_word = True
            continue
        out = []
        pos = 0
        for m in WORD.finditer(part):
            out.append(part[pos:m.start()])
            first = not seen_word
            out.append(spell(m.group(0), first))
            seen_word = True
            pos = m.end()
        out.append(part[pos:])
        parts[i] = ''.join(out)
    return ''.join(parts)


# ------------------------------------------------------------------ transform

shouted = 0
plainbold = 0
changed = []

for path in files:
    text = io.open(path, encoding='utf-8', newline='').read()
    counts = [0, 0]

    def repl(m):
        body = m.group(1)
        if is_shout(body):
            counts[0] += 1
            return '**' + lower_span(body) + '**'
        counts[1] += 1
        return '**' + body + '**'

    new = SPAN.sub(repl, text)
    shouted += counts[0]
    plainbold += counts[1]
    if new != text:
        changed.append((path, counts[0], counts[1]))
        if APPLY:
            io.open(path, 'w', encoding='utf-8', newline='').write(new)

print('files scanned      : %d' % len(files))
print('files changed      : %d' % len(changed))
print('shouted spans       : %d  -> sentence case, bold' % shouted)
print('mixed-case spans    : %d  -> bold, italic dropped' % plainbold)
print('prose spellings learned : %d' % len(canonical))
print('')
for path, a, b in changed:
    print('  %-52s %3d shouted %3d bold' % (os.path.relpath(path, HERE), a, b))
if not APPLY:
    print('')
    print('DRY RUN - nothing written.  Re-run with --apply.')
