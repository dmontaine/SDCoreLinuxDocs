* p30-processes.b - PSTAT levels and PDUMP, for User document 30.
*
* WHY A PROBE AND NOT sdtcl.  Both verbs take a user number, and the number
* changes every session, so it cannot be written into a command list; @user.no
* is the only way to name "me".  And PSTAT is much more interesting run from
* inside a program than from the TCL prompt - at the prompt the only thing on
* the call stack is PSTAT itself, so the levels that report a call stack have
* nothing to report.  Here there is a program, a subroutine and CPROC beneath
* them, which is what the levels are for.
*
* WHAT THIS DOES NOT COVER, said rather than left to be assumed: PHANTOM and
* PDEBUG are NOT here and must not be added.  A phantom child inherits the
* pipe a scripted session is fed down, so the job never completes even after
* the parent exits - measured 24 Aug 2026 and it cost two sd.exe processes.
* PDEBUG is worse: it polls keyready()/keyin(), so down a pipe it eats the
* commands that have not run yet.  Both are described from source.
      crt 'ZZMATH.START'
      crt 'ZZMATH.USERNO=' : @user.no

      gosub one.level.down

      crt 'ZZMATH.END'
      stop

one.level.down:

*  ---------------  PSTAT at each level, seen from inside a call

      execute 'pstat user ' : @user.no capturing out
      crt 'ZZMATH.PSTAT0.START'
      crt change(out, @fm, char(10))
      crt 'ZZMATH.PSTAT0.END'

      execute 'pstat user ' : @user.no : ' level 1' capturing out
      crt 'ZZMATH.PSTAT1.START'
      crt change(out, @fm, char(10))
      crt 'ZZMATH.PSTAT1.END'

      execute 'pstat user ' : @user.no : ' level 3' capturing out
      crt 'ZZMATH.PSTAT3.START'
      crt change(out, @fm, char(10))
      crt 'ZZMATH.PSTAT3.END'

*  ---------------  PDUMP of this process
*
*  The dump is an EVENT, not a call: PDUMP sets a flag and the target process
*  writes the file at its next event check.  For a process dumping itself that
*  is after the EXECUTE has returned, so the "Dumping process state as ..."
*  line lands in the transcript rather than in the capture, and BOTH are
*  printed here so it is obvious which said what.

      execute 'pdump ' : @user.no capturing out
      crt 'ZZMATH.PDUMP.CAPTURED=[' : change(out, @fm, ' | ') : ']'
      crt 'ZZMATH.PDUMP.RETURN=' : @system.return.code
      nap 500
      crt 'ZZMATH.PDUMP.DONE'

*  ---------------  LISTU and STATUS from a program

      execute 'listu' capturing out
      crt 'ZZMATH.LISTU.START'
      crt change(out, @fm, char(10))
      crt 'ZZMATH.LISTU.END'

      execute 'status' capturing out
      crt 'ZZMATH.STATUS=[' : change(out, @fm, ' | ') : ']'

      return
   end
