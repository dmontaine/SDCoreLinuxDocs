#
# docmap.py <gpl.bp/BCOMP>
#
# Assign every name BCOMP accepts to exactly one User-set document, and report
# what is unassigned or assigned twice.  The point is that a document set which
# quietly misses a function must fail this rather than look finished.
#
import re
import sys

BCOMP = sys.argv[1]
src = open(BCOMP, 'r', encoding='latin-1', newline='').read()

TABLES = ['statements', 'non.debug.statements', 'restricted.statements',
          'reserved.names', 'intrinsics']
WORD = re.compile(r'"([A-Z][A-Z0-9.$]*)"')

tables = {}
for name in TABLES:
    got = set()
    for line in src.split('\n'):
        s = line.strip()
        if s.startswith('*'):
            continue
        if re.match(re.escape(name) + r'\s*(<[^>]*>)?\s*:?=', s):
            got.update(WORD.findall(s))
    if not got:
        sys.exit('EMPTY table %s - refusing to report' % name)
    tables[name] = got

everything = set()
for t in TABLES:
    everything |= tables[t]

DOCS = {
 '01 Program Structure': """
   PROGRAM SUBROUTINE SUB FUNCTION COMMON COM
   CLEARCOMMON DELETE.COMMON EQUATE EQU INCLUDE DIM DIMENSION MAT MATBUILD
   MATPARSE INMAT CLEAR END VOID CALL CALLV SUBR CATALOGUED ARG ARG.COUNT
   SET.ARG ASSIGNED UNASSIGNED SET.UNASSIGNED VARTYPE RETURN VARSET
 """,
 # 18 is the modern half of program structure: everything that gives a name a
 # scope, and everything to do with objects.  These were all assigned to 01
 # until 27 Aug 2026, which is why docmap reported 411 of 411 while page 01
 # covered them in eight lines and three of its sentences were wrong.
 '18 Modern Program Structure': """
   CLASS PUBLIC PRIVATE LOCAL DEFFUN
   OBJECT OBJINFO INHERIT DISINHERIT UNLOAD.OBJECT GET SET
 """,
 '02 Program Control': """
   IF ELSE THEN CASE BEGIN FOR NEXT STEP TO LOOP REPEAT WHILE UNTIL DO
   CONTINUE EXIT GO GOTO GOSUB ON BREAK ABORT STOP CHAIN ENTER EXECUTE PERFORM
   RUN QUIT SET.EXIT.STATUS SLEEP NAP RQM PAUSE WAKE REM REMARK NULL
   SET.BREAK.HANDLER REMOVE.BREAK.HANDLER CAPTURING RETURNING PASSLIST RTNLIST
   CURRENT.LEVEL TRAPPING SET.STATUS
 """,
 # 05 was cut in two when it went over the length the pages are kept under.
 # Reading and changing a piece stayed; everything that operates on the array
 # as a whole went to 05a.  The label is what tells a reader where to look, so
 # it is split with the page rather than left naming a page half the names are
 # no longer on.
 '05 Dynamic Arrays': """
   EXTRACT INSERT DELETE REPLACE LOCATE DEL INS FIND FINDSTR DCOUNT
   BEFORE IN SETTING FROM
 """,
 '05a Operating on Whole Arrays': """
   REMOVE RAISE LOWER VSLICE REUSE SPLICE SUBSTRINGS FIELDSTORE GETREM SETREM
   ANDS ORS NOTS NOT EQS NES GTS GES LTS LES IFS CATS COUNTS LENS NUMS
   ABSS NEGS MODS TRIMS TRIMBS TRIMFS SOUNDEXS SPACES STRS FMTS ICONVS OCONVS
   FOLDS INDEXS FIELDS SUBSTITUTE SWAP MARK.MAPPING SORTINIT SORTADD SORTCLEAR
   MAXIMUM MINIMUM SUM SUMMATION
 """,
 '06 Data Conversion': """
   ICONV OCONV FMT XTD DTX CHAR SEQ ASCII EBCDIC ITYPE DPARSE CONVERT
   SETNLS GETNLS PRECISION PWR PRINTERR
 """,
 '07 File Handling': """
   OPEN OPENPATH CLOSE READ READL READU READV READVL READVU WRITE WRITEU
   WRITEV WRITEVU DELETE DELETEU MATREAD MATREADL MATREADU MATWRITE MATWRITEU
   CLEARFILE CREATE.FILE CREATE CONFIGURE.FILE FILEINFO FILE OUTERJOIN TRANS
   RTRANS XLATE RECORDLOCKED RECORDLOCKL RECORDLOCKU FILELOCK FILEUNLOCK LOCK
   UNLOCK RELEASE RELEASE.LOCK TRANSACTION COMMIT ROLLBACK SET.TRIGGER
   FLUSH DIR MODIFY LOCKED OVERWRITE READONLY WAITING FROM
 """,
 '08 Select Lists': """
   SELECT SSELECT SELECTE SELECTN SELECTV SELECTINDEX SELECTINFO SELECTLEFT
   SELECTRIGHT SETLEFT SETRIGHT READNEXT READLIST SAVELIST DELETELIST GETLIST
   FORMLIST CLEARSELECT LISTINDEX INDICES BY
 """,
 '09 Alternate Key Indexes': """
   AKCLEAR AKDELETE AKENABLE AKREAD AKRELEASE AKWRITE CREATE.AK DELETE.AK
 """,
 '10 Sequential Files': """
   OPENSEQ READSEQ WRITESEQ WRITESEQF CLOSESEQ SEEK WEOFSEQ READBLK WRITEBLK
   NOBUF DELETESEQ TIMEOUT REWIND STATUS APPEND OVERWRITE READONLY
 """,
 '11 CSV Files': """
   READCSV WRITECSV INPUTCSV PRINTCSV MATREADCSV DPARSE.CSV CSVDQ
 """,
 '12 Terminal Input and Output': """
   PRINT CRT DISPLAY INPUT INPUTFIELD INPUTCLEAR INPUTERR INPUTBLK KEYIN KEYINC
   KEYINR KEYCODE KEYREADY KEYEDIT KEYEXIT KEYTRAP KEYBOARD.INPUT HEADING
   FOOTING PAGE PROMPT ECHO CLEARINPUT CLEARDATA DATA TCLREAD TERMINFO BINDKEY
   SAVE.SCREEN RESTORE.SCREEN COL1 COL2 PANNING HIDDEN NOCASEINVERT
   GET.PORT.PARAMS SET.PORT.PARAMS APPEND EDIT OVERLAY UPCASE
 """,
 '13 Printing': """
   PRINTER PRINTER.SETTING SETPU GETPU HUSH COMO FOOTING
 """,
# 14 carries no names of its own on purpose.  Every lock and transaction name
# is introduced in 07 File Handling, which is where a reader meets them; 14 is
# the deeper treatment - what the OTHER session sees - and assigning the names
# twice would only defeat the duplicate check.  TESTLOCK and GETLOCKS belong to
# it and are absent from the roster because they are internal-only intrinsics,
# which BCOMP keeps in a separate table this script does not read.
 '14 Locks and Transactions': """
 """,
 '15 Sockets': """
   OPEN.SOCKET CLOSE.SOCKET READ.SOCKET WRITE.SOCKET CREATE.SERVER.SOCKET
   ACCEPT.SOCKET.CONNECTION SET.SOCKET.MODE SOCKET.INFO SERVER.ADDR WRITEPKT
 """,
 '16 System and Environment': """
   SYSTEM CONFIG ENV DATE TIME TIMEDATE SYSMSG GET.MESSAGES ADD COMPARE
 """,
 '16a Status, Encryption and the Machine': """
   STATUS OS.ERROR OS.EXECUTE SENDMAIL UMASK CHGPHANT SENTENCE CHECKSUM
   SDENCRYPT SDDECRYPT CCALL REMOVE.TOKEN RESET.MODES SET.MODES ERRMSG
   PROCREAD PROCWRITE LOGMSG SET.EXIT.STATUS
 """,
 '17 Debugging': """
   DEBUG DEBUG.ON DEBUG.OFF DEBUG.SET BREAKPOINT WATCH
 """,
 '04 String Functions': """
   LEN INDEX COUNT FIELD TRIM TRIMB TRIMF CROP SPACE STR UPCASE DOWNCASE
   SWAPCASE FOLD
 """,
 '04a String Matching and Replacing': """
   CHANGE COMPARE ALPHA MATCHFIELD QUOTE DQUOTE SQUOTE SOUNDEX
 """,
 '03 Math Functions': """
   ABS ACOS ASIN ATAN COS SIN TAN EXP LN SQRT INT MOD DIV IDIV RDIV REM NEG
   RND RANDOMIZE
 """,
 '03a Numeric Tests and Formatting': """
   MAX MIN NUM BITAND BITNOT BITOR BITRESET BITSET BITTEST BITXOR SHIFT
 """,
}

