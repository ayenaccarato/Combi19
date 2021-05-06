from django import forms
from combi19app.models import Usuario, Vehiculo, Ruta, Ciudad, Viaje


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
class Registro_viaje (forms.ModelForm):
    class Meta:
        model = Viaje
        fields = ('fecha_salida',
                  'fecha_llegada',
                  'hora_salida',
                  'am_pm_salida',
                  'hora_llegada',
                  'am_pm_llegada',
                  'ruta',
                  'ciudad_origen',
                  'ciudad_destino',
                  'chofer',
                  'vehiculo',
                  'asientos_total',
                  'asientos_disponibles',
                  )
        widgets = {'fecha_salida': forms.DateInput(attrs={'tipe': 'date'}), 'fecha_llegada': forms.DateInput(attrs={'tipe': 'date'})}
