from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import HttpResponse, HttpRequest
from combi19app.forms import Registro, Registro_admin, Registro_vehiculo, Registro_ruta, Registro_ciudad, Registro_viaje, Registro_chofer, Registro_insumo, Registro_info_de_contacto, Registro_comentario, Registro_anuncio, Registro_usuario
from combi19app.models import Usuario, Vehiculo, Ruta, Ciudad, Viaje, Insumo, InformacionDeContacto, Comentario, Anuncio
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django import db
from datetime import datetime, timedelta, date
import dateutil.parser

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

def ver_perfil_admin(request):
    print('ver perfil', request.user.id)
    admin = Usuario.objects.get(id=request.user.id)
    long_c = admin.long_contra
    return render (request, "ver_perfil_admin.html", {'admin': admin, 'longitud': long_c})

def editar_admin(request):
    admin = Usuario.objects.get(id=request.user.id)
    registro = Registro_admin(instance=admin)
    return render(request, "modificar_admin.html", {"dato": registro, "admin": admin})

def ver_perfil_chofer(request):
    chofer = Usuario.objects.get(id=request.user.id)
    long_c = chofer.long_contra
    return render (request, "ver_perfil_chofer.html", {'chofer': chofer, 'longitud': long_c})

def editar_chofer(request):
    chofer = Usuario.objects.get(id=request.user.id)
    registro = Registro_chofer(instance=chofer)
    return render(request, "modificar_chofer2.html", {"dato": registro, "chofer": chofer})

def ver_perfil_usuario(request):
    usuario = Usuario.objects.get(id=request.user.id)
    long_c = usuario.long_contra
    return render (request, "ver_perfil_usuario.html", {'usuario': usuario, 'longitud': long_c})

def editar_usuario(request):
    usuario = Usuario.objects.get(id=request.user.id)
    registro = Registro_usuario(instance=usuario)
    return render(request, "modificar_usuario.html", {"dato": registro, "usuario": usuario})

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

def actualizar_admin(request, id_admin):
    admin = Usuario.objects.get(id=request.user.id)
    registro = Registro_admin(request.POST, instance=admin)
    if registro.is_valid():
        print('entro')
        confirmacion = errores(registro)
        if len(confirmacion) == 0:
            registro.save()
    print('neee')
    response = redirect('/ver_perfil_admin/')
    return response

def actualizar_chofer(request, id_chofer):
    chofer = Usuario.objects.get(id=request.user.id)
    registro = Registro_chofer(request.POST, instance=chofer)
    if registro.is_valid():
        print('entro')
        confirmacion = errores(registro)
        if len(confirmacion) == 0:
            registro.save()
    print('neee')
    response = redirect('/ver_perfil_chofer/')
    return response

def actualizar_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id=request.user.id)
    registro = Registro_usuario(request.POST, instance=usuario)
    if registro.is_valid():
        print('hola')
        confirmacion = errores(registro)
        if len(confirmacion) == 0:
            registro.save()
    print('neeee')
    response = redirect('/ver_perfil_usuario/')
    return response

def cambiar_contra(request):

    return render(request, "cambiar_contra.html")

def cambiar_contra_admin(request):
    admin = Usuario.objects.get(id=request.user.id)
    print(admin)
    registro = Registro(instance=admin)
    return render(request, "cambiar_contra_admin.html", {"dato": registro, "admin": admin})

def actualizar_contra_admin(request, id_admin):
    admin = Usuario.objects.get(id=request.user.id)
    print(admin.id)
    registro = Registro(request.POST, instance=admin)

    if registro.is_valid():
        registro.save_admin()
        print('guardado')

    response = redirect('/accounts/login/')
    return response

def errores_ruta(ruta):
    lista = []

    rutas = Ruta.objects.all()
    for r in rutas:
        if ruta.cleaned_data.get('nombre').upper() == r.nombre:
            lista+=[1]
            break

    if ruta.cleaned_data.get('origen') == ruta.cleaned_data.get('destino'):
        lista+=[2]

    return set(lista)

