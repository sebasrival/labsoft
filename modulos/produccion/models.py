from django.db import models
from django.forms import model_to_dict
from modulos.compras.models import MateriaPrima
TIPO_IVA = [
    ( 5,'IVA5',),
    ( 10,'IVA10'),
    (0,'EXENTA')
]
TIPO_ORDEN = [
    ( 'PENDIENTE','PENDIENTE'),
    ( 'EN PRODUCCION','EN PRODUCCION'),
    ('FINALIZADA','FINALIZADA')
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
    stock_inicial= models.IntegerField(default=0,blank=True)

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


class Equipo(models.Model):
    codigo= models.CharField(max_length=30, null=False,unique=True)
    nombre= models.CharField(max_length=150, blank=True)


    def __str__(self):
        return '%s %s' % (self.codigo, self.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['id']=self.id
        item['codigo'] = self.codigo
        item['descripcion'] = self.nombre

        return item

    class Meta:
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'


class OrdenElaboracion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_teorica = models.IntegerField()
    estado = models.CharField(max_length=15,choices=TIPO_ORDEN,default=TIPO_ORDEN[0])
    numero = models.IntegerField()
    fecha_emision = models.DateField()
    fecha_vigencia = models.DateField()
    elaborado_por = models.CharField(max_length=200)
    aprobado_por = models.CharField(max_length=200)
    verificado_por = models.CharField(max_length=200)
    descripcion_modificacion= models.CharField(max_length=100,default='Emision Inicial')


    def toJSON(self):
        item = model_to_dict(self)
        item['id']=self.id
        item['numero'] = self.numero
        item['estado'] = self.estado
        item['fecha_emision'] = self.fecha_emision
        item['fecha_vigencia'] = self.fecha_vigencia
        item['cantidad_teorica'] = self.cantidad_teorica
        item['producto'] = self.producto.nombre
     


        return item
    class Meta:
        verbose_name = 'Orden de Elaboración'
        verbose_name_plural = 'Ordenes de Elaboración'

    def __str__(self):
        return self.numero


class DetalleOrdenElaboracion(models.Model):
    orden = models.ForeignKey(OrdenElaboracion, on_delete=models.CASCADE)
    materia = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE)
    inci= models.CharField(max_length=30)
    cantidad = models.FloatField()
    unidad_medida = models.CharField(max_length=30)


    class Meta:
        verbose_name = 'Detalle Orden de Elaboración'
        verbose_name_plural = 'Detalles de orden de elaboracion'

    def __str__(self):
        return self.orden


class EquipoOrdenElaboracion(models.Model):
    orden = models.ForeignKey(OrdenElaboracion, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Equipo en Orden de Elaboración'
        verbose_name_plural = 'Equipos de orden de elaboracion'

    def __str__(self):
        return self.orden



class FormulaProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    materia= models.ForeignKey(MateriaPrima, on_delete=models.CASCADE)
    cantidad= models.FloatField()
    
    class Meta:
        verbose_name = 'Formula'
        verbose_name_plural = 'Formulas'

    def toJSON(self):
        item = model_to_dict(self)
        item['producto_id'] = self.producto.id
        item['id'] = self.materia.id
        item['codigo']=self.materia.codigo
        item['inci']=self.materia.inci
        item['unidad_medida']=self.materia.um
        item['cantidad'] = self.cantidad
        item['descripcion'] = self.materia.descripcion

        return item
    def __str__(self):
        return self.orden
