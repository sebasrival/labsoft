from django.urls import path
from .views import ProductoListView, ProductoCreateView, ProductoDeleteView, ProductoUpdateView

app_name='produccion'

urlpatterns = [
    # producto
    path('productos/list/', ProductoListView.as_view(), name='producto_list'),
    path('productos/add/', ProductoCreateView.as_view(), name='producto_add'),
    path('productos/edit/<int:pk>/', ProductoUpdateView.as_view(), name='producto_edit'),
    path('productos/del/<int:pk>/', ProductoDeleteView.as_view(), name='producto_del'),
]
