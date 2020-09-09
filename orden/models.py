from django.db import models

# Create your models here.
from equipos.models import Equipo


class OrdenElaboracion(models.Model):
    codigo_elaboracion = models.CharField(max_length=200)
    codigo_producto = models.CharField(max_length=150)
    desc_producto = models.TextField()
    cant_teorica = models.IntegerField()
    vencimiento = models.DateField()
    estado = models.CharField(max_length=15)
    orden_numero = models.IntegerField()
    fecha_emision = models.DateField()
    fecha_vigencia = models.DateField()
    hora_inicio = models.DateTimeField(null=True, blank=True)
    hora_final = models.DateTimeField(null=True, blank=True)
    realizado_por = models.CharField(max_length=200)
    verificado_por = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Orden de Elaboración'
        verbose_name_plural = 'Ordenes de Elaboración'

    def __str__(self):
        return self.codigo_elaboracion
