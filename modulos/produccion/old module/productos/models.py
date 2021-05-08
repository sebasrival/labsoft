from django.db import models


# Create your models here.
class Producto(models.Model):
    codigo_producto = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=100, null=False)
    volumen = models.FloatField(blank=True, null=True, default=0)
    color = models.CharField(max_length=10, blank=True, default='')
    precio = models.FloatField()
    cantidad_contenido = models.FloatField(blank=True)
    tipo = models.CharField(max_length=10, blank=True, default='')


    def __str__(self):
        return '%s %s' % (self.codigo_producto, self.nombre)

    def obtener_dict(self):
        dict = {}
        dict['codigo_producto'] = self.codigo_producto
        dict['nombre'] = self.nombre
        dict['tipo'] = self.tipo
        dict['volumen'] = self.volumen
        dict['color'] = self.color
        dict['precio'] = self.precio
        dict['cantidad_contenido'] = self.cantidad_contenido
        return dict

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
