from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import HttpResponse, HttpRequest
from combi19app.forms import Registro, Registro_vehiculo, Registro_ruta, Registro_ciudad, Registro_viaje
from combi19app.models import Usuario, Vehiculo, Ruta, Ciudad, Viaje
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django import db
db.connections.close_all()
# Create your views here.
@login_required
def home (request):
    if request.user.tipo_usuario == 1:
        ciudades = Ciudad.objects.all()
        rutas = Ruta.objects.all()
        vehiculos = Vehiculo.objects.all()
        viajes = Viaje.objects.all()
        choferes = Usuario.objects.filter(tipo_usuario=2)
        usuarios = Usuario.objects.filter(tipo_usuario=3)
        return render (request, "home.html", {"ciudades":len(ciudades), "rutas":len(rutas), "choferes":len(choferes), "vehiculos":len(vehiculos), "viajes":len(viajes), "usuarios":len(usuarios), "nombre": request.user.nombre})
    elif request.user.tipo_usuario == 2:
        return render(request, "homeChofer.html", {"nombre": request.user.nombre})
    else:
        return render (request,"homePasajeros.html", {"nombre": request.user.nombre})

def login(request):

    return render (request, "registration/login.html")

def cambiar_contra(request):

    return render(request, "cambiar_contra.html")


#busca los campos incorrectos (repetidos) que llevan el valor None
def errores(registro):
    lista = []

    if registro.cleaned_data.get('dni') == None:
        lista+=[1]
    # user= Usuario.objects.all().__str__()
    # base_de_datos=user.replace('<QuerySet [', '').replace('1>,', '1').replace('2>,', '2').replace('3>,', '3').replace('<Usuario: ', '').replace('>', '').replace(']', '').split(' ')
    # lista_de_usuarios=[]
    #
    # for i in range(0,len(base_de_datos),4):
    #     lista_de_usuarios.append(base_de_datos[i:i+4])
    #
    # lista_de_usuarios.pop(len(lista_de_usuarios) -1)
    return set(lista)

def errores_ruta(ruta):
    lista = []

    if ruta.cleaned_data.get('nombre') == None:
        lista+=[1]
    if ruta.cleaned_data.get('origen') == ruta.cleaned_data.get('destino'):
        lista+=[2]

    return set(lista)

def errores_ciudad(ciudad):
    lista = []

    if ciudad.cleaned_data.get('codigo_postal') == None:
        lista+=[1]

    return set(lista)

def errores_viaje(viaje):
    lista=[]

    if viaje.cleaned_data.get('ciudad_origen') == viaje.cleaned_data.get('ciudad_destino'):
        lista+=[1]
    if viaje.cleaned_data.get('fecha_salida') > viaje.cleaned_data.get('fecha_llegada'):
        lista+=[2]

    return set(lista)

def errores_vehiculo(vehiculo):
    lista = []
    vehiculos = Vehiculo.objects.all()
    for v in vehiculos:
        if vehiculo.cleaned_data.get('patente').upper() == v.patente:
            lista+=[1]
            break
    return set(lista)

def calcular_minutos():
    minutos=[]
    for i in range(0,60):
        minutos+=[i]
    return minutos


class FormularioRegistro (HttpRequest):

    def crear_formulario(request):
        registro = Registro()
        return render (request, "registrarse.html", {"dato":registro})

    @csrf_exempt
    def procesar_formulario (request):
        registro = Registro(request.POST)
        if registro.is_valid():
            registro.save()
            registro = Registro()
            return render(request, "registrarse.html", {"dato": registro, "mensaje": "ok"})
        else:
            confirmacion=errores(registro)
            registro = Registro()
            return render(request, "registrarse.html", {"mensaje": "not_ok", "errores": confirmacion})

