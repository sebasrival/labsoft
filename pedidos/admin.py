from django.contrib import admin
from .models import Pedido, PedidoDetalle


class PedidoDetalleInline(admin.TabularInline):
    model = PedidoDetalle
    extra = 1

class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        PedidoDetalleInline,
    ]
    search_fields = ['cliente__nombre__icontains']
    list_display = ('cliente', 'fecha_pedido', 'fecha_entrega', 'estado')

# Register your models here.
admin.site.register(Pedido, PedidoAdmin)