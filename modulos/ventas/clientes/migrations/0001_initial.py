# Generated by Django 3.0.7 on 2021-03-04 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_documento', models.CharField(max_length=200, unique=True)),
                ('nombre', models.CharField(blank=True, max_length=50)),
                ('apellido', models.CharField(blank=True, max_length=50)),
                ('razon_social', models.CharField(blank=True, max_length=100)),
                ('descuento', models.FloatField(default=0)),
                ('bonificacion', models.FloatField(default=0)),
                ('es_entidad', models.BooleanField(default=False)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.CharField(blank=True, max_length=100)),
                ('direccion', models.CharField(blank=True, max_length=150)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
    ]
