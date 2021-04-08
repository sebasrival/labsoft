from django.contrib import admin
from modulos.ventas.ventas.models import Factura, FacturaDetalle, VentasConf

# Register your models here.
admin.site.register(Factura)
admin.site.register(FacturaDetalle)
admin.site.register(VentasConf)
