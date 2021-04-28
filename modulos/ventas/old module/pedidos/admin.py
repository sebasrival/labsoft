from django.contrib import admin
from .models import Pedido, PedidoDetalle
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Clases para import y export
class PedidoResource(resources.ModelResource):
    class Meta:
        model = Pedido

class PedidoDetalleResource(resources.ModelResource):
    class Meta:
        model = PedidoDetalle

# Clases para el sitio de administracion
class PedidoDetalleInline(admin.TabularInline):
    model = PedidoDetalle
    extra = 1

class PedidoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    inlines = [
        PedidoDetalleInline,
    ]
    search_fields = ['cliente__nombre__icontains']
    list_display = ('cliente', 'fecha_pedido', 'fecha_entrega', 'estado')
    resources_class = PedidoResource

class PedidoDetalleAdmin (ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['__all__']
    list_display = ('pedido', 'producto', 'cantidad')
    ordering = ['pedido']
    resources_class = PedidoDetalleInline

# Register your models here.
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(PedidoDetalle, PedidoDetalleAdmin)