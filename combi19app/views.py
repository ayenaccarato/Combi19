from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import HttpResponse, HttpRequest
from combi19app.forms import Registro, Registro_admin, Registro_vehiculo, Registro_ruta, Registro_ciudad, Registro_viaje, Registro_chofer, Registro_insumo, Registro_info_de_contacto, Registro_comentario, Registro_anuncio, Registro_usuario, Registro_contra, Registro_pasaje, Registro_tarjeta, Registro_ticket, Registro_premium, Registro_premium_pago, Registro_test, Registro_usuario_premium, Registro_puntuar, Registro_viaje_puntos
from combi19app.models import Usuario, Vehiculo, Ruta, Ciudad, Viaje, Insumo, InformacionDeContacto, Comentario, Anuncio, Pasaje, Tarjeta, Ticket, Premium, Test, Premium_pago, Puntuar
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
        viajes = Viaje.objects.filter(estado='activo')
        choferes = Usuario.objects.filter(tipo_usuario=2)
        usuarios = Usuario.objects.filter(tipo_usuario=3)
        return render (request, "home.html", {"ciudades":len(ciudades), "rutas":len(rutas), "choferes":len(choferes), "vehiculos":len(vehiculos), "viajes":len(viajes), "usuarios":len(usuarios), "nombre": request.user.nombre})
    elif request.user.tipo_usuario == 2:
        viajes = Viaje.objects.filter(chofer_id=request.user.id, estado='activo')
        if len(viajes) != 0:
            for v in viajes:
                current_time = datetime.now()
                hora = str((current_time.hour - 3))+":"+str(current_time.minute)+":"+str(current_time.second)
                if v.fecha_salida.date() < current_time.date():
                    v.estado = 'realizado'
                    v.save()
                else:
                    if v.fecha_salida.date() == current_time.date():
                        if str(v.fecha_salida.time()) < hora:
                            v.estado = 'realizado'
                            v.save()
        return render(request, "homeChofer.html", {"nombre": request.user.nombre, "viajes": len(viajes)})
    else:
        pasajes = Pasaje.objects.filter(id_user=request.user.id, estado='activo')
        viajes = []
        for p in pasajes:
            viajes.append(p.nro_viaje_id)

        if request.user.is_premium:
            al_dia = Premium_pago.objects.filter(id_user= request.user.id)
            al_dia_fecha = str(al_dia[len(al_dia)-1]).replace('Premium_pago object (', '').replace(')','')
            al_dia_fecha = Premium_pago.objects.get(id = int(al_dia_fecha))
            al_dia_fecha=str(al_dia_fecha.fecha).replace('00:00:00+00:00','').split('-')
            if al_dia_fecha[1] == "07":
                ok=True
            else:
                ok=False
            debe = 7 - int(al_dia_fecha[1])
            return render (request,"homePasajerosPremium.html", {"nombre": request.user.nombre, "viajes": len(set(viajes)),"ok":ok, "debe":debe})
        else:
            return render (request,"homePasajeros.html", {"nombre": request.user.nombre, "viajes": len(set(viajes))})

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

def editar_chofer2(request):
    chofer = Usuario.objects.get(id=request.user.id)
    registro = Registro_chofer(instance=chofer)
    return render(request, "modificar_chofer2.html", {"dato": registro, "chofer": chofer})

def ver_perfil_usuario(request):
    usuario = Usuario.objects.get(id=request.user.id)
    long_c = usuario.long_contra
    if request.user.is_premium:
        return render (request, "ver_perfil_usuario.html", {'usuario': usuario, 'longitud': long_c, 'base': "premium_base.html"})
    else:
        return render (request, "ver_perfil_usuario.html", {'usuario': usuario, 'longitud': long_c, 'base': "usuario_base.html"})

def editar_usuario(request):
    usuario = Usuario.objects.get(id=request.user.id)
    registro = Registro_usuario(instance=usuario)
    if request.user.is_premium:
        return render(request, "modificar_usuario.html", {"dato": registro, "usuario": usuario, 'base': "premium_base.html"})
    else:
        return render(request, "modificar_usuario.html", {"dato": registro, "usuario": usuario, 'base': "usuario_base.html"})


def errores(registro):
    lista = []

    if registro.cleaned_data.get('dni') == None:
        lista+=[1]
    return set(lista)

def actualizar_admin(request, id_admin):
    admin = Usuario.objects.get(id=request.user.id)
    registro = Registro_admin(request.POST, instance=admin)
    if registro.is_valid():
        confirmacion = errores(registro)
        if len(confirmacion) == 0:
            registro.save()
    response = redirect('/ver_perfil_admin/')
    return response

def actualizar_chofer2(request, id_chofer):
    chofer = Usuario.objects.get(id=request.user.id)
    registro = Registro_chofer(request.POST, instance=chofer)
    if registro.is_valid():
        confirmacion = errores(registro)
        if len(confirmacion) == 0:
            registro.save()
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

def confirmar_usuario(registro):
    lista = []
    usuarios = Usuario.objects.all()
    for us in usuarios:
        dni = us.dni
        if registro == str(dni):
            lista+=[1]
            break

    return set(lista)

def cambiar_contra(request):
    registro = Registro()
    return render(request, "verificar_dni.html", {'usuario': registro})

def procesar_contra(request):
    if request.POST.get('dni') != None:
        confirmacion = confirmar_usuario(request.POST.get('dni'))
        if len(confirmacion) != 0:
            usuario = Usuario.objects.get(dni=request.POST.get('dni'))
            registro = Registro(request.POST, instance=usuario)
            return render(request, "cambiar_contra.html", {'usuario': usuario})
        else:
            return render(request, "verificar_dni.html", {'mensaje': "no existe"})
    else:
        cambiar_contra(request)
        return render(request, "verificar_dni.html", {'dni': request.POST.get('dni')})

def actualizar_contra(request):
    confirmacion = confirmar_usuario(request.POST.get('dni'))
    if len(confirmacion) != 0:
        usuario = Usuario.objects.get(dni=request.POST.get('dni'))
        registro = Registro(request.POST, instance=usuario)
        if registro.is_valid():
            if registro.cleaned_data.get('tipo_usuario') == 1:
                registro.save_admin()
            elif registro.cleaned_data.get('tipo_usuario') == 2:
                registro.save_chofer()
            else:
                registro.save()

        response = redirect('/accounts/login/')
        return response
        #return render(request, "cambiar_contra.html", {'usuario': usuario, 'mensaje': "existe"})


def cambiar_contra_admin(request):
    admin = Usuario.objects.get(id=request.user.id)
    registro = Registro(instance=admin)
    return render(request, "cambiar_contra_admin.html", {"dato": registro, "admin": admin})

def actualizar_contra_admin(request, id_admin):
    admin = Usuario.objects.get(id=request.user.id)
    registro = Registro(request.POST, instance=admin)
    if registro.is_valid():
        registro.save_admin()

    response = redirect('/accounts/login/')
    return response

def cambiar_contra_usuario(request):
    usuario = Usuario.objects.get(id=request.user.id)
    registro = Registro(instance=usuario)
    if request.user.is_premium:
        return render(request, "cambiar_contra_usuario.html", {"dato": registro, "usuario": usuario, 'base':"premium_base.html"})
    else:
        return render(request, "cambiar_contra_usuario.html", {"dato": registro, "usuario": usuario, 'base':"usuario_base.html"})


def actualizar_contra_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id=request.user.id)
    registro = Registro(request.POST, instance=usuario)

    if registro.is_valid():
        registro.save()

    response = redirect('/accounts/login/')
    return response

def cambiar_contra_chofer(request):
    chofer = Usuario.objects.get(id=request.user.id)
    registro = Registro(instance=chofer)
    return render(request, "cambiar_contra_chofer.html", {"dato": registro, "chofer": chofer})

def actualizar_contra_chofer(request, id_chofer):
    chofer = Usuario.objects.get(id=request.user.id)
    registro = Registro(request.POST, instance=chofer)
    if registro.is_valid():
        registro.save_chofer()
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
    print('ruta', ruta.cleaned_data.get('nombre'), 'otra', r_vieja.nombre )
    if ruta.cleaned_data.get('nombre').upper() != r_vieja.nombre:
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

def errores_viaje(viaje,id_viaje):
    lista=[]
    if viaje.cleaned_data.get('precio') == None:
        lista+=[5]
    viajes = Viaje.objects.filter(vehiculo_id = viaje.cleaned_data.get('vehiculo').id, estado='activo')
    for v in viajes:
        if(id_viaje == 0 or id_viaje != v.id):
            #date = dateutil.parser.parse
            diaDespues = v.fecha_salida.date()+timedelta(days=+1)
            fechaDelViaje = viaje.cleaned_data.get('fecha_salida').date()
            fechaDelViajeDT = viaje.cleaned_data.get('fecha_salida')
            if v.fecha_salida.date() == viaje.cleaned_data.get('fecha_salida').date():
                lista+=[1]
                break
            elif v.fecha_llegada.date().strftime("%Y-%m-%d") == fechaDelViaje.strftime("%Y-%m-%d"):
                hora = viaje.cleaned_data.get('hora_salida').split(':')
                if hora[2] == "AM":
                    fechaDelViajeDT = fechaDelViajeDT.replace(hour = int(hora[0]), minute=int(hora[1]))
                else:
                    if int(hora[0]) == 12 :
                        fechaDelViajeDT = fechaDelViajeDT.replace(hour = 0, minute=int(hora[1]))
                    else:
                        fechaDelViajeDT = fechaDelViajeDT.replace(hour = int(hora[0]) + 12, minute=int(hora[1]))
                if (v.fecha_llegada.hour >= fechaDelViajeDT.hour):
                    lista+=[2]

                    break

    viajes2 = Viaje.objects.filter(chofer_id = viaje.cleaned_data.get('chofer').id, estado='activo')
    for v in viajes2:
        #date = dateutil.parser.parse
        if(id_viaje == 0 or id_viaje != v.id):
            diaDespues = v.fecha_salida.date()+timedelta(days=+1)
            fechaDelViaje = viaje.cleaned_data.get('fecha_salida').date()
            fechaDelViajeDT = viaje.cleaned_data.get('fecha_salida')
            if v.fecha_salida.date() == viaje.cleaned_data.get('fecha_salida').date():
                lista+=[3]
                break

            elif v.fecha_llegada.date().strftime("%Y-%m-%d") == fechaDelViaje.strftime("%Y-%m-%d"): #Si fecha de llegada = fecha del viaje
                hora = viaje.cleaned_data.get('hora_salida').split(':')
                if hora[2] == "AM":
                    fechaDelViajeDT = fechaDelViajeDT.replace(hour = int(hora[0]), minute=int(hora[1]))
                else:
                    if int(hora[0]) == 12 :
                        fechaDelViajeDT = fechaDelViajeDT.replace(hour = 0, minute=int(hora[1]))
                    else:
                        fechaDelViajeDT = fechaDelViajeDT.replace(hour = int(hora[0]) + 12, minute=int(hora[1]))
                if (v.fecha_llegada.hour >= fechaDelViajeDT.hour):
                    lista+=[4]
                    break
                if (v.fecha_llegada.hour <= fechaDelViajeDT.hour):
                    if fechaDelViajeDT.hour in range(v.fecha_llegada.hour, (v.fecha_llegada.hour+8)):
                        lista+=[6]
                        break

    return set(lista)

