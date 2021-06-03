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
    path('registrar_admin/', views.FormularioRegistroAdmin.crear_formulario),
    path('guardarRegistroChofer/', views.FormularioRegistroChofer.procesar_formulario),
    path('guardarRegistroAdmin/', views.FormularioRegistroAdmin.procesar_formulario),
    path('ver_perfil_admin/', views.ver_perfil_admin),
    path('cambiar_contra/', views.cambiar_contra),
    path('agregar_vehiculo/', views.FormularioVehiculo.crear_formulario),
    path('guardar_vehiculo/', views.FormularioVehiculo.procesar_formulario),
    path('modificar_ruta/', views.FormularioRuta.editar_ruta),
    path('actualizar_ruta/<int:id_ruta>/', views.FormularioRuta.actualizar_ruta),
    path('listar_rutas/', views.ListarRuta.crear_listado),
    path('listar_rutas/ver_detalle_ruta/<int:id_ruta>/',views.ListarRuta.mostrar_detalle),
    path('listar_rutas/ver_detalle_viaje_ruta/<int:id_ruta>/',views.ListarRuta.mostrar_detalle_viaje_ruta),
    path('listar_rutas/modificar_ruta/<int:id_ruta>/',views.FormularioRuta.editar_ruta),
    path('listar_rutas/actualizar_ruta/<int:id_ruta>/',views.FormularioRuta.actualizar_ruta, name="actualizar_ruta"),
    path('listar_rutas/eliminar_ruta/<int:id_ruta>/',views.ListarRuta.eliminar_ruta),
    path('listar_vehiculos/', views.ListarVehiculos.crear_listado, name='listarVehiculos'),
    path('listar_vehiculos/ver_detalle_vehiculo/<int:id_vehiculo>/',views.ListarVehiculos.mostrar_detalle),
    path('listar_vehiculos/ver_detalle_viaje_vehiculo/<int:id_vehiculo>/',views.ListarVehiculos.mostrar_detalle_viaje_vehiculo),
    path('listar_vehiculos/eliminar_vehiculo/<int:id_vehiculo>/',views.EliminarVehiculo.eliminar_vehiculo),
    path('listar_vehiculos/editar_vehiculo/<int:id_vehiculo>', views.FormularioVehiculo.editar, name = "editarVehiculo"),
    path('actualizar_vehiculo/<int:id_vehiculo>', views.FormularioVehiculo.actualizar, name = "actualizarVehiculo"),
    path('agregar_ruta/', views.FormularioRuta.crear_formulario),
    path('guardar_ruta/', views.FormularioRuta.procesar_formulario),
    path('agregar_ciudad/', views.FormularioCiudad.crear_formulario),
    path('guardar_ciudad/', views.FormularioCiudad.procesar_formulario),
    path('listar_ciudades/', views.ListarCiudad.crear_listado),
    path('listar_ciudades/ver_detalle_ciudad/<int:id_ciudad>/',views.ListarCiudad.mostrar_detalle),
    path('listar_ciudades/ver_detalle_viaje_ciudad/<int:id_ciudad>/',views.ListarCiudad.mostrar_detalle_viaje_ciudad),
    path('listar_ciudades/eliminar_ciudad/<int:id_ciudad>/',views.EliminarCiudad.eliminar_ciudad),
    path('listar_ciudades/editar_ciudad/<int:id_ciudad>/', views.FormularioCiudad.editar, name = "editarCiudad"),
    path('listar_ciudades/editar_ciudad/<int:id_ciudad>/actualizarCiudad/', views.FormularioCiudad.actualizar, name = "actualizarCiudad"),
    path('listar_choferes/', views.ListarChofer.crear_listado),
    path('actualizar_chofer/<int:id_chofer>/', views.FormularioRegistroChofer.actualizar_chofer),
    path('listar_choferes/ver_detalle_chofer/<int:id_chofer>/',views.ListarChofer.mostrar_detalle),
    path('listar_choferes/ver_detalle_viaje_chofer/<int:id_chofer>/',views.ListarChofer.mostrar_detalle_viaje_chofer),
    path('listar_choferes/modificar_chofer/<int:id_chofer>/',views.FormularioRegistroChofer.editar_chofer),
    path('listar_choferes/actualizar_chofer/<int:id_chofer>/',views.FormularioRegistroChofer.actualizar_chofer, name="actualizar_chofer"),
    path('listar_choferes/eliminar_chofer/<int:id_chofer>/',views.ListarChofer.eliminar_chofer),
    path('agregar_viaje/', views.FormularioViaje.crear_formulario),
    path('guardar_viaje/', views.FormularioViaje.procesar_formulario),
    path('listar_viajes/', views.ListarViajes.crear_listado),
    path('listar_viajes/ver_detalle_viaje/<int:id_viaje>/',views.ListarViajes.mostrar_detalle),
    path('listar_viajes/eliminar_viaje/<int:id_viaje>/',views.FormularioViaje.eliminar_viaje),
    path('actualizar_viaje/<int:id_viaje>/', views.FormularioViaje.actualizar_viaje),
    path('listar_viajes/modificar_viaje/<int:id_viaje>/',views.FormularioViaje.editar_viaje),
    path('listar_viajes/actualizar_viaje/<int:id_viaje>/',views.FormularioViaje.actualizar_viaje, name="actualizar_viaje"),
    path('listar_admin/', views.ListarAdministradores.crear_listado),
    path('listar_admin/eliminar_admin/<int:id_admin>/',views.ListarAdministradores.eliminar_admin),
    path('listar_pasajeros/', views.ListarPasajeros.crear_listado),
    path('listar_insumos/', views.ListarInsumos.crear_listado),
    path('agregar_insumo/', views.FormularioInsumo.crear_formulario),
    path('guardar_insumo/', views.FormularioInsumo.procesar_formulario),
    path('ver_info_de_contacto/', views.FormularioInfoDeContacto.ver_info_contacto),
    path('menu_info_de_contacto/', views.FormularioInfoDeContacto.menu_editar_info_contacto),
    path('menu_info_de_contacto/modificar_texto/<int:id_texto>/',views.FormularioInfoDeContacto.editar_info_contacto),
    path('actualizar_info_de_contacto/<int:id_texto>', views.FormularioInfoDeContacto.actualizarInfoDeContacto, name = "actualizarInfoDeContacto"),
    path('cartelera/', views.FormularioComentario.crear_formulario),
    path('cartelera/c/', views.FormularioComentario.procesar_formulario),
    path('cartelera/c/<int:id_coment>/',views.FormularioComentario.eliminar_comentario),
    path('agregar_anuncio/', views.FormularioAnuncio.crear_formulario),
    path('guardar_anuncio/', views.FormularioAnuncio.procesar_formulario),
    path('cartelera/a/<int:id_anuncio>/',views.FormularioAnuncio.eliminar_anuncio),
    path('cartelera/editar_anuncio/<int:id_anuncio>/', views.FormularioAnuncio.editar, name = "editarAnuncio"),
    path('cartelera/editar_anuncio/<int:id_anuncio>/actualizarAnuncio/',views.FormularioAnuncio.actualizar, name="actualizar_anuncio"),
    path('home/', views.home),
    path('accounts/', include ('django.contrib.auth.urls')),
    path('', views.home),

]
urlpatterns += staticfiles_urlpatterns()
