from django.shortcuts import render
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
        return render (request, "home.html")
    else:
        return render (request,"homePasajeros.html")

def login(request):

    return render (request, "registration/login.html")

def cambiar_contra(request):

    return render(request, "cambiar_contra.html")


#busca los campos incorrectos (repetidos) que llevan el valor None
def errores(registro):
    lista = []

    if registro.cleaned_data.get('usuario') == None:
        lista+=[1]
    if registro.cleaned_data.get('dni') == None:
        lista+=[2]
    if registro.cleaned_data.get('email') == None:
        lista+=[3]
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
    lista_de_nombre = []

    if ciudad.cleaned_data.get('codigo_postal') == None:
        lista+=[1]
    c = Ciudad.objects.all().__str__()
    base_de_datos=c.replace('<QuerySet [', '').replace('<Ciudad: ', '').replace('>', '').replace('>]>', '').replace(']','').split(',')

    for i in range(0,len(base_de_datos),4):
         lista_de_nombre.append(base_de_datos[i:i+4])

    for i in lista_de_nombre:
        if i[0].strip() == ciudad.cleaned_data.get('nombre'):
            lista+=[2]

    return set(lista)

def calcular_minutos():
    minutos=[]
    for i in range(0,60):
        minutos+=[i]
    return minutos

def calcular_dias():
    dias=[]
    for i in range(1,32):
        dias+=[i]
    return dias

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

class FormularioVehiculo (HttpRequest):

    def crear_formulario(request):
        vehiculo = Registro_vehiculo()
        return render (request, "agregar_vehiculo.html", {"dato": vehiculo})

    def procesar_formulario(request):
        vehiculo = Registro_vehiculo(request.POST)
        if vehiculo.is_valid():
            vehiculo.save()
            vehiculo = Registro_vehiculo()
            return render (request, "agregar_vehiculo.html", {"dato": vehiculo, "mensaje": "ok"})
        else:
            vehiculo = Registro_vehiculo()
            return render (request, "agregar_vehiculo.html", {"mensaje": "not_ok"})

    def editar(request, patente_vehiculo):
        vehiculo = Vehiculo.objects.get(patente=patente_vehiculo)
        form = Registro_vehiculo(instance=vehiculo)
        return render (request, "modificar_vehiculo.html", {"form":form, "vehiculo":vehiculo})

    def actualizar(request, patente_vehiculo):
        vehiculo = Vehiculo.objects.get(patente=patente_vehiculo)
        form = Registro_vehiculo(request.POST, instance = vehiculo)
        if form.is_valid():
        #    db.connections.close_all()
            form.save()
            return render (request, "modificar_vehiculo.html", {"form":form, "vehiculo":vehiculo, "mensaje": "ok"})
        else:
            return render (request, "modificar_vehiculo.html", {"form":form, "vehiculo":vehiculo})

class ListarVehiculos(HttpRequest):

    def crear_listado(request):
        vehiculos = Vehiculo.objects.all()
        contexto = {'vehiculos': vehiculos, 'cantidad':len(vehiculos)}
        return render (request, "listar_vehiculos.html", contexto)

    def mostrar_detalle(request, patente_vehiculo):
        detalle= Vehiculo.objects.get(pk=patente_vehiculo)
        return render (request, "listar_vehiculos.html", {"dato":detalle, "mensaje":"detalle"})

class EliminarVehiculo(HttpRequest):

    def eliminar_vehiculo(request, patente_vehiculo):
        vehiculo_eliminado = Vehiculo.objects.get(pk=patente_vehiculo)
        vehiculo_eliminado.delete()
        vehiculo = Vehiculo.objects.all()
        return render (request, "listar_vehiculos.html", {"vehiculos": vehiculo, "mensaje":"eliminado", "cantidad": len(vehiculo)})

class FormularioRuta (HttpRequest):

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

    def editar_ruta(request, nombre):
        ruta = Ruta.objects.get(nombre=nombre)
        registro = Registro_ruta(instance=ruta)
        ciudad = Ciudad.objects.all()
        return render(request, "modificar_ruta.html", {"dato": registro, "rutas": ruta, "ciudades": ciudad})

    def actualizar_ruta(request, nombre):
        ruta = Ruta.objects.get(nombre=nombre)
        registro = Registro_ruta(request.POST, instance=ruta)
        if registro.is_valid():
            registro.save()
        rutas = Ruta.objects.all()
        return render (request, "listar_rutas.html", {"rutas": rutas, "mensaje": "editado"})

