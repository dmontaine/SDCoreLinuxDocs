* p18-objects.b - using the class, and local subroutines and functions.
*
* Run with sdprobe.ps1 AFTER p18-class-base.b and p18-class.b are compiled and
* privately catalogued as ZZBASE and ZZCLS.  tools\probes\README.md says so.
*
* IT REFUSES THE NULL CASE by printing objinfo(o,0) before it uses the object:
* every -> call below would fail loudly on a non-object, but a run that never
* created one at all could otherwise look like a tidy set of blanks.
*  A LOCAL FUNCTION MUST BE DECLARED BEFORE IT IS USED and a local
*  subroutine need not be.  Measured: without these two lines the compiler
*  reads doubled(21) as a matrix reference and gives
*  "Data item or constant not found where expected" plus "Matrix DOUBLED is
*  not referenced in a DIM statement".  gpl.bp/DEBUG:47 does the same thing.
   deffun doubled(n) local
   deffun peek() local

      crt 'ZZMATH.START'

*  ---------------  create an instance

      o = object('ZZCLS')
      crt 'ZZMATH.ISOBJ=' : objinfo(o, 0)
      crt 'ZZMATH.CLASS=' : objinfo(o, 1)

*  ---------------  a public subroutine, twice

      o->deposit(40)
      o->deposit(2)

*  ---------------  a public function

      crt 'ZZMATH.TOTAL.X1=' : o->total(1)
      crt 'ZZMATH.TOTAL.X10=' : o->total(10)

*  ---------------  a public member variable, read and written directly

      crt 'ZZMATH.LABEL.INITIAL=' : o->label
      o->label = 'Direct'
      crt 'ZZMATH.LABEL.AFTER=' : o->label

*  ---------------  the GET/SET property: written like a variable, and the
*  SET routine changes what the GET routine later reports

      o->owner = 'MIXED Case Name'
      crt 'ZZMATH.OWNER=' : o->owner
      crt 'ZZMATH.LABEL.AFTER.SET=' : o->label

*  ---------------  inheritance, from the INHERITS clause on the CLASS line

      crt 'ZZMATH.WHOAMI=' : o->whoami()
      crt 'ZZMATH.TAG=' : o->tag
      crt 'ZZMATH.REVEAL=' : o->reveal()

*  ---------------  local subroutines and functions, called like external ones
*
*  REACHING A PRIVATE MEMBER FROM OUTSIDE IS NOT TESTED HERE ON PURPOSE: it
*  is a runtime abort, which would take the rest of the run with it.  It is
*  measured separately with sdcompile.ps1 -ExpectErrors.

      shared.probe = 'set in the main program'

*  A LOCAL SUBROUTINE IS REACHED WITH gosub name(args), NOT WITH call.
*  Measured: call tally(3,4,answer) compiles and then fails at run time with
*  "Unable to load 'TALLY' object code" - call looks in the catalogue.
*  gpl.bp/DEBUG:145 uses the gosub form.
      gosub tally(3, 4, answer)
      crt 'ZZMATH.LOCAL.SUB=' : answer
      crt 'ZZMATH.LOCAL.FUNC=' : doubled(21)
      crt 'ZZMATH.LOCAL.SEES.MAIN=' : peek()

*  ---------------  what does PRIVATE inside a local routine actually scope?
*  tally set 'working' and took an argument named 'a'.  If either leaks, the
*  main program can see it.  ASKED, not asserted.

      crt 'ZZMATH.PRIVATE.LEAKED=' : assigned(working)
      crt 'ZZMATH.ARGNAME.LEAKED=' : assigned(a)

*  ---------------  releasing the object runs DESTROY.OBJECT

      crt 'ZZMATH.BEFORE.UNLOAD'
      o = ''
      crt 'ZZMATH.AFTER.UNLOAD'

      crt 'ZZMATH.END'

*  ---------------  AFTER THE END MARKER, because it aborts.
*  Reaching a private member from outside the class.  The measurement above
*  is banked before this is attempted - PROJECT_STATUS section 6's pattern.

      p = object('ZZCLS')
      crt 'ZZMATH.AFTER.END.PRIVATE.NEXT'
      crt p->balance
      crt 'ZZMATH.AFTER.END.PRIVATE.REACHED'
      stop

*  ======================================================================
*  Local routines.  They live in this program, are not catalogued, and are
*  called exactly as an external subroutine or function would be.

*  THE return IS NOT OPTIONAL.  Measured: without it this routine falls into
*  its own end, which BCOMP emits as OP.STOP, and the whole program stops
*  silently - no error, no further output, and the object's DESTROY.OBJECT
*  still runs, so it looks like a clean finish.  gpl.bp/DEBUG's five local
*  subroutines all carry an explicit return.
   local subroutine tally(a, b, result)
      private working
      working = a + b
      result = working
      return
   end

   local function doubled(n)
      return n * 2
   end

*  Does a local routine share the main program's variables?  ASKED, not
*  asserted: assigned() answers 0 for a name this routine has never set,
*  without the runtime error that reading it would raise.
   local function peek()
      return 'assigned(shared.probe)=' : assigned(shared.probe)
   end

end
