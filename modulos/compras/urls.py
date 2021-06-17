from django.urls import path
from .views import ProveedorListView, ProveedorCreateView, ProveedorDeleteView, ProveedorUpdateView, \
    FacturaCompraCreateView, SearchProveedor, SearchMateriaPrima, FacturaCompraListView, FacturaCompraDeleteView, \
    FacturaCompraUpdateView, StockMateriaPrimaListView, StockMateriaPrimaCreateView, StockMateriaUpdateView, \
    StockMateriaPrimaDeleteView

app_name = 'compras'

urlpatterns = [
    # proveedores
    path('proveedores/list/', ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedores/add/', ProveedorCreateView.as_view(), name='proveedor_add'),
    path('proveedores/edit/<int:pk>/', ProveedorUpdateView.as_view(), name='proveedor_edit'),
    path('proveedores/del/<int:pk>/', ProveedorDeleteView.as_view(), name='proveedor_del'),

    path('proveedores/search/', SearchProveedor.as_view(), name='search_proveedor'),

    # materia prima
    path('materiaprima/search/', SearchMateriaPrima.as_view(), name='search_materia'),

    # factura
    path('factura/add/', FacturaCompraCreateView.as_view(), name='factura_add'),
    path('factura/list/', FacturaCompraListView.as_view(), name='factura_list'),
    path('factura/del/<int:pk>/', FacturaCompraDeleteView.as_view(), name='factura_del'),
    path('factura/update/<int:pk>/', FacturaCompraUpdateView.as_view(), name='factura_edit'),

    # stock materia prima
    path('stock/materia/list/', StockMateriaPrimaListView.as_view(), name='stock_list'),
    path('stock/materia/add/', StockMateriaPrimaCreateView.as_view(), name='stock_add'),
    path('stock/materia/edit/<int:pk>/', StockMateriaUpdateView.as_view(), name='stock_edit'),
    path('stock/materia/del/<int:pk>/', StockMateriaPrimaDeleteView.as_view(), name='stock_del'),
]
