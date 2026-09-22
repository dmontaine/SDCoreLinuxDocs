* p16b-osexec.b - OS.EXECUTE from an ordinary account, for User document 16.
* Whether it is permitted at all is decided by field 2 of the account's
* os.users record, not by the VOC, so the interesting result is whichever way
* it goes - and the END marker after it is what proves the program survived.
      crt 'ZZMATH.START'
      crt 'admin.flag=' : system(1050)
      crt 'os.error.before=' : os.error()

      out = ''
      os.execute 'cmd /c echo hello-from-os-execute' capturing out
      crt 'os.execute.status=' : status()
      crt 'os.error.after=' : os.error()
      crt 'captured.fields=' : dcount(out, @fm)
      crt 'captured=[' : change(out, @fm, ' | ') : ']'
      crt 'system.return.code=' : @system.return.code

      out2 = ''
      os.execute 'cmd /c exit 3' capturing out2
      crt 'exit3.status=' : status()
      crt 'exit3.system.return.code=' : @system.return.code
      crt 'exit3.captured=[' : change(out2, @fm, ' | ') : ']'

      crt 'ZZMATH.END'
      stop
   end
