from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Cliente

# Clases para import y export
class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente

# Clase para el sitio de administracion
class ClienteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['ruc', 'cedula', 'nombre', 'razon_social']
    list_display = ('ruc', 'cedula', 'nombre', 'apellido', 'email',
                    'razon_social', 'telefono', 'descuento', 'bonificacion')
    list_display_links = ('ruc', 'cedula')
    resource_class = ClienteResource


# Register your models here.
admin.site.register(Cliente, ClienteAdmin)
