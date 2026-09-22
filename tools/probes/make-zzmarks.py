"""Write ZZMARKS into an account's BP: a fixture for the one editor test that
cannot be done down a pipe.

WHY IT EXISTS.  PROJECT_STATUS item 5.3 says to type "micro gpl.bp EDIT" from
an unelevated console.  That command cannot work: gpl.bp does not resolve in a
user account - measured, "File not found" - so it needs LOGTO SDSYS, which needs
elevation, which is the opposite of what the item is testing.  The runnable form
is "micro bp <record>" in the user's own account.

AND THE RECORD IS CHOSEN TO TEST THE RISKY PART.  Opening any old source proves
micro draws.  It does not prove the thing that would silently destroy a user's
data: EDIT converts value, subvalue and text marks to ~ tokens on the way out
and back on the way in, and a mistake there corrupts the record without saying
so.  This fixture carries all five token cases plus the two escapes, so quitting
WITHOUT SAVING must leave the record byte-identical, and saving unchanged must
too.

It is written as bytes, not text: the marks are real 0xFD/0xFC/0xFB characters
and a text-mode write would mangle both those and the line endings.
"""

import io
import os
import sys

VM = b'\xfd'   # value mark
SM = b'\xfc'   # subvalue mark
TM = b'\xfb'   # text mark

account = sys.argv[1] if len(sys.argv) > 1 else 'don'
bp = os.path.join(os.environ['ProgramData'], 'SD', 'user_accounts', account, 'bp')
dest = os.path.join(bp, 'ZZMARKS')

lines = [
 b"* ZZMARKS - the fixture for the screen-editor round trip.  See",
 b"* tools/probes/make-zzmarks.py for why this record looks like this.",
 b"*",
 b"* EVERY LINE BELOW CONTAINS SOMETHING EDIT HAS TO CONVERT AND CONVERT BACK.",
 b"* Open it with 'micro bp ZZMARKS', look at it, quit WITHOUT saving, and the",
 b"* record must come back byte for byte.  Then open it again, save unchanged,",
 b"* and it must still come back byte for byte.  Anything else is data loss.",
 b"      a = 'value mark here:" + VM + b"end'",
 b"      b = 'subvalue mark here:" + SM + b"end'",
 b"      c = 'text mark here:" + TM + b"end'",
 b"      d = 'two marks running:" + VM + VM + b"end'",
 b"      e = 'mark comma mark:" + TM + b"," + TM + VM + b"end'",
 b"      f = 'a literal tilde: a~b, and a doubled one: a~~b'",
 b"      g = 'tilde before a mark: a~" + VM + b"b'",
 b"      h = 'backtick before a mark: `" + VM + b"'",
 b"      i = 'the token strings themselves: ~~  ~`  ~!  ~-  ~,'",
 b"      j = 'a lone bang a!b and a lone comma a,b'",
 b"      crt a : b : c : d : e : f : g : h : i : j",
 b"   end",
]

blob = b'\n'.join(lines) + b'\n'

if not os.path.isdir(bp):
    sys.exit('no bp directory at %s' % bp)

with io.open(dest, 'wb') as f:
    f.write(blob)

print('wrote   : %s' % dest)
print('bytes   : %d' % len(blob))
print('marks   : VM=%d SM=%d TM=%d'
      % (blob.count(VM), blob.count(SM), blob.count(TM)))
print('tildes  : %d' % blob.count(b'~'))
if not (blob.count(VM) and blob.count(SM) and blob.count(TM) and blob.count(b'~')):
    sys.exit('REFUSED: the fixture is missing one of the things it exists to test')
import hashlib
print('sha256  : %s' % hashlib.sha256(blob).hexdigest()[:32].upper())
