from django.contrib import admin

# Register your models here.
from modulos.accounts.models import User

admin.site.register(User)