from django.db import models
METODOS_PAGOS = [
    ('TARJETA CREDITO/DEBITO', 'Tarjeta Credito/Debito'),
    ('EFECTIVO', 'Efectivo'),
    ('TRANSFERENCIA BANCARIA', 'Transferencia Bancaria'),
    ('CHEQUE', 'Cheque')
]


# Create your models here.
class Pago(models.Model):
    nro_factura=models.CharField(max_length=20, unique=True)
    fecha_pago = models.DateField()
    monto_total=models.IntegerField()
    metodo_pago = models.CharField(max_length=40, choices=METODOS_PAGOS, default=METODOS_PAGOS[0])
    es_contado = models.BooleanField()
    es_cliente = models.BooleanField()



    class Meta():
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
