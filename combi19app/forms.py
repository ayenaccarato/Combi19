from django import forms
from combi19app.models import Usuario

class Registro (forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('usuario',
                   'contraseña',
                   'nombre',
                   'apellido',
                   'dni',
                   'direccion',
                   'email',
                   'telefono',
                   )
        
