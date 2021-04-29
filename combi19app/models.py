from django.db import models

# Create your models here.

class Usuario (models.Model):
    usuario = models.CharField(max_length=15)
    contraseña = models.CharField(max_length=8)
    dni = models.BigIntegerField(primary_key = True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    email = models.EmailField( max_length=254, blank=True, null=True)
    direccion = models.CharField(max_length=20)
    telefono = models.IntegerField()
    tipo_usuario = models.IntegerField()

    def __str__(self):
        return "El usuario %s con DNI %s, es de tipo %s" % (self.usuario, self.dni, self.tipo_usuario)

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