def errores_ruta2(ruta, r_vieja):
    lista = []

    rutas = Ruta.objects.all()
    if ruta.cleaned_data.get('nombre') != r_vieja.nombre:
        for r in rutas:
            if ruta.cleaned_data.get('nombre').upper() == r.nombre:
                lista+=[1]
                break

    if ruta.cleaned_data.get('origen') == ruta.cleaned_data.get('destino'):
        lista+=[2]

    return set(lista)

def errores_ciudad(ciudad):
    lista = []
    ciudades = Ciudad.objects.all()
    for c in ciudades:
        if ciudad.cleaned_data.get('codigo_postal') == c.codigo_postal:
            lista+=[1]
            break

    for c in ciudades:
        if (ciudad.cleaned_data.get('nombre').upper() == c.nombre) and ciudad.cleaned_data.get('provincia') == c.provincia:
            lista+=[2]
            break

    return set(lista)

def errores_ciudad2(ciudad, c_vieja):
    lista = []
    ciudades = Ciudad.objects.all()
    if ciudad.cleaned_data.get('codigo_postal') != c_vieja.codigo_postal:
        for c in ciudades:
            if ciudad.cleaned_data.get('codigo_postal') == c.codigo_postal:
                lista+=[1]
                break
            else:
                if c_vieja.nombre != ciudad.cleaned_data.get('nombre').upper() or c_vieja.provincia != ciudad.cleaned_data.get('provincia'):
                    if ciudad.cleaned_data.get('nombre').upper() == c.nombre and ciudad.cleaned_data.get('provincia') == c.provincia:
                        lista+=[2]
                        break

    else:
        for c in ciudades:
            print('entro al else')
            if (ciudad.cleaned_data.get('nombre').upper() == c.nombre) and (ciudad.cleaned_data.get('provincia') == c.provincia):
                print('if')
                lista+=[2]
                break


    return set(lista)

def errores_viaje(viaje):
    lista=[]

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

def verificar_eliminacion_ciudad(ciudad):
    lista = []
    lista2= []
    lista2+=[str(ciudad)]
    string = lista2[0]
    string = string.replace('<bound method QuerySet.first of <QuerySet [<Ciudad: ', '').replace('>]>>','').strip()
    verificacion1 = str(Ruta.objects.filter(codigo_origen=int(string)).first)
    verificacion2 = str(Ruta.objects.filter(codigo_destino=int(string)).first)
    print('verificacion antes',verificacion1)
    print('verificacion 2 antes', verificacion2)
    verificacion1 = verificacion1.replace('<bound method QuerySet.first of <QuerySet ','').replace('[','').replace(']>>','')
    verificacion2 = verificacion2.replace('<bound method QuerySet.first of <QuerySet ','').replace('[','').replace(']>>','')
    print('verificacion',verificacion1)
    print('verificacion2',verificacion2)
    if len(verificacion1) != 0 or len(verificacion2) != 0:
        lista+=[1]
    return set(lista)

class FormularioRegistro (HttpRequest):

    def crear_formulario(request):
        registro = Registro()
        return render (request, "registrarse.html", {"dato":registro})

    @csrf_exempt
    def procesar_formulario (request):
        registro = Registro(request.POST)
        if registro.is_valid():
            print(registro.cleaned_data.get('dni'))
            registro.save()
            registro = Registro()
            return render(request, "registrarse.html", {"dato": registro, "mensaje": "ok"})
        else:
            print(registro.cleaned_data.get('dni'))
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
            confirmacion = errores(registro)
            if len(confirmacion) == 0:
                registro.save_chofer()
                registro = Registro()
                return render(request, "registrar_chofer.html", {"dato": registro, "mensaje": "ok"})
        confirmacion=errores(registro)
        registro = Registro()
        return render(request, "registrar_chofer.html", {"mensaje": "not_ok", "errores": confirmacion})
    @login_required
    def editar_chofer(request, id_chofer):
        chofer = Usuario.objects.get(id=id_chofer)
        registro = Registro_chofer(instance=chofer)
        return render(request, "modificar_chofer.html", {"dato": registro, "choferes": chofer})
    @login_required
    def actualizar_chofer(request, id_chofer):
        chofer = Usuario.objects.get(id=id_chofer)
        registro = Registro_chofer(request.POST, instance=chofer)
        if registro.is_valid():
            confirmacion = errores(registro)
            if len(confirmacion) == 0:
                registro.save()
        response = redirect('/listar_choferes/')
        return response
        #choferes = Usuario.objects.filter(tipo_usuario=2)
        #return render (request, "listar_choferes.html", {"choferes": choferes, "mensaje": "editado", "cantidad": len(choferes)})


