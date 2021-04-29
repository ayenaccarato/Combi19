from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse

# Create your views here.

def bienvenida(request):
    doc = get_template("bienvenido.html")
    documento = doc.render({})

    return HttpResponse(documento)

def registrarse(request):
    doc = get_template("registrarse.html")
    documento = doc.render({})

    return HttpResponse(documento)
