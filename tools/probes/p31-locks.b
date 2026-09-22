* p31-locks.b - what LIST.READU actually prints, for User document 31.
*
* One session is enough for this one.  getlocks() reports every lock in the
* system including the caller's own, so a session that takes an update lock, a
* read lock and then a file lock can run LIST.READU against itself and see all
* four lock types the report can print.  The two-session rig (sdprobe2) is for
* CONTENTION, which is a different question and is measured on document 14.
*
* IT REFUSES ITS OWN RESULT IF NOTHING WAS LOCKED.  recordlocked() is checked
* before each listing is captured: a LIST.READU that says "no active locks"
* because the lock was never taken is a tidy negative that looks like a
* finding, and this prints the lock state beside it so that cannot pass.
      crt 'ZZMATH.START'
      crt 'ZZMATH.USERNO=' : @user.no

      open 'ZZLK31A' to f else
         execute 'create.file zzlk31a' capturing junk
         crt 'ZZMATH.CREATE.SAID=[' : change(junk, @fm, ' | ') : ']'
         open 'ZZLK31A' to f else
            crt 'ZZMATH.NO.FILE status=' : status()
            crt 'ZZMATH.END'
            stop
         end
      end

      clearfile f
      write 'alpha' to f, 'R1'
      write 'beta' to f, 'R2'
      write 'gamma' to f, 'R3'

*  ---------------  update lock and read lock

      readu rec from f, 'R1' else crt 'ZZMATH.R1.MISSING'
      readl rec from f, 'R2' else crt 'ZZMATH.R2.MISSING'

      crt 'ZZMATH.RECORDLOCKED.R1=' : recordlocked(f, 'R1')
      crt 'ZZMATH.RECORDLOCKED.R2=' : recordlocked(f, 'R2')
      crt 'ZZMATH.RECORDLOCKED.R3=' : recordlocked(f, 'R3')

      execute 'list.readu' capturing out
      crt 'ZZMATH.READU.START'
      crt change(out, @fm, char(10))
      crt 'ZZMATH.READU.END'

      execute 'list.readu detail' capturing out
      crt 'ZZMATH.DETAIL.START'
      crt change(out, @fm, char(10))
      crt 'ZZMATH.DETAIL.END'

*  ---------------  the same listing restricted to one user

      execute 'list.readu ' : @user.no capturing out
      crt 'ZZMATH.MINE.START'
      crt change(out, @fm, char(10))
      crt 'ZZMATH.MINE.END'

*  ---------------  file lock

      release f, 'R1'
      release f, 'R2'
      crt 'ZZMATH.AFTER.RELEASE.R1=' : recordlocked(f, 'R1')

      filelock f locked
         crt 'ZZMATH.FILELOCK=refused status=' : status()
      end

      execute 'list.readu' capturing out
      crt 'ZZMATH.FX.START'
      crt change(out, @fm, char(10))
      crt 'ZZMATH.FX.END'

      fileunlock f

*  ---------------  task lock, so LIST.LOCKS can be quoted from a real holder

      lock 7 then
         crt 'ZZMATH.TASKLOCK7=taken'
      end else
         crt 'ZZMATH.TASKLOCK7=refused status=' : status()
      end

      execute 'list.locks' capturing out
      crt 'ZZMATH.LOCKS.START'
      crt change(out, @fm, char(10))
      crt 'ZZMATH.LOCKS.END'

      unlock 7

      close f

*  ---------------  tidy up, and measure DELETE.FILE's own confirmations
*
*  NO.QUERY IS NOT ENOUGH AND THE STACKED ANSWERS ARE WHY THIS PROBE DOES NOT
*  HANG.  An earlier run of it did: DELETEF:233 guards message 6135, "OK to
*  delete DATA portion", on FORCE alone, and CREATE.FILE had written the OS
*  name into the VOC upper case while the verb was typed lower case, so the
*  two differ and the prompt fires.  Capturing the output rather than letting
*  it print is what makes the prompt text itself the evidence.
      data 'Y', 'Y', 'Y', 'Y'
      execute 'delete.file zzlk31a no.query' capturing junk
      crt 'ZZMATH.DELETE.SAID=[' : change(junk, @fm, ' | ') : ']'
      cleardata

      crt 'ZZMATH.END'
      stop
   end
