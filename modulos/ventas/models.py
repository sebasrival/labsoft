from django.db import models
from modulos.produccion.models import Producto
from django.forms import model_to_dict

ESTADOS_PEDIDOS = [
    ('PENDIENTE', 'Pendiente'),
    ('CANCELADO', 'Cancelado'),
    ('FINALIZADO', 'Finalizado'),
]


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
    cedula = models.CharField(max_length=15, unique=True, blank=True)
    nombre = models.CharField(max_length=50, blank=True)
    apellido = models.CharField(max_length=50, blank=True)
    razon_social = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20,blank=True)
    email = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return '%s %s' % (self.nombre, self.apellido)

    def toJSON(self):
        item = model_to_dict(self)
        item['id']=self.id
        item['nombre'] = self.nombre
        item['ruc'] = self.ruc
        item['apellido'] = self.apellido
        item['razon_social'] = self.razon_social
        item['cedula'] = self.cedula
        return item

    class Meta():
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Cobro(models.Model):
    metodo_cobro = models.CharField(max_length=100)
    descripcion = models.TextField()
    medio_cobro = models.TextField()
    cantidad_cuotas=models.IntegerField(default=1)

    def toJSON(self):
        item = model_to_dict(self)
        item['id']=self.id
        item['tipo_cobro'] = self.metodo_cobro
        item['medio_cobro']=self.medio_cobro
        item['cantidad_cuotas'] = self.cantidad_cuotas
        return item
    class Meta:
        verbose_name = "Cobro"
        verbose_name_plural = "Plural"

        
class FacturaVenta(models.Model):
    nro_factura = models.CharField(max_length=20, blank=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_venta = models.CharField(max_length=200, blank=True)
    monto_iva1 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)  # 5%
    monto_iva2 = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)  # 10% preguntar si esta bien
    total = models.FloatField(default=0)
    estado=models.CharField(max_length=200, blank=True)
    exenta = models.DecimalField( default=0.00, decimal_places=2, max_digits=9)
    fecha_emision = models.DateField()
    cobro = models.ForeignKey(Cobro, on_delete=models.PROTECT)

    def __str__(self):
        return 'Nro Factura: %s - Cliente: %s' % (self.nro_factura, self.cliente)
    def toJSON(self):
        item = model_to_dict(self)
        item['id']=self.id
        item['nro_factura'] = self.nro_factura
        item['cliente'] = self.cliente.razon_social
        item['cliente_ruc']=self.cliente.ruc
        item['fecha_emision'] = self.fecha_emision
        item['estado'] = self.estado
        item['total'] = self.total
        item['tipo_venta'] = self.tipo_venta
        item['cobro_id']=self.cobro.id
        return item
  
    def obtener_total(self):
        return int(self.total)
    def obtener_montoiva1(self):
        return round(self.monto_iva1)
    def obtener_montoiva2(self):
        return round(self.monto_iva2)
    class Meta:
        verbose_name = 'FacturaVenta'
        verbose_name_plural = 'Facturas'
        ordering = ['id']


class FacturaVentaDetalle(models.Model):
    factura = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE)
    producto= models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    def obtener_subtotal(self):
        return int(self.cantidad)*int(self.precio)

    def obtener_total(self):
        return int(self.cantidad)*int(self.precio)

    def obtener_precio(self):
        return round(self.precio)
    class Meta:
        ordering = ['id']




class Cuota(models.Model):
    cobro = models.ForeignKey(Cobro, on_delete=models.CASCADE)
    estado = models.CharField(max_length=100)
    nro_cuota=models.IntegerField(default=1)
    fecha_vencimiento = models.DateField()
    fecha_pago_cuota = models.DateField(null=True)
    monto_cuota=models.IntegerField(default=0)

    def toJSON(self):
        item = model_to_dict(self)
        item['id']=self.id
        item['cobro_id'] = self.cobro.id
        item['nro_cuota'] = self.nro_cuota
        item['estado'] = self.estado
        item['fecha_vencimiento'] = self.fecha_vencimiento
        item['fecha_pago'] = self.fecha_pago_cuota
        item['monto_cuota'] = self.monto_cuota
        return item
    class Meta:
        verbose_name = "Cuota"
        verbose_name_plural = "Plural"


# Create your models here.
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_pedido = models.DateField()
    fecha_entrega = models.DateField(null=True)
    estado = models.CharField(max_length=100, choices=ESTADOS_PEDIDOS)
    total = models.IntegerField(default=0)
    def toJSON(self):
        item = model_to_dict(self)
        item['id']=self.id
        item['cliente_id'] = self.cliente.id
        item['cliente'] = self.cliente.razon_social
        item['cliente_ruc']=self.cliente.ruc
        item['estado'] = self.estado
        item['total'] = self.total
        return item
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'



class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(blank=False)
    def toJSON(self):
        item = model_to_dict(self)
        item['id']=self.id
        item['codigo_producto'] = self.producto.codigo_producto
        item['descripcion_producto']=self.producto.nombre
        item['cantidad'] = self.cantidad
        item['precio'] = self.producto.precio
        item['total'] = self.producto.precio * self.cantidad
        return item
    class Meta:
        ordering = ['id']