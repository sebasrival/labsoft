from django.db import models
from django.forms import model_to_dict

TIPO_IVA = [
    ( 5,'IVA5',),
    ( 10,'IVA10'),
    (0,'EXENTA')
]

# Create your models here.
class Producto(models.Model):
    codigo_producto = models.CharField(max_length=50,unique=True)
    nombre = models.CharField(max_length=100, null=False)
    volumen = models.FloatField(blank=True, null=True, default=0)
    color = models.CharField(max_length=10, blank=True, default='')
    precio = models.FloatField()
    cantidad_contenido = models.FloatField(blank=True)
    tipo = models.CharField(max_length=10, blank=True, default='')
    tasa_iva= models.IntegerField(default=0,choices=TIPO_IVA)

    def __str__(self):
        return '%s %s' % (self.codigo_producto, self.nombre)
    
    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre
        item['precio'] = self.precio
        item['tipo'] = self.tipo
        item['tasa_iva'] = self.tasa_iva
        return item


    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'





class StockProductos(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad= models.IntegerField()


    def __str__(self):
        return '%s %s' % (self.producto, self.nombre)

    def obtener_dict(self):
        dict = {}
        dict['producto'] = self.producto
        dict['cantidad'] = self.cantidad

        return dict

    class Meta:
        verbose_name = 'StockProducto'
        verbose_name_plural = 'StockProductos'


