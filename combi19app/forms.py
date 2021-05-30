from django import forms
from combi19app.models import Usuario, Vehiculo, Ruta, Ciudad, Viaje, Insumo, InformacionDeContacto
from datetime import datetime, timedelta

class Registro (forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ( 'password',
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

    def save_admin(self, commit=True):
        usuario = super().save(commit= False)
        usuario.set_password(self.cleaned_data['password'])
        usuario.tipo_usuario=1
        if commit:
            usuario.save()
        return usuario

class Registro_chofer (forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ( 'nombre',
                   'apellido',
                   'dni',
                   'direccion',
                   'email',
                   'telefono',
                   )

class Registro_vehiculo (forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ('patente',
                   'marca',
                   'modelo',
                   'capacidad',
                   'premium',
                   )

    def save_vehiculo(self, commit=True):
        vehiculo = super().save(commit= False)
        vehiculo.patente = vehiculo.patente.upper()
        if commit:
            vehiculo.save()
        return vehiculo

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

    def save_ruta(self, ciudades, commit=True):
        ruta = super().save(commit= False)
        for i in ciudades:
            if ruta.origen == i.nombre:
                ruta.codigo_origen = i.codigo_postal
            if ruta.destino == i.nombre:
                ruta.codigo_destino = i.codigo_postal
        if commit:
            ruta.save()
        return ruta

class Registro_ciudad (forms.ModelForm):
    class Meta:
        model = Ciudad
        fields = ('nombre',
                   'provincia',
                   'codigo_postal',
                   'pais',
                   )

    def save_ciudad(self, commit=True):
        ciudad = super().save(commit= False)
        ciudad.nombre = ciudad.nombre.upper()
        if commit:
            ciudad.save()
        return ciudad


class Registro_viaje (forms.ModelForm):
    class Meta:
        model = Viaje
        fields = ('fecha_salida',
                  'fecha_llegada',
                  'hora_salida',
                  'ruta',
                  'chofer',
                  'vehiculo',
                  'asientos_total',
                  'asientos_disponibles',
                  'vendidos'
                  )

    def save_viaje(self, vehiculo, ruta, commit=True):
        viaje = super().save(commit= False)
        viaje.asientos_total = vehiculo.capacidad
        viaje.asientos_disponibles = vehiculo.capacidad
        hora = viaje.hora_salida.split(':')
        if hora[2] == "AM":
            viaje.fecha_salida = viaje.fecha_salida.replace(hour = int(hora[0]), minute=int(hora[1]))
        else:
            if int(hora[0]) == 12 :
                viaje.fecha_salida = viaje.fecha_salida.replace(hour = 0, minute=int(hora[1]))
            else:
                viaje.fecha_salida = viaje.fecha_salida.replace(hour = int(hora[0]) + 12, minute=int(hora[1]))
        if ruta.duracion_en == 'minutos':
            viaje.fecha_llegada = viaje.fecha_salida + timedelta(minutes = int(ruta.duracion))
        else:
            viaje.fecha_llegada = viaje.fecha_salida + timedelta(hours = int(ruta.duracion))
        if commit:
            viaje.save()
        return viaje

    def save_viaje2(self, fechas, commit=True):
        viaje = super().save(commit= False)
        viaje.fecha_salida = fechas.fecha_salida
        viaje.fecha_llegada = fechas.fecha_llegada
        if commit:
            viaje.save()
        return viaje

class Registro_insumo(forms.ModelForm):

    class Meta:
        model = Insumo
        fields = ('nombre',
                  'precio'
                  )
class Registro_info_de_contacto(forms.ModelForm):
    class Meta:
        model = InformacionDeContacto
        fields = ('email',
                  'direccion',
                  'telefono1',
                  'telefono2',
                  'celular',
                  'descripcion'
                  )
    def saveTelefono2None(self, commit=True):
        info = super().save(commit=False)
        info.telefono2 = None
        if commit:
            info.save()
        return info
