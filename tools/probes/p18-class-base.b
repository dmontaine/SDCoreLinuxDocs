* p18-class-base.b - a base class, for User document 18.
*
* Catalogued privately as ZZBASE and inherited by ZZCLS via the INHERITS
* clause on its CLASS statement.  Everything here is deliberately small: the
* point is to see WHICH members reach a caller through inheritance and what
* the lifecycle hooks do, not to model anything.
   class zzbase

   private secret
   public tag

   public subroutine create.object
      secret = 'base-private'
      tag = 'base-tag'
      crt 'ZZBASE.CREATE.OBJECT'
   end

   public subroutine destroy.object
      crt 'ZZBASE.DESTROY.OBJECT'
   end

   public function whoami()
      return 'ZZBASE'
   end

   public function reveal()
      return secret
   end

end
