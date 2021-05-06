from django import forms
from combi19app.models import Usuario, Vehiculo, Ruta, Ciudad
#from django.contrib.auth import get_user_model

#Usuario = get_user_model()

class Registro (forms.ModelForm):
    #password = forms.CharField(label='Contraseña', widget= forms.CharField(max_length=10))

    class Meta:
        model = Usuario
        fields = ('usuario',
                   'password',
                   'nombre',
                   'apellido',
                   'dni',
                   'direccion',
                   'email',
                   'telefono',
                   )

    def save(self, commit=True):
        usuario = super().save(commit= False)
        usuario.set_password(self.cleaned_data['password'])
        if commit:
            usuario.save()
        return usuario

    def save_chofer(self, commit=True):
        usuario = super().save(commit= False)
        usuario.set_password(self.cleaned_data['password'])
        usuario.tipo_usuario=2
        if commit:
            usuario.save()
        return usuario

class Registro_vehiculo (forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ('patente',
                   'marca',
                   'modelo',
                   'capacidad',
                   'premium',
                   )

class Registro_ruta (forms.ModelForm):
    class Meta:
        model = Ruta
        fields = ('origen',
                  'destino',
                  'nombre',
                  'km',
                  'duracion',
                  'duracion_en'
                  )

class Registro_ciudad (forms.ModelForm):
    class Meta:
        model = Ciudad
        fields = ('nombre',
                   'provincia',
                   'codigo_postal',
                   'pais',
                   )
