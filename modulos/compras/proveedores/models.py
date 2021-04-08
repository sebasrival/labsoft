from django.db import models


# Create your models here.
class Proveedor(models.Model):
    ruc=models.CharField(max_length=200, unique=True)
    razon_social = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=150, blank=True)

  


    class Meta():
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