def errores_vehiculo(vehiculo):
    lista = []
    vehiculos = Vehiculo.objects.all()
    for v in vehiculos:
        if vehiculo.cleaned_data.get('patente').upper() == v.patente:
            lista+=[1]
            break
    return set(lista)

def errores_tarjeta(tarjeta):
    lista = []
    vencido = tarjeta.cleaned_data.get('vencimiento').split('/')
    if int(vencido[1]) < 21:
        lista+=[1]
    else:
        if int(vencido[1]) == 21:
            if int(vencido[0]) <= 7:
                lista+=[1]
    return set(lista)

def errores_ven(tarjeta):
    lista = []
    vencido = int(str(tarjeta).replace('Tarjeta object ','').replace('(','').replace(')',''))
    vencido = Tarjeta.objects.get(id=vencido)
    vencido = vencido.vencimiento.split('/')
    if int(vencido[1]) < 21:
        lista+=[1]
    else:
        if int(vencido[1]) == 21:
            if int(vencido[0]) <= 7:
                lista+=[2]
    return set(lista)

def errores_tareta2(tarjetas):
    for i in tarjetas:
        confirmacion=errores_ven(i)
        if len(confirmacion) != 0:
            i.delete()
    return tarjetas

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

def errores_vehiculo2(vehiculo, v_viejo):
    lista = []
    vehiculos = Vehiculo.objects.all()
    if vehiculo.cleaned_data.get('patente').upper() != v_viejo.patente:
        for v in vehiculos:
            if vehiculo.cleaned_data.get('patente').upper() == v.patente:
                lista+=[1]
                break
    return set(lista)

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
        vehiculo2 = Vehiculo.objects.get(id=id_vehiculo)
        form = Registro_vehiculo(request.POST, instance = vehiculo)
        if form.is_valid():
        #    db.connections.close_all()
            confirmacion = errores_vehiculo2(form, vehiculo2)
            if len(confirmacion) == 0:
                form.save()
            else:
                return render (request, "modificar_vehiculo.html", {"form":form, "vehiculo":vehiculo, "mensaje": "not_ok"})
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
        ruta2 = Ruta.objects.get(id=id_ruta)
        ciudad = Ciudad.objects.all()
        registro = Registro_ruta(request.POST, instance=ruta)
        if registro.is_valid():
            confirmacion = errores_ruta2(registro, ruta2)
            if len(confirmacion) == 0 :
                registro.save_ruta(ciudad)
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
            else:
                ciudad =Ciudad.objects.get(id=id_ciudad)
                return render (request, "modificar_ciudad.html", {"ciudad": ciudad, "errores": ok, "mensaje": "not_ok"})
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
        if request.user.is_premium:
            return render (request, "buscar_viaje_ciudad_origen.html",{"ciudades": ciudades, "base":"premium_base.html"})
        else:
            return render (request, "buscar_viaje_ciudad_origen.html",{"ciudades": ciudades, "base":"usuario_base.html"})


    @login_required
    def listar_ciudades_result(request):
        if request.GET.get('origen')==request.GET.get('destino'):
            ciudades = Ciudad.objects.all()
            return render (request, "buscar_viaje_ciudad_origen.html",{"ciudades": ciudades, "errores": 1})

        ruta = Ruta.objects.filter(origen=request.GET.get('origen'), destino=request.GET.get('destino'))
        viajes = []
        for r in ruta:
            if(request.GET.get('fecha_salida') != ""):
                date = dateutil.parser.parse(request.GET.get('fecha_salida'))
                if(date.day>12):
                    viajes += Viaje.objects.filter(ruta_id=r.id ,fecha_salida__year=date.year,fecha_salida__day=date.day, fecha_salida__month=date.month, estado='activo')
                else:
                    viajes += Viaje.objects.filter(ruta_id=r.id ,fecha_salida__year=date.year,fecha_salida__day=date.month, fecha_salida__month=date.day, estado='activo')
            else:
                viaje = Viaje.objects.filter(ruta_id=r.id)
                hoy = datetime.today()
                hora = str((hoy.hour - 3)) +":"+ str(hoy.minute) +":"+ str(hoy.second)
                for v in viaje:
                    if v.fecha_salida.date() > hoy.date():
                        viajes.append(v)
                    else:
                        if v.fecha_salida.date() == hoy.date():
                            if str(v.fecha_salida.time()) > hora:
                                viajes.append(v)
        if request.user.is_premium:
            return render (request, "buscar_viaje_result.html",{"viajes": viajes, "rutas":ruta, "base":"premium_base.html"})
        else:
            return render (request, "buscar_viaje_result.html",{"viajes": viajes, "rutas":ruta, "base": "usuario_base.html"})



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

def eliminar_pasajes(pasaje, ticket):

    for p in pasaje:
        for t in ticket:
            if p.id_user == t.id_user:
                t.delete()
        p.delete()

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
            confirmacion = errores_viaje(viaje,0)
            if len(confirmacion) == 0:
                v = Vehiculo.objects.get(patente=viaje.cleaned_data.get('vehiculo'))
                r = Ruta.objects.get(nombre=viaje.cleaned_data.get('ruta'))
                viaje.save_viaje(v,r)
                viaje = Registro_viaje()
                return render (request, "agregar_viaje.html", {"dato": viaje, "mensaje":"ok", "minutos":minutos, "choferes":choferes, "vehiculos": vehiculos, "ciudades":ciudades, "rutas":rutas})
        confirmacion=errores_viaje(viaje,0)
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
        registro1 = Registro_viaje(instance=viaje)
        registro = Registro_viaje(request.POST, instance=viaje)
        minutos = calcular_minutos()
        choferes = Usuario.objects.all()
        vehiculos = Vehiculo.objects.all()
        ciudades = Ciudad.objects.all()
        rutas = Ruta.objects.all()
        if registro.is_valid():
            print("ok")
            confirmacion = errores_viaje(registro,id_viaje)
            confirmacion = list(confirmacion)
            if len(confirmacion) == 0:
                v = Vehiculo.objects.get(patente=registro.cleaned_data.get('vehiculo'))
                r = Ruta.objects.get(nombre=registro.cleaned_data.get('ruta'))
                registro.save_viaje(v,r)
            else:
                viajes = Viaje.objects.all()
                return render (request, "modificar_viaje.html", {"viajes": viaje, "errores":confirmacion[0], "mensaje": "not_ok", "minutos":minutos, "choferes":choferes, "vehiculos": vehiculos, "ciudades":ciudades, "rutas":rutas})
        else:
            print(registro.cleaned_data.get('precio'))
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
        pasaje = Pasaje.objects.filter(nro_viaje_id= id_viaje, estado='cancelado')
        ticket = Ticket.objects.filter(viaje_id= id_viaje)
        try:
            viaje.delete()
            viaje = Viaje.objects.all()
            rutas = []
            for v in viaje:
                r = Ruta.objects.get(id = v.ruta_id)
                if r not in rutas:
                    rutas.append(r)
            return render (request, "listar_viajes.html", {"rutas": rutas, "viajes": viaje, "mensaje":"eliminado", "cantidad": len(viaje)})
        except:
            pasaje_activo = Pasaje.objects.filter(nro_viaje_id= id_viaje, estado='activo')
            print('activo', pasaje_activo)
            if len(pasaje_activo) == 0:
                eliminar = eliminar_pasajes(pasaje, ticket)
                viaje.delete()
                viaje = Viaje.objects.all()
                rutas = []
                for v in viaje:
                    r = Ruta.objects.get(id = v.ruta_id)
                    if r not in rutas:
                        rutas.append(r)
                return render (request, "listar_viajes.html", {"rutas": rutas, "viajes": viaje, "mensaje":"eliminado", "cantidad": len(viaje)})
            else:
                viaje = Viaje.objects.all()
                rutas = []
                for v in viaje:
                    r = Ruta.objects.get(id = v.ruta_id)
                    if r not in rutas:
                        rutas.append(r)
                return render (request, "listar_viajes.html", {"rutas": rutas, "viajes": viaje, "mensaje":"no_puede", "cantidad": len(viaje)})