class FormularioRegistroChofer (HttpRequest):
    @login_required
    def crear_formulario(request):
        registro = Registro()
        return render (request, "registrar_chofer.html", {"dato":registro})
    @csrf_exempt
    def procesar_formulario (request):
        registro = Registro(request.POST)
        if registro.is_valid():
            registro.save_chofer()
            registro = Registro()
            return render(request, "registrar_chofer.html", {"dato": registro, "mensaje": "ok"})
        else:
            confirmacion=errores(registro)
            registro = Registro()
            return render(request, "registrar_chofer.html", {"mensaje": "not_ok", "errores": confirmacion})
    @login_required
    def editar_chofer(request, dni):
        chofer = Usuario.objects.get(dni=dni)
        registro = Registro_chofer(instance=chofer)
        return render(request, "modificar_chofer.html", {"dato": registro, "choferes": chofer})
    @login_required
    def actualizar_chofer(request, dni):
        chofer = Usuario.objects.get(dni=dni)
        registro = Registro_chofer(request.POST, instance=chofer)
        if registro.is_valid():
            registro.save()
        response = redirect('/listar_choferes/')
        return response
        #choferes = Usuario.objects.filter(tipo_usuario=2)
        #return render (request, "listar_choferes.html", {"choferes": choferes, "mensaje": "editado", "cantidad": len(choferes)})

class FormularioVehiculo (HttpRequest):
    @login_required
    def crear_formulario(request):
        vehiculo = Registro_vehiculo()
        return render (request, "agregar_vehiculo.html", {"dato": vehiculo})
    @login_required
    def procesar_formulario(request):
        vehiculo = Registro_vehiculo(request.POST)
        if vehiculo.is_valid():
            confirmacion = errores_vehiculo(vehiculo)
            if len(confirmacion) == 0:
                vehiculo.save_vehiculo()
                vehiculo = Registro_vehiculo()
                return render (request, "agregar_vehiculo.html", {"dato": vehiculo, "mensaje": "ok"})
            else:
                vehiculo = Registro_vehiculo()
                return render (request, "agregar_vehiculo.html", {"mensaje": "not_ok"})
        else:
            vehiculo = Registro_vehiculo()
            return render (request, "agregar_vehiculo.html", {"mensaje": "vacio"})

    @login_required
    def editar(request, patente_vehiculo):
        vehiculo = Vehiculo.objects.get(patente=patente_vehiculo)
        form = Registro_vehiculo(instance=vehiculo)
        return render (request, "modificar_vehiculo.html", {"form":form, "vehiculo":vehiculo})

    @login_required
    def actualizar(request, patente_vehiculo):
        vehiculo = Vehiculo.objects.get(patente=patente_vehiculo)
        form = Registro_vehiculo(request.POST, instance = vehiculo)
        if form.is_valid():
        #    db.connections.close_all()
            form.save()
            response = redirect('/listar_vehiculos/')
            return response
        #    vehiculos= Vehiculo.objects.all()
        #    return render (request, "listar_vehiculos.html", {"form":form,"vehiculos":vehiculos, "vehiculo":vehiculo, "mensaje": "editado"})

class ListarVehiculos(HttpRequest):
    @login_required
    def crear_listado(request):
        vehiculos = Vehiculo.objects.all()
        contexto = {'vehiculos': vehiculos, 'cantidad':len(vehiculos)}
        return render (request, "listar_vehiculos.html", contexto)
    @login_required
    def mostrar_detalle(request, patente_vehiculo):
        detalle= Vehiculo.objects.get(pk=patente_vehiculo)
        return render (request, "listar_vehiculos.html", {"dato":detalle, "mensaje":"detalle"})
    @login_required
    def mostrar_detalle_viaje_vehiculo(request, patente_vehiculo):
        detalle= Vehiculo.objects.get(pk=patente_vehiculo)
        return render (request, "listar_vehiculos.html", {"dato":detalle, "mensaje":"detalleViajeVehiculo"})

