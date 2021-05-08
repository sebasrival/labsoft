from django.db import models
ESTADOS_EQUIPOS = [
    ('ACTIVO', 'ACTIVO'),
    ('INACTIVO', 'INACTIVO')
]


# Create your models here.
class Equipo(models.Model):
    codigo_equipo=models.CharField(max_length=20, unique=True)
    nombre=models.CharField(max_length=60, unique=True)
    descripcion=models.CharField(max_length=80, unique=True)
    estado = models.CharField(max_length=40, choices=ESTADOS_EQUIPOS, default=ESTADOS_EQUIPOS[0])
    modelo=models.CharField(max_length=80, unique=True)
    costo=models.IntegerField()
    codigo_elaboracion=models.CharField(max_length=80, unique=True)


    class Meta():
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"
