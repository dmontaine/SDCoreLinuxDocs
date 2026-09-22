* p16c-config.b - what CONFIG() does with a name it does not know, for User
* document 16.  Both calls are AFTER the END marker on purpose: the answer is
* not a value but an abort, so anything placed after them is not measured.
      crt 'ZZMATH.START'
      crt 'config(NUMLOCKS)=[' : config('NUMLOCKS') : '] status=' : status()
      crt 'config(GRPSIZE)=[' : config('GRPSIZE') : '] status=' : status()
      crt 'ZZMATH.END'

      crt 'now the lower case spelling of a real key:'
      crt 'config(numlocks)=[' : config('numlocks') : '] status=' : status()
      crt 'and a key that does not exist:'
      crt 'config(NOSUCHKEY)=[' : config('NOSUCHKEY') : '] status=' : status()
      crt 'neither aborted'
      stop
   end
