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
from productos.views import agregar_producto, lista_producto
from pedidos.views import agregar_pedido

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logoutUser, name="logout"),
    path('', home, name="index"),
    # clientes
    path('agregar_cliente/', agregar_cliente, name="add_cliente"),
    path('lista_cliente/', lista_cliente, name="lista_cliente"),
    path('editar_cliente/<id>/', editar_cliente, name="editar_cliente"),
    path('eliminar_cliente/<id>/', delete_cliente, name="delete_cliente"),
    # Productos
    path('agregar_producto/', agregar_producto, name="add_producto"),
    path('lista_producto/', lista_producto, name="lista_producto"),
    # pedidos
    path('agregar_pedido/', agregar_pedido, name='add_pedido')
]
