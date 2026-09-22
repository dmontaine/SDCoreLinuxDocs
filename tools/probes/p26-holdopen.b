* p26-holdopen.b - does SD still hold the working copy open while the editor
* runs?  For the "Permission denied" micro reported on save, 27 Aug 2026.
*
* THE QUESTION.  EDIT writes the working copy into $hold and then hands the
* path to an external editor with os.execute.  If SD has not let go of the file
* by then, the editor cannot write it, and Windows reports a sharing violation
* the same way it reports a permission error - which is exactly the message
* micro printed.
*
* THE TEST MIRRORS EDIT'S OWN SEQUENCE: write a record into $hold, then, from
* inside os.execute - the same place the editor runs - try to open that file
* for writing with no sharing.  If that fails, the editor would fail too, and
* for a reason that has nothing to do with anybody's permissions.
*
* THE CONTROL IS THE SECOND ATTEMPT, after an explicit close.  A test that only
* ever fails proves nothing about the cause; one that fails and then succeeds
* names it.
$include syscom keys.h

      crt 'ZZMATH.START'
      crt 'ZZMATH.USERNO=' : @user.no

      open '$hold' to hold.f else
         crt 'ZZMATH.NO.HOLD status=' : status()
         crt 'ZZMATH.END'
         stop
      end

      id = 'zzholdopen.editing'
      write 'one line of working copy' to hold.f, id

      hold.dir = fileinfo(hold.f, FL$PATH)
      crt 'ZZMATH.HOLD.DIR=' : hold.dir
      posix.file = hold.dir : '/' : id
      crt 'ZZMATH.POSIX=' : posix.file

*  The probe runs in PowerShell, so give it a PowerShell path.  cygpath is not
*  available to a program; converting by hand is enough for /cygdrive/X/...
      win.file = posix.file
      if win.file[1,11] = '/cygdrive/' : win.file[11,1] then
         drive = upcase(win.file[11,1])
         win.file = drive : ':' : win.file[12,999999]
      end
      win.file = change(win.file, '/', '\')
      crt 'ZZMATH.WINPATH=' : win.file

      q = char(39)
      ps = 'try { $f=[System.IO.File]::Open(' : q : win.file : q
      ps := ', ' : q : 'Open' : q : ', ' : q : 'Write' : q : ', ' : q : 'None' : q : ')'
      ps := '; $f.Close(); Write-Output ' : q : 'EXCLUSIVE-OPEN-OK' : q : ' }'
      ps := ' catch { Write-Output (' : q : 'BLOCKED: ' : q : ' + $_.Exception.GetType().Name) }'

*  ---------------  attempt 1: while SD has the file as it left it

      os.execute ps capturing out1
      crt 'ZZMATH.WHILE.SD.HAS.IT=[' : change(trim(out1), @fm, ' | ') : ']'

*  ---------------  attempt 2, the control: after closing the file

      close hold.f
      os.execute ps capturing out2
      crt 'ZZMATH.AFTER.CLOSE=[' : change(trim(out2), @fm, ' | ') : ']'

*  ---------------  tidy up

      open '$hold' to hold.f then
         delete hold.f, id
         crt 'ZZMATH.CLEANED=yes'
      end

      crt 'ZZMATH.END'
      stop
   end
