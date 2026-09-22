* p34-conversions.b - the worked-example table in User document 34, run rather
* than asserted.  Each line prints the code, the input, and what oconv and fmt
* actually returned, so the page can quote the machine instead of a guess.
      crt 'ZZMATH.START'

      d = 20899
      crt 'D2/            [' : oconv(d, 'D2/') : ']'
      crt 'D2[DD/MM/YY]   [' : fmt(oconv(d, 'D2/'), '10L') : ']'
      crt 'D[DD MMM YYYY] [' : fmt(oconv(d, 'D'), '12L') : ']'
      crt 'D  bare        [' : oconv(d, 'D') : ']'
      crt 'DD             [' : oconv(d, 'DD') : ']'
      crt 'ML             [' : oconv(d, 'ML') : ']'

      crt 'MD2 on 1234567 [' : fmt(oconv(1234567, 'MD2'), '10R2,') : ']'
      crt 'MD2, raw       [' : oconv(1234567, 'MD2') : ']'
      crt 'MD2, with comma[' : oconv(1234567, 'MD2,') : ']'

      crt 'MCU on hello   [' : fmt(oconv('hello', 'MCU'), '10L') : ']'
      crt 'MCL on HELLO   [' : oconv('HELLO', 'MCL') : ']'
      crt 'MCT two words  [' : oconv('hello there world', 'MCT') : ']'

      crt 'MX on 255      [' : fmt(oconv(255, 'MX'), '8R') : ']'
      crt 'MX raw         [' : oconv(255, 'MX') : ']'
      crt 'MB on 5        [' : oconv(5, 'MB') : ']'

      crt 'T wrap 12      [' : fmt('the quick brown fox jumps', '12T') : ']'

      crt 'ZZMATH.END'
