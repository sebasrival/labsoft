from django.urls import path
from .views import ProveedorListView

app_name='compras'

urlpatterns = [
    path('proveedores/list/', ProveedorListView.as_view(), name='proveedor_list')
]
