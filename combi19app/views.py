from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse, HttpRequest
from combi19app.forms import Registro, Registro_vehiculo, Registro_ruta, Registro_ciudad
from combi19app.models import Usuario, Vehiculo, Ruta, Ciudad
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
# Create your views here.

def home (request):
    return render (request, "home.html")

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

    if ruta.cleaned_data.get('identificador') == None:
        lista+=[1]
    if ruta.cleaned_data.get('nombre') == None:
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

class FormularioRegistro (HttpRequest):
    @login_required
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

class FormularioRuta (HttpRequest):

    def crear_formulario(request):
        ruta = Registro_ruta()
        return render (request, "agregar_ruta.html", {"dato": ruta})

    def procesar_formulario(request):
        ruta = Registro_ruta(request.POST)
        if ruta.is_valid():
            ruta.save()
            ruta = Registro_ruta()
            return render (request, "agregar_ruta.html", {"dato": ruta, "mensaje": "ok"})
        else:
            confirmacion=errores_ruta(ruta)
            ruta = Registro_ruta()
            return render (request, "agregar_ruta.html", {"mensaje": "not_ok", "errores":confirmacion})

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