class ListarViajes(HttpRequest):
    @login_required
    def crear_listado(request):
        viajes = Viaje.objects.filter(estado='activo')
        # viajes = []
        # rutas = []
        # for v in viaje:
        #     if v.estado == 'activo':
        #         hoy = datetime.today()
        #         if v.fecha_salida.date() >= hoy.date():
        #             print('agrego')
        #             viajes.append(v)
        #         else:
        #             if v.fecha_salida.date() < hoy.date():
        #                 print('fecha salida', fecha_salida.date(), 'hoy', hoy.date())
        #                 v.estado = 'realizado'
        #                 v.save()
        #     r = Ruta.objects.get(id = v.ruta_id)
        #     if r not in rutas:
        #         rutas.append(r)
        contexto = {'viajes': viajes, 'cantidad':len(viajes)}
        return render (request, "listar_viajes.html", contexto)

    @login_required
    def mostrar_detalle(request, id_viaje):
        detalle= Viaje.objects.get(id=id_viaje)
        ruta= Ruta.objects.get(id=detalle.ruta_id)
        return render (request, "listar_viajes.html", {"dato":detalle,"ruta":ruta, "mensaje":"detalle"})

    @login_required
    def listar_viajes_por_realizar(request):
        pasajes = Pasaje.objects.filter(id_user=request.user.id, estado='activo')
        viajes = []
        rutas = []
        for p in pasajes:
            viaje = Viaje.objects.get(id=p.nro_viaje_id, estado='activo')
            ruta = Ruta.objects.get(id=viaje.ruta_id)
            if ruta not in rutas:
                rutas.append(ruta)
            viajes.append(viaje)

            # if p.estado == 'activo':
            #     viaje = Viaje.objects.get(id=p.nro_viaje_id)
            #     ruta = Ruta.objects.get(id=viaje.ruta_id)
            #     if ruta not in rutas:
            #         rutas.append(ruta)
            #     current_time = datetime.today()
            #     hora = str((current_time.hour - 3)) +":"+ str(current_time.minute) +":"+ str(current_time.second)
            #     if(viaje.fecha_salida.date() > current_time.date()):
            #         viajes.append(viaje)
            #     else:
            #         if(viaje.fecha_salida.date() == current_time.date()):
            #             if(str(viaje.fecha_salida.time()) > hora):
            #                 viajes.append(viaje)

        if request.user.is_premium:
            return render (request, "ver_viajes_por_realizar.html", {'viajes': set(viajes), 'rutas': rutas, "base":"premium_base.html"})
        else:
            return render (request, "ver_viajes_por_realizar.html", {'viajes': set(viajes), 'rutas': rutas, "base":"usuario_base.html"})

    @login_required
    def listar_viajes_realizados(request):
        pasajes = Pasaje.objects.filter(id_user=request.user.id)
        print('pasajes', pasajes)
        viajes = []
        rutas = []
        for p in pasajes:
            viaje = Viaje.objects.get(id=p.nro_viaje_id)
            ruta = Ruta.objects.get(id=viaje.ruta_id)
            if ruta not in rutas:
                rutas.append(ruta)
            if viaje.estado == 'realizado':
                viajes.append(viaje)
            # if p.estado == 'activo':
            #     print('hola')
            #     viaje = Viaje.objects.get(id=p.nro_viaje_id)
            #     ruta = Ruta.objects.get(id=viaje.ruta_id)
            #     if ruta not in rutas:
            #         rutas.append(ruta)
            #     current_time = datetime.today()
            #     hora = str((current_time.hour - 3)) +":"+ str(current_time.minute) +":"+ str(current_time.second)
            #     if(viaje.fecha_salida.date() < current_time.date()):
            #         viajes.append(viaje)
            #     else:
            #         if(viaje.fecha_salida.date() == current_time.date()):
            #             if(str(viaje.fecha_salida.time()) < hora):
            #                 viajes.append(viaje)

        if request.user.is_premium:
            return render (request, "ver_viajes_realizados.html", {'viajes': set(viajes), 'rutas': rutas, "base":"premium_base.html"})
        else:
            return render (request, "ver_viajes_realizados.html", {'viajes': set(viajes), 'rutas': rutas, "base":"usuario_base.html"})

    @login_required
    def listar_proximos_viajes(request):
        viajes = Viaje.objects.filter(chofer_id=request.user.id, estado='activo')
        viajes_por_hacer = []
        rutas = []
        for v in viajes:
            viaje = Viaje.objects.get(id=v.id)
            ruta = Ruta.objects.get(id=viaje.ruta_id)
            if ruta not in rutas:
                rutas.append(ruta)
            viajes_por_hacer.append(viaje)
            # if v.estado == 'activo':
            #     viaje = Viaje.objects.get(id=v.id)
            #     ruta = Ruta.objects.get(id=viaje.ruta_id)
            #     if ruta not in rutas:
            #         rutas.append(ruta)
            #     current_time = datetime.today()
            #     hora = str((current_time.hour - 3)) +":"+ str(current_time.minute) +":"+ str(current_time.second)
            #     if(viaje.fecha_salida.date() > current_time.date()):
            #         viajes_por_hacer.append(viaje)
            #     else:
            #         if(viaje.fecha_salida.date() == current_time.date()):
            #             if(str(viaje.fecha_salida.time()) > hora):
            #                 viajes_por_hacer.append(viaje)
        contexto ={'viajes': viajes_por_hacer, 'rutas': rutas, 'cantidad': len(viajes_por_hacer)}
        return render (request, "listar_proximos_viajes.html", contexto)

    @login_required
    def listar_viajes_iniciados(request):
        viajes = Viaje.objects.filter(chofer_id=request.user.id)
        viajes_iniciados = []
        rutas = []
        for v in viajes:
            viaje = Viaje.objects.get(id=v.id)
            ruta = Ruta.objects.get(id=viaje.ruta_id)
            if ruta not in rutas:
                rutas.append(ruta)
            if v.estado == 'iniciado':
                viajes_iniciados.append(viaje)
        #         current_time = datetime.today()
        #         hora = str((current_time.hour - 3)) +":"+ str(current_time.minute) +":"+ str(current_time.second)
        #         if(viaje.fecha_salida.date() > current_time.date()):
        #             viajes_iniciados.append(viaje)
        #         else:
        #             if(viaje.fecha_salida.date() == current_time.date()):
        #                 if(str(viaje.fecha_salida.time()) > hora):
        #                     viajes_iniciados.append(viaje)
        contexto ={'viajes': viajes_iniciados, 'rutas': rutas, 'cantidad': len(viajes_iniciados)}
        return render (request, "listar_viajes_iniciados.html", contexto)

    @login_required
    def mostrar_detalle_chofer(request, id_viaje):
        detalle= Viaje.objects.get(id=id_viaje)
        ruta= Ruta.objects.get(id=detalle.ruta_id)
        return render (request, "listar_proximos_viajes.html", {"dato":detalle,"ruta":ruta, "mensaje":"detalle"})

    @login_required
    def cancelar_viaje_chofer(request, id_viaje):
        viajes = Viaje.objects.filter(chofer_id=request.user.id, estado='activo')
        if len(viajes) != 0:
            hoy = datetime.today()
            viaje = Viaje.objects.get(id=id_viaje, chofer_id=request.user.id, estado='activo')
        viaje.estado = 'cancelado'
        viaje.save()
        viajes = Viaje.objects.filter(chofer_id=request.user.id, estado='activo')
        return render (request, "listar_proximos_viajes.html", {"viaje": viaje, "viajes": viajes, "mensaje": 'cancelado'})
        #ListarViajes.listar_proximos_viajes(request)

    @login_required
    def confirmar_cancelado_viaje(request,id_viaje):
        viaje = Viaje.objects.get(id= id_viaje)
        return render (request, "cancelar_viaje.html", {"base":"chofer_base.html", "viaje": viaje})

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
        admins = Usuario.objects.filter(tipo_usuario=1)
        admin_eliminado = Usuario.objects.get(pk=id_admin)
        try:
            if id_admin != request.user.id:
                if len(admins) > 1:
                    admin_eliminado.delete()
                    admin = Usuario.objects.filter(tipo_usuario=1)
                    return render (request, "listar_admin.html", {"admin": admin, "mensaje":"eliminado", "cantidad": len(admin)})
            else:
                admin = Usuario.objects.filter(tipo_usuario=1)
                return render (request, "listar_admin.html", {"admin": admin, "mensaje":"no_puede", "cantidad": len(admin)})
        except:
            admin = Usuario.objects.filter(tipo_usuario=1)
            return render (request, "listar_admin.html", {"admin": admin, "mensaje":"no_puede", "cantidad": len(admin)})

    @login_required
    def confirmar_eliminado_admin(request, id_admin):
        usuario = Usuario.objects.get(id=id_admin)
        return render (request, "eliminar_admin.html", {"base":"admin_base.html", "usuario": usuario})

class ListarPasajeros(HttpRequest):
    @login_required
    def crear_listado(request):
        usuarios = Usuario.objects.filter(tipo_usuario=3)
        contexto = {'usuarios': usuarios, 'cantidad':len(usuarios)}
        return render (request, "listar_pasajeros.html", contexto)

    @login_required
    def eliminar_pasajero(request, id_usuario, id_viaje):
        pasajero_el = Pasaje.objects.get(id_user=id_usuario, nro_viaje_id=id_viaje)
        viaje = Viaje.objects.get(id=id_viaje)
        if viaje.estado == 'activo':
            testeado = False
            test = Test.objects.all()
            for t in test:
                if t.pasaje == pasajero_el.id:
                    if pasajero_el.id == 'Presente: aceptado' or  pasajero_el.id == 'Presente: rechazado':
                        testeado = True
                        break
            if not testeado:
                pasajero_el.delete()
                pasajeros = Pasaje.objects.filter(nro_viaje_id = id_viaje)
                viaje = Viaje.objects.get(id = id_viaje)
                return render (request, "ver_pasajeros.html", {"pasajeros":pasajeros, "viaje":viaje, "base":"chofer_base.html", 'mensaje':'eliminado'})
        pasajeros = Pasaje.objects.filter(nro_viaje_id = id_viaje)
        viaje = Viaje.objects.get(id = id_viaje)
        return render (request, "ver_pasajeros.html", {"pasajeros":pasajeros, "viaje":viaje, "base":"chofer_base.html"})

    @login_required
    def confirmar_eliminado_pasajero(request,id_viaje, id_usuario):
        pasajero = Pasaje.objects.get(id_user = id_usuario, nro_viaje_id=id_viaje)
        usuario = Usuario.objects.get(id=id_usuario)
        viaje = Viaje.objects.get(id= id_viaje)
        return render (request, "eliminar_pasajero.html", {"base":"chofer_base.html", "viaje": viaje, "pasajero": pasajero, "usuario": usuario})


def errores_insumo(insumo):
    lista= []
    insumos = Insumo.objects.all()

    for i in insumos:
        if insumo.cleaned_data.get('nombre').upper() == i.nombre:
            lista+=[1]
            break
        if insumo.cleaned_data.get('precio') == None:
            lista+=[2]
    return set(lista)

def errores_insumo2(insumo, i_vieja):
    lista = []
    insumos = Insumo.objects.all()
    if insumo.cleaned_data.get('nombre').upper() != i_vieja.nombre:
        for i in insumos:
            if insumo.cleaned_data.get('nombre').upper() == i.nombre:
                lista+=[1]
                break

    if insumo.cleaned_data.get('precio') == None:
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
                insumo.save_insumo()
                insumo = Registro_insumo()
                return render (request, "agregar_insumo.html", {"dato": insumo, "mensaje":"ok"})

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
        insumo2 = Insumo.objects.get(id=id_insumo)
        registro = Registro_insumo(request.POST, instance=insumo)
        if registro.is_valid():
            confirmacion = errores_insumo2(registro, insumo2)
            if len(confirmacion) == 0:
                registro.save_insumo()
                insumos = Insumo.objects.all()
                contexto = {'insumos': insumos, 'cantidad':len(insumos)}
                return render (request, "listar_insumos.html", contexto)
            else:
                insumo = Insumo.objects.get(id=id_insumo)
                return render (request, "modificar_insumo.html", {"insumos": insumo, "errores": confirmacion, "mensaje": "not_ok"})
        else:
            confirmacion = errores_insumo2(registro, insumo2)
            return render (request, "modificar_insumo.html", {"errores":confirmacion, "mensaje": "not_ok", "insumos":insumo})

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

    @login_required
    def eliminar_insumo(request, id_insumo):
        insumo = Insumo.objects.get(id=id_insumo)
        try:
            insumo.delete()
            insumo = Insumo.objects.all()
            return render (request, "listar_insumos.html", {"insumos": insumo, "mensaje":"eliminado", "cantidad": len(insumo)})
        except:
            insumo = Insumo.objects.all()
            return render (request, "listar_insumos.html", {"insumos": insumo, "mensaje":"no_puede", "cantidad": len(insumo)})

