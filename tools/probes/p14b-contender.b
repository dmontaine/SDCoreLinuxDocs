* p14b-contender.b - session B, phase 2.  Asks what the other session's READL
* and FILELOCK look like from outside, which completes the RECORDLOCKED() code
* table.  Signals go to ZZLOCKG, never to the file under lock - see the note in
* p14b-holder.b.
      crt 'ZZCONT.START'
      crt 'ZZCONT.USERNO=' : @user.no

      open 'ZZLOCKF' to f else
         crt 'ZZCONT.NO.DATA.FILE status=' : status()
         crt 'ZZCONT.END'
         stop
      end
      waitg = 0
      loop
         open 'ZZLOCKG' to g then exit
         nap 250
         waitg += 1
      while waitg < 60
      repeat
      crt 'ZZCONT.SIGNAL.FILE.WAIT=' : waitg
      open 'ZZLOCKG' to g else
         crt 'ZZCONT.NO.SIGNAL.FILE status=' : status()
         crt 'ZZCONT.END'
         stop
      end

      waited = 0
      holder = ''
      loop
         read holder from g, 'HOLDING' then exit
         nap 250
         waited += 1
      while waited < 160
      repeat
      crt 'ZZCONT.WAITED1.TICKS=' : waited
      crt 'ZZCONT.SAW.USERNO=' : holder

      crt '--- somebody else holds a READL ---'
      rl = recordlocked(f, 'R1')
      crt 'ZZCONT.RECORDLOCKED.R1=' : rl
      crt 'ZZCONT.RECORDLOCKED.R1.status=' : status()
      if rl < 0 then crt 'ZZCONT.CONTENDED.recordlocked.readl'

      readl r from f, 'R1' locked
         crt 'ZZCONT.CONTENDED.readl.vs.readl status=' : status()
      end then
         crt 'ZZCONT.readl.SHARED.ok recordlocked=' : recordlocked(f, 'R1')
         release f, 'R1'
         crt 'ZZCONT.readl.released recordlocked=' : recordlocked(f, 'R1')
      end else
         crt 'ZZCONT.readl.else.branch'
      end

      readu r from f, 'R1' locked
         crt 'ZZCONT.CONTENDED.readu.vs.readl status=' : status()
      end then
         crt 'ZZCONT.readu.vs.readl.TOOK.IT'
         release f, 'R1'
      end else
         crt 'ZZCONT.readu.else.branch'
      end

      write 'yes' to g, 'DONE1'

      waited = 0
      holder2 = ''
      loop
         read holder2 from g, 'HOLDING2' then exit
         nap 250
         waited += 1
      while waited < 160
      repeat
      crt 'ZZCONT.WAITED2.TICKS=' : waited
      crt 'ZZCONT.SAW2.USERNO=' : holder2

      crt '--- somebody else holds a FILELOCK ---'
      fl = recordlocked(f, 'R1')
      crt 'ZZCONT.FILELOCKED.R1=' : fl
      crt 'ZZCONT.FILELOCKED.R1.status=' : status()
      crt 'ZZCONT.FILELOCKED.R2=' : recordlocked(f, 'R2')
      if fl < 0 then crt 'ZZCONT.CONTENDED.recordlocked.filelock'

      readu r2 from f, 'R2' locked
         crt 'ZZCONT.CONTENDED.readu.under.filelock status=' : status()
      end then
         crt 'ZZCONT.R2.TOOK.IT.under.filelock'
         release f, 'R2'
      end else
         crt 'ZZCONT.R2.else.branch'
      end

      read plain from f, 'R2' then
         crt 'ZZCONT.plain.read.under.filelock=ok [' : plain : ']'
      end else
         crt 'ZZCONT.plain.read.under.filelock=else status=' : status()
      end

      write 'yes' to g, 'DONE2'

      waited = 0
      loop
         read d from g, 'RELEASED' then exit
         nap 250
         waited += 1
      while waited < 160
      repeat
      crt 'ZZCONT.WAITED3.TICKS=' : waited
      crt 'ZZCONT.AFTER.FILEUNLOCK=' : recordlocked(f, 'R1')

      write 'yes' to g, 'FINISHED'
      close f
      close g
      crt 'ZZCONT.END'
      stop
   end
