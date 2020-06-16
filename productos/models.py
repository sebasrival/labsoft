from django.db import models


# Create your models here.
class Producto(models.Model):
    codigo_producto = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.TextField(blank=True)
    volumen = models.FloatField(blank=True, null=True, default=0)
    color = models.CharField(max_length=10, blank=True, default='')
    precio = models.FloatField()
    cantidad_neto = models.FloatField(blank=True)

    def __str__(self):
        return '%s %s' % (self.codigo_producto, self.nombre)

    def obtener_dict(self):
        dict = {}
        dict['codigo_producto'] = self.codigo_producto
        dict['nombre'] = self.nombre
        dict['description'] = self.descripcion
        dict['volumen'] = self.volumen
        dict['color'] = self.color
        dict['precio'] = self.precio
        dict['cantidad_neto'] = self.cantidad_neto
        return dict

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
