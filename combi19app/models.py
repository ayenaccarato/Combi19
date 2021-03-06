from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime, timedelta, date

# Create your models here.
class Usuario_Manager(BaseUserManager):
    def create_user(self, email, dni, nombre, apellido, direccion, telefono, password=None):
        us = self.model(
            email= self.normalize_email(email),
            dni=dni,
            nombre = nombre,
            apellido=apellido,
            direccion=direccion,
            telefono=telefono
        )
        us.long_contra = len(password)
        us.set_password(password)
        us.puntos = 0
        us.save(using=self._db)
        return us

    def create_superuser(self, password, email, dni, nombre, apellido, direccion, telefono):
        us = self.create_user(
            password=password,
            email=email,
            dni=dni,
            nombre = nombre,
            apellido=apellido,
            direccion=direccion,
            telefono=telefono
        )
        us.long_contra = len(password)
        # us.super_usuario = True
        us.is_admin = True
        us.is_superuser = True
        us.is_active= True
        us.tipo_usuario= 1
        us.puntos = 0
        us.save(using=self._db)
        return us


class Usuario(AbstractBaseUser, PermissionsMixin):
    dni = models.BigIntegerField(unique=True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    email = models.EmailField( max_length=254)
    direccion = models.CharField(max_length=20)
    telefono = models.IntegerField()
    long_contra = models.IntegerField()
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    puntos = models.IntegerField()
    #is_active = models.BooleanField(default= True)
    #staff = models.BooleanField(default= False)
    is_active = models.BooleanField(default=True, verbose_name='account is activated')
    is_admin = models.BooleanField(default=False, verbose_name='staff account')
    is_premium = models.BooleanField(default=False)
    fecha_premium =  models.DateTimeField('%m/%d/%Y', default=datetime.now)
    # super_usuario = models.BooleanField(default=False)
    tipo_usuario = models.IntegerField(default = 3)
    objects = Usuario_Manager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellido', 'direccion', 'telefono']

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.dni)

    @property
    def is_staff(self):
        return self.is_admin

class Vehiculo (models.Model):
    patente = models.CharField(max_length=10)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=4)
    capacidad = models.IntegerField( verbose_name="Cantidad de asientos")
    premium = models.BooleanField()


    def publish(self):
            self.save()

    def __str__(self):
        return self.patente

class Ciudad (models.Model):
    nombre = models.CharField(max_length=30)
    provincia = models.CharField(max_length=25)
    codigo_postal = models.IntegerField()
    pais = models.CharField(max_length=20, default="Argentina")

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.codigo_postal)


class Ruta (models.Model):
    origen = models.CharField(max_length=30)
    destino = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30)
    km = models.IntegerField()
    duracion = models.IntegerField()
    duracion_en = models.CharField(max_length=10)
    codigo_origen = models.IntegerField()
    codigo_destino = models.IntegerField()

    def publish(self):
        self.save()

    def __str__(self):
        return self.nombre

class Viaje (models.Model):
    fecha_salida = models.DateTimeField()
    fecha_llegada = models.DateTimeField('%m/%d/%Y')
    hora_salida = models.CharField(max_length=20)
    ruta = models.ForeignKey(Ruta, related_name='+', on_delete=models.PROTECT)
    chofer = models.ForeignKey(Usuario, related_name='+', on_delete=models.PROTECT)
    vehiculo = models.ForeignKey(Vehiculo, related_name='+', on_delete=models.PROTECT)
    asientos_total = models.IntegerField(default=0)
    asientos_disponibles = models.IntegerField(default=0)
    vendidos = models.IntegerField()
    precio = models.FloatField()
    estado = models.CharField(max_length=20)
    puntaje = models.IntegerField()
    def publish(self):
        self.save()

class InformacionDeContacto(models.Model):
    email = models.EmailField( max_length=254)
    direccion = models.CharField(max_length=50)
    telefono1 = models.IntegerField(null=True, blank=True)
    telefono2 = models.IntegerField(null=True, blank=True)
    celular = models.IntegerField(null=True, blank=True)
    descripcion = models.CharField(max_length=50)

class Insumo(models.Model):
    nombre = models.CharField(max_length=60)
    precio = models.FloatField()
    stock = models.IntegerField()
    sabor = models.BooleanField()
    categoria = models.CharField(max_length=20)

class Comentario(models.Model):
    usuario_dni=models.BigIntegerField()
    usuario_nombre = models.CharField(max_length=50)
    texto=models.CharField(max_length=10000)
    fecha_y_hora=models.CharField(max_length=50)
    viaje = models.ForeignKey(Viaje, related_name='+', on_delete=models.PROTECT)

class Anuncio(models.Model):
    titulo = models.CharField(max_length=20)
    texto = models.CharField(max_length=10000)
    fecha_y_hora=models.CharField(max_length=50)

class Tarjeta(models.Model):
    numero = models.CharField(max_length=50)
    vencimiento = models.CharField(max_length=6)
    titular = models.CharField(max_length=30)
    emisor = models.CharField(max_length=20)
    codigo = models.IntegerField()
    id_user = models.ForeignKey(Usuario, related_name='+', on_delete=models.PROTECT)

class Pasaje(models.Model):
    id_user = models.BigIntegerField()
    dni = models.BigIntegerField()
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    nro_viaje = models.ForeignKey(Viaje, related_name='+', on_delete=models.PROTECT)
    estado = models.CharField(max_length=20)
    tarjeta = models.ForeignKey(Tarjeta, related_name='+', on_delete=models.PROTECT, null = True, blank=True)

class Ticket(models.Model):
    viaje = models.ForeignKey(Viaje, related_name='+', on_delete=models.PROTECT)
    insumo = models.ForeignKey(Insumo, related_name='+', on_delete=models.PROTECT, null = True)
    cantidad= models.IntegerField(null=True)
    precio_ticket = models.FloatField(null=True)
    id_user = models.IntegerField()
    id_pasaje = models.IntegerField()

class Test(models.Model):
    pasaje = models.IntegerField()
    viaje = models.IntegerField()
    temperatura = models.CharField(max_length=20)
    olfato = models.BooleanField()
    gusto = models.BooleanField()
    contacto = models.BooleanField()

class Premium_pago(models.Model):
    id_user = models.IntegerField()
    fecha = models.DateTimeField('%m/%d/%Y')
    nro_tarjeta = models.CharField(max_length=50)

class Premium(models.Model):
    descuento = models.IntegerField()
    cuota = models.FloatField()

class Puntuar(models.Model):
    id_viaje = models.IntegerField()
    id_user = models.IntegerField()
