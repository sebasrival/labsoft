from django.urls import path
from .views import ProveedorListView, ProveedorCreateView

app_name='compras'

urlpatterns = [
    path('proveedores/list/', ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedores/add/', ProveedorCreateView.as_view(), name='proveedor_add')
]