class FormularioRegistroAdmin (HttpRequest):
    @login_required
    def crear_formulario(request):
        registro = Registro()
        return render (request, "registrar_admin.html", {"dato":registro})
    @csrf_exempt
    def procesar_formulario (request):
        registro = Registro(request.POST)
        if registro.is_valid():
            confirmacion = errores(registro)
            if len(confirmacion) == 0:
                registro.save_admin()
                registro = Registro()
                return render(request, "registrar_admin.html", {"dato": registro, "mensaje": "ok"})
        confirmacion=errores(registro)
        registro = Registro()
        return render(request, "registrar_admin.html", {"mensaje": "not_ok", "errores": confirmacion})

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
    def editar(request, id_vehiculo):
        vehiculo = Vehiculo.objects.get(id=id_vehiculo)
        form = Registro_vehiculo(instance=vehiculo)
        return render (request, "modificar_vehiculo.html", {"form":form, "vehiculo":vehiculo})

    @login_required
    def actualizar(request, id_vehiculo):
        vehiculo = Vehiculo.objects.get(id=id_vehiculo)
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
    def mostrar_detalle(request, id_vehiculo):
        detalle= Vehiculo.objects.get(pk=id_vehiculo)
        return render (request, "listar_vehiculos.html", {"dato":detalle, "mensaje":"detalle"})
    @login_required
    def mostrar_detalle_viaje_vehiculo(request, id_vehiculo):
        detalle= Vehiculo.objects.get(pk=id_vehiculo)
        return render (request, "listar_vehiculos.html", {"dato":detalle, "mensaje":"detalleViajeVehiculo"})

class EliminarVehiculo(HttpRequest):
    @login_required
    def eliminar_vehiculo(request, id_vehiculo):
        vehiculo_eliminado = Vehiculo.objects.get(pk=id_vehiculo)
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
                ruta.save_ruta(ciudad)
                ruta = Registro_ruta()
                return render (request, "agregar_ruta.html", {"dato": ruta, "mensaje": "ok", "ciudades": ciudad})

        confirmacion=errores_ruta(ruta)
        ruta = Registro_ruta()
        return render (request, "agregar_ruta.html", {"mensaje": "not_ok", "errores":confirmacion, "ciudades": ciudad})

    @login_required
    def editar_ruta(request, id_ruta):
        ruta = Ruta.objects.get(id=id_ruta)
        registro = Registro_ruta(instance=ruta)
        ciudad = Ciudad.objects.all()
        return render(request, "modificar_ruta.html", {"dato": registro, "rutas": ruta, "ciudades": ciudad})
    @login_required
    def actualizar_ruta(request, id_ruta):
        ruta = Ruta.objects.get(id=id_ruta)
        registro = Registro_ruta(request.POST, instance=ruta)
        if registro.is_valid():
            confirmacion = errores_ruta2(registro, ruta)
            if len(confirmacion) == 0 :
                registro.save()
                response = redirect('/listar_rutas/')
                return response
            else:
                ciudad = Ciudad.objects.all()
                return render (request, "modificar_ruta.html", {"rutas":ruta,"ciudades":ciudad, "mensaje": "not_ok", "errores":confirmacion})
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
    def editar(request, id_ciudad):
        ciudad = Ciudad.objects.get(id=id_ciudad)
        form = Registro_ciudad(instance=ciudad)
        return render (request, "modificar_ciudad.html", {"form":form, "ciudad":ciudad})
    @login_required
    def actualizar(request, id_ciudad):
        ciudad = Ciudad.objects.get(id=id_ciudad)
        ciudad2 = Ciudad.objects.get(id=id_ciudad)
        form = Registro_ciudad(request.POST, instance = ciudad)
        if form.is_valid():
            ok = errores_ciudad2(form, ciudad2)
            if len(ok) == 0:
                form.save_ciudad()
        print('errores', ok, 'ciudad', ciudad, 'form', form)
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
    def mostrar_detalle(request, id_ciudad):
        detalle= Ciudad.objects.get(pk=id_ciudad)
        return render (request, "listar_ciudades.html", {"dato":detalle, "mensaje":"detalle"})
    @login_required
    def mostrar_detalle_viaje_ciudad(request, id_ciudad):
        detalle= Ciudad.objects.get(pk=id_ciudad)
        return render (request, "listar_ciudades.html", {"dato":detalle, "mensaje":"detalleViajeCiudad"})

