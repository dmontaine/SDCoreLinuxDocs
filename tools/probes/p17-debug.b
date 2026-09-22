* p17-debug.b - what a session can find out about debugging without entering
* the debugger.  The full screen debugger reads the keyboard, so a piped
* session cannot drive it; everything here is measurable from one.
*
* The DEBUG statement below is deliberate: this program is compiled WITHOUT
* the DEBUGGING keyword, and the claim being tested is that it therefore does
* nothing.  If that claim is wrong the session stops here and the END marker
* never prints, which is exactly what the null-case guard is for.
      crt 'ZZMATH.START'

      crt '--- can this session draw a full screen ---'
      crt 'tty=[' : @tty : '] len=' : len(@tty)
      sreg = terminfo('sreg')
      crt 'terminfo.sreg.len=' : len(sreg)
      crt 'terminfo.cup.len=' : len(terminfo('cup'))
      crt 'terminfo.clear.len=' : len(terminfo('clear'))
      crt 'term.type=[' : system(7) : ']'
      crt 'crtwide=' : @crtwide : ' crthigh=' : @crthigh
      crt 'is.phantom=' : system(25)
      crt 'break.key.enabled=' : system(23)

      crt '--- who has the debugger, per account ---'
      open 'VOC' to voc else
         crt 'NO VOC'
         crt 'ZZMATH.END'
         stop
      end
      names = 'debug' : @fm : 'debugging' : @fm : 'pdebug' : @fm : 'basic' : @fm : 'run'
      n = dcount(names, @fm)
      for i = 1 to n
         nm = names<i>
         read r from voc, nm then
            crt 'voc[' : nm : ']=[' : change(r, @fm, ' | ') : ']'
         end else
            crt 'voc[' : nm : ']=NOT IN THIS ACCOUNT'
         end
      next i
      close voc

      crt '--- the call stack, which is what STACK shows in the debugger ---'
      cs = system(1002)
      crt 'call.stack.fields=' : dcount(cs, @fm)
      crt 'call.stack=[' : change(cs, @fm, ' | ') : ']'
      gosub deeper
      crt 'internal.subroutine.depth.at.top=' : system(1029)

      crt '--- STATUS() and OS.ERROR() after a failure ---'
      open 'NOSUCHFILE' to nf then
         crt 'unexpected open'
      end else
         crt 'open.failed.status=' : status() : ' os.error=' : os.error()
      end

      crt '--- the DEBUG statement, compiled without DEBUGGING ---'
      crt 'before.debug.statement'
      debug
      crt 'after.debug.statement - the program is still running'

      crt 'ZZMATH.END'
      stop

deeper:
      crt 'internal.subroutine.depth.inside.gosub=' : system(1029)
      crt 'call.stack.inside=[' : change(system(1002), @fm, ' | ') : ']'
      return
   end
