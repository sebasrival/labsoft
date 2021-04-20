from django.db import models

# Create your models here.
class Proveedores(models.Model):
    ruc = models.CharField(max_length=200, unique=True)
    razon_social = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return {'%s %s'} % (self.ruc, self.razon_social)

    class Meta():
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

class Pago(models.Model):
    metodo_pago = models.CharField(max_length=100)
    descripcion = models.TextField()

    class Meta():
        verbose_name = "Pago"
        verbose_name_plural = "Plural"

ESTADOS_FACTURA = [
    ('PENDIENTE', 'Pendiente'),
    ('CANCELADO', 'Cancelado'),
    ('FINALIZADO', 'Finalizado'),
    ('EMITIDO', 'Emitido')
]

class MateriaPrima(models.Model):
    cod_materia = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    inci = models.CharField(max_length=100)
    um = models.CharField(max_length=5)

    class Meta:
        verbose_name = 'Materia Prima'
        verbose_name_plural = 'Materias Primas'

class FacturaCompra:
    nro_factura = models.CharField(max_length=200, unique=True)
    tipo_factura = models.BooleanField()#true: contado false: credito
    id_proveedor = models.ForeignKey(Proveedores, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20, choices=ESTADOS_FACTURA, default=ESTADOS_FACTURA[0])
    sub_total = models.FloatField(default=0)
    total_iva1 = models.FloatField(default=0) #5%
    total_iva2 = models.FloatField(default=0) #10% preguntar si esta bien
    total = models.FloatField(default=0)
    descuento = models.IntegerField(default=0)
    id_pago = models.ForeignKey(Pago)


    def __str__(self):
        return ('Factura Compra: %s - Proveedor: %s') % (self.nro_factura, self.id_proveedor.razon_social)

    class Meta:
        verbose_name = 'Factura Compra'
        verbose_name_plural = 'Facturas Compras'

class FacturaConDet(models.Model):
    id_factura = models.ForeignKey(FacturaCompra)
    cod_materia = models.ForeignKey(MateriaPrima)
    cantidad = models.IntegerField(default=1)
    precio = models.FloatField(default=0)
    descripcion = models.CharField(max_length=200, blank=True)
    sub_iva = models.FloatField(default=0)

    class Meta:
        ordering = ['id']

class StockMateriaPrima(models.Model):
    cod_materia = models.ForeignKey(MateriaPrima)
    cantidad = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'Stock de Materia Prima'
        verbose_name_plural = 'Stocks de materias primas'