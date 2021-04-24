from django.db import models

# Create your models here.

class Usuario (models.Model):
    usuario = models.CharField(max_length=15)
    contraseña = models.CharField(max_length=8)

# class Chofer (models.Model):
#     usuario =
#     nombre = models.CharField(max_length=30)
#     apellido = models.CharField(max_length=50)
#     dni = models.IntegerField()
#     direccion = models.CharField(max_length=50)
#     telefono = models.
#     email =
