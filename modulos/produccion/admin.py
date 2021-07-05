from django.contrib import admin

# Register your models here.
from modulos.produccion.models import *

admin.site.register(Producto)
admin.site.register(StockProductos)
admin.site.register(Equipo)
admin.site.register(OrdenElaboracion)
admin.site.register(DetalleOrdenElaboracion)
admin.site.register(EquipoOrdenElaboracion)
admin.site.register(Formula)
admin.site.register(FormulaProducto)