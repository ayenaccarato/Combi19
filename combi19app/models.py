from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class Usuario_Manager(BaseUserManager):
    def create_user(self, usuario, email, dni, nombre, apellido, direccion, telefono, password=None):
        us = self.model(
            usuario=usuario,
            email= self.normalize_email(email),
            dni=dni,
            nombre = nombre,
            apellido=apellido,
            direccion=direccion,
            telefono=telefono
        )
        us.set_password(password)
        us.save(using=self._db)
        return us

    def create_superuser(self, usuario, email, dni, nombre, apellido, direccion, telefono, password):
        us = self.create_user(
            usuario=usuario,
            email=email,
            dni=dni,
            nombre = nombre,
            apellido=apellido,
            direccion=direccion,
            telefono=telefono
        )
        # us.super_usuario = True
        us.admin = True
        us.is_staff = True
        us.is_superuser = True
        us.is_active= True
        us.save(using=self._db)
        return us


class Usuario(AbstractBaseUser, PermissionsMixin):
    usuario = models.CharField(max_length=15, unique=True)
    #contraseña = models.CharField(max_length=3000)
    dni = models.BigIntegerField(primary_key = True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    email = models.EmailField( max_length=254, unique=True)
    direccion = models.CharField(max_length=20)
    telefono = models.IntegerField()
    #is_active = models.BooleanField(default= True)
    staff = models.BooleanField(default= False)
    admin = models.BooleanField(default=False)
    # super_usuario = models.BooleanField(default=False)
    #tipo_usuario = models.IntegerField(default = 3)
    objects = Usuario_Manager()

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['dni', 'email', 'nombre', 'apellido', 'direccion', 'telefono']

    def publish(self):
        self.save()

    def __str__(self):
        return "%s %s %s %s" % (self.usuario, self.dni,self.email, self.tipo_usuario)

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff
    #class Meta:
    #    verbose_name = "Usuario"
    #    verbose_name_plural = "Usuarios"


class Vehiculo (models.Model):
    patente = models.CharField(max_length=10)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    capacidad = models.IntegerField( verbose_name="Cantidad de asientos")
    premium = models.BooleanField() # probar con 0 y 1 sino funca

    def __str__(self):
        return self.patente

class Ciudad (models.Model):
    nombre = models.CharField(max_length=30)
    provincia = models.CharField(max_length=25)
    codigo_postal = models.IntegerField(primary_key=True)
    pais = models.CharField(max_length=20)

class Ruta (models.Model):
    ident = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30)

class Viaje (models.Model):
    fecha_salida = models.DateTimeField()
    fecha_llegada = models.DateTimeField('%m/%d/%Y %H:%M') # fijarse si es ida y vuelta
    ciudad_origen = models.ForeignKey(Ciudad, related_name = 'ciudad_origen', on_delete=models.PROTECT)
    ciudad_destino = models.ForeignKey(Ciudad, related_name = 'ciudad_destino', on_delete=models.PROTECT)
    chofer = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT)
    asientos_total = models.IntegerField()
    asientos_disponibles = models.IntegerField()

class Tarjeta(models.Model):
    nro = models.BigIntegerField()
    banco = models.CharField(max_length=20)
    entidad = models.CharField(max_length=20)

class Pasajes(models.Model):
    dni = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    nro_viaje = models.ForeignKey(Viaje, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20)
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.PROTECT)






#     usuario =
#     nombre = models.CharField(max_length=30)
#     apellido = models.CharField(max_length=50)
#     dni = models.IntegerField()
#     direccion = models.CharField(max_length=50)
#     telefono = models.
#     email =
