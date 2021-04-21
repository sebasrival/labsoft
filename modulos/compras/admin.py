from django.contrib import admin

# Register your models here.
from modulos.compras.models import Proveedores, MateriaPrima, Pago, FacturaCompra, FacturaConDet, StockMateriaPrima

admin.site.register(Proveedores)
admin.site.register(Pago)
admin.site.register(MateriaPrima)
admin.site.register(FacturaCompra)
admin.site.register(FacturaConDet)
admin.site.register(StockMateriaPrima)