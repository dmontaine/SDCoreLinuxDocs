      crt 'ZZDBG.START'
      n = 41
      debug
      n = n + 1
      m = n * 2
      k = 'some text'
      dim arr(3)
      arr(1) = 'first'
      crt 'ZZDBG.N=' : n : ' M=' : m : ' K=' : k
      crt 'ZZDBG.END'
      stop
   end
