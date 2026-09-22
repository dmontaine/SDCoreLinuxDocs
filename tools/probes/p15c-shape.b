* p15c-shape.b - the worked client shape from User document 15, run rather than
* composed.  The far end is the same session, so the reply is written into the
* socket before the read loop starts; the loop itself is exactly what the page
* prints.
      crt 'ZZMATH.START'
      port = 45125

      srv = create.server.socket('127.0.0.1', port, 0)
      if socket.info(srv, 0) = 0 then
         crt 'NO LISTENER status=' : status()
         crt 'ZZMATH.END'
         stop
      end

      skt = open.socket('127.0.0.1', port, 0)
      if socket.info(skt, 0) = 0 then
         crt 'no connection: ' : status()
         crt 'ZZMATH.END'
         stop
      end
      far = accept.socket.connection(srv, 2000)

      x = set.socket.mode(skt, 4, 1)
      crt 'set.blocking=' : x
      n = write.socket(skt, 'PING' : char(10), 0, 5000)
      crt 'request.bytes=' : n

* the far end answers, in three pieces, so the loop has to reassemble them
      n = write.socket(far, 'PON', 0, 5000)
      n = write.socket(far, 'G one', 0, 5000)
      n = write.socket(far, char(10), 0, 5000)

      reply = ''
      chunks = 0
      loop
         chunk = read.socket(skt, 2048, 0, 5000)
         s = status()
         chunks += 1
         reply := chunk
      until s = 7013 or index(reply, char(10), 1) > 0 or chunks > 20
      repeat
      crt 'chunks.read=' : chunks
      crt 'reply=[' : reply[1, len(reply) - 1] : '] status=' : s
      crt 'terminator.found.at=' : index(reply, char(10), 1)

      crt '--- and the same loop when the far end just closes ---'
      close.socket far
      reply2 = ''
      chunks = 0
      loop
         chunk = read.socket(skt, 2048, 0, 5000)
         s = status()
         chunks += 1
         reply2 := chunk
      until s = 7013 or index(reply2, char(10), 1) > 0 or chunks > 20
      repeat
      crt 'closed.chunks=' : chunks : ' status=' : s : ' len=' : len(reply2)

      close.socket skt
      close.socket srv
      crt 'ZZMATH.END'
      stop
   end
