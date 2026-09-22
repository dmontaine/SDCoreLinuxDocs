* p15b-blocking.b - does READ.SOCKET's timeout do anything by default?
* The first socket probe read only sockets that already had data waiting, which
* cannot tell a blocking read from a non-blocking one.  This one reads a socket
* with nothing on it and times the call.
      crt 'ZZMATH.START'
      port = 45124

      srv = create.server.socket('127.0.0.1', port, 0)
      if socket.info(srv, 0) = 0 then
         crt 'NO SERVER SOCKET status=' : status()
         crt 'ZZMATH.END'
         stop
      end
      cli = open.socket('127.0.0.1', port, 0)
      inc = accept.socket.connection(srv, 2000)
      crt 'all.three.open=' : socket.info(srv,0) : socket.info(cli,0) : socket.info(inc,0)

      crt '--- the blocking flag as each socket is born ---'
      crt 'server.blocking=' : socket.info(srv, 4)
      crt 'client.blocking=' : socket.info(cli, 4)
      crt 'incoming.blocking=' : socket.info(inc, 4)

      crt '--- read with flags 0 and a 5 second timeout, nothing sent ---'
      t0 = system(1020)
      d = read.socket(inc, 100, 0, 5000)
      t1 = system(1020)
      crt 'default.read.ms=' : t1 - t0 : ' len=' : len(d) : ' status=' : status()

      crt '--- the same read with the BLOCKING flag (1) and 2 second timeout ---'
      t0 = system(1020)
      d = read.socket(inc, 100, 1, 2000)
      t1 = system(1020)
      crt 'flag1.read.ms=' : t1 - t0 : ' len=' : len(d) : ' status=' : status()

      crt '--- after SET.SOCKET.MODE(s, 4, 1), flags 0 again ---'
      x = set.socket.mode(inc, 4, 1)
      crt 'set.blocking.returned=' : x : ' now=' : socket.info(inc, 4)
      t0 = system(1020)
      d = read.socket(inc, 100, 0, 2000)
      t1 = system(1020)
      crt 'after.setmode.read.ms=' : t1 - t0 : ' len=' : len(d) : ' status=' : status()

      crt '--- and with data waiting, it returns at once either way ---'
      n = write.socket(cli, 'ready', 0, 2000)
      t0 = system(1020)
      d = read.socket(inc, 100, 0, 2000)
      t1 = system(1020)
      crt 'with.data.ms=' : t1 - t0 : ' len=' : len(d) : ' [' : d : ']'

      close.socket inc
      close.socket cli
      close.socket srv
      crt 'ZZMATH.END'
      stop
   end
