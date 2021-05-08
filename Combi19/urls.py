"""Combi19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, logout_then_login
#from Combi19.views import *
#from combi19app.views import bienvenida, cambiar_contra, FormularioRegistro
from combi19app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registrarse/', views.FormularioRegistro.crear_formulario),
    path('guardarRegistro/', views.FormularioRegistro.procesar_formulario),
    path('registrar_chofer/', views.FormularioRegistroChofer.crear_formulario),
    path('guardarRegistroChofer/', views.FormularioRegistroChofer.procesar_formulario),
    path('cambiar_contra/', views.cambiar_contra),
    path('agregar_vehiculo/', views.FormularioVehiculo.crear_formulario),
    path('guardar_vehiculo/', views.FormularioVehiculo.procesar_formulario),
    path('modificar_ruta/', views.FormularioRuta.editar_ruta),
    path('actualizar_ruta/<str:nombre>/', views.FormularioRuta.actualizar_ruta),
    path('listar_rutas/', views.ListarRuta.crear_listado),
    path('listar_rutas/ver_detalle_ruta/<str:nombre>/',views.ListarRuta.mostrar_detalle),
    path('listar_rutas/modificar_ruta/<str:nombre>/',views.FormularioRuta.editar_ruta),
    path('listar_rutas/actualizar_ruta/<str:nombre>/',views.FormularioRuta.actualizar_ruta, name="actualizar_ruta"),
    path('listar_rutas/eliminar_ruta/<str:nombre>/',views.ListarRuta.eliminar_ruta),
    path('listar_vehiculos/', views.ListarVehiculos.crear_listado, name='listarVehiculos'),
    path('listar_vehiculos/ver_detalle_vehiculo/<patente_vehiculo>/',views.ListarVehiculos.mostrar_detalle),
    path('listar_vehiculos/eliminar_vehiculo/<patente_vehiculo>/',views.EliminarVehiculo.eliminar_vehiculo),
    path('listar_vehiculos/editar_vehiculo/<patente_vehiculo>', views.FormularioVehiculo.editar, name = "editarVehiculo"),
    path('actualizar_vehiculo/<patente_vehiculo>', views.FormularioVehiculo.actualizar, name = "actualizarVehiculo"),
    path('agregar_ruta/', views.FormularioRuta.crear_formulario),
    path('guardar_ruta/', views.FormularioRuta.procesar_formulario),
    path('agregar_ciudad/', views.FormularioCiudad.crear_formulario),
    path('guardar_ciudad/', views.FormularioCiudad.procesar_formulario),
    path('listar_ciudades/', views.ListarCiudad.crear_listado),
    path('listar_ciudades/ver_detalle_ciudad/<int:codigo_postal>/',views.ListarCiudad.mostrar_detalle),
    path('listar_ciudades/eliminar_ciudad/<int:codigo_postal>/',views.EliminarCiudad.eliminar_ciudad),
    path('listar_ciudades/editar_ciudad/<int:codigo_postal>/', views.FormularioCiudad.editar, name = "editarCiudad"),
    path('listar_ciudades/editar_ciudad/<int:codigo_postal>/actualizarCiudad/', views.FormularioCiudad.actualizar, name = "actualizarCiudad"),
    path('listar_choferes/', views.ListarChofer.crear_listado),
    path('actualizar_chofer/<int:dni>/', views.FormularioRegistroChofer.actualizar_chofer),
    path('listar_choferes/ver_detalle_chofer/<int:dni>/',views.ListarChofer.mostrar_detalle),
    path('listar_choferes/modificar_chofer/<int:dni>/',views.FormularioRegistroChofer.editar_chofer),
    path('listar_choferes/actualizar_chofer/<int:dni>/',views.FormularioRegistroChofer.actualizar_chofer, name="actualizar_chofer"),
    path('listar_choferes/eliminar_chofer/<int:dni>/',views.ListarChofer.eliminar_chofer),
    path('agregar_viaje/', views.FormularioViaje.crear_formulario),
    path('guardar_viaje/', views.FormularioViaje.procesar_formulario),

    path('listar_viajes/', views.ListarViajes.crear_listado),
    path('listar_viajes/ver_detalle_viaje/<int:id_viaje>/',views.ListarViajes.mostrar_detalle),
    #path('listar_viajes/eliminar_viaje/<int:id_viaje>/',views.EliminarViaje.eliminar_viaje),
    #path('actualizar_viaje/<int:id_viaje>/', views.FormularioRegistroViaje.actualizar_viaje),
    #path('listar_viajes/modificar_viaje/<int:id_viaje>/',views.FormularioRegistroViaje.editar_viaje),
    #path('listar_viajes/actualizar_viaje/<int:id_viaje>/',views.FormularioRegistroViaje.actualizar_viaje),

    path('home/', views.home),
    path('accounts/', include ('django.contrib.auth.urls')),
    path('', views.home),

]
urlpatterns += staticfiles_urlpatterns()
