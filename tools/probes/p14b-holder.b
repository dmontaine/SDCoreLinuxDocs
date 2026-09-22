* p14b-holder.b - session A, phase 2.  Completes the RECORDLOCKED() table by
* holding the two lock kinds phase 1 did not: a shared READL lock, then a whole
* FILELOCK.
*
* THE SIGNALS LIVE IN A SECOND FILE ON PURPOSE.  A FILELOCK on the data file
* blocks the other session's writes to it too, so a rendezvous record inside
* the locked file deadlocks the pair: each waits for a write the other cannot
* make.  ZZLOCKG carries the signals and is never locked.
      crt 'ZZHOLD.START'
      crt 'ZZHOLD.USERNO=' : @user.no

      open 'ZZLOCKF' to f else
         crt 'ZZHOLD.NO.DATA.FILE status=' : status()
         crt 'ZZHOLD.END'
         stop
      end
      open 'ZZLOCKG' to g else
         execute 'create.file zzlockg' capturing junk
         crt 'ZZHOLD.CREATE.SAID=[' : change(junk, @fm, ' | ') : ']'
         open 'ZZLOCKG' to g else
            crt 'ZZHOLD.NO.SIGNAL.FILE status=' : status()
            crt 'ZZHOLD.END'
            stop
         end
      end

      clearfile f
      clearfile g
      write 'alpha' to f, 'R1'
      write 'beta' to f, 'R2'

      crt '--- phase 1: a shared READL lock ---'
      readl rec from f, 'R1' else
         crt 'ZZHOLD.R1.MISSING'
      end
      crt 'ZZHOLD.SELF.READL.R1=' : recordlocked(f, 'R1')
      write @user.no to g, 'HOLDING'

      waited = 0
      loop
         read d from g, 'DONE1' then exit
         nap 250
         waited += 1
      while waited < 160
      repeat
      crt 'ZZHOLD.WAITED1.TICKS=' : waited
      release f, 'R1'
      crt 'ZZHOLD.AFTER.READL.RELEASE=' : recordlocked(f, 'R1')

      crt '--- phase 2: a whole FILELOCK ---'
* RECORDLOCKED() = 3 is LOCK$MY.FILELOCK, so it is the direct test of whether
* this session got the file lock.  FILELOCK itself reports nothing on success.
      got = @false
      tries = 0
      loop
      until got or tries >= 40
         filelock f locked
            nap 250
         end
         tries += 1
         if recordlocked(f, 'R1') = 3 then got = @true
      repeat
      crt 'ZZHOLD.FILELOCK.TRIES=' : tries
      crt 'ZZHOLD.SELF.FILELOCK.R1=' : recordlocked(f, 'R1')
      crt 'ZZHOLD.SELF.FILELOCK.R2=' : recordlocked(f, 'R2')
      write @user.no to g, 'HOLDING2'

      waited = 0
      loop
         read d from g, 'DONE2' then exit
         nap 250
         waited += 1
      while waited < 160
      repeat
      crt 'ZZHOLD.WAITED2.TICKS=' : waited

      fileunlock f
      crt 'ZZHOLD.AFTER.FILEUNLOCK=' : recordlocked(f, 'R1')
      write 'yes' to g, 'RELEASED'

      waited = 0
      loop
         read d from g, 'FINISHED' then exit
         nap 250
         waited += 1
      while waited < 120
      repeat
      crt 'ZZHOLD.WAITED3.TICKS=' : waited

      close f
      close g
      crt 'ZZHOLD.END'
      stop
   end
