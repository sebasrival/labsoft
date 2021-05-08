from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Producto

# Clase para import y export
class ProductoResource (resources.ModelResource):
    class Meta:
        model = Producto

#Clase para el sitio de administracion
class ProductoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['codigo_producto', 'nombre']
    list_display = ('codigo_producto', 'nombre', 'descripcion', 'volumen', 'cantidad_neto', 'color', 'precio')
    resources_class = ProductoResource
    
# Register your models here.
admin.site.register(Producto, ProductoAdmin)
