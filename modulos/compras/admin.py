from django.contrib import admin

# Register your models here.
from modulos.compras.models import Proveedor, MateriaPrima, Pago, FacturaCompra, FacturaDet, StockMateriaPrima

admin.site.register(Proveedor)
admin.site.register(Pago)
admin.site.register(MateriaPrima)
admin.site.register(FacturaCompra)
admin.site.register(FacturaDet)
admin.site.register(StockMateriaPrima)