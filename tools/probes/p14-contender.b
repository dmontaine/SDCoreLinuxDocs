* p14-contender.b - session B for User document 14.  Waits for the holder's
* signal, then asks every question that can only be asked of somebody else's
* lock.  Every LOCK and READU here carries a LOCKED or ELSE clause on purpose:
* a bare LOCK retries for ever and a bare READU blocks for ever, and the one
* deliberate blocking read at the end is bounded by the holder releasing.
      crt 'ZZCONT.START'
      crt 'ZZCONT.USERNO=' : @user.no

      open 'ZZLOCKF' to f else
         crt 'ZZCONT.NO.FILE'
         crt 'ZZCONT.END'
         stop
      end

      waited = 0
      holder = ''
      loop
         read holder from f, 'HOLDING' then exit
         nap 250
         waited += 1
      while waited < 160
      repeat
      crt 'ZZCONT.WAITED.TICKS=' : waited
      crt 'ZZCONT.SAW.USERNO=' : holder

      crt '--- RECORDLOCKED against another session ---'
      rl = recordlocked(f, 'R1')
      crt 'ZZCONT.RECORDLOCKED.R1=' : rl
      crt 'ZZCONT.RECORDLOCKED.R1.status=' : status()
      if rl < 0 then crt 'ZZCONT.CONTENDED.recordlocked'
      crt 'ZZCONT.RECORDLOCKED.R2=' : recordlocked(f, 'R2')

      crt '--- READU with a LOCKED clause ---'
      readu r from f, 'R1' locked
         crt 'ZZCONT.CONTENDED.readu.locked status=' : status()
      end then
         crt 'ZZCONT.readu.TOOK.THE.LOCK'
         release f, 'R1'
      end else
         crt 'ZZCONT.readu.else.branch'
      end

      crt '--- READL with a LOCKED clause ---'
      readl r from f, 'R1' locked
         crt 'ZZCONT.CONTENDED.readl.locked status=' : status()
      end then
         crt 'ZZCONT.readl.TOOK.THE.LOCK'
         release f, 'R1'
      end else
         crt 'ZZCONT.readl.else.branch'
      end

      crt '--- an unlocked record in the same file ---'
      readu r2 from f, 'R2' locked
         crt 'ZZCONT.R2.blocked status=' : status()
      end then
         crt 'ZZCONT.R2.taken recordlocked=' : recordlocked(f, 'R2')
         release f, 'R2'
      end else
         crt 'ZZCONT.R2.else.branch'
      end

      crt '--- task locks ---'
      lock 7 then
         crt 'ZZCONT.tasklock7.TAKEN'
         unlock 7
      end else
         crt 'ZZCONT.CONTENDED.tasklock7 status=' : status()
      end
      lock 8 then
         crt 'ZZCONT.tasklock8=taken status=' : status()
         unlock 8
      end else
         crt 'ZZCONT.tasklock8=refused status=' : status()
      end

      crt '--- FILELOCK while somebody holds one record ---'
* FILELOCK has no THEN/ELSE, only LOCKED, so success is invisible unless a flag
* is set in the LOCKED branch.  It must be released if it was taken, or this
* session deadlocks the holder's own next write.
      fl.blocked = @false
      filelock f locked
         fl.blocked = @true
         crt 'ZZCONT.CONTENDED.filelock status=' : status()
      end
      if not(fl.blocked) then
         crt 'ZZCONT.filelock.TAKEN recordlocked.R1=' : recordlocked(f, 'R1')
         fileunlock f
         crt 'ZZCONT.filelock.released'
      end

      crt '--- the blocking form, released by the other session ---'
      write 'yes' to f, 'DONE'
      t0 = system(1020)
      readu r from f, 'R1' else
         crt 'ZZCONT.blocking.readu.else'
      end
      t1 = system(1020)
      crt 'ZZCONT.BLOCKING.READU.WAITED.MS=' : t1 - t0
      crt 'ZZCONT.AFTER.WAIT.RECORDLOCKED=' : recordlocked(f, 'R1')
      release f, 'R1'
      write 'yes' to f, 'FINISHED'

      close f
      crt 'ZZCONT.END'
      stop
   end
