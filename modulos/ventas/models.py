from django.db import models
from modulos.produccion.models import Producto



ESTADOS_FACTURA = [
    ('PENDIENTE', 'Pendiente'),
    ('CANCELADO', 'Cancelado'),
    ('FINALIZADO', 'Finalizado'),
]

# Create your models here.
class VentasConf(models.Model):
    iva_porc = models.FloatField(default=0.1)
    calc_iva = models.IntegerField(default=11)


TIPO_IVA = [
    ('IVA5', '5%'),
    ('IVA10', '10%'),
    ('EXENTA', 'Exenta')
]
# Modelo de Cliente.
class Cliente (models.Model):
    ruc = models.CharField(max_length=15, unique=True)
    cedula = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=50, blank=True)
    apellido = models.CharField(max_length=50, blank=True)
    razon_social = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return '%s %s' % (self.nombre, self.apellido)


    class Meta():
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Cobro(models.Model):
    metodo_cobro = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo_cobro = models.TextField()
    cantidad_cuotas=models.IntegerField(default=1)
    class Meta:
        verbose_name = "Cobro"
        verbose_name_plural = "Plural"

        
class FacturaVenta(models.Model):
    nro_factura = models.CharField(max_length=20, blank=False)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_venta = models.CharField(max_length=200, blank=True)
    monto_iva1 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)  # 5%
    monto_iva2 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)  # 10% preguntar si esta bien
    total = models.FloatField(default=0)
    exenta = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    fecha_emision = models.DateField()
    id_cobro = models.ForeignKey(Cobro, on_delete=models.PROTECT)

    def __str__(self):
        return 'Nro Factura: %s - Cliente: %s' % (self.nro_factura, self.cliente)

    class Meta:
        verbose_name = 'FacturaVenta'
        verbose_name_plural = 'Facturas'
        ordering = ['id']


class FacturaVentaDetalle(models.Model):
    id_factura = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE)
    id_producto= models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    descripcion = models.CharField(max_length=200, blank=True)
    tipo_iva = models.CharField(max_length=10, choices=TIPO_IVA, default=TIPO_IVA[1])

    class Meta:
        ordering = ['id']





class Cuota(models.Model):
    id_cobro = models.ForeignKey(Cobro, on_delete=models.CASCADE)
    estado = models.CharField(max_length=100)
    nro_cuota=models.IntegerField(default=1)
    fecha_vencimiento = models.DateField()
    fecha_pago_cuota = models.DateField()

    class Meta:
        verbose_name = "Cuota"
        verbose_name_plural = "Plural"


