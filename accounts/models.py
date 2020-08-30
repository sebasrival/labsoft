from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from labsoft.settings import STATIC_URL, MEDIA_URL


class User(AbstractUser):
     profile = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)

     def get_profile(self):
         if self.profile:
             return '{}{}'.format(MEDIA_URL, self.profile)
         return '{}{}'.format(STATIC_URL, 'img/profile.png')

     class Meta:
         verbose_name = 'Usuario'
         verbose_name_plural = 'Usuarios'