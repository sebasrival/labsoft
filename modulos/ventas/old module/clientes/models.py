from django.db import models

# Create your models here.
class Cliente (models.Model):
    id_documento = models.CharField(max_length=200, unique=True)
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
            return '%s' % (self.razon_social)
        else:
            return '%s %s' % (self.nombre, self.apellido)


    class Meta():
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"