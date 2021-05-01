from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse, HttpRequest
from combi19app.forms import Registro
from combi19app.models import Usuario
from django.views.decorators.csrf import csrf_exempt
import crypt
from django.views.generic.edit import UpdateView
# Create your views here.

def bienvenida(request):

    return render (request, "bienvenido.html")


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
            print('error')
            confirmacion=errores(registro)
            registro = Registro()
            return render(request, "registrarse.html", {"mensaje": "not_ok", "errores": confirmacion})
