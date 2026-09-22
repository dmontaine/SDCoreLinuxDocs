* p14c-txn.b - transactions, for User document 14.  One transaction shape per
* section, none of them nested, each printing SYSTEM(1008) before and after so
* the reading can be taken as a delta.  An earlier draft nested a transaction
* inside another and the readings were unusable; that case is measured on its
* own at the end and is a defect, not a feature.
*
* Inside a transaction every record written or deleted must ALREADY be locked
* by this session (op_dio3.c:770), so every write below is preceded by
* RECORDLOCKU.  Section 6 measures what happens when it is not.
      crt 'ZZMATH.START'
      crt 'ZZMATH.USERNO=' : @user.no

      open 'ZZLOCKF' to f else
         execute 'create.file zzlockf' capturing junk
         open 'ZZLOCKF' to f else
            crt 'ZZMATH.NO.FILE status=' : status()
            crt 'ZZMATH.END'
            stop
         end
      end
      clearfile f
      write 'base' to f, 'R1'
      write 'base' to f, 'R2'
      write 'base' to f, 'R3'
      write 'base' to f, 'R4'
      release

      crt '--- 0. outside any transaction ---'
      crt 'level=' : system(1008) : ' number=' : system(1007)
      readu q from f, 'R1' else null
      crt 'readu.then.recordlocked=' : recordlocked(f, 'R1')
      write 'plain' to f, 'R1'
      crt 'write.releases.the.lock=' : recordlocked(f, 'R1')
      read v from f, 'R1' then crt 'R1=[' : v : ']' else crt 'R1=else'
      release

      crt '--- 1. BEGIN TRANSACTION ... COMMIT ---'
      l0 = system(1008)
      begin transaction
         crt '1.in.level=' : system(1008) : ' number=' : system(1007)
         recordlocku f, 'R1'
         write 'committed' to f, 'R1'
         crt '1.write.kept.the.lock=' : recordlocked(f, 'R1')
         read v from f, 'R1' then crt '1.own.read=[' : v : ']' else crt '1.own.read=else'
         commit
      end transaction
      crt '1.level.delta=' : system(1008) - l0 : ' number=' : system(1007)
      crt '1.lock.after.commit=' : recordlocked(f, 'R1')
      read v from f, 'R1' then crt '1.R1=[' : v : ']' else crt '1.R1=else'
      release

      crt '--- 2. BEGIN TRANSACTION ... ROLLBACK ---'
      l0 = system(1008)
      begin transaction
         recordlocku f, 'R2'
         write 'rolled' to f, 'R2'
         read v from f, 'R2' then crt '2.own.read=[' : v : ']' else crt '2.own.read=else'
         rollback
      end transaction
      crt '2.level.delta=' : system(1008) - l0 : ' number=' : system(1007)
      crt '2.lock.after.rollback=' : recordlocked(f, 'R2')
      read v from f, 'R2' then crt '2.R2=[' : v : ']' else crt '2.R2=else'
      release

      crt '--- 3. BEGIN TRANSACTION ... END TRANSACTION, no COMMIT ---'
      l0 = system(1008)
      begin transaction
         recordlocku f, 'R3'
         write 'never.committed' to f, 'R3'
         read v from f, 'R3' then crt '3.own.read=[' : v : ']' else crt '3.own.read=else'
      end transaction
      crt '3.level.delta=' : system(1008) - l0 : ' number=' : system(1007)
      read v from f, 'R3' then crt '3.R3=[' : v : ']' else crt '3.R3=else'
      release

      crt '--- 4. TRANSACTION START / TRANSACTION COMMIT ---'
      l0 = system(1008)
      transaction start
      crt '4.in.level=' : system(1008) : ' number=' : system(1007)
      recordlocku f, 'R4'
      write 'ts.committed' to f, 'R4'
      transaction commit
      crt '4.level.delta=' : system(1008) - l0 : ' number=' : system(1007)
      read v from f, 'R4' then crt '4.R4=[' : v : ']' else crt '4.R4=else'
      release

      crt '--- 5. TRANSACTION START / TRANSACTION ABORT ---'
      l0 = system(1008)
      transaction start
      recordlocku f, 'R5'
      write 'ts.aborted' to f, 'R5'
      transaction abort
      crt '5.level.delta=' : system(1008) - l0 : ' number=' : system(1007)
      read v from f, 'R5' then crt '5.R5=[' : v : ']' else crt '5.R5=else'
      release

      crt '--- 6. a write with no lock, inside a transaction ---'
      l0 = system(1008)
      begin transaction
         write 'no.lock.held' to f, 'RX' on error
            crt '6.ON.ERROR.status=' : status()
         end
         read v from f, 'RX' then crt '6.RX=[' : v : ']' else crt '6.RX=else'
         rollback
      end transaction
      crt '6.level.delta=' : system(1008) - l0
      write 'no.lock.held' to f, 'RX'
      read v from f, 'RX' then crt '6.same.write.outside=[' : v : ']' else crt '6.same.write.outside=else'
      release

      crt '--- 7. a rolled back DELETE ---'
      l0 = system(1008)
      begin transaction
         recordlocku f, 'R1'
         delete f, 'R1'
         read v from f, 'R1' then crt '7.own.read=[' : v : ']' else crt '7.own.read=else'
         rollback
      end transaction
      crt '7.level.delta=' : system(1008) - l0
      read v from f, 'R1' then crt '7.R1=[' : v : ']' else crt '7.R1=else'
      release

      crt '--- 8. NESTED, and this one is the defect ---'
      l0 = system(1008)
      begin transaction
         recordlocku f, 'R2'
         write 'outer' to f, 'R2'
         begin transaction
            crt '8.nested.level=' : system(1008) : ' number=' : system(1007)
            recordlocku f, 'R3'
            write 'inner' to f, 'R3'
            commit
         end transaction
         crt '8.after.inner.commit.number=' : system(1007)
         commit
      end transaction
      crt '8.level.delta=' : system(1008) - l0
      read v from f, 'R2' then crt '8.outer.R2=[' : v : ']' else crt '8.outer.R2=else'
      read v from f, 'R3' then crt '8.inner.R3=[' : v : ']' else crt '8.inner.R3=else'
      release

      close f
      crt 'ZZMATH.END'
      stop
   end