# Documents not yet written; named here so the coverage report can tell "later"
# from "missed".  All seventeen categories are written as of 26 Aug 2026, so it
# is empty - it stays because a new category would start life in it.
#
# THE RESTRICTED NAMES ARE STILL ASSIGNED TO USER DOCUMENTS HERE, ON PURPOSE.
# The owner moved them off the User SYNTAX CARD on 26 Aug 2026 and into the
# Technical set; the User pages that DESCRIBE them - 09 is nothing else, 13,
# 16, 17 in part - still do, so this script is still telling the truth about
# where each name is explained.  If those pages move too, move the names here
# with them.
#
# 18 SYNTAX IS DELIBERATELY NOT HERE.  It is not a category: it is one
# alphabetical run of EVERY name, so listing it would assign all 411 twice and
# defeat the duplicate check this script exists for.  Its own completeness is
# checked by tools/mksyntax.py, which refuses to write the page if a single
# name accepted by BCOMP has no line on it.
LATER = {}

# Names that legitimately belong in more than one document, because the
# language really does use one word for two things.  Listed explicitly so that
# an ACCIDENTAL double assignment is still reported.
SHARED = set("""
  DELETE FOOTING STATUS SET.EXIT.STATUS COMPARE REM FROM SETTING IN
  OVERWRITE READONLY APPEND UPCASE
""".split())

