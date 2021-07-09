from django.urls import path
from .views import *

app_name='reportes'

urlpatterns = [

    path('produccion/mantenimiento/pdf/', MantenimientoEquipoPdfView.as_view(), name='mantenimientos_pdf'),
    path('ventas/reporteventas/pdf/', ReporteVentaPdfView.as_view(), name='ventas_pdf'),




]
