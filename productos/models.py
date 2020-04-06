from django.db import models

# Create your models here.
class Producto (models.Model):
    codigo_producto = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.TextField(blank=True)
    volumen = models.FloatField(blank=True)
    color = models.CharField(max_length=10, blank=True)
    precio = models.FloatField(blank=True)
    cantidad_neto = models.FloatField(blank=True)

    def __str__(self):
        return '%s %s' % (self.codigo_producto, self.nombre)

    class Meta():
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos' 
