from django.contrib import admin
from ventas.models import Factura, FacturaDetalle, VentasConf

# Register your models here.
admin.site.register(Factura)
admin.site.register(FacturaDetalle)
admin.site.register(VentasConf)
