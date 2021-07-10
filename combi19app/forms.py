from django import forms
from combi19app.models import Usuario, Vehiculo, Ruta, Ciudad, Viaje, Insumo, InformacionDeContacto, Comentario, Anuncio, Pasaje, Tarjeta, Ticket, Test, Premium_pago, Premium, Puntuar
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
        usuario.long_contra = len(usuario.password)
        usuario.set_password(self.cleaned_data['password'])
        usuario.puntos = 0
        if commit:
            usuario.save()
        return usuario

    def save_chofer(self, commit=True):
        usuario = super().save(commit= False)
        usuario.long_contra = len(usuario.password)
        usuario.set_password(self.cleaned_data['password'])
        usuario.tipo_usuario=2
        usuario.puntos = 0
        if commit:
            usuario.save()
        return usuario

    def save_admin(self, commit=True):
        usuario = super().save(commit= False)
        usuario.long_contra = len(usuario.password)
        usuario.set_password(self.cleaned_data['password'])
        usuario.tipo_usuario=1
        usuario.puntos = 0
        if commit:
            usuario.save()
        return usuario

class Registro_admin (forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ( 'dni',
                   'nombre',
                   'apellido',
                   'email',
                   'telefono',
                   'direccion',
                   )

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

class Registro_usuario (forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ( 'dni',
                   'nombre',
                   'apellido',
                   'email',
                   'telefono',
                   'direccion',
                   )

class Registro_usuario_premium (forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ( 'dni',
                   'nombre',
                   'apellido',
                   'email',
                   'telefono',
                   'direccion',
                   'is_premium',
                   'fecha_premium'
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
        ruta.nombre = ruta.nombre.upper()
        if commit:
            ruta.save()
        return ruta

class Registro_ciudad (forms.ModelForm):
    class Meta:
        model = Ciudad
        fields = ('nombre',
                   'provincia',
                   'codigo_postal',
                   'pais'
                   )

    def save_ciudad(self, commit=True):
        ciudad = super().save(commit= False)
        ciudad.nombre = ciudad.nombre.upper()
        if commit:
            ciudad.save()
        return ciudad

class Registro_viaje_sin_estado (forms.ModelForm):
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
                  'vendidos',
                  'precio',
                  )

    def save_viaje5(self, commit=True):
        viaje = super().save(commit=False)
        viaje.asientos_disponibles = viaje.asientos_disponibles + 1
        if commit:
            viaje.save()
        return viaje

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
                  'vendidos',
                  'precio',
                  'estado'
                  )

    def save_viaje(self, vehiculo, ruta, commit=True):
        viaje = super().save(commit= False)
        viaje.asientos_total = vehiculo.capacidad
        viaje.asientos_disponibles = vehiculo.capacidad - viaje.vendidos
        hora = viaje.hora_salida.split(':')
        viaje.puntaje = 0
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
        viaje.puntaje = 0
        if commit:
            viaje.save()
        return viaje

    def save_viaje3(self, ruta, cantidad, commit=True):
        viaje= super().save(commit = True)
        viaje.vendidos = viaje.vendidos + cantidad
        hora = viaje.hora_salida.split(':')
        viaje.puntaje = 0
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

    def save_viaje4(self, commit=True):
        viaje = super().save(commit=False)
        viaje.estado = 'cancelado'
        viaje.puntaje = 0
        if commit:
            viaje.save()
        return viaje

    def save_viaje5(self, commit=True):
        viaje = super().save(commit=False)
        viaje.asientos_disponibles = viaje.asientos_disponibles + 1
        if commit:
            viaje.save()
        return viaje

class Registro_viaje_puntos (forms.ModelForm):

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
                  'vendidos',
                  'precio',
                  'estado',
                  'puntaje'
                  )
    def save_puntos(self, puntos, commit=True):
        viaje = super().save(commit=False)
        viaje.puntaje += puntos
        if commit:
            viaje.save()
        return viaje

class Registro_insumo(forms.ModelForm):

    class Meta:
        model = Insumo
        fields = ('nombre',
                  'precio',
                  'stock',
                  'sabor',
                  'categoria'
                  )
    def save_insumo(self, commit=True):
        insumo = super().save(commit=False)
        insumo.nombre = insumo.nombre.upper()
        if commit:
            insumo.save()
        return insumo

    def save_insumo2(self, cantidad, commit=True):
        insumo = super().save(commit = True)
        insumo.stock = insumo.stock - cantidad
        if commit:
            insumo.save()
        return insumo

    def save_insumo3(self, cantidad, commit=True):
        insumo = super().save(commit = True)
        insumo.stock = insumo.stock + cantidad
        if commit:
            insumo.save()
        return insumo

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

class Registro_comentario(forms.ModelForm):

    class Meta:
        model = Comentario
        fields = ('usuario_dni',
                  'texto',
                  'fecha_y_hora',
                  'usuario_nombre',
                  'viaje'
                  )
class Registro_anuncio(forms.ModelForm):

    class Meta:
        model = Anuncio
        fields = ('titulo',
                  'texto',
                  'fecha_y_hora'
                  )

class Registro_contra(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('dni',
                  'password'
                  )

class Registro_pasaje(forms.ModelForm):

    class Meta:
        model = Pasaje
        fields = ('id_user',
                  'dni',
                  'nombre',
                  'apellido',
                  'nro_viaje',
                  'estado',
                  'tarjeta',
                  )

    def save_sube(self, commit=True):
        pasaje= super().save(commit = True)
        pasaje.estado = "Presente: ACEPTADO"
        if commit:
            pasaje.save()
        return pasaje

    def save_no_sube(self, commit=True):
        pasaje= super().save(commit = True)
        pasaje.estado = "Presente: RECHAZADO"
        if commit:
            pasaje.save()
        return pasaje

class Registro_tarjeta(forms.ModelForm):

    class Meta:
        model = Tarjeta
        fields = ('numero',
                  'vencimiento',
                  'titular',
                  'emisor',
                  'codigo',
                  'id_user'
                  )

class Registro_ticket(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ('viaje',
                  'id_user',
                  'id_pasaje',
                  'insumo',
                  'cantidad',
                  )

    def save_ticket(self, precio_insumo,commit=True):
        ticket= super().save(commit = True)
        ticket.precio_ticket = precio_insumo * float(ticket.cantidad)
        if commit:
            ticket.save()
        return ticket

    def save_ticket2(self, precio_insumo, cant, commit=True):
        ticket= super().save(commit = True)
        ticket.cantidad = ticket.cantidad + cant
        ticket.precio_ticket = precio_insumo * float(ticket.cantidad)
        if commit:
            ticket.save()
        return ticket

class Registro_test(forms.ModelForm):

    class Meta:
        model = Test
        fields = ('pasaje',
                  'viaje',
                  'temperatura',
                  'olfato',
                  'gusto',
                  'contacto'
                  )

class Registro_premium_pago(forms.ModelForm):

    class Meta:
        model = Premium_pago
        fields = ('id_user',
                  'fecha',
                  'nro_tarjeta'
                  )


class Registro_premium(forms.ModelForm):

    class Meta:
        model = Premium
        fields = ('descuento',
                  'cuota',
                  )

class Registro_puntuar(forms.ModelForm):

    class Meta:
        model = Puntuar
        fields = ('id_viaje',
                  'id_user',
                  )
