* p18-class.b - the class module measured for User document 18.
*
* It exercises, in one compile: the INHERITS clause, private and public
* member variables, the CREATE.OBJECT and DESTROY.OBJECT lifecycle hooks, a
* public subroutine and a public function with arguments, and a GET/SET pair
* forming a property.
*
* CATALOGUED PRIVATELY, not globally - a global catalogue needs an elevated
* session (User document 24), and nothing here should.
   class zzcls inherits zzbase

   private balance
   public label

   public subroutine create.object
      balance = 0
      label = 'unnamed'
      crt 'ZZCLS.CREATE.OBJECT balance=' : balance
   end

   public subroutine destroy.object
      crt 'ZZCLS.DESTROY.OBJECT balance=' : balance
   end

*  ---------------  a public subroutine, called for its effect

   public subroutine deposit(amount)
      balance += amount
   end

*  ---------------  a public function, called for its answer

   public function total(scale)
      return balance * scale
   end

*  ---------------  a GET/SET pair: one name, read and written like a variable

   get owner
      return 'owner<' : label : '>'
   end

   set owner(value)
      label = downcase(value)
   end

*  ---------------  overriding an inherited member

   public function whoami()
      return 'ZZCLS'
   end

end
