from django.db import models

from clientes.models import Cliente
from productos.models import Producto

ESTADOS_PEDIDOS = [
    ('PENDIENTE', 'Pendiente'),
    ('CANCELADO', 'Cancelado'),
    ('FINALIZADO', 'Finalizado'),
]


# Create your models here.
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    fecha_pedido = models.DateField()
    fecha_entrega = models.DateField()
    estado = models.CharField(max_length=15, choices=ESTADOS_PEDIDOS, default=ESTADOS_PEDIDOS[0])

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['id']

    def __str__(self):
        return 'Nro Pedido: %s - Cliente: %s' % (self.id, self.cliente)


class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(blank=False)

    class Meta:
        ordering = ['id']