class FormularioCiudad (HttpRequest):

    def crear_formulario(request):
        ciudad = Registro_ciudad()
        return render (request, "agregar_ciudad.html", {"dato": ciudad})

    def procesar_formulario(request):
        ciudad = Registro_ciudad(request.POST)
        if ciudad.is_valid():
         confirmacion=errores_ciudad(ciudad)
         if len(confirmacion) == 0:
             ciudad.save()
             ciudad = Registro_ciudad()
             return render (request, "agregar_ciudad.html", {"dato": ciudad, "mensaje": "ok"})
        confirmacion=errores_ciudad(ciudad)
        ciudad = Registro_ciudad()
        return render (request, "agregar_ciudad.html", {"mensaje": "not_ok", "errores":confirmacion})

class ListarCiudad (HttpRequest):

    def crear_listado(request):
        ciudad = Ciudad.objects.all()
        print(ciudad)
        contexto = {'ciudades': ciudad, 'cantidad':len(ciudad)}
        return render (request, "listar_ciudades.html", contexto)

    def mostrar_detalle(request, codigo_postal):
        detalle= Ciudad.objects.get(pk=codigo_postal)
        return render (request, "listar_ciudades.html", {"dato":detalle, "mensaje":"detalle"})

class EliminarCiudad (HttpRequest):

    def eliminar_ciudad(request, codigo_postal):
        ciudad_eliminada = Ciudad.objects.get(pk=codigo_postal)
        ciudad_eliminada.delete()
        ciudad = Ciudad.objects.all()
        return render (request, "listar_ciudades.html", {"ciudades": ciudad, "mensaje":"eliminado", "cantidad": len(ciudad)})

class ListarRuta (HttpRequest):

    def crear_listado(request):
        ruta = Ruta.objects.all()
        print(ruta)
        contexto = {'rutas': ruta, 'cantidad':len(ruta)}
        return render (request, "listar_rutas.html", contexto)

    def mostrar_detalle(request, nombre):
        detalle= Ruta.objects.get(pk=nombre)
        return render (request, "listar_rutas.html", {"dato":detalle, "mensaje":"detalle"})

    def eliminar_ruta(request, nombre):
        ruta_eliminada = Ruta.objects.get(pk=nombre)
        ruta_eliminada.delete()
        ruta = Ruta.objects.all()
        return render (request, "listar_rutas.html", {"rutas": ruta, "mensaje":"eliminado", "cantidad": len(ruta)})


class FormularioViaje (HttpRequest):

    def crear_formulario(request):
        viaje = Registro_viaje()
        minutos = calcular_minutos()
        dias = calcular_dias()
        choferes = Usuario.objects.all
        vehiculos = Vehiculo.objects.all
        ciudades = Ciudad.objects.all
        rutas = Ruta.objects.all
        return render (request, "agregar_viaje.html", {"dato": viaje,"dias":dias, "minutos":minutos, "choferes":choferes, "vehiculos": vehiculos, "ciudades":ciudades, "rutas":rutas})

    def procesar_formulario(request):
        viaje = Registro_viaje(request.POST)
        minutos = calcular_minutos()
        dias = calcular_dias()
        choferes = Usuario.objects.all
        vehiculos = Vehiculo.objects.all
        ciudades = Ciudad.objects.all
        rutas = Ruta.objects.all
        if viaje.is_valid():
            #confirmacion=errores_ciudad(ciudad)
            #if len(confirmacion) == 0:
            viaje.save()
            viaje = Registro_viaje()
            return render (request, "agregar_viaje.html", {"dato": viaje, "dias":dias, "minutos":minutos, "choferes":choferes, "vehiculos": vehiculos, "ciudades":ciudades, "rutas":rutas})
        else:
            #confirmacion=errores_ciudad(ciudad)
            viaje = Registro_viaje()
            return render (request, "agregar_viaje.html", {"mensaje": "not_ok", "minutos":minutos, "choferes":choferes, "vehiculos": vehiculos, "ciudades":ciudades, "rutas":rutas})
