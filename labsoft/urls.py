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
from django.urls import path, include

from modulos.accounts.views import lista_usuarios, agregar_usuario, editar_usuario, delete_user, agregar_rol,\
    editar_rol, delete_rol

from django.conf import settings
from .views import home, logoutUser
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logoutUser, name="logout"),
    path('', home, name="index"),

    #módulo compras
    path('modulos/compras/', include('modulos.compras.urls')),

    #módulo ventas
    path('modulos/ventas/', include('modulos.ventas.urls')),
    #módulo produccion
    path('modulos/produccion/', include('modulos.produccion.urls')),
    #módulo reportes
    path('modulos/reportes/', include('modulos.reportes.urls')),
    # #usuarios
    path('user/list/', lista_usuarios, name='list_user'),
    path('user/add/', agregar_usuario, name='add_user'),
    path('user/edit/<id>', editar_usuario, name='edit_user'),
    path('user/delete/<id>', delete_user, name="delete_user"),

    path('rol/add/', agregar_rol, name='add_rol'),
    path('rol/edit/<id>/', editar_rol, name='editar_rol'),
    path('rol/delete/<id>/', delete_rol, name='delete_rol')
   ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