class EliminarCiudad (HttpRequest):
    @login_required
    def eliminar_ciudad(request, id_ciudad):
        ciudad = Ciudad.objects.filter(pk=id_ciudad).first
        ciudad_eliminada = Ciudad.objects.get(pk=id_ciudad)
        confirmacion = verificar_eliminacion_ciudad(ciudad)
        ciudades = Ciudad.objects.all()
        if len(confirmacion) == 0:
            try:
                ciudad_eliminada.delete()
                return render (request, "listar_ciudades.html", {"ciudades": ciudades, "mensaje":"eliminado", "cantidad": len(ciudades)})
            except:
                return render (request, "listar_ciudades.html", {"ciudades": ciudades, "mensaje":"no_puede", "cantidad": len(ciudades)})
        else:
            return render (request, "listar_ciudades.html", {"ciudades": ciudades, "mensaje":"no_puede2", "cantidad": len(ciudades)})

class BuscarCiudad(HttpRequest):
    @login_required
    def listar_ciudades(request):
        ciudades = Ciudad.objects.all()
        return render (request, "buscar_viaje_ciudad_origen.html",{"ciudades": ciudades})

    @login_required
    def listar_ciudades_result(request):
        ruta = Ruta.objects.filter(origen=request.GET.get('origen'), destino=request.GET.get('destino'))
        print(ruta[1].id)
        viajes = []
        for r in ruta:
            date = dateutil.parser.parse(request.GET.get('fecha_salida'))
            #viajes += Viaje.objects.filter(ruta_id=r.id).filter(fecha_salida=date.date())
            viajes += Viaje.objects.filter(ruta_id=r.id ,fecha_salida__year=date.year,fecha_salida__day=date.day, fecha_salida__month=date.month)

        return render (request, "buscar_viaje_result.html",{"viajes": viajes})

