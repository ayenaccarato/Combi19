from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse, HttpRequest
from combi19app.forms import Registro
from combi19app.models import Usuario
import crypt
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

    def procesar_formulario (request):
        registro = Registro(request.POST)
        if registro.is_valid():
            password=crypt.crypt(registro.cleaned_data.get('contraseña'), 'salt')
            d=registro.cleaned_data.get('dni')
            # cambios = {'contraseña': password}
            # obj = Registro.objects.get(dni=request.dni)
            # for key, value in cambios.items():
            #     setattr(obj, key, value)
            # obj.save()
            #registro.set_password(registro.cleaned_data['contraseña'])
            #p = Usuario.objects.get(dni=request.dni)
            #q = Registro(request.POST, instance= p)
            #p['contraseña'] = crypt.crypt(q.cleaned_data.get('contraseña'), 'salt')
            #registro.save()
            #r= Registro.objects.get(dni=registro.cleaned_data.get('contraseña')).update(contraseña=password)
            print('sin error')
            registro.save()
        #    us = Usuario.objects.get(dni= registro.cleaned_data.get('dni'))
        #    us.contraseña = password
        #    us.save()

            r=Registro.objects.filter(dni=d).update(contraseña=password)
            registro = Registro()
            return render(request, "registrarse.html", {"dato": registro, "mensaje": "ok"})
        else:
            print('error')
            confirmacion=errores(registro)
            registro = Registro()
            return render(request, "registrarse.html", {"mensaje": "not_ok", "errores": confirmacion})
