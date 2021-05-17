from django.urls import path
from .views import ClienteListView, ClienteCreateView, ClienteDeleteView, ClienteUpdateView

app_name='ventas'

urlpatterns = [
    # Clientees
    path('clientes/list/', ClienteListView.as_view(), name='cliente_list'),
    path('clientes/add/', ClienteCreateView.as_view(), name='cliente_add'),
    path('clientes/edit/<int:pk>/', ClienteUpdateView.as_view(), name='cliente_edit'),
    path('clientes/del/<int:pk>/', ClienteDeleteView.as_view(), name='cliente_del'),
]
