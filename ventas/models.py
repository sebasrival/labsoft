from django.db import models

from clientes.models import Cliente
from productos.models import Producto


ESTADOS_FACTURA = [
    ('PENDIENTE', 'Pendiente'),
    ('CANCELADO', 'Cancelado'),
    ('FINALIZADO', 'Finalizado'),
]

# Create your models here.
class VentasConf(models.Model):
    iva_porc = models.FloatField(default=0.1)
    calc_iva = models.IntegerField(default=11)


class Factura(models.Model):
    nro_factura = models.CharField(max_length=20, blank=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    fecha_emision = models.DateField()
    es_contado = models.BooleanField(default=True)
    estado = models.CharField(max_length=15, choices=ESTADOS_FACTURA, default=ESTADOS_FACTURA[0])
    total_iva = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return 'Nro Factura: %s - Cliente: %s' % (self.nro_factura, self.cliente)

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['id']


class FacturaDetalle(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200, blank=True)
    cantidad = models.IntegerField(blank=False)


    class Meta:
        ordering = ['id']