class ListarRuta (HttpRequest):
    @login_required
    def crear_listado(request):
        ruta = Ruta.objects.all()
        contexto = {'rutas': ruta, 'cantidad':len(ruta)}
        return render (request, "listar_rutas.html", contexto)
    @login_required
    def mostrar_detalle(request, id_ruta):
        detalle= Ruta.objects.get(pk=id_ruta)
        return render (request, "listar_rutas.html", {"dato":detalle, "mensaje":"detalle"})
    @login_required
    def mostrar_detalle_viaje_ruta(request, id_ruta):
        detalle= Ruta.objects.get(pk=id_ruta)
        return render (request, "listar_rutas.html", {"dato":detalle, "mensaje":"detalleViajeRuta"})
    @login_required
    def eliminar_ruta(request, id_ruta):
        ruta_eliminada = Ruta.objects.get(pk=id_ruta)
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
                r = Ruta.objects.get(nombre=viaje.cleaned_data.get('ruta'))
                viaje.save_viaje(v,r)
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
            print("ok")
            confirmacion = errores_viaje(registro)
            if len(confirmacion) == 0:
                v = Vehiculo.objects.get(patente=registro.cleaned_data.get('vehiculo'))
                r = Ruta.objects.get(nombre=registro.cleaned_data.get('ruta'))
                registro.save_viaje(v,r)
        else:
            print(registro.cleaned_data.get('vehiculo'))
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
    def mostrar_detalle(request, id_chofer):
        detalle = Usuario.objects.get(pk=id_chofer)
        return render (request, "listar_choferes.html", {"dato": detalle, "mensaje":"detalle"})
    @login_required
    def mostrar_detalle_viaje_chofer(request, id_chofer):
        detalle = Usuario.objects.get(pk=id_chofer)
        return render (request, "listar_choferes.html", {"dato": detalle, "mensaje":"detalleViajeChofer"})
    @login_required
    def eliminar_chofer(request, id_chofer):
        chofer_eliminado = Usuario.objects.get(pk=id_chofer)
        try:
            chofer_eliminado.delete()
            chofer = Usuario.objects.filter(tipo_usuario=2)
            return render (request, "listar_choferes.html", {"choferes": chofer, "mensaje":"eliminado", "cantidad": len(chofer)})
        except:
            chofer = Usuario.objects.filter(tipo_usuario=2)
            return render (request, "listar_choferes.html", {"choferes": chofer, "mensaje":"no_puede", "cantidad": len(chofer)})

class ListarAdministradores(HttpRequest):
    @login_required
    def crear_listado(request):
        admin = Usuario.objects.filter(tipo_usuario=1)
        contexto = {'admin': admin, 'cantidad':len(admin)}
        return render (request, "listar_admin.html", contexto)
    @login_required
    def mostrar_detalle(request, id_admin):
        detalle= Usuario.objects.get(pk=id_admin)
        return render (request, "listar_admin.html", {"dato":detalle, "mensaje":"detalle"})

    @login_required
    def eliminar_admin(request, id_admin):
        admin_eliminado = Usuario.objects.get(pk=id_admin)
        try:
            admin_eliminado.delete()
            admin = Usuario.objects.filter(tipo_usuario=1)
            return render (request, "listar_admin.html", {"admin": admin, "mensaje":"eliminado", "cantidad": len(admin)})
        except:
            admin = Usuario.objects.filter(tipo_usuario=1)
            return render (request, "listar_admin.html", {"admin": admin, "mensaje":"no_puede", "cantidad": len(admin)})

class ListarPasajeros(HttpRequest):
    @login_required
    def crear_listado(request):
        usuarios = Usuario.objects.filter(tipo_usuario=3)
        contexto = {'usuarios': usuarios, 'cantidad':len(usuarios)}
        return render (request, "listar_pasajeros.html", contexto)

def errores_insumo(insumo):
    lista= []
    insumos = Insumo.objects.all()

    for i in insumos:
        if insumo.cleaned_data.get('nombre') == i.nombre:
            lista+=[1]
            break
    if str(insumo.cleaned_data.get('precio')).find(','):
        lista+=[2]
    return set(lista)

class FormularioInsumo(HttpRequest):
    @login_required
    def crear_formulario(request):
        insumo = Registro_insumo()
        return render (request, "agregar_insumo.html", {"dato": insumo})

    @login_required
    def procesar_formulario(request):
        insumo = Registro_insumo(request.POST)
        if insumo.is_valid():
            confirmacion = errores_insumo(insumo)
            if len(confirmacion) == 0:
                print('entro')
                insumo.save_insumo()
                insumo = Registro_insumo()
                return render (request, "agregar_insumo.html", {"dato": insumo, "mensaje":"ok"})

        print('nope', insumo.cleaned_data.get('nombre'), insumo.cleaned_data.get('precio'))
        confirmacion=errores_insumo(insumo)
        insumo = Registro_insumo()
        return render (request, "agregar_insumo.html", {"errores":confirmacion, "mensaje": "not_ok"})

    @login_required
    def editar_insumo(request, id_insumo):
        insumo = Insumo.objects.get(id=id_insumo)
        registro = Registro_insumo(instance=insumo)
        return render(request, "modificar_insumo.html", {"dato": registro, "insumos": insumo})

    @csrf_exempt
    def actualizar_insumo(request, id_insumo):
        insumo = Insumo.objects.get(id=id_insumo)
        registro = Registro_insumo(request.POST, instance=insumo)
        nombre = insumo.nombre
        if registro.is_valid():
            if nombre != registro.cleaned_data.get('nombre'):
                confirmacion = errores_insumo(registro)
                if len(confirmacion) == 0:
                    registro.save_insumo()
            else:
                registro.save_insumo()
        response = redirect('/listar_insumos/')
        return response

