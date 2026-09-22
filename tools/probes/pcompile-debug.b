* pcompile-debug.b - the compile-time half of User document 17.  What the
* compiler says about the debugging statements when an ordinary account
* compiles them.  The listing is the measurement.
*
* POSITIVE CONTROL first.
      a = len('control')
      crt 'control ' : a

* --- DEBUG is NOT restricted: any account may write it.  Whether it does
*     anything depends on the DEBUGGING keyword on the BASIC command line.
      debug

* --- TRACE was removed from the compiler on 28 Jul 24 (BCOMP:2199 comment)
      trace

* --- restricted: internal programs only
      writepkt 'x'
      keyboard.input
      como on
      quit

* --- and one that is NOT restricted, as a contrast
      x = 1
      loop
      until x > 2
         x += 1
      repeat
      crt 'x=' : x

      crt 'end of probe'
   end