class EliminarVehiculo(HttpRequest):
    @login_required
    def eliminar_vehiculo(request, patente_vehiculo):
        vehiculo_eliminado = Vehiculo.objects.get(pk=patente_vehiculo)
        try:
            vehiculo_eliminado.delete()
            vehiculo = Vehiculo.objects.all()
            return render (request, "listar_vehiculos.html", {"vehiculos": vehiculo, "mensaje":"eliminado", "cantidad": len(vehiculo)})
        except:
            vehiculo = Vehiculo.objects.all()
            return render (request, "listar_vehiculos.html", {"vehiculos": vehiculo, "mensaje":"no_puede", "cantidad": len(vehiculo)})

class FormularioRuta (HttpRequest):
    @login_required
    def crear_formulario(request):
        ruta = Registro_ruta()
        ciudad = Ciudad.objects.all()
        return render (request, "agregar_ruta.html", {"dato": ruta, "ciudades": ciudad})

    @csrf_exempt
    def procesar_formulario(request):
        ruta = Registro_ruta(request.POST)
        ciudad = Ciudad.objects.all()
        if ruta.is_valid():
            confirmacion=errores_ruta(ruta)
            if len(confirmacion) == 0:
                ruta.save()
                ruta = Registro_ruta()
                return render (request, "agregar_ruta.html", {"dato": ruta, "mensaje": "ok", "ciudades": ciudad})
        confirmacion=errores_ruta(ruta)
        ruta = Registro_ruta()
        return render (request, "agregar_ruta.html", {"mensaje": "not_ok", "errores":confirmacion, "ciudades": ciudad})
    @login_required
    def editar_ruta(request, nombre):
        ruta = Ruta.objects.get(nombre=nombre)
        registro = Registro_ruta(instance=ruta)
        ciudad = Ciudad.objects.all()
        return render(request, "modificar_ruta.html", {"dato": registro, "rutas": ruta, "ciudades": ciudad})
    @login_required
    def actualizar_ruta(request, nombre):
        ruta = Ruta.objects.get(nombre=nombre)
        registro = Registro_ruta(request.POST, instance=ruta)
        if registro.is_valid():
            registro.save()
            response = redirect('/listar_rutas/')
            return response
        #rutas = Ruta.objects.all()
        #return render (request, "listar_rutas.html", {"rutas": rutas, "mensaje": "editado"})

class FormularioCiudad (HttpRequest):
    @login_required
    def crear_formulario(request):
        ciudad = Registro_ciudad()
        return render (request, "agregar_ciudad.html", {"dato": ciudad})
    @login_required
    def procesar_formulario(request):
        ciudad = Registro_ciudad(request.POST)
        if ciudad.is_valid():
            confirmacion=errores_ciudad(ciudad)
            if len(confirmacion) == 0:
                ciudad.save_ciudad()
                ciudad = Registro_ciudad()
                return render (request, "agregar_ciudad.html", {"dato": ciudad, "mensaje": "ok"})
        confirmacion=errores_ciudad(ciudad)
        ciudad = Registro_ciudad()
        return render (request, "agregar_ciudad.html", {"mensaje": "not_ok", "errores":confirmacion})
    @login_required
    def editar(request, codigo_postal):
        ciudad = Ciudad.objects.get(codigo_postal=codigo_postal)
        form = Registro_ciudad(instance=ciudad)
        return render (request, "modificar_ciudad.html", {"form":form, "ciudad":ciudad})
    @login_required
    def actualizar(request, codigo_postal):
        ciudad = Ciudad.objects.get(codigo_postal=codigo_postal)
        form = Registro_ciudad(request.POST, instance = ciudad)
        if form.is_valid():
            form.save()
            response = redirect('/listar_ciudades/')
            return response
            #ciudades= Ciudad.objects.all()
            #return render (request, "listar_ciudades.html", {"form":form, "ciudad":ciudad, "mensaje": "ok", "ciudades":ciudades, "mensaje": "editado"})

