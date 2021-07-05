from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Cliente)
admin.site.register(Cobro)
admin.site.register(FacturaVenta)
admin.site.register(FacturaVentaDetalle)
admin.site.register(Cuota)
admin.site.register(Pedido)
admin.site.register(PedidoDetalle)