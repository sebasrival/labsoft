from django.contrib import admin
from .models import Cliente


class ClienteAdmin(admin.ModelAdmin):
    search_fields = ['ruc', 'cedula', 'nombre', 'razon_social']
    list_display = ('ruc', 'cedula', 'nombre', 'apellido', 'email',
                    'razon_social', 'telefono', 'descuento', 'bonificacion')
    list_display_links = ('ruc', 'cedula')


# Register your models here.
admin.site.register(Cliente, ClienteAdmin)
