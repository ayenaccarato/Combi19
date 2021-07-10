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
    path('ver_perfil_admin/modificar_admin/', views.editar_admin),
    path('actualizar_admin/<int:id_admin>/', views.actualizar_admin),
    path('ver_perfil_admin/actualizar_admin/<int:id_admin>/', views.actualizar_admin, name="actualizar_admin"),
    path('ver_perfil_chofer/', views.ver_perfil_chofer),
    path('ver_perfil_chofer/modificar_chofer2/', views.editar_chofer2),
    path('actualizar_chofer2/<int:id_chofer>/', views.actualizar_chofer2),
    path('ver_perfil_chofer/actualizar_chofer2/<int:id_chofer>/', views.actualizar_chofer2, name="actualizar_chofer2"),
    path('ver_perfil_usuario/', views.ver_perfil_usuario),
    path('ver_perfil_usuario/modificar_usuario/', views.editar_usuario),
    path('actualizar_usuario/<int:id_usuario>/', views.actualizar_usuario),
    path('ver_perfil_usuario/actualizar_usuario/<int:id_usuario>/', views.actualizar_usuario, name="actualizar_usuario"),

    path('verificar_dni/', views.cambiar_contra),
    path('cambiar_contra/', views.procesar_contra),
    path('actualizar_contra/', views.actualizar_contra),

    path('cambiar_contra_admin/', views.cambiar_contra_admin),
    path('actualizar_contra_admin/', views.actualizar_contra_admin),
    path('actualizar_contra_admin/<int:id_admin>/', views.actualizar_contra_admin),
    path('cambiar_contra_usuario/', views.cambiar_contra_usuario),
    path('actualizar_contra_usuario/', views.actualizar_contra_usuario),
    path('actualizar_contra_usuario/<int:id_usuario>/', views.actualizar_contra_usuario),
    path('cambiar_contra_chofer/', views.cambiar_contra_chofer),
    path('actualizar_contra_chofer/', views.actualizar_contra_chofer),
    path('actualizar_contra_chofer/<int:id_chofer>/', views.actualizar_contra_chofer),
    #path('ver_perfil_admin/actualizar_contra/<int:id_admin>/', views.actualizar_contra_admin, name="actualizar_contraAdmin"),
    path('agregar_vehiculo/', views.FormularioVehiculo.crear_formulario),
    path('guardar_vehiculo/', views.FormularioVehiculo.procesar_formulario),
    path('modificar_ruta/', views.FormularioRuta.editar_ruta),
    path('listar_rutas/', views.ListarRuta.crear_listado),
    path('listar_rutas/ver_detalle_ruta/<int:id_ruta>/',views.ListarRuta.mostrar_detalle),
    path('listar_rutas/ver_detalle_viaje_ruta/<int:id_ruta>/',views.ListarRuta.mostrar_detalle_viaje_ruta),
    path('listar_rutas/modificar_ruta/<int:id_ruta>/',views.FormularioRuta.editar_ruta),
    path('actualizar_ruta/<int:id_ruta>/', views.FormularioRuta.actualizar_ruta),
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
    path('actualizar_ciudad/<int:id_ciudad>', views.FormularioCiudad.actualizar),
    path('listar_ciudades/actualizar_ciudad/<int:id_ciudad>/', views.FormularioCiudad.actualizar, name = "actualizarCiudad"),
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
    path('eliminar_admin/<int:id_admin>/confirmar_eliminado_admin/', views.ListarAdministradores.confirmar_eliminado_admin),
    path('listar_pasajeros/', views.ListarPasajeros.crear_listado),
    path('listar_insumos/', views.ListarInsumos.crear_listado),
    path('actualizar_insumo/<int:id_insumo>/', views.FormularioInsumo.actualizar_insumo),
    path('listar_insumos/ver_detalle_insumo/<int:id_insumo>/',views.ListarInsumos.mostrar_detalle),
    path('listar_insumos/modificar_insumo/<int:id_insumo>/', views.FormularioInsumo.editar_insumo),
    path('listar_insumos/actualizar_insumo/<int:id_insumo>/',views.FormularioInsumo.actualizar_insumo, name="actualizar_insumo"),
    path('listar_insumos/eliminar_insumo/<int:id_insumo>/',views.ListarInsumos.eliminar_insumo),
    path('agregar_insumo/', views.FormularioInsumo.crear_formulario),
    path('guardar_insumo/', views.FormularioInsumo.procesar_formulario),
    path('ver_info_de_contacto/', views.FormularioInfoDeContacto.ver_info_contacto),
    path('menu_info_de_contacto/', views.FormularioInfoDeContacto.menu_editar_info_contacto),
    path('menu_info_de_contacto/modificar_texto/<int:id_texto>/',views.FormularioInfoDeContacto.editar_info_contacto),
    path('actualizar_info_de_contacto/<int:id_texto>', views.FormularioInfoDeContacto.actualizarInfoDeContacto, name = "actualizarInfoDeContacto"),
    path('cartelera/', views.FormularioComentario.mostrar_viajes),
    path('guardar_comentario/<int:id_viaje>/<int:tipo>/<int:id_user>/', views.FormularioComentario.guardar_comentario),
    path('eliminar_comentario/<int:id_viaje>/<int:tipo>/<int:id_coment>/<int:id_user>/',views.FormularioComentario.eliminar_comentario),
    path('ver_comentario/<int:id_viaje>/<int:tipo>/<int:id_user>/',views.FormularioComentario.ver_comentarios),
    path('agregar_anuncio/', views.FormularioAnuncio.crear_formulario),
    path('guardar_anuncio/', views.FormularioAnuncio.procesar_formulario),
    path('cartelera/a/<int:id_anuncio>/',views.FormularioAnuncio.eliminar_anuncio),
    path('cartelera/editar_anuncio/<int:id_anuncio>/', views.FormularioAnuncio.editar, name = "editarAnuncio"),
    path('cartelera/editar_anuncio/<int:id_anuncio>/actualizarAnuncio/',views.FormularioAnuncio.actualizar, name="actualizar_anuncio"),
    path('buscar_viaje_origen', views.BuscarCiudad.listar_ciudades),
    path('buscar_viaje', views.BuscarCiudad.listar_ciudades_result),
    path('cancelar_compra/', views.ComprarPasaje.cancelar),
    path('estadisticas_registro_usuario/', views.Estadisticas.registro_usuarios),
    path('estadisticas_registro_usuario/buscar/', views.Estadisticas.registro_usuarios_ver),
    path('estadisticas_registro_premium/', views.Estadisticas.registro_usuarios_premium),
    path('estadisticas_registro_premium/buscar/', views.Estadisticas.registro_premium_ver),
    path('estadisticas_pasajes_covid/', views.Estadisticas.pasajes_covid),
    path('estadisticas_pasajes_covid/buscar/', views.Estadisticas.pasajes_covid_ver),
    path('viaje_buscar/', views.Estadisticas.viajes_ver),
    path('estadisticas_viajes', views.Estadisticas.viajes),
    path('estadisticas_pasajeros', views.Estadisticas.pasajeros),
    path('pasajero_buscar/', views.Estadisticas.pasajeros_ver),
    path('comprar_pasaje_cantidad/<int:id_viaje>/', views.ComprarPasaje.comprar_pasaje_cantidad),
    path('comprar_pasaje_cantidad/<int:id_viaje>/comprar_pasaje_completar_datos', views.ComprarPasaje.comprar_pasaje_completar_datos),
    path('comprar_pasaje_completar_datos/<int:id_viaje>/', views.ComprarPasaje.comprar_pasaje_completar_datos),
    path('comprar_pasaje_menu/<int:id_viaje>/', views.ComprarPasaje.comprar_pasaje_menu),
    path('comprar_pasaje/carrito/<int:id_viaje>/', views.ComprarPasaje.mi_carrito),
    path('comprar_pasaje/carrito/<int:id_viaje>/<int:id_ticket>/', views.ComprarPasaje.eliminar_mi_carrito),
    path('comprar_pasaje/tarjeta/<int:id_viaje>/', views.ComprarPasaje.tarjeta),
    path('verificar/<int:id_viaje>/', views.ComprarPasaje.procesar_tarjeta),
    path('otra_tarjeta/<int:id_viaje>/', views.ComprarPasaje.otra_tarjeta),
    path('pagar/<int:id_viaje>/', views.ComprarPasaje.procesar_pasaje),
    path('comprar_pasaje_con/<int:id_viaje>/<int:id_tarjeta>/', views.ComprarPasaje.setear_tarjeta),
    path('comprar_pasaje/tienda/<int:id_viaje>/', views.ComprarPasaje.ver_tienda),
    path('comprar_pasaje/tienda/<int:id_viaje>/agregar/<int:id_insumo>/', views.ComprarPasaje.procesar_ver_tienda),
    path('comprar_pasaje/tienda/<int:id_viaje>/<int:id_insumo>/ok/', views.ComprarPasaje.procesar_confirmacion_insumo),
    path('comprar_pasaje/carrito/<int:id_viaje>/<int:id_ticket>/confirmar_eliminado/', views.ComprarPasaje.confirmar_eliminado),
    path('ver_viajes_por_realizar/', views.ListarViajes.listar_viajes_por_realizar),
    path('ver_viajes_realizados/', views.ListarViajes.listar_viajes_realizados_usuario),
    path('ver_pasaje/detalle/<int:id_viaje>/<int:id_pasaje>/cancelar', views.ComprarPasaje.cancelar_pasaje),
    path('ver_pasaje/detalle/cancelar/confirmar/<int:id_viaje>/<int:id_pasaje>/', views.ComprarPasaje.confirmar_cancelar_pasaje),
    path('ver_pasaje/detalle/<int:id_viaje>/', views.ComprarPasaje.ver_detalle_pasaje),
    path('ver_pasaje/detalle/<int:id_viaje>/realizados/', views.ComprarPasaje.ver_detalle_pasaje_realizados),
    path('reembolsos/', views.reembolso),
    path('listar_proximos_viajes/', views.ListarViajes.listar_proximos_viajes),
    path('listar_proximos_viajes/ver_detalle_viaje_chofer/<int:id_viaje>/', views.ListarViajes.mostrar_detalle_chofer),
    path('listar_viajes_realizados/ver_detalle_viaje_chofer/<int:id_viaje>/', views.ListarViajes.mostrar_detalle_chofer_realizados),
    path('listar_viajes_iniciados/ver_detalle_viaje_chofer/<int:id_viaje>/', views.ListarViajes.mostrar_detalle_chofer_iniciados),
    path('listar_proximos_viajes/cancelar_viaje_chofer/<int:id_viaje>/', views.ListarViajes.cancelar_viaje_chofer),
    path('listar_proximos_viajes/cancelar_viaje_chofer/<int:id_viaje>/confirmar_cancelado_viaje', views.ListarViajes.confirmar_cancelado_viaje),
    path('testeo/<int:id_pasaje>/', views.Testeo.test),
    path('solicitar_suscripcion/', views.Suscripcion.solicitar_suscripcion),
    path('registrar_tarjeta_suscripcion/', views.Suscripcion.registrar_tarjeta),
    path('confirmar_pago_suscripcion/',views.Suscripcion.procesar_formulario_tarjeta),
    path('bienvenida_suscripcion/', views.Suscripcion.actualizar_usuario),
    path('ver_suscripcion/', views.Suscripcion.ver_suscripcion),
    path('confirmar_desuscripcion/', views.Suscripcion.confirmar_desuscripcion),
    path('home/des/', views.Suscripcion.actualizar_usuario2),
    path('pagar_deuda/', views.Suscripcion.ponerse_al_dia),
    path('registrar_tarjeta_suscripcion/rep/', views.Suscripcion.registrar_tarjeta_devuelta),
    path('ver_suscripcion/deu/', views.Suscripcion.ver_suscripcion_sin_deudas),
    path('ver_info_suscripcion/', views.Suscripcion.ver_info_suscripcion),
    path('modificar_suscripcion/<int:id_premium>/', views.Suscripcion.editar_info_suscripcion),
    path('actualizar_info_suscripcion/<int:id_premium>/', views.Suscripcion.actualizar_info_suscripcion),
    path('ver_pasajeros/<int:id_viaje>/', views.Testeo.ver_pasajeros),
    path('ver_pasajeros/guardar_test/<int:id_viaje>/<int:id_pasaje>/', views.Testeo.procesar_formulario_test),
    path('eliminar_pasajero/<int:id_usuario>/<int:id_viaje>/', views.ListarPasajeros.eliminar_pasajero),
    path('listar_pasajeros/eliminar/<int:id_usuario>/<int:id_viaje>/confirmar_eliminado_pasajero/', views.ListarPasajeros.confirmar_eliminado_pasajero),

    path('editar_test/<int:id_pasaje>/', views.Testeo.editar_test),
    path('ver_pasajeros/guardar_test/<int:id_viaje>/<int:id_pasaje>/editado/', views.Testeo.actualizar_test),
    path('ver_test/<int:id_pasaje>/', views.Testeo.ver_test),
    path('confirmar_ausente/<int:id_pasaje>/', views.Testeo.confirmar_ausente),
    path('ver_pasajeros/<int:id_pasaje>/<int:id_viaje>/ausente', views.Testeo.actualizar_pasaje_ausente),
    path('estadisticas/', views.Estadisticas.puntos_viaje),
    path('listar_viajes_iniciados/', views.ListarViajes.listar_viajes_iniciados),
    path('listar_viajes_realizados/', views.ListarViajes.listar_viajes_realizados),
    path('puntuar/<int:id_viaje>/', views.FormularioComentario.puntuar),
    path('guardar_puntos/<int:id_viaje>/', views.FormularioComentario.guardar_puntos),
    path('ver_pasajeros/iniciar_viaje/<int:id_viaje>/', views.Testeo.iniciar_viaje),

    path('nueva_tarjeta_suscripcion/', views.Suscripcion.cambiar_de_tarjeta),
    path('procesar_otra_tarjeta_suscripcion/', views.Suscripcion.procesar_formulario_tarjeta_nueva),

    path('home/', views.home),
    path('accounts/', include ('django.contrib.auth.urls')),
    path('', views.home),

]
urlpatterns += staticfiles_urlpatterns()
