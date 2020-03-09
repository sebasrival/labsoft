from django.db import models

# Create your models here.
class Cliente (models.Model):
    ruc = models.CharField(max_length=200, unique=True)
    cedula = models.CharField(max_length=200, unique=True, blank=True)
    nombre = models.CharField(max_length=50, blank=True)
    apellido = models.CharField(max_length=50, blank=True)
    razon_social = models.CharField(max_length=100, blank=True)
    descuento = models.FloatField(default=0)
    bonificacion = models.FloatField(default=0)
    es_entidad = models.BooleanField(default=False)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=150, blank=True)

    def __str__(self):
        if self.es_entidad:
            return '%s %s %s' % (self.cedula, self.nombre, self.apellido)
        else:
            return '%s %s' % (self.ruc, self.razon_social)

    class Meta():
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"