class ListarCiudad (HttpRequest):
    @login_required
    def crear_listado(request):
        ciudad = Ciudad.objects.all()
        print(ciudad)
        contexto = {'ciudades': ciudad, 'cantidad':len(ciudad)}
        return render (request, "listar_ciudades.html", contexto)
    @login_required
    def mostrar_detalle(request, codigo_postal):
        detalle= Ciudad.objects.get(pk=codigo_postal)
        return render (request, "listar_ciudades.html", {"dato":detalle, "mensaje":"detalle"})
    @login_required
    def mostrar_detalle_viaje_ciudad(request, codigo_postal):
        detalle= Ciudad.objects.get(pk=codigo_postal)
        return render (request, "listar_ciudades.html", {"dato":detalle, "mensaje":"detalleViajeCiudad"})

class EliminarCiudad (HttpRequest):
    @login_required
    def eliminar_ciudad(request, codigo_postal):
        ciudad_eliminada = Ciudad.objects.get(pk=codigo_postal)
        try:
            ciudad_eliminada.delete()
            ciudad = Ciudad.objects.all()
            return render (request, "listar_ciudades.html", {"ciudades": ciudad, "mensaje":"eliminado", "cantidad": len(ciudad)})
        except:
            ciudad = Ciudad.objects.all()
            return render (request, "listar_ciudades.html", {"ciudades": ciudad, "mensaje":"no_puede", "cantidad": len(ciudad)})

class ListarRuta (HttpRequest):
    @login_required
    def crear_listado(request):
        ruta = Ruta.objects.all()
        contexto = {'rutas': ruta, 'cantidad':len(ruta)}
        return render (request, "listar_rutas.html", contexto)
    @login_required
    def mostrar_detalle(request, nombre):
        detalle= Ruta.objects.get(pk=nombre)
        return render (request, "listar_rutas.html", {"dato":detalle, "mensaje":"detalle"})
    @login_required
    def mostrar_detalle_viaje_ruta(request, nombre):
        detalle= Ruta.objects.get(pk=nombre)
        return render (request, "listar_rutas.html", {"dato":detalle, "mensaje":"detalleViajeRuta"})
    @login_required
    def eliminar_ruta(request, nombre):
        ruta_eliminada = Ruta.objects.get(pk=nombre)
        try:
            ruta_eliminada.delete()
            ruta = Ruta.objects.all()
            return render (request, "listar_rutas.html", {"rutas": ruta, "mensaje":"eliminado", "cantidad": len(ruta)})
        except:
            ruta = Ruta.objects.all()
            return render (request, "listar_rutas.html", {"rutas": ruta, "mensaje":"no_puede", "cantidad": len(ruta)})


def errores_viajes(viaje, dato):

    if viaje.cleaned_data.get('fecha_salida') == None:
        viaje.fecha_salida = dato.fecha_salida
        print('viaje salida', viaje.fecha_salida)
    if viaje.cleaned_data.get('fecha_llegada') == None:
        viaje.fecha_llegada = dato.fecha_llegada

    return viaje

