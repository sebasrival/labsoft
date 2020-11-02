from django.db import models
METODOS_PAGOS = [
    ('TARJETA CREDITO/DEBITO', 'Tarjeta Credito/Debito'),
    ('EFECTIVO', 'Efectivo'),
    ('TRANSFERENCIA BANCARIA', 'Transferencia Bancaria'),
    ('CHEQUE', 'Cheque')
]
ESTADOS_PAGOS = [
    ('PENDIENTE', 'Pendiente'),
    ('FINALIZADO', 'Finalizado')
]
TIPO_PAGO= [
    ('CONTADO', 'Contado'),
    ('CREDITO', 'Credito')
]
ESTADOS_CUOTAS = [
    ('PENDIENTE', 'PENDIENTE'),
    ('PAGADA', 'PAGADA')
]

# Create your models here.
class Pago(models.Model):
    cedula=models.CharField(max_length=20,null=True)
    nro_factura=models.CharField(max_length=20, unique=True)
    fecha_pago = models.DateField()
    monto_total=models.IntegerField()
    estado=models.CharField(max_length=40, choices=ESTADOS_PAGOS, default=ESTADOS_PAGOS[0])
    metodo_pago = models.CharField(max_length=40, choices=METODOS_PAGOS, default=METODOS_PAGOS[0])
    tipo_pago = models.CharField(max_length=40, choices=TIPO_PAGO, default=TIPO_PAGO[0])
    cantidad_cuotas=models.IntegerField(default=1)



    class Meta():
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

class PagoCuota(models.Model):
    id_pago=models.ForeignKey(Pago, on_delete=models.PROTECT)
    fecha_pago = models.DateField(null=True)
    fecha_vencimiento=models.DateField()
    monto_cuota=models.IntegerField()
    estado=models.CharField(max_length=40, choices=ESTADOS_CUOTAS, default=ESTADOS_CUOTAS[0])



    class Meta():
        verbose_name = "PagoCuota"
        verbose_name_plural = "Pagos Cuotas"
