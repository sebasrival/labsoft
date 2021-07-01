from django.urls import path
from .views import *

app_name='produccion'

urlpatterns = [
    # producto
    path('productos/list/', ProductoListView.as_view(), name='producto_list'),
    path('productos/add/', ProductoCreateView.as_view(), name='producto_add'),
    path('productos/edit/<int:pk>/', ProductoUpdateView.as_view(), name='producto_edit'),
    path('productos/del/<int:pk>/', ProductoDeleteView.as_view(), name='producto_del'),

    # equipo
    path('equipos/list/', EquipoListView.as_view(), name='equipo_list'),
    path('equipos/add/', EquipoCreateView.as_view(), name='equipo_add'),
    path('equipos/edit/<int:pk>/', EquipoUpdateView.as_view(), name='equipo_edit'),
    path('equipos/del/<int:pk>/', EquipoDeleteView.as_view(), name='equipo_del'),
    
    
    path('orden/list/', OrdenListView.as_view(), name='orden_list'),
    path('orden/add/', OrdenCreateView.as_view(), name='orden_add'),
    path('orden/edit/<int:pk>/', OrdenUpdateView.as_view(), name='orden_edit'),
    path('orden/del/<int:pk>/', OrdenDeleteView.as_view(), name='orden_del'),

    path('formula/add/', FormulaCreateView.as_view(), name='formula_add'),
    path('formula/edit/<int:pk>/', FormulaUpdateView.as_view(), name='formula_edit'),
    path('formula/list/', FormulaListView.as_view(), name='formula_list'),
    path('formula/del/<int:pk>/', FormulaDeleteView.as_view(), name='formula_del'),

]
