* p14-holder.b - session A for User document 14.  Takes an update lock on R1
* and task lock 7, signals that it is holding, waits for the contender to say
* it has finished measuring, then releases.  It never waits for ever: both
* rendezvous loops are bounded, so a contender that dies cannot leave this
* session pinned on the pipe.
      crt 'ZZHOLD.START'
      crt 'ZZHOLD.USERNO=' : @user.no

      open 'ZZLOCKF' to f else
         execute 'create.file zzlockf' capturing junk
         crt 'ZZHOLD.CREATE.SAID=[' : change(junk, @fm, ' | ') : ']'
         open 'ZZLOCKF' to f else
            crt 'ZZHOLD.NO.FILE status=' : status()
            crt 'ZZHOLD.END'
            stop
         end
      end

      clearfile f
      write 'alpha' to f, 'R1'
      write 'beta' to f, 'R2'

      readu rec from f, 'R1' else
         crt 'ZZHOLD.R1.MISSING'
      end
      crt 'ZZHOLD.SELF.RECORDLOCKED.R1=' : recordlocked(f, 'R1')
      crt 'ZZHOLD.SELF.RECORDLOCKED.R2=' : recordlocked(f, 'R2')

      lock 7 then
         crt 'ZZHOLD.TASKLOCK7=taken'
      end else
         crt 'ZZHOLD.TASKLOCK7=refused owner=' : status()
      end

      write @user.no to f, 'HOLDING'
      crt 'ZZHOLD.SIGNALLED'

      waited = 0
      loop
         read d from f, 'DONE' then exit
         nap 250
         waited += 1
      while waited < 160
      repeat
      crt 'ZZHOLD.WAITED.TICKS=' : waited

      release f, 'R1'
      unlock 7
      crt 'ZZHOLD.AFTER.RELEASE.RECORDLOCKED.R1=' : recordlocked(f, 'R1')
      write 'yes' to f, 'RELEASED'

      waited2 = 0
      loop
         read d from f, 'FINISHED' then exit
         nap 250
         waited2 += 1
      while waited2 < 120
      repeat
      crt 'ZZHOLD.WAITED2.TICKS=' : waited2

      close f
      crt 'ZZHOLD.END'
      stop
   end
