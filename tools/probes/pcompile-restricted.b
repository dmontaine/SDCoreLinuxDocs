* pcompile-restricted.b - what BCOMP refuses to compile for an ordinary
* account.  Every line below is deliberate; the compiler's complaint is the
* measurement.  Line numbers in the listing map to the comment on each line.
*
* POSITIVE CONTROL first: if these do not compile, the run says nothing about
* the lines that follow.
      a = len('control')
      crt 'control ' : a
      b = system(18)
      c = oconv(date(), 'D4-')

* --- internal-only intrinsics (BCOMP int.intrinsics) ---
      v1 = kernel(28, 0)
      v2 = ospath('C:', 1)
      v3 = testlock(5)
      v4 = getlocks(0, 0)
      v5 = option('X')
      v6 = pterm(1, '')
      v7 = sdext(101, 'pw', 'salt')

* --- restricted statements (BCOMP restricted.statements) ---
      debug.on
      debug.off
      debug.set x to 1
      breakpoint 1, 2
      watch qq
      set.modes 0
      reset.modes 0
      remove.token
      release.lock 5

* --- errmsg: in BCOMP's statement table, no opcode behind it ---
      errmsg 'nothing'

* --- MATBUILD ... USING: the keyword compiles as a variable ---
      dim mm(3)
      mm(1) = 'a' ; mm(2) = 'b' ; mm(3) = 'c'
      matbuild s from mm using '-'

      crt 'never reached'
   end
