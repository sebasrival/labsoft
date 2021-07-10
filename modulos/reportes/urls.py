from django.urls import path
from .views import *

app_name='reportes'

urlpatterns = [

    path('produccion/mantenimiento/pdf/', MantenimientoEquipoPdfView.as_view(), name='mantenimientos_pdf'),
    path('reportes/ventas', PantallaReporteVenta, name="pantalla_reporte_ventas"),
    path('reportes/orden', PantallaReporteOrden, name="pantalla_reporte_ordenes"),

    path('ventas/reporteventas/pdf/<int:year>/', ReporteVentaPdfView.as_view(), name='ventas_pdf'),
    path('ventas/reporteventas/pdf/<int:year>/<int:mes>/', ReporteVentaMensualPdfView.as_view(), name='ventas_mes_pdf'),
    path('reportes/ventasMensual', PantallaReporteVentaMensual, name="mes_reporte_ventas"),
    path('reportes/productosMensual', PantallaReporteProductoMensual, name="mes_reporte_productos"),

    path('produccion/reporteproductos/pdf/<int:year>/<int:mes>/', ReporteProductosMensualPdfView.as_view(), name='productos_mes_pdf'),
    path('produccion/reporteorden/pdf/<start>/<end>/<estado>/', ReporteOrdenPdfView.as_view(), name='reporte_orden_pdf'),



]
