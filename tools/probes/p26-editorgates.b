* p26-editorgates.b - what EDIT's three gates see, for User document 26.
*
* WHY THIS EXISTS RATHER THAN JUST TYPING "micro gpl.bp EDIT".  EDIT refuses a
* session with no terminal, and a piped session is supposed to be one - but
* "supposed to be" is the assumption, not the measurement.  If K$TTY is NOT
* empty down a pipe then micro launches, tries to draw on a pipe, and hangs the
* session; that costs a user-table slot and an elevated sd -cleanup.
*
* SO THE GATE IS READ BEFORE THE VERB IS TYPED.  This prints exactly what
* check.permitted will test, and nothing here can block.
      crt 'ZZMATH.START'
      crt 'ZZMATH.USERNO=' : @user.no

*  ---------------  gate 1: is there a terminal to draw on?
*
*  EDIT tests kernel(K$TTY, 0) and an ordinary program may not call kernel() at
*  all - it is a restricted intrinsic.  @tty is the same value for an ordinary
*  session: LOGIN's case statement assigns it from kernel(K$TTY, 0) for
*  anything that is not a phantom, a telnet session or a port.

      tty = @tty
      crt 'ZZMATH.AT.TTY=[' : tty : ']'
      crt 'ZZMATH.TTY.EMPTY=' : (tty = '')

*  ---------------  gate 3: the os.users record, read the way EDIT reads it

      ds = @ds
      os.rec = 'NO RECORD'
      openpath @sdsys : ds : 'os.users' to f then
         read os.rec from f, @logname else
            read os.rec from f, downcase(@logname) else
               read os.rec from f, upcase(@logname) else os.rec = 'NO RECORD'
            end
         end
         close f
      end else
         os.rec = 'NO FILE status=' : status()
      end

      crt 'ZZMATH.LOGNAME=' : @logname
      crt 'ZZMATH.OSUSERS.F1=[' : trim(os.rec<1>) : ']'
      crt 'ZZMATH.OSUSERS.F2=[' : trim(os.rec<2>) : ']'

*  ---------------  the verdict EDIT would reach

      begin case
         case tty = ''
            crt 'ZZMATH.VERDICT=REFUSED - no terminal'
         case downcase(trim(os.rec<2>, ' ', 'B')) = 'yes'
            crt 'ZZMATH.VERDICT=PERMITTED - os.users field 2'
         case 1
            crt 'ZZMATH.VERDICT=REFUSED - not in os.users'
      end case

      crt 'ZZMATH.END'
      stop
   end
