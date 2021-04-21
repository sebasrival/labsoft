from django.db import models


# Create your models here.
class Proveedores(models.Model):
    ruc = models.CharField(max_length=200, unique=True)
    razon_social = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return '%s %s' % (self.ruc, self.razon_social)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"


class Pago(models.Model):
    metodo_pago = models.CharField(max_length=100)
    descripcion = models.TextField()

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Plural"


ESTADOS_FACTURA = [
    ('RECIBIDO', 'Recibido'),
    ('NORECIBIDO', 'No Recibido')
]


class MateriaPrima(models.Model):
    cod_materia = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    inci = models.CharField(max_length=100)
    um = models.CharField(max_length=5)  # unidad de medida

    class Meta:
        verbose_name = 'Materia Prima'
        verbose_name_plural = 'Materias Primas'


class FacturaCompra(models.Model):
    nro_factura = models.CharField(max_length=200, unique=True)
    tipo_factura = models.BooleanField()  # true: contado false: credito
    id_proveedor = models.ForeignKey(Proveedores, on_delete=models.PROTECT)
    estado = models.CharField(max_length=12, choices=ESTADOS_FACTURA, default=ESTADOS_FACTURA[0])
    monto_iva1 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)  # 5%
    monto_iva2 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)  # 10% preguntar si esta bien
    total = models.FloatField(default=0)
    exenta = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    id_pago = models.ForeignKey(Pago, on_delete=models.PROTECT)

    def __str__(self):
        return 'Factura Compra: %s - Proveedor: %s' % (self.nro_factura, self.id_proveedor.razon_social)

    class Meta:
        verbose_name = 'Factura Compra'
        verbose_name_plural = 'Facturas Compras'

TIPO_IVA = [
    ('IVA5', '5%'),
    ('IVA10', '10%'),
    ('EXENTA', 'Exenta')
]

class FacturaConDet(models.Model):
    id_factura = models.ForeignKey(FacturaCompra, on_delete=models.CASCADE)
    cod_materia = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    descripcion = models.CharField(max_length=200, blank=True)
    tipo_iva = models.CharField(max_length=10, choices=TIPO_IVA, default=TIPO_IVA[1])

    class Meta:
        ordering = ['id']


class StockMateriaPrima(models.Model):
    cod_materia = models.ForeignKey(MateriaPrima, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Stock de Materia Prima'
        verbose_name_plural = 'Stocks de materias primas'