class FormularioViaje (HttpRequest):
    @login_required
    def crear_formulario(request):
        viaje = Registro_viaje()
        minutos = calcular_minutos()
        choferes = Usuario.objects.all()
        vehiculos = Vehiculo.objects.all()
        ciudades = Ciudad.objects.all()
        rutas = Ruta.objects.all()
        return render (request, "agregar_viaje.html", {"dato": viaje, "minutos":minutos, "choferes":choferes, "vehiculos": vehiculos, "ciudades":ciudades, "rutas":rutas})
    @login_required
    def procesar_formulario(request):
        viaje = Registro_viaje(request.POST)
        minutos = calcular_minutos()
        choferes = Usuario.objects.all()
        vehiculos = Vehiculo.objects.all()
        ciudades = Ciudad.objects.all()
        rutas = Ruta.objects.all()
        if viaje.is_valid():
            confirmacion = errores_viaje(viaje)
            if len(confirmacion) == 0:
                v = Vehiculo.objects.get(patente=viaje.cleaned_data.get('vehiculo'))
                viaje.save_viaje(v)
                viaje = Registro_viaje()
                return render (request, "agregar_viaje.html", {"dato": viaje, "mensaje":"ok", "minutos":minutos, "choferes":choferes, "vehiculos": vehiculos, "ciudades":ciudades, "rutas":rutas})
        confirmacion=errores_viaje(viaje)
        viaje = Registro_viaje()
        return render (request, "agregar_viaje.html", {"errores":confirmacion, "mensaje": "not_ok", "minutos":minutos, "choferes":choferes, "vehiculos": vehiculos, "ciudades":ciudades, "rutas":rutas})
    @login_required
    def editar_viaje(request, id_viaje):
        viaje = Viaje.objects.get(id=id_viaje)
        registro = Registro_viaje(instance=viaje)
        minutos = calcular_minutos()
        choferes = Usuario.objects.all()
        vehiculos = Vehiculo.objects.all()
        rutas = Ruta.objects.all()
        ciudades = Ciudad.objects.all()
        return render(request, "modificar_viaje.html", {"dato": registro, "viajes": viaje, "rutas": rutas, "ciudades": ciudades, "minutos": minutos, "vehiculos": vehiculos, "choferes": choferes})

    @csrf_exempt
    def actualizar_viaje(request, id_viaje):
        viaje = Viaje.objects.get(id=id_viaje)
        registro = Registro_viaje(request.POST, instance=viaje)
        if registro.is_valid():
            v = Vehiculo.objects.get(patente=registro.cleaned_data.get('vehiculo'))
            registro.save_viaje(v)
        else:
            dato = errores_viajes(registro, viaje)
            if dato.is_valid():
                dato.save_viaje2(dato)
        #viajes = Viaje.objects.all()
        #return render (request, "listar_viajes.html", {"viajes": viajes, "mensaje": "editado", "cantidad": len(viajes)})
        response = redirect('/listar_viajes/')
        return response

    def eliminar_viaje(request, id_viaje):
        viaje = Viaje.objects.get(id=id_viaje)
        viaje.delete()
        viaje = Viaje.objects.all()
        return render (request, "listar_viajes.html", {"viajes": viaje, "mensaje":"eliminado", "cantidad": len(viaje)})

class ListarViajes(HttpRequest):
    @login_required
    def crear_listado(request):
        viaje = Viaje.objects.all()
        contexto = {'viajes': viaje, 'cantidad':len(viaje)}
        return render (request, "listar_viajes.html", contexto)
    @login_required
    def mostrar_detalle(request, id_viaje):
        detalle= Viaje.objects.get(id=id_viaje)
        return render (request, "listar_viajes.html", {"dato":detalle, "mensaje":"detalle"})



class ListarChofer(HttpRequest):

    @csrf_exempt
    def crear_listado(request):
        chofer = Usuario.objects.filter(tipo_usuario=2)
        contexto = {'choferes': chofer, 'cantidad': len(chofer)}
        return render (request, "listar_choferes.html", contexto)
    @login_required
    def mostrar_detalle(request, dni):
        detalle = Usuario.objects.get(pk=dni)
        return render (request, "listar_choferes.html", {"dato": detalle, "mensaje":"detalle"})
    @login_required
    def mostrar_detalle_viaje_chofer(request, dni):
        detalle = Usuario.objects.get(pk=dni)
        return render (request, "listar_choferes.html", {"dato": detalle, "mensaje":"detalleViajeChofer"})
    @login_required
    def eliminar_chofer(request, dni):
        chofer_eliminado = Usuario.objects.get(pk=dni)
        try:
            chofer_eliminado.delete()
            chofer = Usuario.objects.filter(tipo_usuario=2)
            return render (request, "listar_choferes.html", {"choferes": chofer, "mensaje":"eliminado", "cantidad": len(chofer)})
        except:
            chofer = Usuario.objects.filter(tipo_usuario=2)
            return render (request, "listar_choferes.html", {"choferes": chofer, "mensaje":"no_puede", "cantidad": len(chofer)})
