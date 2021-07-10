from modulos.ventas.models import FacturaVenta, FacturaVentaDetalle
from modulos.produccion.models import OrdenElaboracion
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
    
    def obtener_cantidad_producida(self,mes,anho):
        cantidad_producida = 0 
        ordenes=OrdenElaboracion.objects.filter(producto_id=self.id,fecha_emision__year=anho,fecha_emision__month=mes)
        for orden in ordenes:
             cantidad_producida =cantidad_producida + float(orden.cantidad_teorica) / ((orden.producto.cantidad_contenido) / float(1000))
        return cantidad_producida

    def obtener_cantidad_vendida(self,mes,anho):
        cantidad_vendida = 0 
        facturas=FacturaVenta.objects.filter(fecha_emision__year=anho,fecha_emision__month=mes)
        for factura in facturas:
            for facturadetalle in FacturaVentaDetalle.objects.filter(factura_id=factura.id,producto_id=self.id):
                cantidad_vendida=cantidad_vendida+ facturadetalle.cantidad
        return cantidad_vendida
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
