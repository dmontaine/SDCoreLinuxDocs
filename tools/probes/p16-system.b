* p16-system.b - probe for User document 16, System and Environment.
* Prints its own START and END markers; sdprobe.ps1 refuses the run otherwise.

      crt 'ZZMATH.START'

      crt '--- SYSTEM() ---'
      keys = '7 9 10 11 12 18 23 24 25 26 27 31 32 38 42 91'
      keys := ' 1000 1001 1005 1006 1007 1008 1009 1010 1011 1012'
      keys := ' 1013 1014 1015 1017 1020 1024 1028 1029 1030 1031 1050'
      n = dcount(keys, ' ')
      for i = 1 to n
         k = field(keys, ' ', i) + 0
         v = system(k)
         if len(v) > 60 then v = v[1,60] : '...'
         crt 'system(' : k : ')=[' : v : ']'
      next i

      crt '--- system(1025) environment ---'
      e = system(1025)
      crt 'env.count=' : dcount(e, @fm)
      crt 'env.first=[' : e<1> : ']'

      crt '--- system(1003) open files ---'
      crt 'open.files=[' : change(system(1003), @fm, '|') : ']'

      crt '--- ENV() ---'
      crt 'env(PATH).len=' : len(env('PATH'))
      crt 'env(NOSUCHVAR)=[' : env('NOSUCHVAR') : ']'
      crt 'env(nosuchvar).len=' : len(env('nosuchvar'))
      crt 'env(path).len=' : len(env('path'))
      crt 'env(ProgramData)=[' : env('ProgramData') : ']'

      crt '--- CONFIG() ---'
      cfgs = 'FILERULE GRPSIZE MAXIDLEN NUMFILES SORTMEM SPOOLER NUMLOCKS'
      n = dcount(cfgs, ' ')
      for i = 1 to n
         c = field(cfgs, ' ', i)
         crt 'config(' : c : ')=[' : config(c) : '] status=' : status()
      next i

      crt '--- DATE TIME TIMEDATE ---'
      d = date()
      t = time()
      crt 'date()=' : d
      crt 'time()=' : t
      crt 'timedate()=[' : timedate() : ']'
      crt 'oconv(date,D4-)=[' : oconv(d, 'D4-') : ']'
      crt 'oconv(time,MTS)=[' : oconv(t, 'MTS') : ']'
      crt '@date=' : @date
      crt '@time=' : @time
      crt 'system(1005)-date*86400-time=' : system(1005) - (d * 86400) - t

      crt '--- SYSMSG() ---'
      crt 'sysmsg(2831)=[' : sysmsg(2831) : ']'
      crt 'sysmsg(3006)=[' : sysmsg(3006) : ']'
      crt 'sysmsg(1)=[' : sysmsg(1) : ']'
      crt 'sysmsg(2201)=[' : sysmsg(2201) : ']'
      crt 'sysmsg(99999)=[' : sysmsg(99999) : ']'
      crt 'sysmsg(6711,ABC)=[' : sysmsg(6711, 'ABC') : ']'

      crt '--- GET.MESSAGES() ---'
      gm = get.messages()
      crt 'get.messages().fields=' : dcount(gm, @fm)
      crt 'get.messages()=[' : change(gm, @fm, '|')[1,120] : ']'

      crt '--- CHECKSUM() ---'
      crt 'checksum(ABC)=' : checksum('ABC')
      crt 'checksum(abc)=' : checksum('abc')
      crt 'checksum(empty)=' : checksum('')
      crt 'checksum(ACB)=' : checksum('ACB')
      crt 'checksum(A:@fm:B)=' : checksum('A' : @fm : 'B')

      crt '--- SDENCRYPT / SDDECRYPT ---'
      plain = 'The quick brown fox'
      ct = sdencrypt(plain, 'secretkey', 202)
      crt 'plain.len=' : len(plain)
      crt 'cipher.len=' : len(ct)
      crt 'cipher.status=' : status()
      crt 'cipher.eq.plain=' : (ct = plain)
      back = sddecrypt(ct, 'secretkey', 202)
      crt 'roundtrip=[' : back : ']'
      crt 'roundtrip.ok=' : (back = plain)
      crt 'roundtrip.status=' : status()

      crt '--- SENTENCE() and @variables ---'
      crt 'sentence()=[' : sentence() : ']'
      crt '@sentence=[' : @sentence : ']'
      crt 'sentence.eq.at=' : (sentence() = @sentence)
      crt '@who=[' : @who : ']'
      crt '@logname=[' : @logname : ']'
      crt '@user=[' : @user : ']'
      crt '@path=[' : @path : ']'
      crt '@sdsys=[' : @sdsys : ']'
      crt '@user.no=' : @user.no
      crt '@tty=[' : @tty : ']'
      crt '@user.return.code=[' : @user.return.code : ']'
      crt '@system.return.code=[' : @system.return.code : ']'
      crt '@crtwide=' : @crtwide
      crt '@crthigh=' : @crthigh

      crt '--- OS.ERROR() ---'
      crt 'os.error.at.start=' : os.error()

      crt '--- UMASK() ---'
      u = umask(-1)
      crt 'umask(-1)=' : u
      crt 'umask(18)=' : umask(18)
      crt 'umask(-1).after=' : umask(-1)
      x = umask(u)
      crt 'umask.restored=' : umask(-1)

      crt '--- LOGMSG ---'
      logmsg 'ZZMATH probe: logmsg reached the error log'
      crt 'logmsg.returned status=' : status()

      crt 'ZZMATH.END'
      stop
   end
