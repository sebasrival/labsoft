from django.contrib import admin
from .models import Producto

class ProductoAdmin(admin.ModelAdmin):
    search_fields = ['codigo_producto', 'nombre']
    list_display = ('codigo_producto', 'nombre', 'descripcion', 'volumen', 'cantidad_neto', 'color', 'precio')

# Register your models here.
admin.site.register(Producto, ProductoAdmin)