from django.contrib import admin
from .models import Pedido, PedidoDetalle

# Register your models here.
class PedidoDetalleInline(admin.TabularInline):
    model = PedidoDetalle
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        PedidoDetalleInline,
    ]

admin.site.register(Pedido, PedidoAdmin)