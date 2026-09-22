* p15-sockets.b - sockets, for User document 15.  One program is both ends:
* CREATE.SERVER.SOCKET calls listen(), so a client can connect on loopback and
* sit in the backlog until this same session accepts it.  That is what makes a
* socket measurable from a single session.
*
* The numeric keys are the SKT$ values from SYSCOM KEYS.H; that record is
* reachable with $INCLUDE KEYS.H from an account, but the numbers are written
* out here so the listing shows what was actually passed.
*    flags 0 = SKT$TCP + SKT$STREAM + blocking
*    SET.SOCKET.MODE / SOCKET.INFO keys: 0 open, 1 type, 2 port, 3 ip,
*    4 blocking, 5 no.delay, 6 keep.alive, 7 family
*    read/write flags: 1 = SKT$BLOCKING, 2 = SKT$NON.BLOCKING
      crt 'ZZMATH.START'

      port = 45123
      spare = 45199

      crt '--- CREATE.SERVER.SOCKET ---'
      srv = create.server.socket('127.0.0.1', port, 0)
      crt 'server.status=' : status()
      crt 'server.is.socket=' : socket.info(srv, 0)
      if socket.info(srv, 0) = 0 then
         crt 'NO SERVER SOCKET - nothing below would mean anything'
         crt 'ZZMATH.END'
         stop
      end
      crt 'server.type=' : socket.info(srv, 1)
      crt 'server.port=' : socket.info(srv, 2)
      crt 'server.ip=[' : socket.info(srv, 3) : ']'
      crt 'server.blocking=' : socket.info(srv, 4)
      crt 'server.nodelay=' : socket.info(srv, 5)
      crt 'server.keepalive=' : socket.info(srv, 6)
      crt 'server.family=' : socket.info(srv, 7)

      crt '--- OPEN.SOCKET, to our own listener ---'
      cli = open.socket('127.0.0.1', port, 0)
      crt 'client.status=' : status()
      crt 'client.is.socket=' : socket.info(cli, 0)
      crt 'client.type=' : socket.info(cli, 1)
      crt 'client.port=' : socket.info(cli, 2)
      crt 'client.ip=[' : socket.info(cli, 3) : ']'
      crt 'client.family=' : socket.info(cli, 7)

      crt '--- ACCEPT.SOCKET.CONNECTION ---'
      inc = accept.socket.connection(srv, 2000)
      crt 'accept.status=' : status()
      crt 'incoming.is.socket=' : socket.info(inc, 0)
      crt 'incoming.type=' : socket.info(inc, 1)
      crt 'incoming.port=' : socket.info(inc, 2)
      crt 'incoming.ip=[' : socket.info(inc, 3) : ']'

      crt '--- WRITE.SOCKET / READ.SOCKET ---'
      n = write.socket(cli, 'hello world', 0, 2000)
      crt 'write.returned=' : n : ' status=' : status()
      d = read.socket(inc, 100, 0, 2000)
      crt 'read=[' : d : '] len=' : len(d) : ' status=' : status()

      crt '--- a short read: asking for fewer bytes than were sent ---'
      n = write.socket(cli, 'abcdefghij', 0, 2000)
      d = read.socket(inc, 4, 0, 2000)
      crt 'short.read=[' : d : '] len=' : len(d)
      d = read.socket(inc, 100, 0, 2000)
      crt 'remainder=[' : d : '] len=' : len(d)

      crt '--- a non-blocking read with nothing to read ---'
      d = read.socket(inc, 100, 2, 500)
      crt 'nonblocking.len=' : len(d) : ' status=' : status()

      crt '--- do marks survive the wire ---'
      m = 'a' : @fm : 'b' : @vm : 'c' : @sm : 'd'
      n = write.socket(cli, m, 0, 2000)
      d = read.socket(inc, 100, 0, 2000)
      crt 'marks.len.sent=' : len(m) : ' received=' : len(d)
      crt 'marks.identical=' : (d = m)

      crt '--- a NUL and the high bytes ---'
      b = char(0) : char(1) : char(255) : 'Z'
      n = write.socket(cli, b, 0, 2000)
      d = read.socket(inc, 100, 0, 2000)
      crt 'binary.len.sent=' : len(b) : ' received=' : len(d)
      crt 'binary.identical=' : (d = b)

      crt '--- SET.SOCKET.MODE ---'
      crt 'set.blocking(0)=' : set.socket.mode(inc, 4, 0)
      crt 'blocking.now=' : socket.info(inc, 4)
      crt 'set.blocking(1)=' : set.socket.mode(inc, 4, 1)
      crt 'blocking.now=' : socket.info(inc, 4)
      crt 'set.nodelay(1)=' : set.socket.mode(inc, 5, 1)
      crt 'nodelay.now=' : socket.info(inc, 5)
      crt 'set.keepalive(0)=' : set.socket.mode(inc, 6, 0)
      crt 'keepalive.now=' : socket.info(inc, 6)
      crt 'set.badkey(99)=' : set.socket.mode(inc, 99, 1) : ' status=' : status()

      crt '--- SERVER.ADDR ---'
      crt 'server.addr(localhost)=[' : server.addr('localhost') : '] status=' : status()
      crt 'server.addr(127.0.0.1)=[' : server.addr('127.0.0.1') : '] status=' : status()
* server.addr() on an unresolvable name is measured LAST, after the END marker:
* it blocks in the operating system resolver and does not come back promptly,
* so anything after it would not be measured at all.

      crt '--- what the far end closing looks like ---'
      close.socket cli
      d = read.socket(inc, 100, 0, 2000)
      crt 'read.after.peer.close.len=' : len(d) : ' status=' : status()
      d = read.socket(inc, 100, 0, 2000)
      crt 'read.again.len=' : len(d) : ' status=' : status()

      crt '--- a connection nobody is listening for ---'
      bad = open.socket('127.0.0.1', spare, 0)
      crt 'refused.is.socket=' : socket.info(bad, 0) : ' status=' : status()

      crt '--- two listeners on one port ---'
      srv2 = create.server.socket('127.0.0.1', port, 0)
      crt 'second.listener.is.socket=' : socket.info(srv2, 0) : ' status=' : status()

      close.socket inc
      close.socket srv
      crt 'ZZMATH.END'

* --- deliberately last: an unresolvable name -------------------------------
      crt 'RESOLVER.T0=' : system(1020)
      bogus = server.addr('no.such.host.invalid')
      crt 'RESOLVER.T1=' : system(1020) : ' answer=[' : bogus : '] status=' : status()
      stop
   end