class ListarInsumos(HttpRequest):
    @login_required
    def crear_listado(request):
        insumo = Insumo.objects.all()
        contexto = {'insumos': insumo, 'cantidad':len(insumo)}
        return render (request, "listar_insumos.html", contexto)

    @login_required
    def mostrar_detalle(request, id_insumo):
        detalle= Insumo.objects.get(pk=id_insumo)
        return render (request, "listar_insumos.html", {"dato":detalle, "mensaje":"detalle"})

    def eliminar_insumo(request, id_insumo):
        insumo = Insumo.objects.get(id=id_insumo)
        insumo.delete()
        insumo = Insumo.objects.all()
        return render (request, "listar_insumos.html", {"insumos": insumo, "mensaje":"eliminado", "cantidad": len(insumo)})

class FormularioInfoDeContacto(HttpRequest):
    @login_required
    def ver_info_contacto(request):
        texto = InformacionDeContacto.objects.get(id=1)
        contexto = {'texto':texto}
        return render (request, "infoContacto.html", contexto)
    @login_required
    def menu_editar_info_contacto(request):
        texto = InformacionDeContacto.objects.get(id=1)
        contexto = {'texto':texto}
        return render (request, "menu_info_de_contacto.html", contexto)
    @login_required
    def editar_info_contacto(request, id_texto):
        texto = InformacionDeContacto.objects.get(id=id_texto)
        form = Registro_info_de_contacto(instance=texto)
        return render (request, "modificar_info_de_contacto.html", {"form":form, "texto":texto})
    @login_required
    def actualizarInfoDeContacto(request, id_texto):
        texto = InformacionDeContacto.objects.get(id=id_texto)
        form = Registro_info_de_contacto(request.POST, instance = texto)

        if form.is_valid():
        #    db.connections.close_all()
            if form.cleaned_data.get('telefono2') == 0:
                form.saveTelefono2None()
            form.save()
            response = redirect('/menu_info_de_contacto/')
            return response
        else:
            print(form.cleaned_data.get('direccion'))
            print(form.cleaned_data.get('email'))
            print(form.cleaned_data.get('celular'))
            print(form.cleaned_data.get('telefono1'))
            print(form.cleaned_data.get('telefono2'))
            print(form.cleaned_data.get('descripcion'))

