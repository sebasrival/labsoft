from django.urls import path
from .views import *

app_name='reportes'

urlpatterns = [
    path('reporte/produccion/mantenimiento/pdf/', MantenimientoEquipoPdfView.as_view(), name='mantenimientos_pdf'),
    path('reporte/ventas/reporteventas/pdf/', ReporteVentaPdfView.as_view(), name='ventas_pdf'),
    path('reporte/compras/', ReporteCompraPdfView.as_view(), name='reporte_compras'),
    path('reporte/compras/materiasprimas/', ReporteMateriaPrima.as_view(), name="reporte_materias_primas")
]