assigned = {}
dupes = []
for group in (DOCS, LATER):
    for doc, names in group.items():
        for n in names.split():
            if n in assigned and n not in SHARED:
                dupes.append((n, assigned[n], doc))
            assigned[n] = doc

known = set(assigned)
missing = sorted(everything - known)
bogus = sorted(known - everything)

print('BCOMP accepts        : %d name(s)' % len(everything))
print('assigned to a document: %d name(s)' % len(known & everything))
print()
if dupes:
    print('=== ASSIGNED TWICE (%d) ===' % len(dupes))
    for n, a, b in dupes:
        print('  %-24s %s  AND  %s' % (n, a, b))
    print()
if bogus:
    print('=== ASSIGNED BUT NOT ACCEPTED BY BCOMP (%d) - typo or removed ===' % len(bogus))
    print('  ' + ' '.join(bogus))
    print()
print('=== ACCEPTED BY BCOMP, ASSIGNED NOWHERE (%d) ===' % len(missing))
print('  ' + ' '.join(missing) if missing else '  none')
print()
for doc in sorted(DOCS):
    names = sorted(n for n in DOCS[doc].split() if n in everything)
    print('%-26s %3d name(s)' % (doc, len(names)))
sys.exit(1 if (missing or dupes or bogus) else 0)