class FormularioComentario(HttpRequest):
    @login_required
    def crear_formulario(request):
        comentario = Registro_comentario()
        anuncio = Registro_anuncio()
        comentarios = Comentario.objects.all().order_by('-id')
        anuncios = Anuncio.objects.all().order_by('-id')
        if (request.user.tipo_usuario == 1):
            return render (request, "carteleraPasajero.html",{"base": "admin_base.html", "tipo": request.user.tipo_usuario,"comentarios": comentarios, "anuncios":anuncios, "is_c":len(comentarios), "is_a":len(anuncios)})
        else:
            if (request.user.tipo_usuario == 2):
                return render (request, "carteleraPasajero.html",{"base": "chofer_base.html","tipo": request.user.tipo_usuario,"comentarios": comentarios, "anuncios":anuncios ,"is_c":len(comentarios), "is_a":len(anuncios)})
            else:
                return render (request, "carteleraPasajero.html",{"base": "usuario_base.html","dni":request.user.dni, "user":request.user.nombre + ' '+ request.user.apellido,"tipo": request.user.tipo_usuario,"comentarios": comentarios, "anuncios":anuncios ,"is_c":len(comentarios), "is_a":len(anuncios)})

    @login_required
    def procesar_formulario(request):
        comentario = Registro_comentario(request.POST)
        if comentario.is_valid():
                comentario.save()
                comentario = Registro_comentario()
                anuncios = Anuncio.objects.all().order_by('-id')
                comentarios = Comentario.objects.all().order_by('-id')
                if (request.user.tipo_usuario == 1):
                    return render (request, "carteleraPasajero.html",{"base": "admin_base.html", "tipo": request.user.tipo_usuario,"comentarios": comentarios, "anuncios":anuncios, "is_c":len(comentarios), "is_a":len(anuncios)})
                else:
                    if (request.user.tipo_usuario == 2):
                        return render (request, "carteleraPasajero.html",{"base": "chofer_base.html","tipo": request.user.tipo_usuario,"comentarios": comentarios, "anuncios":anuncios ,"is_c":len(comentarios), "is_a":len(anuncios)})
                    else:
                        return render (request, "carteleraPasajero.html",{"base": "usuario_base.html","dni":request.user.dni, "user":request.user.nombre + ' '+ request.user.apellido,"tipo": request.user.tipo_usuario,"comentarios": comentarios, "anuncios":anuncios ,"is_c":len(comentarios), "is_a":len(anuncios)})

    @login_required
    def eliminar_comentario(request, id_coment):
        comentario_eliminado = Comentario.objects.get(pk=id_coment)
        comentario_eliminado.delete()
        comentarios = Comentario.objects.all().order_by('-id')
        anuncios = Anuncio.objects.all().order_by('-id')
        if (request.user.tipo_usuario == 1):
            return render (request, "carteleraPasajero.html",{"base": "admin_base.html", "tipo": request.user.tipo_usuario,"comentarios": comentarios, "anuncios":anuncios, "is_c":len(comentarios), "is_a":len(anuncios)})
        else:
            return render (request, "carteleraPasajero.html",{"base": "usuario_base.html","dni":request.user.dni, "user":request.user.nombre + ' '+ request.user.apellido,"tipo": request.user.tipo_usuario,"comentarios": comentarios, "anuncios":anuncios ,"is_c":len(comentarios), "is_a":len(anuncios)})

class FormularioAnuncio(HttpRequest):
    @login_required
    def crear_formulario(request):
        anuncio = Registro_anuncio()
        return render (request, "agregar_anuncio.html", {"dni": request.user.dni})

    @login_required
    def procesar_formulario(request):
        anuncio = Registro_anuncio(request.POST)
        if anuncio.is_valid():
            anuncio.save()
            anuncio = Registro_anuncio()
            return render (request, "agregar_anuncio.html", {"dni": request.user.dni, "mensaje":"ok"})


    @login_required
    def eliminar_anuncio(request, id_anuncio):
        anuncio_eliminado = Anuncio.objects.get(pk=id_anuncio)
        anuncio_eliminado.delete()
        comentarios = Comentario.objects.all().order_by('-id')
        anuncios = Anuncio.objects.all().order_by('-id')
        return render (request, "carteleraPasajero.html",{"base": "admin_base.html","tipo": request.user.tipo_usuario,"comentarios": comentarios, "anuncios":anuncios, "is_c":len(comentarios), "is_a":len(anuncios)})

    @login_required
    def editar(request, id_anuncio):
        anuncio = Anuncio.objects.get(id=id_anuncio)
        form = Registro_anuncio(instance=anuncio)
        return render (request, "modificar_anuncio.html", {"form":form, "anuncio":anuncio})

    @login_required
    def actualizar(request, id_anuncio):
        anuncio = Anuncio.objects.get(id=id_anuncio)
        form = Registro_anuncio(request.POST, instance = anuncio)
        if form.is_valid():
            form.save()
            return render (request,"modificar_anuncio.html", {"form":form, "anuncio":anuncio, "mensaje": "ok"})
        print(form.cleaned_data.get('titulo'))
        print(form.cleaned_data.get('texto'))
        print(form.cleaned_data.get('fecha_y_hora'))
