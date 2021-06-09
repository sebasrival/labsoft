from django.urls import path
from .views import *

app_name='ventas'

urlpatterns = [
    # Clientees
    path('clientes/list/', ClienteListView.as_view(), name='cliente_list'),
    path('clientes/add/', ClienteCreateView.as_view(), name='cliente_add'),
    path('clientes/edit/<int:pk>/', ClienteUpdateView.as_view(), name='cliente_edit'),
    path('clientes/del/<int:pk>/', ClienteDeleteView.as_view(), name='cliente_del'),

    path('facturas/add/', FacturaVentaCreateView.as_view(), name='factura_add'),
    path('facturas/list/', FacturaVentaListView.as_view(), name='factura_list'),
    path('facturas/edit/<int:pk>/', FacturaVentaUpdateView.as_view(), name='factura_edit'),
    path('facturas/del/<int:pk>/', FacturaVentaDeleteView.as_view(), name='factura_del'),
    path('facturas/invoice/pdf/<int:pk>/', FacturaPdfView.as_view(), name='factura_invoice_pdf'),



]