class FormularioInfoDeContacto(HttpRequest):
    @login_required
    def ver_info_contacto(request):
        texto = InformacionDeContacto.objects.get(id=1)
        if request.user.tipo_usuario == 2:
            return render (request, "infoContacto.html", {"texto":texto, "base":"chofer_base.html"})
        else:
            if request.user.is_premium:
                return render (request, "infoContacto.html", {"texto":texto, "base":"premium_base.html"})
            else:
                return render (request, "infoContacto.html", {"texto":texto, "base":"usuario_base.html"})

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
    def mostrar_viajes(request):
        anuncio = Registro_anuncio()
        anuncios = Anuncio.objects.all().order_by('-id')
        viajes = Viaje.objects.all()
        viajes_hechos= Viaje.objects.filter(estado='realizado')
        nombre_chofer={}
        viajes_usuario=[]
        usuario = request.user.id
        pasajes = Pasaje.objects.filter(id_user=request.user.id, estado='activo')
        habilita = []

        #faltaria agregar que el viaje sea realizado
        hoy = datetime.today()
        hora = str((hoy.hour - 3)) +":"+ str(hoy.minute) +":"+ str(hoy.second)
        for i in viajes:
            # hab_votar = Puntuar.objects.filter(id_user=request.user.id, id_viaje=i.id)
            # if len(hab_votar) == 0:
            #     habilita+=[i.id]
            # if i.fecha_llegada.date() < hoy.date():
            #     viajes_hechos+=[i]
            # else:
            #     if i.fecha_llegada.date() == hoy.date():
            #         if str(i.fecha_llegada.time()) < hora:
            #             viajes_hechos+=[i]
            if len(pasajes) != 0:
                pasaje = Pasaje.objects.filter(id_user=request.user.id, nro_viaje_id=i.id)
                if len(pasaje) != 0:
                    for p in pasaje:
                        viajes_usuario+=[p.nro_viaje_id]
                    hab_votar = Puntuar.objects.filter(id_user=request.user.id, id_viaje=i.id)
                    if len(hab_votar) == 0:
                        habilita+=[i.id]
            chofer = Usuario.objects.get (id = i.chofer_id)
            nombre_chofer[i.chofer]= chofer.nombre +' '+ chofer.apellido

        if (request.user.tipo_usuario == 1):
             return render (request, "carteleraPasajero.html",{"base": "admin_base.html", "tipo": request.user.tipo_usuario,"viajes": viajes_hechos,'viajes_usuario': set(viajes_usuario), "anuncios":anuncios, "is_c":len(viajes_hechos), "is_a":len(anuncios), "usuario":usuario, "nombre_chofer":nombre_chofer})
        else:
             if (request.user.tipo_usuario == 2):
                 return render (request, "carteleraPasajero.html",{"base": "chofer_base.html","tipo": request.user.tipo_usuario,"anuncios":anuncios ,"viajes":viajes_hechos,'viajes_usuario': set(viajes_usuario),"is_c":len(viajes_hechos), "is_a":len(anuncios), "usuario":usuario, "nombre_chofer":nombre_chofer})
             else:
                 if request.user.is_premium:
                      return render (request, "carteleraPasajero.html",{"base": "premium_base.html","tipo": request.user.tipo_usuario,"anuncios":anuncios ,"viajes_usuario": set(viajes_usuario), "viajes":viajes_hechos, "is_c":len(viajes_hechos), "is_a":len(anuncios), "usuario":usuario, "nombre_chofer":nombre_chofer, "habilitados": set(habilita)})
                 else:
                     return render (request, "carteleraPasajero.html",{"base": "usuario_base.html","tipo": request.user.tipo_usuario,"anuncios":anuncios ,"viajes_usuario": set(viajes_usuario), "viajes":viajes_hechos, "is_c":len(viajes_hechos), "is_a":len(anuncios), "usuario":usuario, "nombre_chofer":nombre_chofer, "habilitados": set(habilita)})


    def puntuar(request, id_viaje):
        viaje = Viaje.objects.get(id=id_viaje)
        v_puntuar = Registro_viaje_puntos(instance=viaje)
        puntuado = Registro_puntuar()
        if request.user.is_premium:
            return render (request, "puntuar.html", {'base':"premium_base.html", 'viaje': viaje, 'v_puntuar': v_puntuar, 'usuario':request.user.id})
        else:
            return render (request, "puntuar.html", {'base':"usuario_base.html", 'viaje': viaje, 'v_puntuar': v_puntuar, 'usuario':request.user.id})

    def guardar_puntos(request, id_viaje):
        viaje = Viaje.objects.get(id=id_viaje)
        puntos = viaje.puntaje
        v_puntuar = Registro_viaje_puntos(request.POST, instance=viaje)

        if v_puntuar.is_valid():
            print('holaa')
            v_puntuar.save_puntos(puntos)
            puntuado = Registro_puntuar(request.POST)
            if puntuado.is_valid():
                puntuado.save()
        anuncio = Registro_anuncio()
        anuncios = Anuncio.objects.all().order_by('-id')
        viajes = Viaje.objects.all()
        viajes_hechos=[]
        nombre_chofer={}
        viajes_usuario=[]
        usuario = request.user.id
        pasajes = Pasaje.objects.filter(id_user=request.user.id, estado='activo')
        habilita = []
        #faltaria agregar que el viaje sea realizado
        hoy = datetime.today()
        hora = str((hoy.hour - 3)) +":"+ str(hoy.minute) +":"+ str(hoy.second)
        for i in viajes:
            hab_votar = Puntuar.objects.filter(id_user=request.user.id, id_viaje=i.id)
            if len(hab_votar) == 0:
                habilita+=[i.id]
            if i.fecha_llegada.date() < hoy.date():
                viajes_hechos+=[i]
            else:
                if i.fecha_llegada.date() == hoy.date():
                    if str(i.fecha_llegada.time()) < hora:
                        viajes_hechos+=[i]
            if len(pasajes) != 0:
                pasaje = Pasaje.objects.filter(id_user=request.user.id, nro_viaje_id=i.id)
                if len(pasaje) != 0:
                    for p in pasaje:
                        viajes_usuario+=[p.nro_viaje_id]
            chofer = Usuario.objects.get (id = i.chofer_id)
            nombre_chofer[i.chofer]= chofer.nombre +' '+ chofer.apellido

        if request.user.is_premium:
            return render (request, "carteleraPasajero.html",{"base": "premium_base.html","tipo": request.user.tipo_usuario,"anuncios":anuncios ,"viajes_usuario": set(viajes_usuario), "viajes":viajes_hechos, "is_c":len(viajes_hechos), "is_a":len(anuncios), "usuario":usuario, "nombre_chofer":nombre_chofer, "habilitados": set(habilita)})
        else:
            return render (request, "carteleraPasajero.html",{"base": "usuario_base.html","tipo": request.user.tipo_usuario,"anuncios":anuncios ,"viajes_usuario": set(viajes_usuario), "viajes":viajes_hechos, "is_c":len(viajes_hechos), "is_a":len(anuncios), "usuario":usuario, "nombre_chofer":nombre_chofer, "habilitados": set(habilita)})

    @login_required
    def ver_comentarios(request,id_viaje,tipo, id_user):
        comentario = Registro_comentario()
        viaje = Viaje.objects.get(id = id_viaje)
        chofer = Usuario.objects.get(id = viaje.chofer_id)
        usuario = Usuario.objects.get(id = id_user)
        comentarios = Comentario.objects.filter(viaje_id = id_viaje).order_by('-id')
        pasaje = Pasaje.objects.filter(id_user = id_user, nro_viaje_id = id_viaje)
        if (tipo == 1):
             return render (request, "ver_comentario.html",{"base": "admin_base.html", "tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje),"usuario":usuario, "chofer":chofer})
        else:
             if (tipo == 2):
                 return render (request, "ver_comentario.html",{"base": "chofer_base.html","tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje), "usuario":usuario, "chofer":chofer})
             else:
                  if request.user.is_premium:
                      return render (request, "ver_comentario.html",{"base": "premium_base.html","tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje), "usuario":usuario, "chofer":chofer})
                  else:
                      return render (request, "ver_comentario.html",{"base": "usuario_base.html","tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje), "usuario":usuario, "chofer":chofer})

    @login_required
    def guardar_comentario(request,id_viaje, tipo, id_user):
        comentario = Registro_comentario(request.POST)
        viaje = Viaje.objects.get(id = id_viaje)
        chofer = Usuario.objects.get(id = viaje.chofer_id)
        usuario = Usuario.objects.get(id = id_user)
        pasaje = Pasaje.objects.filter(id_user = id_user)
        if comentario.is_valid():
            comentario.save()
            comentarios = Comentario.objects.filter(viaje_id = id_viaje).order_by('-id')
            if (tipo == 1):
                 return render (request, "ver_comentario.html",{"base": "admin_base.html", "tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje),"usuario":usuario, "chofer":chofer})
            else:
                 if (tipo == 2):
                     return render (request, "ver_comentario.html",{"base": "chofer_base.html","tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje), "usuario":usuario, "chofer":chofer})
                 else:
                     if request.user.is_premium:
                         return render (request, "ver_comentario.html",{"base": "premium_base.html","tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje), "usuario":usuario, "chofer":chofer})
                     else:
                          return render (request, "ver_comentario.html",{"base": "usuario_base.html","tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje), "usuario":usuario, "chofer":chofer})

    @login_required
    def eliminar_comentario(request, id_viaje,tipo,id_coment, id_user):
        comentario_eliminado = Comentario.objects.get(pk=id_coment)
        comentario_eliminado.delete()
        comentarios = Comentario.objects.filter(viaje_id = id_viaje).order_by('-id')
        viaje = Viaje.objects.get(id = id_viaje)
        chofer = Usuario.objects.get(id = viaje.chofer_id)
        usuario = Usuario.objects.get(id = id_user)
        pasaje = Pasaje.objects.filter(id_user = id_user)
        if (tipo == 1):
            return render (request, "ver_comentario.html",{"base": "admin_base.html", "tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje),"usuario":usuario, "chofer":chofer})
        else:
            if (tipo == 2):
                return render (request, "ver_comentario.html",{"base": "chofer_base.html","tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje), "usuario":usuario, "chofer":chofer})
            else:
                if request.user.is_premium:
                    return render (request, "ver_comentario.html",{"base": "premium_base.html","tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje), "usuario":usuario, "chofer":chofer})
                else:
                    return render (request, "ver_comentario.html",{"base": "usuario_base.html","tipo": tipo ,"viaje": viaje, "comentarios":comentarios, "is_c":len(comentarios), "puede_comentar":len(pasaje), "usuario":usuario, "chofer":chofer})


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
        viajes = Viaje.objects.all()
        viajes_hechos=[]
        nombre_chofer={}
        usuario = request.user.id
        #faltaria agregar que el viaje sea realizado
        hoy = datetime.today()
        hora = str((hoy.hour - 3)) +":"+ str(hoy.minute) +":"+ str(hoy.second)
        for i in viajes:
            if i.fecha_llegada.date() < hoy.date():
                viajes_hechos+=[i]
            else:
                if i.fecha_llegada.date() == hoy.date():
                    if str(i.fecha_llegada.time()) < hora:
                        viajes_hechos+=[i]
            chofer = Usuario.objects.get (id = i.chofer_id)
            nombre_chofer[i.chofer]= chofer.nombre +' '+ chofer.apellido
        if (request.user.tipo_usuario == 1):
             return render (request, "carteleraPasajero.html",{"base": "admin_base.html", "tipo": request.user.tipo_usuario,"comentarios": comentarios, "viajes": viajes_hechos, "anuncios":anuncios, "is_c":len(viajes_hechos), "is_a":len(anuncios), "usuario":usuario, "nombre_chofer":nombre_chofer})
        else:
             if (request.user.tipo_usuario == 2):
                 return render (request, "carteleraPasajero.html",{"base": "chofer_base.html","tipo": request.user.tipo_usuario,"anuncios":anuncios ,"viajes":viajes_hechos,"is_c":len(viajes_hechos), "is_a":len(anuncios), "usuario":usuario, "nombre_chofer":nombre_chofer})
             else:
                 return render (request, "carteleraPasajero.html",{"base": "usuario_base.html","tipo": request.user.tipo_usuario,"anuncios":anuncios ,"viajes":viajes_hechos, "is_c":len(viajes_hechos), "is_a":len(anuncios), "usuario":usuario, "nombre_chofer":nombre_chofer})


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


class ComprarPasaje(HttpRequest):

    @login_required
    def comprar_pasaje_cantidad(request,id_viaje):
        pasaje = Registro_pasaje()
        viaje = Viaje.objects.get(id = id_viaje)
        post = "true"
        usuario = request.user.id
        if request.user.is_premium:
            return render (request, "comprar_pasaje_cantidad.html", {"viaje": viaje,"dato":pasaje,"usuario":usuario, "base":"premium_base.html"})
        else:
            return render (request, "comprar_pasaje_cantidad.html", {"viaje": viaje,"dato":pasaje,"usuario":usuario, "base": "usuario_base.html"})
    @login_required
    def cancelar(request):
        return home(request)

    @login_required
    def comprar_pasaje_completar_datos(request,id_viaje):
        if (request.GET.get('post') =="false"):
            print("borrando pasajes sin abonar")
            Pasaje.objects.filter(estado='no abonado', id_user=request.user.id).delete()
            actual = int(request.GET.get('actual')) + 1
            usuario = request.user.id
            viaje = Viaje.objects.get(id = id_viaje)
            cant = request.GET.get('pasajes')
            if request.user.is_premium:
                return render (request, "comprar_pasaje_form.html", {"base":"premium_base.html","viaje": viaje, "actual":actual,"usuario":usuario, "cant":cant})
            else:
                return render (request, "comprar_pasaje_form.html", {"base":"usuario_base.html","viaje": viaje, "actual":actual,"usuario":usuario, "cant":cant})
        else:
            pasaje = Registro_pasaje(request.POST)
            if(pasaje.is_valid()):
                pasaje.save_pasaje()
                print("se guardo")
            actual = int(request.GET.get('actual').split('-')[0])
            cant = int(request.GET.get('actual').split('-')[1])
            usuario = request.user.id
            viaje = Viaje.objects.get(id = id_viaje)
            if(actual==cant):
                return ComprarPasaje.comprar_pasaje_menu(request,id_viaje)
            else:
                actual = actual+1
                if request.user.is_premium:
                    return render (request, "comprar_pasaje_form.html", {"base":"premium_base.html","viaje": viaje, "actual":actual,"usuario":usuario, "cant":cant})
                else:
                    return render (request, "comprar_pasaje_form.html", {"base":"usuario_base.html","viaje": viaje, "actual":actual,"usuario":usuario, "cant":cant})

    @login_required
    def comprar_pasaje_menu(request,id_viaje):
        viaje = Viaje.objects.get(id =id_viaje)
        hora_llegada = viaje.fecha_llegada.time()
        nombre = Ruta.objects.get(id = viaje.ruta_id)
        chofer = Usuario.objects.get (id = viaje.chofer_id)
        patente = Vehiculo.objects.get ( id = viaje.vehiculo_id).patente
        tipo_asiento = Vehiculo.objects.get ( id = viaje.vehiculo_id).premium
        pasaje = Pasaje.objects.filter(id_user=request.user.id, nro_viaje_id = id_viaje, estado= 'no abonado')
        if request.user.is_premium:
            return render (request, "comprar_pasaje_menu.html", {"base":"premium_base.html", "viaje": viaje, "tipo_asiento":tipo_asiento,"nombre":nombre, "hora_llegada":hora_llegada, "chofer":chofer,"patente":patente,"precio":len(pasaje)*viaje.precio, "ya_tiene":len(pasaje)})
        else:
            return render (request, "comprar_pasaje_menu.html", {"base":"usuario_base.html", "viaje": viaje, "tipo_asiento":tipo_asiento,"nombre":nombre, "hora_llegada":hora_llegada, "chofer":chofer,"patente":patente,"precio":len(pasaje)*viaje.precio, "ya_tiene":len(pasaje)})

    @login_required
    def mi_carrito(request,id_viaje):
        carrito = Ticket.objects.filter(id_user=request.user.id, viaje=id_viaje)
        viaje = Viaje.objects.get(id = id_viaje)
        precio_total =0
        for i in carrito:
            precio_total= precio_total + i.precio_ticket
        if request.user.is_premium:
            return render (request, "comprar_pasaje_carrito.html", {"base":"premium_base.html", "viaje":viaje,"insumos":carrito, "cosas":len(carrito), "precio_total":precio_total})
        else:
            return render (request, "comprar_pasaje_carrito.html", {"base":"usuario_base.html", "viaje":viaje,"insumos":carrito, "cosas":len(carrito), "precio_total":precio_total})

    @login_required
    def confirmar_eliminado(request,id_viaje, id_ticket):
        ticket = Ticket.objects.get(id = id_ticket)
        ins = Insumo.objects.get(id=ticket.insumo.id)
        insumo = Registro_insumo(instance=ins)
        viaje = Viaje.objects.get(id = id_viaje)
        if request.user.is_premium:
            return render (request, "comprar_pasaje_carrito_eliminar.html", {"base":"premium_base.html", "ticket":ticket, "insumo":ins, "viaje": viaje})
        else:
            return render (request, "comprar_pasaje_carrito_eliminar.html", {"base":"usuario_base.html", "ticket":ticket, "insumo":ins, "viaje": viaje})

    @login_required
    def eliminar_mi_carrito(request,id_viaje,id_ticket):
        ticket_eliminado = Ticket.objects.get(id=id_ticket)
        insumo = Insumo.objects.get(id = ticket_eliminado.insumo.id)
        cantidad = ticket_eliminado.cantidad
        form = Registro_insumo(request.POST, instance = insumo)
        ticket_eliminado.delete()
        carrito = Ticket.objects.filter(id_user=request.user.id, viaje=id_viaje)
        viaje = Viaje.objects.get(id = id_viaje)
        precio_total =0
        for i in carrito:
            precio_total= precio_total + i.precio_ticket
        if form.is_valid():
            form.save_insumo3(cantidad)
            if request.user.is_premium:
                return render (request, "comprar_pasaje_carrito.html", {"base":"premium_base.html", "viaje":viaje,"insumos":carrito, "cosas":len(carrito),"precio_total":precio_total})
            else:
                return render (request, "comprar_pasaje_carrito.html", {"base":"usuario_base.html", "viaje":viaje,"insumos":carrito, "cosas":len(carrito),"precio_total":precio_total})

    @login_required
    def tarjeta(request, id_viaje):
        tarjeta = Registro_tarjeta()
        tarjetas_registradas = Tarjeta.objects.filter(id_user_id=request.user.id)
        viaje = Viaje.objects.get(id =id_viaje)
        nombre = Ruta.objects.get(id = viaje.ruta_id)
        carrito = Ticket.objects.filter(id_user=request.user.id, viaje=id_viaje)
        pasaje = Pasaje.objects.filter(id_user=request.user.id, nro_viaje_id = id_viaje, estado= 'no abonado')
        precio_total_pasajes =len(pasaje)*viaje.precio
        precio_total = 0
        if len(carrito) != 0:
            for i in carrito:
                precio_total = precio_total + i.precio_ticket
        precio_total = precio_total + precio_total_pasajes
        usuario = request.user.id
        if len(tarjetas_registradas) != 0:
            tarjetas_registradas = errores_tareta2(tarjetas_registradas)
            if len(tarjetas_registradas) != 0:
                if request.user.is_premium:
                    premium = Premium.objects.get(id=1)
                    precio_p = precio_total * float(premium.descuento) / float(100)
                    precio_p = precio_total - precio_p
                    return render (request, "comprar_pasaje_tarjeta.html", {"cantidad":len(pasaje), "precio_pasajes":precio_total_pasajes, "precio_p":precio_p, "premium": premium ,"base":"premium_base.html", "mensaje":"no","viaje": viaje, "nombre":nombre, "ok":"no","cant":len(pasaje), "usuario":usuario,"tiene_tarjeta":1, "tarjetas":tarjetas_registradas,"carrito":carrito, "compro":len(carrito), "precio_total":precio_total})
                else:
                    return render (request, "comprar_pasaje_tarjeta.html", {"cantidad":len(pasaje), "precio_pasajes":precio_total_pasajes, "base":"usuario_base.html", "mensaje":"no","viaje": viaje, "nombre":nombre, "ok":"no","cant":len(pasaje), "usuario":usuario,"tiene_tarjeta":1, "tarjetas":tarjetas_registradas,"carrito":carrito, "compro":len(carrito), "precio_total":precio_total})
        if request.user.is_premium:
            premium = Premium.objects.get(id=1)
            precio_p = precio_total * float(premium.descuento) / float(100)
            precio_p = precio_total - precio_p
            return render (request, "comprar_pasaje_tarjeta.html", {"cantidad":len(pasaje), "precio_pasajes":precio_total_pasajes, "precio_p":precio_p, "premium": premium, "base":"premium_base.html", "mensaje":"no","viaje": viaje, "nombre":nombre, "ok":"no", "usuario":usuario,"cant":len(pasaje),"tiene_tarjeta":0,"carrito":carrito, "compro":len(carrito), "precio_total":precio_total})
        else:
            return render (request, "comprar_pasaje_tarjeta.html", {"cantidad":len(pasaje), "precio_pasajes":precio_total_pasajes, "base":"usuario_base.html", "mensaje":"no","viaje": viaje, "nombre":nombre, "ok":"no", "usuario":usuario,"cant":len(pasaje),"tiene_tarjeta":0,"carrito":carrito, "compro":len(carrito), "precio_total":precio_total})

    def otra_tarjeta(request, id_viaje):
        tarjeta = Registro_tarjeta()
        tarjetas_registradas= Tarjeta.objects.filter(id_user_id=request.user.id)
        viaje = Viaje.objects.get(id =id_viaje)
        nombre = Ruta.objects.get(id = viaje.ruta_id)
        carrito = Ticket.objects.filter(id_user=request.user.id, viaje=id_viaje)
        usuario = request.user.id
        carrito = Ticket.objects.filter(id_user=request.user.id, viaje=id_viaje)
        pasaje = Pasaje.objects.filter(id_user=request.user.id, nro_viaje_id = id_viaje, estado= 'no abonado')
        precio_total_pasajes =len(pasaje)*viaje.precio
        precio_total = 0
        if len(carrito) != 0:
            for i in carrito:
                precio_total = precio_total + i.precio_ticket
        precio_total = precio_total + precio_total_pasajes
        if len(tarjetas_registradas) != 0:
            if request.user.is_premium:
                premium = Premium.objects.get(id=1)
                precio_p = precio_total * float(premium.descuento) / float(100)
                precio_p = precio_total - precio_p
                return render (request, "comprar_pasaje_tarjeta.html", {"precio_p":precio_p, "premium":premium, "base":"premium_base.html", "mensaje":"otra", "viaje": viaje, "nombre":nombre, "ok":"no", "usuario":usuario,"tiene_tarjeta":1, "tarjetas":tarjetas_registradas,"carrito":carrito, "compro":len(carrito), "precio_total":precio_total, "cantidad":len(pasaje), "precio_pasajes":precio_total_pasajes})
            else:
                return render (request, "comprar_pasaje_tarjeta.html", {"base":"usuario_base.html", "mensaje":"otra", "viaje": viaje, "nombre":nombre, "ok":"no", "usuario":usuario,"tiene_tarjeta":1, "tarjetas":tarjetas_registradas,"carrito":carrito, "compro":len(carrito), "precio_total":precio_total, "cantidad":len(pasaje), "precio_pasajes":precio_total_pasajes})
        else:
            if request.user.is_premium:
                return render (request, "comprar_pasaje_tarjeta.html", {"base":"premium_base.html", "mensaje":"no","viaje": viaje, "nombre":nombre, "ok":"no", "usuario":usuario,"tiene_tarjeta":0,"carrito": carrito, "compro":len(carrito), "precio_total":precio_tota, "cantidad":len(pasaje), "precio_pasajes":precio_total_pasajesl})
            else:
                return render (request, "comprar_pasaje_tarjeta.html", {"base":"usuario_base.html", "mensaje":"no","viaje": viaje, "nombre":nombre, "ok":"no", "usuario":usuario,"tiene_tarjeta":0,"carrito": carrito, "compro":len(carrito), "precio_total":precio_total, "cantidad":len(pasaje), "precio_pasajes":precio_total_pasajes})

    @login_required
    def setear_tarjeta(request, id_viaje, id_tarjeta):
        pasaje = Registro_pasaje()
        viaje_form = Registro_viaje()
        tarjeta = Tarjeta.objects.get(id=id_tarjeta)
        viaje = Viaje.objects.get(id =id_viaje)
        ruta_id = Ruta.objects.get(id=(viaje.ruta).id)
        nombre = Ruta.objects.get(id = viaje.ruta_id)
        usuario = request.user.id
        carrito = Ticket.objects.filter(id_user=request.user.id, viaje=id_viaje)
        pasaje = Pasaje.objects.filter(id_user=request.user.id, nro_viaje_id = id_viaje, estado= 'no abonado')
        precio_total_pasajes =len(pasaje)*viaje.precio
        precio_total = 0
        if len(carrito) != 0:
            for i in carrito:
                precio_total = precio_total + i.precio_ticket
        precio_total = precio_total + precio_total_pasajes
        if request.user.is_premium:
            premium = Premium.objects.get(id=1)
            precio_p = precio_total * float(premium.descuento) / float(100)
            precio_p = precio_total - precio_p
            return render (request, "comprar_pasaje_tarjeta2.html", {"cantidad":len(pasaje),"precio_pasajes":precio_total_pasajes,"precio_p":precio_p,"premium":premium, "base":"premium_base.html", "viaje": viaje, "nombre":nombre,"tarjeta":tarjeta, "usuario":usuario, "carrito":carrito, "compro":len(carrito), "precio_total":precio_total})
        else:
            return render (request, "comprar_pasaje_tarjeta2.html", {"cantidad":len(pasaje),"precio_pasajes":precio_total_pasajes,"base":"usuario_base.html", "viaje": viaje, "nombre":nombre,"tarjeta":tarjeta,"usuario":usuario, "carrito":carrito, "compro":len(carrito), "precio_total":precio_total})

    @login_required
    def procesar_tarjeta(request, id_viaje):
        tarjeta = Registro_tarjeta(request.POST)
        tarjetas_registradas= Tarjeta.objects.filter(id_user_id=request.user.id)
        viaje = Viaje.objects.get(id =id_viaje)
        nombre = Ruta.objects.get(id = viaje.ruta_id)
        carrito = Ticket.objects.filter(id_user=request.user.id, viaje=id_viaje)
        pasajes = Pasaje.objects.filter(id_user=request.user.id, nro_viaje_id = id_viaje, estado= 'no abonado')
        precio_total_pasajes =len(pasajes)*viaje.precio
        precio_total = 0
        if len(carrito) != 0:
            for i in carrito:
                precio_total = precio_total + i.precio_ticket
        precio_total = precio_total + precio_total_pasajes
        usuario = request.user.id
        if tarjeta.is_valid():
            confirmacion= errores_tarjeta(tarjeta)
            if len(confirmacion) == 0:
                pasaje = Registro_pasaje()
                hay_tarjeta = Tarjeta.objects.filter(id_user_id = request.user.id, numero = tarjeta.cleaned_data.get('numero'))
                if len(hay_tarjeta):
                    id_t = Tarjeta.objects.get(numero = tarjeta.cleaned_data.get('numero'), id_user_id =request.user.id)
                else:
                    tarjeta.save()
                    id_t = Tarjeta.objects.last()
                if request.user.is_premium:
                    premium = Premium.objects.get(id=1)
                    precio_p = precio_total * float(premium.descuento) / float(100)
                    precio_p = precio_total - precio_p
                    return render (request, "comprar_pasaje_tarjeta3.html", {"cantidad":len(pasajes),"precio_pasajes":precio_total_pasajes,"precio_p":precio_p,"premium":premium,"base":"premium_base.html", "usuario":usuario, "viaje": viaje, "nombre":nombre, "tarjeta":id_t, "ok":"ok", "carrito":carrito, "compro": len(carrito), "precio_total":precio_total})
                else:
                    return render (request, "comprar_pasaje_tarjeta3.html", {"cantidad":len(pasajes),"precio_pasajes":precio_total_pasajes, "base":"usuario_base.html", "usuario":usuario, "viaje": viaje, "nombre":nombre, "tarjeta":id_t, "ok":"ok", "carrito":carrito, "compro": len(carrito), "precio_total":precio_total})
            else:
                if request.user.is_premium:
                    premium = Premium.objects.get(id=1)
                    precio_p = precio_total * float(premium.descuento) / float(100)
                    precio_p = precio_total - precio_p
                    return render (request, "comprar_pasaje_tarjeta3.html", {"cantidad":len(pasajes),"precio_pasajes":precio_total_pasajes,"precio_p":precio_p,"premium":premium,"base":"premium_base.html", "errores": confirmacion, "usuario":usuario,"viaje": viaje, "nombre":nombre, "ok": "not_ok","carrito":carrito, "compro": len(carrito), "precio_total":precio_total})
                else:
                    return render (request, "comprar_pasaje_tarjeta3.html", {"cantidad":len(pasajes),"precio_pasajes":precio_total_pasajes,"base":"usuario_base.html", "errores": confirmacion, "usuario":usuario,"viaje": viaje, "nombre":nombre, "ok": "not_ok","carrito":carrito, "compro": len(carrito), "precio_total":precio_total})

    @login_required
    def procesar_pasaje(request, id_viaje):
        pasaje = Pasaje.objects.filter(id_user=request.user.id, nro_viaje_id = id_viaje, estado= 'no abonado')
        viaje = Viaje.objects.get(id=id_viaje)
        tarjeta = Registro_tarjeta(request.POST)
        p = Registro_pasaje(request.POST)
        if p.is_valid():
            print(p.cleaned_data.get('tarjeta'))
            tarjeta=p.cleaned_data.get('tarjeta')
        else:
            print(p.cleaned_data.get('tarjeta'))
            tarjeta=p.cleaned_data.get('tarjeta')

        #if tarjeta.is_valid():
            #print(tarjeta.cleaned_data.get('numero'))
            #tarjeta = Tarjeta.objects.get(numero = tarjeta.cleaned_data.get('numero'))
        #else:
            #print(tarjeta.cleaned_data.get('numero'))
        for p in pasaje:
            p.tarjeta = tarjeta
            p.estado ='activo'
            p.save()
        form = Registro_viaje(request.POST, instance = viaje)
        if form.is_valid():
            ruta = Ruta.objects.get(id=(viaje.ruta).id)
            form.save_viaje3(ruta, len(pasaje))
            verificar=Pasaje.objects.filter(id_user=request.user.id, nro_viaje_id = id_viaje, estado= 'activo')
            if request.user.is_premium:
                return render (request, "comprar_pasaje_pagar.html", {"base":"premium_base.html", "aceptado":"si", "pasaje":verificar, "viaje":viaje})
            else:
                return render (request, "comprar_pasaje_pagar.html", {"base":"usuario_base.html", "aceptado":"si", "pasaje":verificar, "viaje":viaje})

    @login_required
    def ver_tienda(request, id_viaje):
        insumos = Insumo.objects.all()
        stocks={}
        for i in insumos:
            stocks[i.id] = range(1,i.stock+1)
        viaje = Viaje.objects.get(id= id_viaje)
        usuario = request.user.id
        if request.user.is_premium:
            return render (request, "comprar_pasaje_tienda.html", {"base":"premium_base.html", "insumos":insumos, "stocks":stocks,"tienda":len(insumos), "viaje":viaje, "usuario":usuario, "vendido":"no"})
        else:
            return render (request, "comprar_pasaje_tienda.html", {"base":"usuario_base.html", "insumos":insumos, "stocks":stocks,"tienda":len(insumos), "viaje":viaje, "usuario":usuario, "vendido":"no"})

    @login_required
    def procesar_ver_tienda(request, id_viaje, id_insumo):
        carrito = Registro_ticket()
        insumo_comprado = Registro_insumo()
        viaje = Viaje.objects.get(id= id_viaje)
        insumo = Insumo.objects.get(id=id_insumo)
        usuario = request.user.id
        insumos = Insumo.objects.all()
        stocks={}
        for i in insumos:
            stocks[i.id] = range(1,i.stock+1)
        if request.user.is_premium:
            return render (request, "comprar_pasaje_seleccionar_cantidad.html", {"base":"premium_base.html", "insumos":insumos,"insumo":insumo, "stocks":stocks, "usuario":usuario, "viaje":viaje})
        else:
            return render (request, "comprar_pasaje_seleccionar_cantidad.html", {"base":"usuario_base.html", "insumos":insumos,"insumo":insumo, "stocks":stocks, "usuario":usuario, "viaje":viaje})

    @login_required
    def procesar_confirmacion_insumo(request, id_viaje, id_insumo):
        ya_esta = Ticket.objects.filter(id_user = request.user.id, viaje_id = id_viaje, insumo_id = id_insumo)
        if len(ya_esta) != 0:
            ins = str(ya_esta).replace('<QuerySet [<Ticket: Ticket object (','').replace(')>]>','')
            ins = Ticket.objects.get(id = ins)
            cant= ins.cantidad
            ticket = Registro_ticket(request.POST, instance= ins)
            ok=True
        else:
            ticket = Registro_ticket(request.POST)
            ok=False
        insumo_comprado = Insumo.objects.get(id=id_insumo)
        viaje = Viaje.objects.get(id= id_viaje)
        usuario = request.user.id
        form = Registro_insumo(request.POST, instance = insumo_comprado)
        if ticket.is_valid():
            cantidad = ticket.cleaned_data.get('cantidad')
            if ok:
                ticket.save_ticket2(insumo_comprado.precio, cant)
            else:
                ticket.save_ticket(insumo_comprado.precio)
            form = Registro_insumo(request.POST, instance = insumo_comprado)
            if form.is_valid():
                form.save_insumo2(cantidad)
                insumos = Insumo.objects.all()
                stocks={}
                for i in insumos:
                    stocks[i.id] = range(1,i.stock+1)
                if request.user.is_premium:
                    return render (request, "comprar_pasaje_tienda.html", {"base":"premium_base.html", "insumos":insumos, "stocks":stocks,"tienda":len(insumos), "viaje":viaje, "usuario":usuario, "vendido":"si"})
                else:
                    return render (request, "comprar_pasaje_tienda.html", {"base":"usuario_base.html", "insumos":insumos, "stocks":stocks,"tienda":len(insumos), "viaje":viaje, "usuario":usuario, "vendido":"si"})

    @login_required
    def cancelar_pasaje(request, id_viaje):
        pasaje = Pasaje.objects.filter(id_user=request.user.id, nro_viaje_id= id_viaje, estado= 'activo')
        print('pasaje', pasaje )
        if len(pasaje) != 0:
            pasaje = Pasaje.objects.get(id_user=request.user.id, nro_viaje_id= id_viaje, estado= 'activo')
        pasaje.estado ='cancelado'
        pasaje.save()
        viaje = Viaje.objects.get(id=id_viaje)
        viaje.asientos_disponibles = viaje.asientos_disponibles + 1
        viaje.save()
        return ListarViajes.listar_viajes_por_realizar(request)

    @login_required
    def ver_detalle_pasaje(request, id_viaje):
        viaje = Viaje.objects.get(id = id_viaje)
        chofer = Usuario.objects.get (id = viaje.chofer_id)
        pasaje = Pasaje.objects.filter(id_user=request.user.id, nro_viaje_id = id_viaje, estado= 'activo')
        if len(pasaje) != 0:
            pasaje = Pasaje.objects.get(id_user=request.user.id, nro_viaje_id = id_viaje, estado= 'activo')
        usuario = Usuario.objects.get(id = pasaje.id_user)
        tarjeta = Tarjeta.objects.get(id = pasaje.tarjeta_id)
        carrito = Ticket.objects.filter(id_user=request.user.id, viaje=id_viaje)
        precio_total = 0
        if len(carrito) != 0:
            for i in carrito:
                precio_total = precio_total + i.precio_ticket
        precio_total = precio_total + viaje.precio
        if request.user.is_premium:
            return render (request, "ver_detalle_pasaje.html", {"base":"premium_base.html", "viaje":viaje, "tarjeta":tarjeta, "usuario":usuario, "chofer":chofer, "precio_total":precio_total, "insumos":carrito, "inumo":len(carrito), "pasaje":pasaje})
        else:
            return render (request, "ver_detalle_pasaje.html", {"base":"usuario_base.html", "viaje":viaje, "tarjeta":tarjeta, "usuario":usuario, "chofer":chofer, "precio_total":precio_total, "insumos":carrito, "inumo":len(carrito), "pasaje":pasaje})

class Testeo(HttpRequest):

    @login_required
    def ver_pasajeros(request, id_viaje):
        pasajeros = Pasaje.objects.filter(nro_viaje_id = id_viaje)
        viaje = Viaje.objects.get(id = id_viaje)
        pasajeros_ = []
        ok = False
        for p in pasajeros:
            if p.estado != 'cancelado':
                pasajeros_.append(p)
        hoy = datetime.today()
        if viaje.fecha_salida.date() == hoy.date():
            inicia = True
            ok = True
            for p in pasajeros_:
                if p.estado == 'activo':
                    ok = False
                    print('holaaa')
                    break
        else:
            inicia = False
        if request.user.tipo_usuario == 1:
            return render (request, "ver_pasajeros.html", {"pasajeros":pasajeros_, "cant_p": len(pasajeros_), "viaje":viaje, "base":"admin_base.html"})
        else:
            return render (request, "ver_pasajeros.html", {"pasajeros":pasajeros_, "cant_p": len(pasajeros_), "viaje":viaje, "base":"chofer_base.html", 'iniciar': ok, 'testear': inicia})

    @login_required
    def iniciar_viaje(request, id_viaje):
        pasajeros = Pasaje.objects.filter(nro_viaje_id = id_viaje)
        viaje = Viaje.objects.filter(id=id_viaje)
        if len(viaje) != 0:
            viaje = Viaje.objects.get(id=id_viaje)
        if viaje.estado == 'activo':
            viaje.estado = 'iniciado'
            viaje.save()
        else:
            viaje.estado = 'realizado'
            viaje.save()
        print('estado de viaje', viaje.estado)
        return render (request, "ver_pasajeros.html", {"pasajeros":pasajeros, "viaje":viaje, "base":"chofer_base.html"})

    @login_required
    def test(request, id_pasaje):
        test = Registro_test()
        pasaje= Pasaje.objects.get(id=id_pasaje)
        pasaje_nuevo = Registro_pasaje(instance=pasaje)
        viaje = Viaje.objects.get(id = pasaje.nro_viaje_id)
        temp = []
        temp.append("menos de 35.0°C")
        for i in range(35,41):
            for x in range(0,10):
                temp.append(str(i)+"."+str(x)+"°C")
        temp.append("más de 40.9°C")

        return render (request, "testeo.html", {"temp":temp, "pasaje":pasaje, "id_pasaje":pasaje.id, "viaje":viaje})

    @login_required
    def procesar_formulario_test(request, id_viaje, id_pasaje):
        test = Registro_test(request.POST)
        pasaje = Pasaje.objects.get(id = id_pasaje)
        pasaje_nuevo = Registro_pasaje(request.POST, instance = pasaje)
        if test.is_valid():
            test.save()
            if pasaje_nuevo.is_valid():
                test_correspondiente = Test.objects.last()
                temperatura = test_correspondiente.temperatura.split('.')
                if test_correspondiente.olfato or test_correspondiente.gusto or test_correspondiente.contacto or int(temperatura[0]) >= 38:
                    pasaje_nuevo.save_no_sube()
                else:
                    pasaje_nuevo.save_sube()
                pasajeros = Pasaje.objects.filter(nro_viaje_id = id_viaje)
                viaje = Viaje.objects.get(id = id_viaje)
                pasajeros_ = []
                ok = True
                for p in pasajeros:
                    if p.estado != 'cancelado':
                        pasajeros_.append(p)
                for p in pasajeros_:
                    if p.estado == 'activo':
                        ok = False
                        print('holaaa')
                        break
                return render (request, "ver_pasajeros.html", {"pasajeros":pasajeros_, 'cant_p': len(pasajeros_), "viaje":viaje, "base":"chofer_base.html", 'iniciar': ok})


    @login_required
    def editar_test(request, id_pasaje):
        test = Test.objects.get(pasaje = id_pasaje)
        test_nuevo = Registro_test(instance = test)
        pasaje= Pasaje.objects.get(id=id_pasaje)
        pasaje_nuevo = Registro_pasaje(instance=pasaje)
        viaje = Viaje.objects.get(id = pasaje.nro_viaje_id)
        temp = []
        temp.append("menos de 35.0°C")
        for i in range(35,41):
            for x in range(0,10):
                temp.append(str(i)+"."+str(x)+"°C")
        temp.append("más de 40.9°C")

        return render (request, "modificar_testeo.html", {"temp":temp, "pasaje":pasaje, "id_pasaje":pasaje.id, "viaje":viaje, "test":test})


    @login_required
    def actualizar_test(request, id_viaje, id_pasaje):
        test = Test.objects.get(pasaje = id_pasaje)
        test_nuevo = Registro_test(request.POST, instance = test)
        pasaje = Pasaje.objects.get(id = id_pasaje)
        pasaje_nuevo = Registro_pasaje(request.POST, instance = pasaje)
        if test_nuevo.is_valid():
            test_nuevo.save()
            if pasaje_nuevo.is_valid():
                temperatura = test.temperatura.split('.')
                if test.olfato or test.gusto or test.contacto or int(temperatura[0]) >= 38:
                    pasaje_nuevo.save_no_sube()
                else:
                    pasaje_nuevo.save_sube()
                pasajeros = Pasaje.objects.filter(nro_viaje_id = id_viaje)
                viaje = Viaje.objects.get(id = id_viaje)
                pasajeros_ = []
                ok = True
                for p in pasajeros:
                    if p.estado != 'cancelado':
                        pasajeros_.append(p)
                for p in pasajeros_:
                    if p.estado == 'activo':
                        ok = False
                        print('holaaa')
                        break
                return render (request, "ver_pasajeros.html", {"editado":"si", "pasajeros":pasajeros_, 'cant_p': len(pasajeros_), 'iniciar': ok, "viaje":viaje, "base":"chofer_base.html"})


    @login_required
    def ver_test(request, id_pasaje):
        test = Test.objects.get(pasaje= id_pasaje)
        pasaje= Pasaje.objects.get(id=id_pasaje)
        viaje = Viaje.objects.get(id = pasaje.nro_viaje_id)
        temp = []
        temp.append("menos de 35.0°C")
        for i in range(35,41):
            for x in range(0,10):
                temp.append(str(i)+"."+str(x)+"°C")
        temp.append("más de 40.9°C")
        if request.user.tipo_usuario == 1:
            return render (request, "ver_test.html", {"base":"admin_base.html","temp":temp, "pasaje":pasaje, "test":test, "viaje":viaje})
        else:
            return render (request, "ver_test.html", {"base":"chofer_base.html", "temp":temp, "pasaje":pasaje, "test":test, "viaje":viaje})

    @login_required
    def confirmar_ausente(request, id_pasaje):
        pasaje = Pasaje.objects.get(id = id_pasaje)
        pasaje_nuevo = Registro_pasaje(instance=pasaje)
        viaje = Viaje.objects.get(id = pasaje.nro_viaje_id)
        return render (request, "confirmar_ausente.html", {"pasaje":pasaje, "viaje":viaje, "id_pasaje":pasaje.id})

    @login_required
    def actualizar_pasaje_ausente(request, id_pasaje, id_viaje):
        pasaje = Pasaje.objects.get(id = id_pasaje)
        pasaje_nuevo = Registro_pasaje(request.POST,instance=pasaje)
        viaje = Viaje.objects.get(id = pasaje.nro_viaje_id)
        if pasaje_nuevo.is_valid():
            pasaje_nuevo.save()
            pasajeros = Pasaje.objects.filter(nro_viaje_id = id_viaje)
            return render (request, "ver_pasajeros.html", {"ausente":"si","pasajeros":pasajeros, "viaje":viaje, "base":"chofer_base.html"})


class Suscripcion(HttpRequest):

    @login_required
    def ver_info_suscripcion(request):
        info = Premium.objects.get(id=1)
        contexto = {'premium':info, "editado":"not"}
        return render (request, "ver_info_suscripcion.html", contexto)

    @login_required
    def editar_info_suscripcion(request, id_premium):
        descuentos=[]
        numero = 5
        for i in range(1,20):
            descuentos.append(numero)
            numero = numero + 5
        info = Premium.objects.get(id=id_premium)
        form = Registro_premium(instance=info)
        return render (request, "modificar_info_suscripcion.html", {"form":form, "premium":info, "descuentos":descuentos})

    @login_required
    def actualizar_info_suscripcion(request, id_premium):
        info = Premium.objects.get(id=id_premium)
        form = Registro_premium(request.POST, instance = info)
        if form.is_valid():
            form.save()
            return render (request, "ver_info_suscripcion.html", {"premium":info, "editado":"ok"})
        else:
            return render (request, "ver_info_suscripcion.html", {"premium":info, "editado":"error"})

    @login_required
    def solicitar_suscripcion(request):
        info = Premium.objects.get(id=1)
        return render (request, "solicitar_suscripcion.html", {"premium":info})

    @login_required
    def registrar_tarjeta(request):
        tarjeta = Registro_tarjeta()
        return render (request, "registrar_tarjeta_suscripcion.html", {"usuario":request.user.id, "devuelta":"not", "base":"usuario_base.html"})

    @login_required
    def procesar_formulario_tarjeta(request):
        tarjeta = Registro_tarjeta(request.POST)
        if tarjeta.is_valid():
            confirmacion=errores_tarjeta(tarjeta)
            if len(confirmacion) == 0:
                numero = tarjeta.cleaned_data.get('numero')
                hay_tarjeta = Tarjeta.objects.filter(id_user_id = request.user.id, numero = numero)
                if len(hay_tarjeta) == 0:
                    tarjeta.save()
                if request.user.is_premium:
                    ticket = Registro_premium_pago()
                    user = Usuario.objects.get(id = request.user.id)
                    al_dia = Premium_pago.objects.filter(id_user= request.user.id)
                    al_dia_fecha = str(al_dia[len(al_dia)-1]).replace('Premium_pago object (', '').replace(')','')
                    al_dia_fecha = Premium_pago.objects.get(id = int(al_dia_fecha))
                    tarjeta = Tarjeta.objects.get(numero = numero, id_user = request.user.id)
                    al_dia_fecha=str(al_dia_fecha.fecha).replace('00:00:00+00:00','').split('-')
                    if al_dia_fecha[1] == "07":
                        ok=True
                    else:
                        ok=False
                    debe = 7 - int(al_dia_fecha[1])
                    meses = []
                    for i in range(int(al_dia_fecha[1])+1,8):
                        if i == 1:
                            meses.append('Enero')
                        else:
                            if i == 2:
                                meses.append('Febrero')
                            else:
                                if i == 3:
                                    meses.append('Marzo')
                                else:
                                    if i == 4:
                                        meses.append('Abril')
                                    else:
                                        if i == 5:
                                            meses.append('Mayo')
                                        else:
                                            if i == 6:
                                                meses.append('Junio')
                                            else:
                                                if i == 7:
                                                    meses.append('Julio')
                                                else:
                                                    if i == 8:
                                                        meses.append('Agosto')
                                                    else:
                                                        if i == 9:
                                                            meses.append('Septiembre')
                                                        else:
                                                            if i == 10:
                                                                meses.append('Octubre')
                                                            else:
                                                                if i == 11:
                                                                    meses.append('Noviembre')
                                                                else:
                                                                    if i == 12:
                                                                        meses.append('Diciembre')
                    info = Premium.objects.get(id=1)
                    pagar = info.cuota * debe
                    return render (request, "pagar_deuda.html", {"premium":info, "meses":meses, "tarjeta":tarjeta, "user":user, "pagar":pagar, "id":request.user.id})
                else:
                    info = Premium.objects.get(id=1)
                    user = Usuario.objects.get(id=request.user.id)
                    registro = Registro_usuario_premium(instance=user)
                    tarjeta_guardada = Tarjeta.objects.get(id_user_id = request.user.id , numero = numero)
                    ticket = Registro_premium_pago()
                    print(request.user.id)
                    return render (request, "pagar_primer_cuota_suscripcion.html", {"premium":info,"user": user, "id":request.user.id, "dato": registro,"ticket":ticket, "tarjeta":tarjeta_guardada, "ok":"ok"})
            else:
                if request.user.is_premium:
                    return render (request, "pagar_deuda.html", {"ok":"not", "errores":confirmacion, "nueva":"si"})
                else:
                    return render (request, "pagar_primer_cuota_suscripcion.html", {"ok":"not", "errores": confirmacion})


    @login_required
    def actualizar_usuario(request):
        user = Usuario.objects.get(id=request.user.id)
        registro = Registro_usuario_premium(request.POST, instance=user)
        ticket = Registro_premium_pago(request.POST)
        if registro.is_valid():
            registro.save()
            if ticket.is_valid():
                ticket.save()
                return render (request, "bienvenida_suscripcion.html")

    @login_required
    def ver_suscripcion(request):
        info = Premium.objects.get(id=1)
        al_dia = Premium_pago.objects.filter(id_user= request.user.id)
        al_dia = str(al_dia[len(al_dia)-1]).replace('Premium_pago object (', '').replace(')','')
        al_dia = Premium_pago.objects.get(id = int(al_dia))
        al_dia_fecha=str(al_dia.fecha).replace('00:00:00+00:00','').split('-')
        if al_dia_fecha[1] == "07":
            ok=True
        else:
            ok=False
        debe = 7 - int(al_dia_fecha[1])
        tarjeta = Tarjeta.objects.get(id_user = request.user.id, numero =al_dia.nro_tarjeta)
        return render (request,"ver_suscripcion.html", {"premium":info, "ok":ok, "debe":debe, "tarjeta":tarjeta})

    @login_required
    def confirmar_desuscripcion(request):
        user = Usuario.objects.get(id=request.user.id)
        registro = Registro_usuario_premium(request.POST, instance=user)
        return render (request,"confirmar_desuscripcion.html", {"user":user, "registro":registro})

    @login_required
    def actualizar_usuario2(request):
        user = Usuario.objects.get(id=request.user.id)
        registro = Registro_usuario_premium(request.POST, instance=user)
        if registro.is_valid():
            registro.save()
            ticket_eliminar = Premium_pago.objects.filter(id_user = request.user.id)
            for i in range(0,len(ticket_eliminar)):
                ticket_i = str(ticket_eliminar[i]).replace('Premium_pago object (', '').replace(')','')
                ticket_e = Premium_pago.objects.get(id = int(ticket_i))
                ticket_e.delete()

            pasajes = Pasaje.objects.filter(id_user=request.user.id)
            viajes = []
            for p in pasajes:
                if p.estado == "activo":
                    viaje = Viaje.objects.get(id=p.nro_viaje_id)
                    current_time = datetime.now()
                    hora = str((current_time.hour - 3))+":"+str(current_time.minute)+":"+str(current_time.second)
                    if viaje.fecha_salida.date() > current_time.date():
                        viajes.append(viaje)
                    else:
                        if viaje.fecha_salida.date() == current_time.date():
                            if str(viaje.fecha_salida.time()) > hora:
                                viajes.append(viaje)
            return render (request, "homePasajeros.html", {"nombre":request.user.nombre, "viajes": len(viajes)})

    @login_required
    def registrar_tarjeta_devuelta(request):
        tarjeta = Registro_tarjeta()
        return render (request, "registrar_tarjeta_suscripcion.html", {"usuario":request.user.id, "devuelta":"ok", "base":"premium_base.html"})

    def ponerse_al_dia(request):
        ticket = Registro_premium_pago()
        user = Usuario.objects.get(id = request.user.id)
        al_dia = Premium_pago.objects.filter(id_user= request.user.id)
        al_dia_fecha = str(al_dia[len(al_dia)-1]).replace('Premium_pago object (', '').replace(')','')
        al_dia_fecha = Premium_pago.objects.get(id = int(al_dia_fecha))
        tarjeta = Tarjeta.objects.get(numero = int(al_dia_fecha.nro_tarjeta), id_user = request.user.id)
        confirmacion = errores_ven(tarjeta)
        if len(confirmacion) == 0:
                al_dia_fecha=str(al_dia_fecha.fecha).replace('00:00:00+00:00','').split('-')
                if al_dia_fecha[1] == "07":
                    ok=True
                else:
                    ok=False
                debe = 7 - int(al_dia_fecha[1])
                meses = []
                for i in range(int(al_dia_fecha[1])+1,8):
                    if i == 1:
                        meses.append('Enero')
                    else:
                        if i == 2:
                            meses.append('Febrero')
                        else:
                            if i == 3:
                                meses.append('Marzo')
                            else:
                                if i == 4:
                                    meses.append('Abril')
                                else:
                                    if i == 5:
                                        meses.append('Mayo')
                                    else:
                                        if i == 6:
                                            meses.append('Junio')
                                        else:
                                            if i == 7:
                                                meses.append('Julio')
                                            else:
                                                if i == 8:
                                                    meses.append('Agosto')
                                                else:
                                                    if i == 9:
                                                        meses.append('Septiembre')
                                                    else:
                                                        if i == 10:
                                                            meses.append('Octubre')
                                                        else:
                                                            if i == 11:
                                                                meses.append('Noviembre')
                                                            else:
                                                                if i == 12:
                                                                    meses.append('Diciembre')
                info = Premium.objects.get(id=1)
                pagar = info.cuota * debe
                return render (request, "pagar_deuda.html", {"premium":info,"meses":meses, "tarjeta":tarjeta, "user":user, "pagar":pagar, "id":request.user.id})
        return render (request, "pagar_deuda.html", {"ok":"not" ,"errores":confirmacion})

    @login_required
    def ver_suscripcion_sin_deudas(request):
        info = Premium.objects.get(id=1)
        ticket = Registro_premium_pago(request.POST)
        if ticket.is_valid():
            ticket.save()
            al_dia = Premium_pago.objects.filter(id_user= request.user.id)
            al_dia = str(al_dia[len(al_dia)-1]).replace('Premium_pago object (', '').replace(')','')
            al_dia = Premium_pago.objects.get(id = int(al_dia))
            al_dia_fecha=str(al_dia.fecha).replace('00:00:00+00:00','').split('-')
            if al_dia_fecha[1] == "07":
                ok=True
            else:
                ok=False
            debe = 7 - int(al_dia_fecha[1])
            tarjeta = Tarjeta.objects.get(id_user = request.user.id, numero =al_dia.nro_tarjeta)
            return render (request,"ver_suscripcion.html", {"premium":info,"ok":ok, "debe":debe, "tarjeta":tarjeta, "pago":"ok"})

class Estadisticas (HttpRequest):

    @login_required
    def registro_usuarios(request):
        return render (request, "estadisticas_registro.html")

    @login_required
    def registro_usuarios_ver(request):
        date = dateutil.parser.parse(request.GET.get('fecha'),dayfirst=True)
        date2 = dateutil.parser.parse(request.GET.get('fecha2'),dayfirst=True)+timedelta(days=+1)
        usuarios = Usuario.objects.filter(date_joined__gte=date,date_joined__lte=date2)
        usuarios_total = Usuario.objects.all()
        cant_usuarios = len(set(usuarios))
        cant_usuarios_total = len(set(usuarios_total))
        porcentaje=(cant_usuarios * 100/ cant_usuarios_total)

        print(usuarios_total)
        print(request.GET.get('fecha'))
        print(request.GET.get('fecha2'))
        return render (request, "estadisticas_registro_ver.html",{"usuarios":len(usuarios), "fecha":request.GET.get('fecha'), "fecha2":request.GET.get('fecha2'), "total":len(usuarios_total), "porcentaje":int(porcentaje)})

    @login_required
    def puntos_viaje(request):
        viajes = Viaje.objects.all()
        puntos = 0
        for v in viajes:
            puntos += v.puntaje
        promedio = puntos / len(viajes)
        return render (request, "estadisticas.html", {"promedio": promedio})

    @login_required
    def viajes(request):
        return render (request, "estadisticas_viajes.html")

    @login_required
    def viajes_ver(request):
        date = dateutil.parser.parse(request.GET.get('fecha'),dayfirst=True)
        date2 = dateutil.parser.parse(request.GET.get('fecha2'),dayfirst=True)+timedelta(days=+1)
        viajes = Viaje.objects.filter(fecha_salida__gte=date,fecha_salida__lte=date2)
        viajes_total = Viaje.objects.all()
        cant_viajes = len(set(viajes))
        cant_viajes_total = len(set(viajes_total))
        porcentaje=(cant_viajes * 100/ cant_viajes_total)
        print(request.GET.get('fecha'))
        print(request.GET.get('fecha2'))
        return render (request, "estadisticas_viaje_ver.html",{"viajes":cant_viajes, "fecha":request.GET.get('fecha'), "fecha2":request.GET.get('fecha2'), "total":cant_viajes_total, "porcentaje":int(porcentaje)})


    @login_required
    def pasajeros(request):
        return render (request, "estadisticas_pasajeros.html")

    @login_required
    def pasajeros_ver(request):
        date = dateutil.parser.parse(request.GET.get('fecha'),dayfirst=True)
        date2 = dateutil.parser.parse(request.GET.get('fecha2'),dayfirst=True)+timedelta(days=+1)
        viajes = Viaje.objects.filter(fecha_salida__gte=date,fecha_salida__lte=date2)
        pasajeros = []
        pasajeros_total = Pasaje.objects.all()
        for v in viajes:
            pasajeros_viaje = Pasaje.objects.filter(nro_viaje_id= v.id)
            for p in pasajeros_viaje:
                pasajeros.append(p)
        cant_pasajeros = len(set(pasajeros))
        print(pasajeros)
        cant_pasajeros_total = len(set(pasajeros_total))
        porcentaje=(cant_pasajeros * 100/ cant_pasajeros_total)
        print(request.GET.get('fecha'))
        print(request.GET.get('fecha2'))
        return render (request, "estadisticas_pasajeros_ver.html",{"pasajeros":cant_pasajeros, "fecha":request.GET.get('fecha'), "fecha2":request.GET.get('fecha2'), "total":cant_pasajeros_total, "porcentaje":int(porcentaje)})
