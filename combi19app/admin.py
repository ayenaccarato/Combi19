from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from combi19app.models import Usuario, Vehiculo, Ciudad, Ruta, Tarjeta, Pasajes

# Register your models here.

class VehiculoAdmin (admin.ModelAdmin):
    list_display=("patente", "marca", "modelo", "capacidad", "premium")
    search_fields=("patente",)

#UserAdmin
class UsuarioAdmin (admin.ModelAdmin):
    #model = Usuario
    list_display = ['email', 'admin']
    list_filter = ['admin']
    ordering = ['email']
    filter_horizontal = ()
    search_fields = ['email']
    fieldsets = ((None, {'fields': ('email', 'password')}), ('Personal Info', {'fields': ()}),
    ('Permissions', {'fields': ('admin','superuser')}))
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email', 'password')}))
    #list_display=("usuario","email","dni","tipo_usuario")
    #list_filter = ['admin', 'staff']

admin.site.register(Usuario)
admin.site.register(Vehiculo, VehiculoAdmin)
admin.site.register(Ciudad)
admin.site.register(Ruta)
admin.site.register(Tarjeta)
admin.site.register(Pasajes)
