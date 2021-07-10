from django.urls import path
from .views import *

app_name='reportes'

urlpatterns = [
    path('reporte/produccion/mantenimiento/pdf/', MantenimientoEquipoPdfView.as_view(), name='mantenimientos_pdf'),
    path('reporte/ventas/reporteventas/pdf/', ReporteVentaPdfView.as_view(), name='ventas_pdf'),
    path('reporte/compras/filtro/', reporte_compras_filtro, name='reporte_compras'),
]
