* p25-holdtrip.b - does a record survive the trip through $hold unchanged?
* Prints its own START and END markers; sdprobe.ps1 refuses the run otherwise.
*
* WHY IT EXISTS.  Owner, 27 Aug 2026, raising the mark-conversion defect:
* "translation between records stored in dynamic files and the temporary
* record in $HOLD needs to be handled seamlessly."  gpl.bp/EDIT's token
* conversion is one leg of that and is proved separately, in Python, before
* any cycle is spent.  THIS IS THE OTHER LEG, and no test had touched it:
* $hold is a DIRECTORY file, so writing a record there turns field marks into
* line separators on disk and reading it back turns them into field marks
* again.  If that leg is lossy, EDIT is lossy however good its tokens are.
*
* IT MEASURES THE LEG WITHOUT THE EDITOR, on purpose - edit and micro need a
* terminal and cannot be driven down a pipe at all, so this is the only part
* of their path a script can reach.
*
* IT PRINTS WHAT IT WROTE AND WHAT CAME BACK, not a verdict: both lengths,
* both field counts, and the position and character code of the first
* difference.  An empty subject is refused out loud, because a clean sweep
* over nothing is the failure this project has paid for more than once.

      crt 'ZZMATH.START'

      vm = char(253)
      sm = char(252)
      tm = char(251)
      bq = char(96)
      cr = char(13)
      lf = char(10)

      labels = 'plain'
      labels<-1> = 'two.fields'
      labels<-1> = 'value.mark'
      labels<-1> = 'subvalue.mark'
      labels<-1> = 'both.marks'
      labels<-1> = 'text.mark'
      labels<-1> = 'lone.tilde'
      labels<-1> = 'double.tilde'
      labels<-1> = 'tilde.backtick'
      labels<-1> = 'tilde.hyphen'
      labels<-1> = 'tilde.before.vm'
      labels<-1> = 'trailing.empty.field'
      labels<-1> = 'leading.empty.field'
      labels<-1> = 'three.lines'
      labels<-1> = 'crlf.in.data'

      n = dcount(labels, @fm)
      crt 'cases=' : n

*     REFUSE THE NULL CASE.  A table nobody filled in would score a clean
*     sweep of nothing and read exactly like a pass.
      if n < 10 then
         crt 'FAIL: only ' : n : ' case(s) - refusing to report a result'
         crt 'ZZMATH.END'
         stop
      end

      open '$hold' to hold.f else
         crt 'FAIL: cannot open $hold in this account'
         crt 'ZZMATH.END'
         stop
      end

      crt 'hold.path=[' : fileinfo(hold.f, 2) : ']'

      same = 0
      diff = 0

      for i = 1 to n
         label = labels<i>

*        THE RECORDS ARE BUILT HERE RATHER THAN HELD IN AN ARRAY, because an
*        array of them would need a delimiter and every delimiter SD has is
*        one of the characters under test.
         begin case
            case i =  1 ; rec = 'HELLO'
            case i =  2 ; rec = 'LINE1' : @fm : 'LINE2'
            case i =  3 ; rec = 'SMITH' : vm : 'JONES'
            case i =  4 ; rec = 'A' : sm : 'B'
            case i =  5 ; rec = 'A' : vm : 'B' : sm : 'C'
            case i =  6 ; rec = 'A' : tm : 'B'
            case i =  7 ; rec = 'a~b'
            case i =  8 ; rec = 'a~~b'
            case i =  9 ; rec = 'a~' : bq : 'b'
            case i = 10 ; rec = 'a~-b'
            case i = 11 ; rec = 'a~' : vm : 'b'
            case i = 12 ; rec = 'A' : @fm : ''
            case i = 13 ; rec = '' : @fm : 'A'
            case i = 14 ; rec = 'ONE' : @fm : 'TWO' : @fm : 'THREE'
            case i = 15 ; rec = 'A' : cr : lf : 'B'
            case 1      ; rec = ''
         end case

         id = 'zzholdtrip.' : i

         wrote.ok = 1
         write rec to hold.f, id on error wrote.ok = 0
         if not(wrote.ok) then
            crt fmt(label, '22L') : ' WRITE ERROR - status ' : status()
            continue
         end

         read back from hold.f, id else back = ''

         del.ok = 1
         delete hold.f, id on error del.ok = 0

         ok = (back = rec)
         if ok then same += 1 else diff += 1

         crt fmt(label, '22L') :
         crt ' len ' : fmt(len(rec), '3R') : '/' : fmt(len(back), '3R') :
         crt '  fields ' : fmt(dcount(rec, @fm), '2R') : '/' :
         crt fmt(dcount(back, @fm), '2R') :
         if ok then
            crt '  same'
         end else
            crt '  DIFFERENT'
            m = len(rec)
            if len(back) > m then m = len(back)
            found = 0
            for j = 1 to m
               if not(found) then
                  a = rec[j,1]
                  b = back[j,1]
                  if a # b then
                     found = 1
                     if a = '' then ca = -1 else ca = seq(a)
                     if b = '' then cb = -1 else cb = seq(b)
                     crt '    first difference at character ' : j :
                     crt ': wrote code ' : ca : ', read code ' : cb
                  end
               end
            next j
            crt '    wrote [' : change(change(change(rec, @fm, '|'), vm, '<VM>'), sm, '<SM>') : ']'
            crt '    read  [' : change(change(change(back, @fm, '|'), vm, '<VM>'), sm, '<SM>') : ']'
         end
         if not(del.ok) then
            crt '    WARNING: ' : id : ' was left behind in $hold'
         end
      next i

      crt 'same=' : same : ' different=' : diff
      if same = 0 then
         crt 'FAIL: nothing came back the same, so this measured nothing useful'
      end

      crt 'ZZMATH.END'
      stop
   end
