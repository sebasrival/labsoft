"""labsoft URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import home, logoutUser
from django.contrib.auth import views as auth_views
from clientes.views import agregar_cliente, lista_cliente, editar_cliente, delete_cliente
from productos.views import agregar_producto, lista_producto, editar_producto, delete_producto, search_products
from pedidos.views import agregar_pedido

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logoutUser, name="logout"),
    path('', home, name="index"),

    # clientes
    path('cliente/add/', agregar_cliente, name="add_cliente"),
    path('cliente/list/', lista_cliente, name="lista_cliente"),
    path('cliente/edit/<id>/', editar_cliente, name="editar_cliente"),
    path('cliente/delete/<id>/', delete_cliente, name="delete_cliente"),

    # Productos
    path('product/add/', agregar_producto, name="add_producto"),
    path('product/list/', lista_producto, name="lista_producto"),
    path('product/edit/<id>/', editar_producto, name="editar_producto"),
    path('product/delete/<id>/', delete_producto, name="delete_producto"),
    path('product/search/', search_products, name='search'),

    # pedidos
    path('pedido/add/', agregar_pedido, name='add_pedido')
]
