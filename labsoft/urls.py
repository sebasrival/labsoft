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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from accounts.views import lista_usuarios, agregar_usuario, editar_usuario, delete_user
from orden.views import agregar_orden, lista_orden, editar_orden, delete_orden
from ventas.views import agregar_factura, list_factura, delete_factura, editar_factura
from django.conf import settings
from .views import home, logoutUser
from django.contrib.auth import views as auth_views
from clientes.views import agregar_cliente, lista_cliente, editar_cliente, delete_cliente
from productos.views import agregar_producto, lista_producto, editar_producto, delete_producto, search_products
from pedidos.views import agregar_pedido, list_pedido, delete_pedido, editar_pedido
from pedidos.views import agregar_pedido
from proveedores.views import agregar_proveedor,lista_proveedor,editar_proveedor,delete_proveedor
from pagos.views import registrar_pago,lista_pagos,editar_pago,delete_pago
from equipos.views import agregar_equipo,lista_equipos,editar_equipo,delete_equipo


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
    path('pedido/add/', agregar_pedido, name='add_pedido'),
    path('pedido/list/', list_pedido, name='list_pedido'),
    path('pedido/edit/<id>', editar_pedido, name='editar_pedido'),
    path('pedido/delete/<id>', delete_pedido, name='delete_pedido'),

    #ventas
    path('factura/add/', agregar_factura, name='add_factura'),
    path('factura/list', list_factura, name='list_factura'),
    path('factura/delete/<id>', delete_factura, name='delete_factura'),
    path('factura/edit/<id>', editar_factura, name="editar_factura"),

    #usuarios
    path('user/list/', lista_usuarios, name='list_user'),
    path('user/add/', agregar_usuario, name='add_user'),
    path('user/edit/<id>', editar_usuario, name='edit_user'),
    path('user/delete/<id>', delete_user, name="delete_user"),

    #proveedores
    path ('proveedor/add/', agregar_proveedor, name='add_proveedor'),
    path ('proveedor/list/',lista_proveedor,name='lista_proveedor'),
    path ('proveedor/edit/<id>/',editar_proveedor,name='editar_proveedor'),
     path('proovedor/delete/<id>/', delete_proveedor, name="delete_proveedor"),

    #pagos
    path ('pago/add/', registrar_pago, name='add_pago'),
    path ('pago/list/',lista_pagos,name='lista_pagos'),
    path ('pago/edit/<id>/',editar_pago,name='editar_pago'),
    path('pago/delete/<id>/', delete_pago, name="delete_pago"),

    
    #equipos
    path ('equipo/add/', agregar_equipo, name='add_equipo'),
    path ('equipo/list/',lista_equipos,name='lista_equipos'),
    path ('equipo/edit/<id>/',editar_equipo,name='editar_equipo'),
    path('equipo/delete/<id>/', delete_equipo, name="delete_equipo"),

    #ordenes
    path ('orden/add/', agregar_orden, name='add_orden'),
    path ('orden/list/',lista_orden,name='lista_orden'),
    path ('orden/edit/<id>/',editar_orden,name='editar_orden'),
    path('orden/delete/<id>/', delete_orden, name="delete_orden")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)