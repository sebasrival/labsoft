from django.urls import path
from .views import ProveedorListView, ProveedorCreateView, ProveedorDeleteView, ProveedorUpdateView, \
    FacturaCompraCreateView

app_name='compras'

urlpatterns = [
    # proveedores
    path('proveedores/list/', ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedores/add/', ProveedorCreateView.as_view(), name='proveedor_add'),
    path('proveedores/edit/<int:pk>/', ProveedorUpdateView.as_view(), name='proveedor_edit'),
    path('proveedores/del/<int:pk>/', ProveedorDeleteView.as_view(), name='proveedor_del'),

    #factura
    path('compras/factura/add', FacturaCompraCreateView.as_view(), name='factura_add')
]
