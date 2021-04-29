from django.contrib import admin
from combi19app.models import Usuario, Vehiculo, Ciudad, Ruta, Tarjeta, Pasajes

# Register your models here.

class VehiculoAdmin (admin.ModelAdmin):
    list_display=("patente", "marca", "modelo", "capacidad", "premium")
    search_fields=("patente",)

admin.site.register(Usuario)
admin.site.register(Vehiculo, VehiculoAdmin)
admin.site.register(Ciudad)
admin.site.register(Ruta)
admin.site.register(Tarjeta)
admin.site.register(Pasajes)
